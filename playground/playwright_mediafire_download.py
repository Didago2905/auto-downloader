from playwright.sync_api import sync_playwright, TimeoutError
from pathlib import Path

MEDIAFIRE_URL = "https://www.mediafire.com/file/52r0ii1ztbwcfzc/La.teor%C3%ADa.del.Big.Bang.1x14.HD1080p-lat.rar/file"
DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    print("Abriendo MediaFire...")
    page.goto(MEDIAFIRE_URL, wait_until="domcontentloaded")

    try:
        print("Esperando botón de descarga...")
        page.wait_for_selector("#downloadButton", timeout=15000)

        print("Haciendo click y esperando descarga...")
        with page.expect_download() as download_info:
            page.click("#downloadButton")

        download = download_info.value
        suggested_name = download.suggested_filename

        ruta_final = DOWNLOADS_DIR / suggested_name
        download.save_as(ruta_final)

        print(f"✅ Descarga completada: {ruta_final}")

    except TimeoutError:
        print("❌ No se pudo iniciar la descarga")

    page.wait_for_timeout(3000)
    browser.close()
