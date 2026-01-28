from pathlib import Path
import re

def leer_links(ruta_archivo):
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo de links: {ruta_archivo}")

    links = []

    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()

        if not linea or linea.startswith("#"):
            continue

        # Extraer la primera URL válida de la línea
        match = re.search(r"(https?://\S+)", linea)

        if match:
            links.append(match.group(1))
        else:
            print(f"⚠️ Línea ignorada (sin URL válida): {linea}")

    return links
