from pathlib import Path
from playwright.sync_api import sync_playwright
import time
import os

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
from core.config import (
    LIBRARY_PATH,
    SERIES_NAME,
    SEASON_NUMBER,
    RAR_PASSWORD,
    CONVERT_TO_MP4,
    DELETE_MKV,
)

# ==========================
# LOGS
# ==========================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_PATH = LOG_DIR / "autodownloader.log"
LOG_RENAME = LOG_DIR / "rename.log"
FAILED_FILE = Path("failed/failed_links.txt")

TOTAL_ORIGINAL_BYTES = 0
TOTAL_CONVERTED_BYTES = 0
PROCESS_START_TIME = None


# ==========================
# HELPERS
# ==========================


def start_global_timer():
    global PROCESS_START_TIME
    PROCESS_START_TIME = time.time()


def log_file_sizes(original_path=None, converted_path=None):
    global TOTAL_ORIGINAL_BYTES, TOTAL_CONVERTED_BYTES

    with open(LOG_PATH, "a", encoding="utf-8") as log:
        if original_path and os.path.exists(original_path):
            size = os.path.getsize(original_path)
            TOTAL_ORIGINAL_BYTES += size
            log.write(f"[ORIGINAL] {original_path} | {size / (1024**2):.2f} MB\n")

        if converted_path and os.path.exists(converted_path):
            size = os.path.getsize(converted_path)
            TOTAL_CONVERTED_BYTES += size
            log.write(f"[MP4] {converted_path} | {size / (1024**2):.2f} MB\n")


def close_global_log():
    if PROCESS_START_TIME is None:
        return

    total_time = time.time() - PROCESS_START_TIME

    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write("\n===== RESUMEN FINAL =====\n")
        log.write(f"Tamaño original: {TOTAL_ORIGINAL_BYTES / (1024**3):.2f} GB\n")
        log.write(f"Tamaño MP4: {TOTAL_CONVERTED_BYTES / (1024**3):.2f} GB\n")
        log.write(f"Tiempo total: {total_time / 60:.2f} min\n")
        log.write("=========================\n\n")


def descargar_rar_seguro(link_real):
    try:
        return descargar_archivo(link_real)
    except Exception:
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

    DESTINO_FINAL = LIBRARY_PATH / SERIES_NAME / f"Season {SEASON_NUMBER:02d}"

    if links:
        start_global_timer()

    for url in links:
        try:
            link_real = obtener_link_real_desde_mediafire(url)
            ruta_rar = descargar_rar_seguro(link_real)

            extraer_rar(ruta_rar, password=RAR_PASSWORD)

            videos = filtrar_videos("extracted")
            if not videos:
                continue

            # Conversión
            if CONVERT_TO_MP4:
                nuevos = []
                for v in videos:
                    if v.suffix.lower() == ".mkv":
                        log_file_sizes(original_path=v)
                        mp4 = convertir_mkv_a_mp4(v, borrar_mkv=DELETE_MKV)
                        log_file_sizes(converted_path=mp4)
                        nuevos.append(mp4)
                if nuevos:
                    videos = nuevos

            movidos = mover_videos(videos, DESTINO_FINAL)

            for v in movidos:
                renombrar_video(
                    ruta_video=v,
                    nombre_serie=SERIES_NAME,
                    log_path=LOG_RENAME,
                )

            limpiar_extracted_completo("extracted")

            if ruta_rar.exists():
                ruta_rar.unlink()

        except Exception:
            FAILED_FILE.parent.mkdir(exist_ok=True)
            FAILED_FILE.write_text(
                (FAILED_FILE.read_text() if FAILED_FILE.exists() else "") + url + "\n",
                encoding="utf-8",
            )

    close_global_log()
