from pathlib import Path
from typing import List, Optional
import re

# ==========================
# CONFIGURACIÓN
# ==========================

SUPPORTED_EXTENSIONS = {".mp4"}

# ==========================
# HELPERS
# ==========================


def listar_videos(carpeta: Path) -> List[Path]:
    """
    Devuelve una lista de archivos de video ordenados de forma HUMANA
    usando números tipo 1.1, 1.10, 1.2, etc.
    """
    if not carpeta.exists() or not carpeta.is_dir():
        return []

    videos = [
        f
        for f in carpeta.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    def clave_orden(video: Path):
        orden = extraer_numero_orden(video.stem)
        return (orden is None, orden)

    return sorted(videos, key=clave_orden)


def construir_nombre(
    nombre_serie: str,
    temporada: int,
    episodio: int,
    extension: str,
) -> str:
    return f"{nombre_serie}.S{temporada:02d}E{episodio:02d}{extension}"


def escribir_log(log_path: Path, original: str, nuevo: str):
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"{original} → {nuevo}\n")


def extraer_numero_episodio(nombre: str) -> Optional[int]:
    """
    Intenta extraer número de episodio explícito (S01E02, E03, etc.)
    """
    match = re.search(r"[eE](\d{1,3})", nombre)
    if match:
        return int(match.group(1))
    return None


def extraer_numero_orden(nombre: str) -> Optional[tuple[int, int]]:
    """
    Extrae números tipo:
    G4T0 1.10 -> (1, 10)
    """
    match = re.search(r"\b(\d+)\.(\d+)\b", nombre)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def pedir_confirmacion(auto_confirm: bool) -> bool:
    if auto_confirm:
        return True
    resp = input("¿Aplicar estos cambios? (y/N): ").strip().lower()
    return resp == "y"


def preview_renombrado(
    videos: List[Path],
    nombre_serie: str,
    temporada: int,
    episodio_inicio: int,
):
    preview = []
    ep = episodio_inicio
    for v in videos:
        nuevo = construir_nombre(nombre_serie, temporada, ep, v.suffix)
        preview.append((v.name, nuevo))
        ep += 1
    return preview


def detectar_temporada_por_orden(videos: List[Path]) -> Optional[int]:
    temporadas = []

    for v in videos:
        orden = extraer_numero_orden(v.stem)
        if orden is None:
            return None
        temporadas.append(orden[0])

    if len(set(temporadas)) == 1:
        return temporadas[0]

    return None


# ==========================
# FUNCIÓN PRINCIPAL
# ==========================


def normalizar_carpeta(
    carpeta: Path,
    nombre_serie: str,
    temporada: int,
    episodio_inicio: int = 1,
    log_path: Optional[Path] = None,
    dry_run: bool = True,
    allow_order_fallback: bool = True,
    auto_confirm: bool = False,
):
    videos = listar_videos(carpeta)

    if not videos:
        print(f"⚠️ No hay videos para normalizar en: {carpeta}")
        return []

    # Detectar patrones
    episodios_detectados = [extraer_numero_episodio(v.stem) for v in videos]
    hay_patron = any(e is not None for e in episodios_detectados)

    temporada_detectada = detectar_temporada_por_orden(videos)

    # ==========================
    # DETECCIÓN DE TEMPORADA
    # ==========================

    if temporada_detectada and temporada_detectada != temporada:
        print(
            f"⚠️ Se detectó posible temporada en nombres: {temporada_detectada} "
            f"(configurada: {temporada})"
        )

        if auto_confirm:
            temporada = temporada_detectada
        else:
            resp = (
                input(
                    f"¿Usar temporada {temporada_detectada} en lugar de {temporada}? (y/N): "
                )
                .strip()
                .lower()
            )

            if resp == "y":
                temporada = temporada_detectada

    # ==========================
    # FALLBACK POR ORDEN
    # ==========================

    if not hay_patron and allow_order_fallback:
        print("⚠️ No se detectó patrón fiable en los nombres.")
        print("➡️ Se propone renombrar por ORDEN.")
        print(f"📁 Archivos detectados: {len(videos)}")

        preview = preview_renombrado(
            videos,
            nombre_serie,
            temporada,
            episodio_inicio,
        )

        print("\n[PREVIEW]")
        for original, nuevo in preview:
            print(f"{original} → {nuevo}")

        if dry_run:
            print("\n🧪 DRY-RUN activo.")

            if not pedir_confirmacion(auto_confirm):
                print("⛔ Operación cancelada.")
                return []

            dry_run = False

    # ==========================
    # RENOMBRADO REAL
    # ==========================

    print(f"\n🧹 Normalizando {len(videos)} archivos en {carpeta}")

    episodio_actual = episodio_inicio
    renombrados = []

    for video in videos:
        nuevo_nombre = construir_nombre(
            nombre_serie,
            temporada,
            episodio_actual,
            video.suffix,
        )
        destino = video.with_name(nuevo_nombre)

        if destino.exists():
            print(f"⏭️ Ya existe, se omite: {destino.name}")
            episodio_actual += 1
            continue

        try:
            video.rename(destino)
            renombrados.append(destino)
            print(f"✏️ {video.name} → {destino.name}")

            if log_path:
                escribir_log(log_path, video.name, destino.name)

        except Exception as e:
            print(f"❌ Error renombrando {video.name}: {e}")

        episodio_actual += 1

    return renombrados
