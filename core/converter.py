import subprocess
from pathlib import Path


def convertir_mkv_a_mp4(archivo_mkv: Path, borrar_mkv: bool = False) -> Path:
    """
    Convierte un archivo MKV a MP4 compatible con navegador:
    - Copia el video (sin recomprimir)
    - Convierte audios a AAC
    - Convierte subtítulos de texto a mov_text
    """

    archivo_mkv = Path(archivo_mkv)

    if not archivo_mkv.exists():
        raise FileNotFoundError(f"No existe el archivo: {archivo_mkv}")

    if archivo_mkv.suffix.lower() != ".mkv":
        raise ValueError("El archivo no es MKV")

    archivo_mp4 = archivo_mkv.with_suffix(".mp4")

    if archivo_mp4.exists():
        print(f"⚠️ MP4 ya existe, se omite: {archivo_mp4.name}")
        return archivo_mp4

    comando = [
        "ffmpeg",
        "-y",
        "-i",
        str(archivo_mkv),
        "-map",
        "0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-c:s",
        "mov_text",
        str(archivo_mp4),
    ]

    print(f"🎬 Convirtiendo: {archivo_mkv.name}")

    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode != 0:
        raise RuntimeError(f"Error al convertir:\n{resultado.stderr}")

    print(f"✅ Convertido a MP4: {archivo_mp4.name}")

    if borrar_mkv:
        archivo_mkv.unlink()
        print(f"🗑️ MKV eliminado: {archivo_mkv.name}")

    return archivo_mp4


# ==========================
# PRUEBA MANUAL
# ==========================
if __name__ == "__main__":
    convertir_mkv_a_mp4(
        Path(r"D:\Series\The Big Bang Theory\Season 01\The.Big.Bang.Theory.S01E01.mkv"),
        borrar_mkv=False,
    )
