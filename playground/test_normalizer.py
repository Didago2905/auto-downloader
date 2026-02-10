from pathlib import Path
from core.normalizer import normalizar_carpeta

normalizar_carpeta(
    carpeta=Path(r"D:\Media\Series\Dark\Season 01"),
    nombre_serie="Dark",
    temporada=1,
    episodio_inicio=1,
    mode="interactive",     # 👈 CLAVE
    dry_run=True,           # primero preview
    auto_confirm=False,     # pregunta al usuario
    log_path=Path("logs/normalizer.log"),
)
