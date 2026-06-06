import os
import re
import requests
from playwright.sync_api import sync_playwright

URL = "https://www.eneba.com/es/xbox-xbox-live-gift-card-300-try-xbox-live-key-turkey"

def get_ratios():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)
        content = page.content()
        browser.close()

    # Imprimir fragmento del HTML para debug
    idx = content.find("TRY")
    if idx > 0:
        print("FRAGMENTO:", content[idx-100:idx+200])
    else:
        print("No se encontró TRY en el HTML")
        print("INICIO HTML:", content[:500])

if __name__ == "__main__":
    get_ratios()
