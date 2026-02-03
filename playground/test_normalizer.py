from pathlib import Path
from core.normalizer import normalizar_carpeta

normalizar_carpeta(
    carpeta=Path(r"D:\Media\Series\Two and a Half Men\Season 04"),
    nombre_serie="Two and a Half Men",
    temporada=1,
    episodio_inicio=1,
    dry_run=True,
    allow_order_fallback=True,
    auto_confirm=False, 
    log_path=Path("logs/normalizer.log"),
)
