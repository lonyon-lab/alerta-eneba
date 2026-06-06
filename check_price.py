Perfecto, esto es exactamente lo que necesitaba. Veo algo importante: la cookie `cf_clearance` que es la protección de Cloudflare. Esa cookie es personal tuya y caduca, así que no podemos usarla directamente en el script.

Pero lo que sí podemos usar es toda la estructura de la petición GraphQL: la URL, los headers básicos y el body con `currency: EUR`. El problema será si Cloudflare bloquea las peticiones sin esa cookie.

Vamos a probarlo. Reemplaza todo el `check_price.py` con esto:

```python
import os
import re
import requests

THRESHOLD = float(os.environ["PRICE_THRESHOLD"])
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SLUGS = [
    "xbox-xbox-live-gift-card-10-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-20-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-25-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-40-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-50-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-80-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-100-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-250-try-xbox-live-key-turkey",
    "xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey",
]

TRY_VALUES = [10, 20, 25, 40, 50, 80, 100, 250, 300]

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
    print(f"{slug}: status {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        try:
            amount = data["data"]["productNoCache"]["preferredAuction"]["price"]["amount"]
            return amount  # en céntimos
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
```

Guarda, ejecuta y dime qué aparece en el log.
