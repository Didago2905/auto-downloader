import subprocess
from pathlib import Path


def es_rar_valido(ruta_archivo):
    with open(ruta_archivo, "rb") as f:
        firma = f.read(6)
    return firma.startswith(b"Rar!")


print("EXTRACTOR.PY CARGADO CORRECTAMENTE")


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
