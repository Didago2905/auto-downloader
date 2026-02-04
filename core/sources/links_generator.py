from pathlib import Path
from typing import Optional

from core.sources.source_interpreter import SourceResolution


class LinksGenerator:
    """
    Genera un archivo de links a partir de una SourceResolution.
    Diseñado para integrarse con el autodownloader existente.
    """

    def __init__(self, output_path: Optional[Path] = None):
        self.output_path = output_path or Path("links.generated.txt")

    def generate(self, resolution: SourceResolution) -> Path | None:
        """
        Genera el archivo de links si la resolución lo permite.
        Devuelve la ruta del archivo generado o None si no aplica.
        """

        if resolution.decision != "resolve":
            return None

        if not resolution.resolved_items:
            return None

        self.output_path.parent.mkdir(exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            for item in resolution.resolved_items:
                f.write(item.link + "\n")

        return self.output_path
