from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

def descargar_con_playwright(url, carpeta_destino="downloads"):
    carpeta = Path(carpeta_destino)
    carpeta.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto(url, wait_until="domcontentloaded")

        try:
            page.wait_for_selector("#downloadButton", timeout=15000)

            with page.expect_download() as download_info:
                page.click("#downloadButton")

            download = download_info.value
            nombre = download.suggested_filename
            ruta_final = carpeta / nombre

            download.save_as(ruta_final)

            browser.close()
            return ruta_final

        except TimeoutError:
            browser.close()
            raise RuntimeError("Playwright no pudo iniciar la descarga")
