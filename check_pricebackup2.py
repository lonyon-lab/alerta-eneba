# Script para trackear el ratio TRY/€ en Eneba
# Web: https://www.eneba.com/es/xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey
# Objetivo: alertar por Telegram cuando cualquier tarjeta Xbox TRY supere X TRY/€
# La API es GraphQL en graphql.eneba.com
# Si se rompe: buscar nuevo sha256Hash en Network del navegador filtrando por "graphql"
# y actualizar la variable SHA en este script

import os
import requests

THRESHOLD = float(os.environ["PRICE_THRESHOLD"])
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SLUGS = [
    "xbox-xbox-live-gift-card-25-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-50-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-100-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-250-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey",
]

TRY_VALUES = [25, 50, 100, 250, 300]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "*/*",
    "Accept-Language": "es_ES",
    "content-type": "application/json",
    "Origin": "https://www.eneba.com",
    "Referer": "https://www.eneba.com/",
}

SHA = "c3aaf0194bab3a8481512069d9bbc707037714c0a60f603497bc820f00a91c11_50e5e0d9351bb05ab629b0eda9b116ae4d96fbb6861836383bc404f1ab5e3680094635224c07d364fff371b7517712ebd33ce0f05504f2fa7e9d66e321168e02"

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
                 params={"chat_id": CHAT_ID, "text": msg})

def main():
    best_ratio = 0
    best_info = None

    for slug, try_val in zip(SLUGS, TRY_VALUES):
        price_cents = get_price(slug)
        if price_cents and price_cents > 0:
            price_eur = price_cents / 100
            ratio = try_val / price_eur
            print(f"{try_val} TRY = {price_eur}€ → {ratio:.2f} TRY/€")
            if ratio > best_ratio:
                best_ratio = ratio
                best_info = (try_val, price_eur)

    if not best_info:
        print("No se obtuvieron precios")
        send_telegram("⚠️ Alerta Eneba: el script no pudo obtener precios. Puede que la API haya cambiado.")
        return

    print(f"Mejor ratio: {best_ratio:.2f} TRY/€ (umbral: {THRESHOLD})")

    if best_ratio >= THRESHOLD:
        send_telegram(
            f"🚨 Alerta Eneba!\n"
            f"Mejor ratio: {best_ratio:.2f} TRY/€\n"
            f"Tarjeta: {best_info[0]} TRY por {best_info[1]}€\n"
            f"https://www.eneba.com/es/xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey"
        )
    else:
        print("Por debajo del umbral, no se envía alerta")

if __name__ == "__main__":
    main()
