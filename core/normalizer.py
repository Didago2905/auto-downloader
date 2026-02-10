from pathlib import Path
from typing import List, Optional
import re

SUPPORTED_EXTENSIONS = {".mp4"}


# ==========================
# HELPERS
# ==========================


def extraer_numero_episodio(nombre: str) -> Optional[int]:
    patterns = [
        r"[sS]\d{1,2}[\s\-_.]*[eE](\d{1,3})",
        r"\b(\d{1,2})x(\d{1,3})\b",
        r"[eE](\d{1,3})",
    ]

    for p in patterns:
        match = re.search(p, nombre)
        if match:
            return int(match.groups()[-1])

    return None


def listar_videos(carpeta: Path) -> List[Path]:
    if not carpeta.exists() or not carpeta.is_dir():
        return []

    def sort_key(f: Path):
        ep = extraer_numero_episodio(f.stem)
        return (ep is None, ep if ep is not None else 0, f.name.lower())

    return sorted(
        [
            f
            for f in carpeta.rglob("*")
            if f.is_file() and f.name.lower().endswith(".mp4")
        ],
        key=sort_key,
    )


def construir_nombre(
    nombre_serie: str,
    temporada: int,
    episodio: int,
    extension: str,
) -> str:
    return f"{nombre_serie}.S{temporada:02d}E{episodio:02d}{extension}"


def escribir_log(log_path: Path, original: str, nuevo: str, mode: str):
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"[{mode}] {original} → {nuevo}\n")


def pedir_confirmacion(auto_confirm: bool) -> bool:
    if auto_confirm:
        return True
    resp = input("¿Aplicar estos cambios? (y/N): ").strip().lower()
    return resp == "y"


def preview(videos: List[Path], nuevos_nombres: List[str]):
    print("\n[PREVIEW]")
    for v, n in zip(videos, nuevos_nombres):
        print(f"{v.name} → {n}")


# ==========================
# FUNCIÓN PRINCIPAL
# ==========================


def normalizar_carpeta(
    carpeta: Path,
    nombre_serie: str,
    temporada: int,
    episodio_inicio: int = 1,
    mode: str = "by_order",  # by_order | by_name | interactive
    log_path: Optional[Path] = None,
    dry_run: bool = True,
    auto_confirm: bool = False,
):
    videos = listar_videos(carpeta)

    if not videos:
        print(f"⚠️ No hay videos para normalizar en: {carpeta}")
        return []

    nuevos_nombres = []

    # ==========================
    # MODO BY_ORDER (DEFAULT)
    # ==========================
    if mode == "by_order":
        episodio = episodio_inicio
        for v in videos:
            nuevos_nombres.append(
                construir_nombre(nombre_serie, temporada, episodio, v.suffix)
            )
            episodio += 1

    # ==========================
    # MODO BY_NAME
    # ==========================
    elif mode == "by_name":
        for v in videos:
            ep = extraer_numero_episodio(v.stem)
            if ep is None:
                raise ValueError(
                    f"No se pudo extraer episodio desde el nombre: {v.name}"
                )
            nuevos_nombres.append(
                construir_nombre(nombre_serie, temporada, ep, v.suffix)
            )

    # ==========================
    # MODO INTERACTIVE
    # ==========================
    elif mode == "interactive":
        episodio = episodio_inicio
        for v in videos:
            nuevos_nombres.append(
                construir_nombre(nombre_serie, temporada, episodio, v.suffix)
            )
            episodio += 1

        preview(videos, nuevos_nombres)

        if dry_run:
            print("\n🧪 DRY-RUN activo.")
            if not pedir_confirmacion(auto_confirm):
                print("⛔ Operación cancelada.")
                return []
            dry_run = False

    else:
        raise ValueError(f"Modo desconocido: {mode}")

    # ==========================
    # RENOMBRADO REAL
    # ==========================
    if dry_run:
        preview(videos, nuevos_nombres)
        return []

    print(f"\n🧹 Normalizando {len(videos)} archivos en {carpeta}")

    renombrados = []

    for v, nuevo in zip(videos, nuevos_nombres):
        destino = v.with_name(nuevo)

        if destino.exists():
            print(f"⏭️ Ya existe, se omite: {destino.name}")
            continue

        try:
            v.rename(destino)
            renombrados.append(destino)
            print(f"✏️ {v.name} → {destino.name}")

            if log_path:
                escribir_log(log_path, v.name, destino.name, mode)

        except Exception as e:
            print(f"❌ Error renombrando {v.name}: {e}")

    return renombrados
