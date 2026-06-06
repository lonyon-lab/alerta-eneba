# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ENEBA PRICE TRACKER                                                        ║
# ║  Trackea ratios de tarjetas Xbox en Eneba y avisa por Telegram              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# ─── SHA (ACTUALIZAR SI LA API FALLA) ────────────────────────────────────────
# Si recibes aviso de SHA inválido:
# 1. Abre Eneba en el navegador
# 2. F12 → Network → filtra "graphql" → abre petición POST → Payload
# 3. Copia el valor de sha256Hash y pégalo aquí
SHA = "c3aaf0194bab3a8481512069d9bbc707037714c0a60f603497bc820f00a91c11_50e5e0d9351bb05ab629b0eda9b116ae4d96fbb6861836383bc404f1ab5e3680094635224c07d364fff371b7517712ebd33ce0f05504f2fa7e9d66e321168e02"

# ─── UMBRALES (EDITAR AQUÍ) ───────────────────────────────────────────────────
# umbral:      avisa cuando el ratio SUBE de este valor (precio barato)
# umbral_bajo: avisa cuando el ratio BAJA de este valor (precio caro, algo raro)
UMBRALES = {
    "TRY": {"umbral": 54,   "umbral_bajo": 48},
    "BRL": {"umbral": 6.8,  "umbral_bajo": 5.5},
    "CLP": {"umbral": 42,   "umbral_bajo": 33},
    "COP": {"umbral": 4200, "umbral_bajo": 3300},
    "ZAR": {"umbral": 20.5, "umbral_bajo": 16},
    "SAR": {"umbral": 4.1,  "umbral_bajo": 3.2},
    "TWD": {"umbral": 38,   "umbral_bajo": 30},
    "HKD": {"umbral": 9.2,  "umbral_bajo": 7.2},
}

# ─── CONFIGURACIÓN DE MONEDAS ─────────────────────────────────────────────────
# Para añadir una moneda nueva:
# 1. Añade su umbral en UMBRALES arriba
# 2. Añade su bloque aquí con slugs y valores
# NOTA: cada slug tiene un campo opcional "sin_stock": True para tarjetas que
# existen pero están habitualmente agotadas — se muestran en el resumen como ⚫
MONEDAS = {
    "TRY": {
        "nombre": "Lira turca",
        "bandera": "🇹🇷",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-25-try-xbox-live-key-turkey",  "valor": 25},
            {"slug": "xbox-xbox-live-gift-card-50-try-xbox-live-key-turkey",  "valor": 50},
            {"slug": "xbox-xbox-live-gift-card-100-try-xbox-live-key-turkey", "valor": 100},
            {"slug": "xbox-xbox-live-gift-card-250-try-xbox-live-key-turkey", "valor": 250},
            {"slug": "xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey", "valor": 300},
        ],
        "umbral": UMBRALES["TRY"]["umbral"],
        "umbral_bajo": UMBRALES["TRY"]["umbral_bajo"],
    },
    "BRL": {
        "nombre": "Real brasileño",
        "bandera": "🇧🇷",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-5-brl-xbox-live-key-brazil",   "valor": 5},
            {"slug": "xbox-xbox-live-gift-card-10-brl-xbox-live-key-brazil",  "valor": 10},
            {"slug": "xbox-xbox-live-gift-card-15-brl-xbox-live-key-brazil",  "valor": 15},
            {"slug": "xbox-xbox-live-gift-card-20-brl-xbox-live-key-brazil",  "valor": 20},
            {"slug": "xbox-xbox-live-gift-card-30-brl-xbox-live-key-brazil",  "valor": 30, "sin_stock": True},
            {"slug": "xbox-xbox-live-gift-card-40-brl-xbox-live-key-brazil",  "valor": 40},
            {"slug": "xbox-xbox-live-gift-card-50-brl-xbox-live-key-brazil",  "valor": 50},
            {"slug": "xbox-xbox-live-gift-card-100-brl-xbox-live-key-brazil", "valor": 100},
        ],
        "umbral": UMBRALES["BRL"]["umbral"],
        "umbral_bajo": UMBRALES["BRL"]["umbral_bajo"],
    },
    "CLP": {
        "nombre": "Peso chileno",
        "bandera": "🇨🇱",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-10-000-clp-xbox-live-key-chile", "valor": 10000, "sin_stock": True},
            {"slug": "xbox-xbox-live-gift-card-20-000-clp-xbox-live-key-chile", "valor": 20000, "sin_stock": True},
            {"slug": "xbox-xbox-live-gift-card-35-000-clp-xbox-live-key-chile", "valor": 35000, "sin_stock": True},
        ],
        "umbral": UMBRALES["CLP"]["umbral"],
        "umbral_bajo": UMBRALES["CLP"]["umbral_bajo"],
    },
    "COP": {
        "nombre": "Peso colombiano",
        "bandera": "🇨🇴",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-30-000-cop-key-colombia",   "valor": 30000},
            {"slug": "xbox-xbox-live-gift-card-55-000-cop-key-colombia",   "valor": 55000},
            {"slug": "xbox-xbox-live-gift-card-100-000-cop-key-colombia",  "valor": 100000},
            {"slug": "xbox-xbox-live-gift-card-150-000-cop-key-colombia",  "valor": 150000},
        ],
        "umbral": UMBRALES["COP"]["umbral"],
        "umbral_bajo": UMBRALES["COP"]["umbral_bajo"],
    },
    "ZAR": {
        "nombre": "Rand sudafricano",
        "bandera": "🇿🇦",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-50-zar-xbox-live-key-south-africa",  "valor": 50},
            {"slug": "xbox-xbox-live-gift-card-100-zar-xbox-live-key-south-africa", "valor": 100},
            {"slug": "xbox-xbox-live-gift-card-150-zar-xbox-live-key-south-africa", "valor": 150},
            {"slug": "xbox-xbox-live-gift-card-200-zar-xbox-live-key-south-africa", "valor": 200},
            {"slug": "xbox-xbox-live-gift-card-500-zar-xbox-live-key-south-africa", "valor": 500},
            {"slug": "xbox-xbox-live-gift-card-600-zar-xbox-live-key-south-africa", "valor": 600},
        ],
        "umbral": UMBRALES["ZAR"]["umbral"],
        "umbral_bajo": UMBRALES["ZAR"]["umbral_bajo"],
    },
    "SAR": {
        "nombre": "Riyal saudí",
        "bandera": "🇸🇦",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-50-sar-xbox-live-key-saudi-arabia",  "valor": 50},
            {"slug": "xbox-xbox-live-gift-card-100-usd-xbox-live-key-saudi-arabia", "valor": 100},
            {"slug": "xbox-xbox-live-gift-card-200-sar-xbox-live-key-saudi-arabia", "valor": 200},
            {"slug": "xbox-xbox-live-gift-card-300-sar-xbox-live-key-saudi-arabia", "valor": 300},
        ],
        "umbral": UMBRALES["SAR"]["umbral"],
        "umbral_bajo": UMBRALES["SAR"]["umbral_bajo"],
    },
    "TWD": {
        "nombre": "Dólar taiwanés",
        "bandera": "🇹🇼",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-200-twd-xbox-live-key-taiwan",  "valor": 200, "sin_stock": True},
            {"slug": "xbox-xbox-live-gift-card-250-twd-xbox-live-key-taiwan",  "valor": 250, "sin_stock": True},
            {"slug": "xbox-xbox-live-gift-card-500-twd-xbox-live-key-taiwan",  "valor": 500, "sin_stock": True},
            {"slug": "xbox-xbox-live-gift-card-1000-twd-xbox-live-key-taiwan", "valor": 1000, "sin_stock": True},
            {"slug": "xbox-xbox-live-gift-card-2000-twd-xbox-live-key-taiwan", "valor": 2000, "sin_stock": True},
        ],
        "umbral": UMBRALES["TWD"]["umbral"],
        "umbral_bajo": UMBRALES["TWD"]["umbral_bajo"],
    },
    "HKD": {
        "nombre": "Dólar de Hong Kong",
        "bandera": "🇭🇰",
        "slugs": [
            {"slug": "xbox-xbox-live-gift-card-150-hkd-xbox-live-key-hong-kong", "valor": 150},
            {"slug": "xbox-xbox-live-gift-card-300-hkd-xbox-live-key-hong-kong", "valor": 300},
            {"slug": "xbox-xbox-live-gift-card-600-hkd-xbox-live-key-hong-kong", "valor": 600},
        ],
        "umbral": UMBRALES["HKD"]["umbral"],
        "umbral_bajo": UMBRALES["HKD"]["umbral_bajo"],
    },
}

# ─── IMPORTS ──────────────────────────────────────────────────────────────────
import os
import json
import time
import csv
import io
import requests
from datetime import datetime, timezone, timedelta

# ─── TELEGRAM ─────────────────────────────────────────────────────────────────
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ─── HEADERS ENEBA ────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "*/*",
    "Accept-Language": "es_ES",
    "content-type": "application/json",
    "Origin": "https://www.eneba.com",
    "Referer": "https://www.eneba.com/",
}

ESTADO_FILE = "estado.json"

# ─── FUNCIONES ────────────────────────────────────────────────────────────────

def send_telegram(msg):
    try:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"Error enviando Telegram: {e}")

def send_telegram_file(filename, content, caption=""):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendDocument",
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"document": (filename, content, "text/csv")},
            timeout=30
        )
    except Exception as e:
        print(f"Error enviando archivo Telegram: {e}")

def get_tipo_cambio_real(monedas):
    """Obtiene todos los tipos de cambio en una sola petición"""
    try:
        # Filtrar SAR porque frankfurter no lo soporta
        monedas_api = [m for m in monedas if m != "SAR"]
        simbolos = ",".join(monedas_api)
        r = requests.get(
            f"https://api.frankfurter.app/latest?from=EUR&to={simbolos}",
            timeout=5
        )
        rates = {}
        if r.status_code == 200:
            rates = r.json().get("rates", {})
        # SAR calculado via USD (tipo fijo 1 USD = 3.75 SAR)
        if "SAR" in monedas and "USD" in rates:
            rates["SAR"] = round(rates["USD"] * 3.75, 4)
        return rates
    except:
        return {}

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
    try:
        r = requests.post(
            "https://graphql.eneba.com/graphql/",
            json=body,
            headers=HEADERS,
            timeout=10
        )
        if r.status_code != 200:
            print(f"❌ SHA inválido o API cambiada (status {r.status_code})")
            send_telegram(
                "⚠️ <b>SHA de Eneba ha cambiado</b>\n"
                "La API no responde correctamente.\n"
                "1. Abre Eneba en el navegador\n"
                "2. F12 → Network → filtra 'graphql'\n"
                "3. Abre petición POST → Payload → sha256Hash\n"
                "4. Actualiza la variable SHA en check_price.py"
            )
            return None, False
        data = r.json()
        if "errors" in data:
            print(f"❌ Error GraphQL: {data['errors']}")
            return None, False
        edges = data["data"]["productNoCache"]["auctions"]["edges"]
        # Precios con stock
        prices_con_stock = [
            e["node"]["price"]["amount"]
            for e in edges
            if e["node"]["isInStock"]
            and e["node"]["isCurrentlyAvailable"]
            and e["node"]["price"]["amount"] > 0
        ]
        # Verificar si hay edges pero sin stock
        hay_producto = len(edges) > 0
        if prices_con_stock:
            return min(prices_con_stock), True
        elif hay_producto:
            return None, False  # Existe pero sin stock
        else:
            return None, None  # No existe o slug incorrecto
    except Exception as e:
        print(f"Error de red en {slug}: {e}")
        return None, None

def cargar_estado():
    if os.path.exists(ESTADO_FILE):
        with open(ESTADO_FILE, "r") as f:
            return json.load(f)
    return {"monedas": {}, "historial": [], "resumenes": {}}

def guardar_estado(estado):
    with open(ESTADO_FILE, "w") as f:
        json.dump(estado, f, indent=2)

def get_ratios_moneda(config):
    """Devuelve lista de resultados con precio y stock para cada tarjeta"""
    resultados = []
    for item in config["slugs"]:
        slug = item["slug"]
        valor = item["valor"]
        forzar_sin_stock = item.get("sin_stock", False)

        if forzar_sin_stock:
            resultados.append({"valor": valor, "precio_eur": None, "ratio": None, "stock": False})
            continue

        price_cents, tiene_stock = get_price(slug)
        if price_cents and tiene_stock:
            price_eur = price_cents / 100
            ratio = valor / price_eur
            resultados.append({"valor": valor, "precio_eur": price_eur, "ratio": ratio, "stock": True})
            print(f"  {valor} = {price_eur:.2f}€ → {ratio:.2f}/€")
        else:
            resultados.append({"valor": valor, "precio_eur": None, "ratio": None, "stock": False})
            print(f"  {valor} = ⚫ Sin stock")
        time.sleep(0.5)
    return resultados

def procesar_alertas(moneda, config, resultados, estado, tipos_cambio):
    con_stock = [r for r in resultados if r["stock"] and r["ratio"]]

    estado_moneda = estado["monedas"].get(moneda, {
        "ultimo_ratio_alertado": None,
        "sobre_umbral": False,
        "bajo_umbral_bajo": False,
        "sin_datos_alertado": False,
    })

    if not con_stock:
        # Solo alertar una vez si no hay datos (no repetir cada 20 min)
        if not estado_moneda.get("sin_datos_alertado"):
            send_telegram(
                f"⚠️ <b>Sin stock: {config['bandera']} {moneda}</b>\n"
                f"Ninguna tarjeta disponible en este momento."
            )
            estado_moneda["sin_datos_alertado"] = True
        estado["monedas"][moneda] = estado_moneda
        return
    else:
        estado_moneda["sin_datos_alertado"] = False

    mejor = max(con_stock, key=lambda x: x["ratio"])
    mejor_ratio = mejor["ratio"]
    umbral = config["umbral"]
    umbral_bajo = config["umbral_bajo"]
    tipo_cambio = tipos_cambio.get(moneda)

    # Comparativa con tipo de cambio real
    comparativa = ""
    if tipo_cambio:
        margen = ((mejor_ratio / tipo_cambio) - 1) * 100
        signo = "+" if margen >= 0 else ""
        comparativa = f"\n💱 Cambio real: {tipo_cambio:.2f} {moneda}/€ ({signo}{margen:.1f}% vs mercado)"

    # Aviso si cae por debajo del umbral bajo
    if mejor_ratio < umbral_bajo and not estado_moneda.get("bajo_umbral_bajo"):
        send_telegram(
            f"📉 <b>Precio alto {config['bandera']} {moneda}</b>\n"
            f"Ratio actual: {mejor_ratio:.2f} {moneda}/€\n"
            f"Por debajo de tu mínimo de {umbral_bajo}{comparativa}"
        )
        estado_moneda["bajo_umbral_bajo"] = True
    elif mejor_ratio >= umbral_bajo:
        estado_moneda["bajo_umbral_bajo"] = False

    # Alerta por umbral alto
    if mejor_ratio >= umbral:
        ultimo = estado_moneda.get("ultimo_ratio_alertado")
        debe_alertar = False
        if not estado_moneda.get("sobre_umbral"):
            debe_alertar = True
        elif ultimo is not None and mejor_ratio > ultimo + 0.5:
            debe_alertar = True

        if debe_alertar:
            send_telegram(
                f"🚨 <b>Alerta {config['bandera']} {moneda}</b>\n"
                f"Mejor ratio: <b>{mejor_ratio:.2f} {moneda}/€</b>\n"
                f"Tarjeta: {mejor['valor']} {moneda} por {mejor['precio_eur']:.2f}€"
                f"{comparativa}"
            )
            estado_moneda["ultimo_ratio_alertado"] = mejor_ratio
            estado_moneda["sobre_umbral"] = True
    else:
        estado_moneda["sobre_umbral"] = False
        estado_moneda["ultimo_ratio_alertado"] = None

    estado["monedas"][moneda] = estado_moneda

def guardar_historial(moneda, resultados, estado, ahora):
    con_stock = [r for r in resultados if r["stock"] and r["ratio"]]
    if not con_stock:
        return
    mejor = max(con_stock, key=lambda x: x["ratio"])
    estado["historial"].append({
        "moneda": moneda,
        "timestamp": ahora.isoformat(),
        "mejor_ratio": round(mejor["ratio"], 2),
        "mejor_valor": mejor["valor"],
        "mejor_precio_eur": round(mejor["precio_eur"], 4),
    })
    limite = (ahora - timedelta(days=180)).isoformat()
    historial_previo = list(estado["historial"])
    estado["historial"] = [h for h in estado["historial"] if h["timestamp"] >= limite]
    if len(estado["historial"]) < len(historial_previo):
        exportar_historial_csv(historial_previo, ahora)

def exportar_historial_csv(historial, ahora):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["moneda", "timestamp", "mejor_ratio", "mejor_valor", "mejor_precio_eur"])
    writer.writeheader()
    writer.writerows(historial)
    contenido = output.getvalue().encode("utf-8")
    nombre = f"historial_eneba_{ahora.strftime('%Y%m%d')}.csv"
    send_telegram_file(nombre, contenido, f"📦 Historial archivado — {ahora.strftime('%d/%m/%Y')}")
    print(f"Historial exportado: {nombre}")

def debe_enviar_resumen(tipo, estado, ahora):
    ultimo = estado.get("resumenes", {}).get(f"ultimo_{tipo}")
    if tipo == "diario":
        return ultimo != ahora.strftime("%Y-%m-%d")
    elif tipo == "semanal":
        return ultimo != f"{ahora.isocalendar()[0]}-W{ahora.isocalendar()[1]}"
    return False

def marcar_resumen_enviado(tipo, estado, ahora):
    if "resumenes" not in estado:
        estado["resumenes"] = {}
    if tipo == "diario":
        estado["resumenes"]["ultimo_diario"] = ahora.strftime("%Y-%m-%d")
    elif tipo == "semanal":
        estado["resumenes"]["ultimo_semanal"] = f"{ahora.isocalendar()[0]}-W{ahora.isocalendar()[1]}"

def formatear_bloque_moneda(moneda, config, resultados, tipo_cambio):
    con_stock = [r for r in resultados if r["stock"] and r["ratio"]]
    lineas = [f"{config['bandera']} <b>{moneda}</b>"]

    if not con_stock:
        # Todas sin stock
        for r in resultados:
            lineas.append(f"  {r['valor']} {moneda} → ⚫ Sin stock")
        lineas.append("")
        return lineas

    mejor = max(con_stock, key=lambda x: x["ratio"])

    for r in resultados:
        if not r["stock"]:
            lineas.append(f"  {r['valor']} {moneda} → ⚫ Sin stock")
        elif r["valor"] == mejor["valor"]:
            lineas.append(f"  🏆 <b>{r['valor']} {moneda} → {r['ratio']:.2f} {moneda}/€</b>")
        else:
            lineas.append(f"  {r['valor']} {moneda} → {r['ratio']:.2f} {moneda}/€")

    lineas.append(f"  (umbral: {config['umbral']})")

    if tipo_cambio:
        margen = ((mejor["ratio"] / tipo_cambio) - 1) * 100
        signo = "+" if margen >= 0 else ""
        lineas.append(f"  💱 Cambio real: {tipo_cambio:.2f} {moneda}/€ ({signo}{margen:.1f}%)")

    lineas.append("")
    return lineas

def enviar_resumen_diario(estado, ahora, tipos_cambio):
    lineas = [f"📊 <b>Resumen diario Eneba — {ahora.strftime('%d/%m/%Y')}</b>\n"]
    for moneda, config in MONEDAS.items():
        print(f"  Obteniendo {moneda}...")
        resultados = get_ratios_moneda(config)
        tipo_cambio = tipos_cambio.get(moneda)
        lineas += formatear_bloque_moneda(moneda, config, resultados, tipo_cambio)
    send_telegram("\n".join(lineas))
    marcar_resumen_enviado("diario", estado, ahora)

def enviar_resumen_semanal(estado, ahora):
    lineas = [f"📈 <b>Resumen semanal Eneba — semana {ahora.isocalendar()[1]}</b>\n"]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for moneda in MONEDAS:
        config = MONEDAS[moneda]
        una_semana = (ahora - timedelta(days=7)).isoformat()
        semana = [h for h in estado["historial"] if h["moneda"] == moneda and h["timestamp"] >= una_semana]
        if not semana:
            lineas.append(f"{config['bandera']} <b>{moneda}</b>: sin datos esta semana\n")
            continue
        mejor = max(semana, key=lambda x: x["mejor_ratio"])
        peor = min(semana, key=lambda x: x["mejor_ratio"])
        mejor_dt = datetime.fromisoformat(mejor["timestamp"])
        peor_dt = datetime.fromisoformat(peor["timestamp"])
        lineas.append(f"{config['bandera']} <b>{moneda}</b>")
        lineas.append(f"  🏆 Mejor: {mejor['mejor_ratio']:.2f} {moneda}/€")
        lineas.append(f"     {dias[mejor_dt.weekday()]} {mejor_dt.strftime('%d/%m')} a las {mejor_dt.strftime('%H:%M')} ({mejor['mejor_valor']} {moneda} por {mejor['mejor_precio_eur']:.2f}€)")
        lineas.append(f"  📉 Peor: {peor['mejor_ratio']:.2f} {moneda}/€")
        lineas.append(f"     {dias[peor_dt.weekday()]} {peor_dt.strftime('%d/%m')} a las {peor_dt.strftime('%H:%M')}\n")
    send_telegram("\n".join(lineas))
    marcar_resumen_enviado("semanal", estado, ahora)

def main():
    ahora = datetime.now(timezone.utc)
    hora_canarias = ahora.hour - 1
    es_lunes = ahora.weekday() == 0

    estado = cargar_estado()

    # Obtener todos los tipos de cambio de una sola vez
    tipos_cambio = get_tipo_cambio_real(list(MONEDAS.keys()))

    # Resumen semanal: lunes después de las 9am
    if es_lunes and hora_canarias >= 9 and debe_enviar_resumen("semanal", estado, ahora):
        print("Enviando resumen semanal...")
        enviar_resumen_semanal(estado, ahora)

    # Resumen diario: después de las 9am
    if debe_enviar_resumen("diario", estado, ahora):
        print("Enviando resumen diario...")
        enviar_resumen_diario(estado, ahora, tipos_cambio)
    else:
        for moneda, config in MONEDAS.items():
            print(f"\nComprobando {moneda}...")
            resultados = get_ratios_moneda(config)
            procesar_alertas(moneda, config, resultados, estado, tipos_cambio)
            guardar_historial(moneda, resultados, estado, ahora)

    guardar_estado(estado)

if __name__ == "__main__":
    main()
