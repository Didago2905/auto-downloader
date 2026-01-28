import re
import unicodedata
from pathlib import Path
from datetime import datetime


def quitar_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def detectar_temporada_episodio(nombre):
    """
    Detecta formatos tipo:
    - 2x05
    - S02E05
    Devuelve (season, episode) o (None, None)
    """
    patrones = [
        re.compile(r"(\d{1,2})x(\d{2})", re.IGNORECASE),
        re.compile(r"S(\d{1,2})E(\d{2})", re.IGNORECASE),
    ]

    for patron in patrones:
        match = patron.search(nombre)
        if match:
            return int(match.group(1)), int(match.group(2))

    return None, None


def renombrar_video(
    ruta_video: Path,
    nombre_serie: str,
    log_path: Path
):
    season, episode = detectar_temporada_episodio(ruta_video.name)

    if season is None or episode is None:
        print(f"⚠️ No se pudo detectar S/E en: {ruta_video.name}")
        return ruta_video

    nombre_limpio = quitar_acentos(nombre_serie)
    nombre_limpio = nombre_limpio.replace(" ", ".")

    nuevo_nombre = (
        f"{nombre_limpio}.S{season:02d}E{episode:02d}"
        f"{ruta_video.suffix}"
    )

    nueva_ruta = ruta_video.with_name(nuevo_nombre)

    if nueva_ruta.exists():
        print(f"⚠️ Ya existe: {nuevo_nombre}")
        return ruta_video

    ruta_video.rename(nueva_ruta)

    # Log
    log_path.parent.mkdir(exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.now().isoformat(timespec='seconds')}]\n"
            f"{ruta_video.name}\n"
            f"→ {nuevo_nombre}\n\n"
        )

    print(f"✏️ Renombrado: {nuevo_nombre}")
    return nueva_ruta
