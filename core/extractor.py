import subprocess
from pathlib import Path

print("EXTRACTOR.PY CARGADO CORRECTAMENTE")


def es_rar_valido(ruta_archivo):
    with open(ruta_archivo, "rb") as f:
        firma = f.read(6)
    return firma.startswith(b"Rar!")





def extraer_rar(archivo_rar, destino="extracted", password=None):
    archivo = Path(archivo_rar)
    if not archivo.exists():
        raise FileNotFoundError(f"No existe el archivo: {archivo_rar}")

    if not es_rar_valido(archivo):
        raise RuntimeError(
            "El archivo descargado NO es un RAR válido. "
            "Probablemente MediaFire devolvió HTML."
        )

    carpeta_destino = Path(destino)
    carpeta_destino.mkdir(exist_ok=True)

    comando = [
        r"C:\Program Files\WinRAR\unrar.exe",
        "x",
        "-o+",
    ]

    if password:
        comando.append(f"-p{password}")
    else:
        comando.append("-p-")

    comando.append(str(archivo))
    comando.append(str(carpeta_destino))

    print(f"Extrayendo: {archivo.name}")

    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode != 0:
        raise RuntimeError(
            f"Error al extraer:\nSTDOUT:\n{resultado.stdout}\nSTDERR:\n{resultado.stderr}"
        )

    print(f"Extraído en: {carpeta_destino}")


def filtrar_videos(carpeta, extensiones=None):
    if extensiones is None:
        extensiones = {".mkv", ".mp4", ".avi", ".mov", ".wmv"}

    carpeta = Path(carpeta)
    videos = []

    for archivo in carpeta.rglob("*"):
        if archivo.is_file() and archivo.suffix.lower() in extensiones:
            videos.append(archivo)

    return videos


def mover_videos(videos, destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)

    movidos = []

    for video in videos:
        destino_final = destino / video.name
        video.replace(destino_final)
        movidos.append(destino_final)

    return movidos


def limpiar_carpetas_vacias(carpeta):
    carpeta = Path(carpeta)

    for sub in sorted([p for p in carpeta.rglob("*") if p.is_dir()], reverse=True):
        if not any(sub.iterdir()):
            sub.rmdir()

def limpiar_carpetas_vacias(carpeta):
    carpeta = Path(carpeta)

    for sub in sorted(
        [p for p in carpeta.rglob("*") if p.is_dir()],
        reverse=True
    ):
        if not any(sub.iterdir()):
            sub.rmdir()
            
def borrar_archivos_no_video(carpeta, extensiones_video=None):
    if extensiones_video is None:
        extensiones_video = {".mkv", ".mp4", ".avi", ".mov", ".wmv"}

    carpeta = Path(carpeta)

    for archivo in carpeta.rglob("*"):
        if archivo.is_file() and archivo.suffix.lower() not in extensiones_video:
            archivo.unlink()

import shutil

def limpiar_extracted_completo(carpeta):
    carpeta = Path(carpeta)

    if not carpeta.exists():
        return

    for item in carpeta.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
