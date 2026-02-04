from typing import Dict, Any, List

from core.sources.source_interpreter import (
    SourceInterpreter,
    SourceResolution,
    ResolvedItem,
)
from core.sources.source_preview import SourcePreview


class MegaSourceInterpreter(SourceInterpreter):
    """
    Intérprete específico para fuentes MEGA.
    Convierte FilePreview -> ResolvedItem cuando la fuente es resoluble.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def interpret(self, preview: SourcePreview) -> SourceResolution:
        # Primero: usar la lógica base (decisión)
        base_resolution = super().interpret(preview)

        # Si no se va a resolver, devolver tal cual
        if base_resolution.decision != "resolve":
            return base_resolution

        # Construir resolved_items a partir del preview
        resolved_items = self._build_resolved_items(preview)

        return SourceResolution(
            decision="resolve",
            reason=base_resolution.reason,
            resolved_items=resolved_items,
            requires_confirmation=base_resolution.requires_confirmation,
            metadata={
                **base_resolution.metadata,
                "provider": "mega",
                "total_items": len(resolved_items),
            },
        )

    # ==========================
    # HELPERS
    # ==========================

    def _build_resolved_items(self, preview: SourcePreview) -> List[ResolvedItem]:
        items: List[ResolvedItem] = []

        for f in preview.files:
            # Por ahora el link es simbólico (placeholder)
            # El resolver real vendrá después
            fake_link = f"mega://download/{f.name}"

            items.append(
                ResolvedItem(
                    link=fake_link,
                    name=f.name,
                    size_estimated=f.size_human,
                )
            )

        return items
