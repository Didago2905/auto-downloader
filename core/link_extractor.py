from bs4 import BeautifulSoup
from pathlib import Path

def extraer_link_descarga_desde_html(ruta_html):
    ruta = Path(ruta_html)

    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta_html}")

    html = ruta.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    boton = soup.find(id="downloadButton")

    if boton is None:
        raise ValueError("No se encontró el botón de descarga")

    href = boton.get("href")

    if not href:
        raise ValueError("El botón no contiene un href")

    return href
