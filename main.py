from pathlib import Path
from playwright.sync_api import sync_playwright

from core.batch import leer_links
from core.downloader import descargar_archivo
from core.playwright_downloader import descargar_con_playwright
from core.extractor import (
    extraer_rar,
    filtrar_videos,
    mover_videos,
    limpiar_extracted_completo,
)
from core.converter import convertir_mkv_a_mp4
from core.renamer import renombrar_video


# ==========================
# CONFIGURACIÓN
# ==========================

PASSWORD = "hackstore.ac"

CONVERTIR_A_MP4 = True
BORRAR_MKV_ORIGINAL = True

RUTA_SERIES = Path(r"D:\Media\Series")
NOMBRE_SERIE = "The Big Bang Theory"
TEMPORADA_ACTUAL = 1

DESTINO_FINAL = RUTA_SERIES / NOMBRE_SERIE / f"Season {TEMPORADA_ACTUAL:02d}"

FAILED_FILE = Path("failed/failed_links.txt")
LOG_RENAME = Path("logs/rename.log")


# ==========================
# HELPERS
# ==========================


def descargar_rar_seguro(link_real):
    try:
        return descargar_archivo(link_real)
    except Exception:
        print("Descarga con requests falló, usando Playwright...")
        return descargar_con_playwright(link_real)


def obtener_link_real_desde_mediafire(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_selector("#downloadButton", timeout=15000)
        link = page.locator("#downloadButton").get_attribute("href")
        browser.close()
        return link


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    links = leer_links("links.txt")

    for i, url in enumerate(links, start=1):
        print(f"\n=== Procesando {i}/{len(links)} ===")
        print(url)

        try:
            # 1. Link real
            link_real = obtener_link_real_desde_mediafire(url)

            # 2. Descargar RAR
            ruta_rar = descargar_rar_seguro(link_real)

            # 3. Extraer
            extraer_rar(ruta_rar, password=PASSWORD)

            # 4. Buscar videos
            videos = filtrar_videos("extracted")

            if not videos:
                print("⚠️ No se encontraron videos")
                continue

            print("🎬 Videos encontrados:")
            for v in videos:
                print(" -", v.name)

            # 5. Convertir MKV → MP4
            if CONVERTIR_A_MP4:
                mp4_generados = []

                for video in videos:
                    if video.suffix.lower() == ".mkv":
                        mp4 = convertir_mkv_a_mp4(video, borrar_mkv=BORRAR_MKV_ORIGINAL)
                        mp4_generados.append(mp4)

                if mp4_generados:
                    videos = mp4_generados

            # 6. Mover a destino final
            movidos = mover_videos(videos, DESTINO_FINAL)

            # 7. Renombrar
            finales = []
            for v in movidos:
                nuevo = renombrar_video(
                    ruta_video=v, nombre_serie=NOMBRE_SERIE, log_path=LOG_RENAME
                )
                finales.append(nuevo)

            # 8. Limpiar temporales
            limpiar_extracted_completo("extracted")

            # 9. Borrar RAR
            if ruta_rar.exists():
                ruta_rar.unlink()
                print(f"🧹 RAR eliminado: {ruta_rar.name}")

            print("🎯 Videos finales listos para streaming:")
            for v in finales:
                print(" -", v.name)

        except Exception as e:
            print("❌ Error con este link:", e)
            FAILED_FILE.parent.mkdir(exist_ok=True)
            FAILED_FILE.write_text(
                (
                    FAILED_FILE.read_text(encoding="utf-8")
                    if FAILED_FILE.exists()
                    else ""
                )
                + url
                + "\n",
                encoding="utf-8",
            )
