import requests
from pathlib import Path

# Headers tipo navegador (clave)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://www.mediafire.com/",
}


def descargar_archivo(url, carpeta_destino="downloads", reintentos=2):
    carpeta = Path(carpeta_destino)
    carpeta.mkdir(exist_ok=True)

    nombre_archivo = url.split("/")[-1]
    ruta_archivo = carpeta / nombre_archivo

    # Si ya existe, reutilizamos
    if ruta_archivo.exists():
        print(f"El archivo ya existe, se reutiliza: {ruta_archivo}")
        return ruta_archivo

    session = requests.Session()
    session.headers.update(HEADERS)

    for intento in range(1, reintentos + 2):
        print(f"Descargando archivo real (intento {intento}): {nombre_archivo}")

        with session.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()

            # Validación rápida por Content-Type
            content_type = r.headers.get("Content-Type", "").lower()
            if "text/html" in content_type:
                if intento <= reintentos:
                    print("MediaFire devolvió HTML. Reintentando...")
                    continue
                raise RuntimeError(
                    "Descarga fallida: se recibió HTML en lugar del archivo."
                )

            with open(ruta_archivo, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        print(f"Archivo descargado en: {ruta_archivo}")
        return ruta_archivo

    raise RuntimeError("No se pudo descargar el archivo real tras varios intentos.")
