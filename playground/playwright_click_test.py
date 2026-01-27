from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://example.com")

    # Espera a que la página esté lista
    page.wait_for_load_state("domcontentloaded")

    # Simula una interacción (scroll)
    page.mouse.wheel(0, 300)

    print("Título antes:", page.title())

    page.wait_for_timeout(3000)

    browser.close()
