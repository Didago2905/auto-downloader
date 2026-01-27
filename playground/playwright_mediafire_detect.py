from playwright.sync_api import sync_playwright, TimeoutError

MEDIAFIRE_URL = " https://www.mediafire.com/file/52r0ii1ztbwcfzc/La.teor%C3%ADa.del.Big.Bang.1x14.HD1080p-lat.rar/file"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Abriendo MediaFire...")
    page.goto(MEDIAFIRE_URL, wait_until="domcontentloaded")

    try:
        print("Esperando botón de descarga...")
        boton = page.wait_for_selector(
            "#downloadButton",
            timeout=15000
        )

        print("✅ Botón de descarga detectado")
        print("Texto del botón:", boton.inner_text())

    except TimeoutError:
        print("❌ No se detectó el botón de descarga")

    page.wait_for_timeout(5000)
    browser.close()
