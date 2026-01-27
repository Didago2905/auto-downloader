from core.link_extractor import extraer_link_descarga_desde_html
from core.downloader import descargar_archivo
from core.playwright_downloader import descargar_con_playwright
from core.extractor import extraer_rar


def descargar_rar_seguro(link_real):
    try:
        ruta = descargar_archivo(link_real)
        return ruta
    except Exception as e:
        print("Descarga con requests falló, usando Playwright...")
        return descargar_con_playwright(link_real)


if __name__ == "__main__":
    ruta_html = "downloads/file"
    PASSWORD = "hackstore.ac"

    link_real = extraer_link_descarga_desde_html(ruta_html)
    print("Link real encontrado:")
    print(link_real)

    ruta_rar = descargar_rar_seguro(link_real)
    extraer_rar(ruta_rar, password=PASSWORD)
