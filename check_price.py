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
    print("Iniciando Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-ES",
            extra_http_headers={"Accept-Language": "es-ES,es;q=0.9"}
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto("https://www.eneba.com/es/", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(6000)
        content = page.content()
        browser.close()

  

    matches = re.findall(r'([\d.]+)\s*TRY por\s*<span[^>]*>1(?:&nbsp;|\s*)US\$</span>', content)
    ratios = [float(m) for m in matches]
    return ratios

def main():
    ratios = get_ratios()
    if not ratios:
        print("No se encontraron ratios")
        return

    best = max(ratios)
    print(f"Mejor ratio: {best} TRY/$ (umbral: {THRESHOLD})")

    if best >= THRESHOLD:
        send_telegram(
            f"🚨 Alerta Eneba!\n"
            f"Ratio actual: {best} TRY por $\n"
            f"Supera tu umbral de {THRESHOLD} TRY/$\n"
            f"{URL}"
        )
    else:
        print("Por debajo del umbral, no se envía alerta")

if __name__ == "__main__":
    main()
