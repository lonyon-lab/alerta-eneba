import os
import re
from playwright.sync_api import sync_playwright

URL = "https://www.eneba.com/es/xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey"

def get_ratios():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-ES"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(6000)
        content = page.content()
        browser.close()

    idx = content.find("TRY por")
    if idx > 0:
        print("FRAGMENTO:", content[idx-50:idx+150])
    else:
        print("Sigue sin encontrar TRY por")
        print("MUESTRA HTML:", content[1000:2000])

if __name__ == "__main__":
    get_ratios()
