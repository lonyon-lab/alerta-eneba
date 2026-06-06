# Script para trackear ratios de tarjetas de regalo en Eneba
# Web base: https://www.eneba.com/es/
# La API es GraphQL en graphql.eneba.com
# Si se rompe: buscar nuevo sha256Hash en Network del navegador filtrando por "graphql"
# y actualizar la variable SHA en este script
# Para añadir una moneda nueva: añadir entrada en MONEDAS con sus slugs, valores y umbrales

import os
import json
import requests
from datetime import datetime, timezone

# ─── CONFIGURACIÓN DE MONEDAS ────────────────────────────────────────────────
# Para añadir una moneda nueva, copia un bloque y rellena slugs, valores y umbrales
MONEDAS = {
    "TRY": {
        "nombre": "Lira turca",
        "bandera": "🇹🇷",
        "slugs": [
            "xbox-xbox-live-gift-card-25-try-xbox-live-key-turkey",
            "xbox-xbox-live-gift-card-50-try-xbox-live-key-turkey",
            "xbox-xbox-live-gift-card-100-try-xbox-live-key-turkey",
            "xbox-xbox-live-gift-card-250-try-xbox-live-key-turkey",
            "xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey",
        ],
        "valores": [25, 50, 100, 250, 300],
        "umbral": float(os.environ.get("PRICE_THRESHOLD_TRY", os.environ.get("PRICE_THRESHOLD", "54"))),
        "umbral_bajo": 40,  # avisa si cae por debajo de este ratio (precio muy alto)
    },
    # Ejemplo BRL (descomentar cuando quieras añadirlo):
    # "BRL": {
    #     "nombre": "Real brasileño",
    #     "bandera": "🇧🇷",
    #     "slugs": [...],
    #     "valores": [...],
    #     "umbral": float(os.environ.get("PRICE_THRESHOLD_BRL", "5")),
    #     "umbral_bajo": 3,
    # },
}

# ─── CONFIGURACIÓN TELEGRAM ───────────────────────────────────────────────────
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ─── CONFIGURACIÓN API ENEBA ──────────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "*/*",
    "Accept-Language": "es_ES",
    "content-type": "application/json",
    "Origin": "https://www.eneba.com",
    "Referer": "https://www.eneba.com/",
}

SHA = "c3aaf0194bab3a8481512069d9bbc707037714c0a60f603497bc820f00a91c11_50e5e0d9351bb05ab629b0eda9b116ae4d96fbb6861836383bc404f1ab5e3680094635224c07d364fff371b7517712ebd33ce0f05504f2fa7e9d66e321168e02"

ESTADO_FILE = "estado.json"

# ─── FUNCIONES ────────────────────────────────────────────────────────────────

def get_price(slug):
    body = {
        "operationName": "ProductNoCache",
        "variables": {
            "isProductVariantSearch": True,
            "isCheapestAuctionIncluded": True,
            "loadCoinsValue": False,
            "currency": "EUR",
            "context": {"country": "ES", "region": "spain", "language": "es_ES"},
            "slug": slug,
            "language": "es_ES",
            "version": 3,
            "abTests": ["CFD755"],
            "packContext": {"country": "ES", "region": "spain", "language": "es_ES"}
        },
        "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": SHA}
        }
    }
    r = requests.post("https://graphql.eneba.com/graphql/", json=body, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        try:
            edges = data["data"]["productNoCache"]["auctions"]["edges"]
            prices = [e["node"]["price"]["amount"] for e in edges if e["node"]["isInStock"] and e["node"]["isCurrentlyAvailable"]]
            return min(prices) if prices else None
        except:
            return None
    return None

def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

def cargar_estado():
    if os.path.exists(ESTADO_FILE):
        with open(ESTADO_FILE, "r") as f:
            return json.load(f)
    return {"monedas": {}, "historial": []}

def guardar_estado(estado):
    with open(ESTADO_FILE, "w") as f:
        json.dump(estado, f, indent=2)

def get_ratios_moneda(config):
    resultados = []
    for slug, valor in zip(config["slugs"], config["valores"]):
        price_cents = get_price(slug)
        if price_cents and price_cents > 0:
            price_eur = price_cents / 100
            ratio = valor / price_eur
            resultados.append({"valor": valor, "precio_eur": price_eur, "ratio": ratio})
            print(f"  {valor} = {price_eur:.2f}€ → {ratio:.2f} TRY/€")
    return resultados

def procesar_alertas(moneda, config, resultados, estado):
    if not resultados:
        send_telegram(f"⚠️ <b>Alerta Eneba {moneda}</b>\nNo se pudieron obtener precios. Puede que la API haya cambiado.")
        return

    mejor = max(resultados, key=lambda x: x["ratio"])
    mejor_ratio = mejor["ratio"]
    umbral = config["umbral"]
    umbral_bajo = config["umbral_bajo"]

    estado_moneda = estado["monedas"].get(moneda, {"ultimo_ratio_alertado": None, "sobre_umbral": False})

    # Aviso si cae por debajo del umbral bajo (precio muy caro)
    if mejor_ratio < umbral_bajo:
        send_telegram(
            f"📉 <b>Precio muy alto en Eneba {config['bandera']} {moneda}</b>\n"
            f"Ratio actual: {mejor_ratio:.2f} {moneda}/€\n"
            f"Está por debajo de tu mínimo de {umbral_bajo}"
        )

    # Lógica de alerta por umbral alto
    if mejor_ratio >= umbral:
        ultimo = estado_moneda.get("ultimo_ratio_alertado")
        debe_alertar = False

        if not estado_moneda.get("sobre_umbral"):
            # Primera vez que supera el umbral
            debe_alertar = True
        elif ultimo is not None and mejor_ratio > ultimo + 0.5:
            # Sigue subiendo significativamente (más de 0.5 TRY/€)
            debe_alertar = True

        if debe_alertar:
            send_telegram(
                f"🚨 <b>Alerta Eneba {config['bandera']} {moneda}</b>\n"
                f"Mejor ratio: <b>{mejor_ratio:.2f} {moneda}/€</b>\n"
                f"Tarjeta: {mejor['valor']} {moneda} por {mejor['precio_eur']:.2f}€\n"
                f"https://www.eneba.com/es/xbox-xbox-live-gift-card-{mejor['valor']}-try-xbox-live-key-turkey"
            )
            estado_moneda["ultimo_ratio_alertado"] = mejor_ratio
            estado_moneda["sobre_umbral"] = True
    else:
        # Por debajo del umbral, resetear
        estado_moneda["sobre_umbral"] = False
        estado_moneda["ultimo_ratio_alertado"] = None

    estado["monedas"][moneda] = estado_moneda

def guardar_historial(moneda, resultados, estado, ahora):
    if not resultados:
        return
    mejor = max(resultados, key=lambda x: x["ratio"])
    estado["historial"].append({
        "moneda": moneda,
        "timestamp": ahora.isoformat(),
        "mejor_ratio": round(mejor["ratio"], 2),
        "mejor_valor": mejor["valor"],
        "mejor_precio_eur": mejor["precio_eur"],
    })
    # Mantener solo últimas 4 semanas (20min * 3 * 24 * 28 = 2016 entradas max por moneda)
    estado["historial"] = estado["historial"][-3000:]

def enviar_resumen_diario(estado, ahora):
    lineas = [f"📊 <b>Resumen diario Eneba — {ahora.strftime('%d/%m/%Y')}</b>\n"]
    for moneda, config in MONEDAS.items():
        resultados = get_ratios_moneda(config)
        if not resultados:
            lineas.append(f"{config['bandera']} <b>{moneda}</b>\n  ⚠️ Sin datos\n")
            continue
        mejor = max(resultados, key=lambda x: x["ratio"])
        lineas.append(f"{config['bandera']} <b>{moneda}</b>")
        for r in resultados:
            lineas.append(f"  {r['valor']} {moneda} → {r['ratio']:.2f} {moneda}/€")
        lineas.append(f"  🏆 Mejor: <b>{mejor['ratio']:.2f} {moneda}/€</b> (umbral: {config['umbral']})\n")
    send_telegram("\n".join(lineas))

def enviar_resumen_semanal(estado, ahora):
    lineas = [f"📈 <b>Resumen semanal Eneba — semana {ahora.isocalendar()[1]}</b>\n"]
    for moneda in MONEDAS:
        historial_moneda = [h for h in estado["historial"] if h["moneda"] == moneda]
        if not historial_moneda:
            lineas.append(f"<b>{moneda}</b>: sin datos esta semana\n")
            continue
        mejor = max(historial_moneda, key=lambda x: x["mejor_ratio"])
        peor = min(historial_moneda, key=lambda x: x["mejor_ratio"])
        mejor_dt = datetime.fromisoformat(mejor["timestamp"])
        peor_dt = datetime.fromisoformat(peor["timestamp"])
        config = MONEDAS[moneda]
        lineas.append(f"{config['bandera']} <b>{moneda}</b>")
        lineas.append(f"  🏆 Mejor: {mejor['mejor_ratio']:.2f} {moneda}/€")
        lineas.append(f"     {mejor_dt.strftime('%A %d/%m a las %H:%M')} ({mejor['mejor_valor']} {moneda} por {mejor['mejor_precio_eur']:.2f}€)")
        lineas.append(f"  📉 Peor: {peor['mejor_ratio']:.2f} {moneda}/€")
        lineas.append(f"     {peor_dt.strftime('%A %d/%m a las %H:%M')}\n")
    send_telegram("\n".join(lineas))

def main():
    ahora = datetime.now(timezone.utc)
    hora_canarias = ahora.hour - 1  # UTC-1 en invierno, UTC en verano aprox
    es_lunes = ahora.weekday() == 0
    es_resumen_diario = hora_canarias == 9 and ahora.minute < 20
    es_resumen_semanal = es_lunes and es_resumen_diario

    estado = cargar_estado()

    if es_resumen_semanal:
        print("Enviando resumen semanal...")
        enviar_resumen_semanal(estado, ahora)

    if es_resumen_diario:
        print("Enviando resumen diario...")
        enviar_resumen_diario(estado, ahora)
    else:
        # Ejecución normal: comprobar precios y alertar
        for moneda, config in MONEDAS.items():
            print(f"\nComprobando {moneda}...")
            resultados = get_ratios_moneda(config)
            procesar_alertas(moneda, config, resultados, estado)
            guardar_historial(moneda, resultados, estado, ahora)

    guardar_estado(estado)

if __name__ == "__main__":
    main()
