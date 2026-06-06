import os
import re
import requests
from playwright.sync_api import sync_playwright

URL = "https://www.eneba.com/es/xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey"
THRESHOLD = float(os.environ["PRICE_THRESHOLD"])
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": msg})

def get_ratios():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)
        content = page.content()
        browser.close()

    # Buscar todos los ratios TRY por euro
    matches = re.findall(r'([\d.]+)\s*TRY por 1\s*€', content)
    ratios = [(float(m), ) for m in matches]
    return ratios

def main():
    ratios = get_ratios()
    if not ratios:
        print("No se encontraron ratios")
        return

    best = max(r[0] for r in ratios)
    print(f"Mejor ratio encontrado: {best} TRY/€ (umbral: {THRESHOLD})")

    if best >= THRESHOLD:
        send_telegram(
            f"🚨 Alerta Eneba!\n"
            f"Ratio actual: {best} TRY por €\n"
            f"Supera tu umbral de {THRESHOLD} TRY/€\n"
            f"{URL}"
        )

if __name__ == "__main__":
    main()
