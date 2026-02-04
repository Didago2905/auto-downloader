from dataclasses import dataclass, field
from typing import List, Dict, Any

from core.sources.source_preview import SourcePreview


# ==========================
# MODELO DE RESOLUCIÓN
# ==========================


@dataclass(frozen=True)
class ResolvedItem:
    link: str
    name: str
    size_estimated: str | None = None


@dataclass(frozen=True)
class SourceResolution:
    decision: str  # "resolve" | "skip" | "blocked"
    reason: str
    resolved_items: List[ResolvedItem] = field(default_factory=list)
    requires_confirmation: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================
# INTERPRETER BASE
# ==========================


class SourceInterpreter:
    """
    Intérprete base de fuentes.

    - Decide si una fuente puede resolverse
    - Respeta configuración
    - NO descarga
    - NO conoce detalles del proveedor
    """

    def __init__(self, config: Dict[str, Any]):
        """
        config esperado (parcial):

        {
          "sources": {
            "resolve_requires_confirmation": true
          }
        }
        """
        self.config = config or {}
        self.sources_config = self.config.get("sources", {})

    # ==========================
    # API PÚBLICA
    # ==========================

    def interpret(self, preview: SourcePreview) -> SourceResolution:
        """
        Interpreta una fuente a partir de su preview.
        """

        # Fuente no resoluble por naturaleza
        if not preview.resolvable:
            return SourceResolution(
                decision="blocked",
                reason="Source marked as not resolvable",
                requires_confirmation=False,
                metadata={
                    "source_type": preview.source_type,
                    "origin": preview.origin,
                },
            )

        # ¿Requiere confirmación humana?
        requires_confirmation = self._requires_confirmation()

        if requires_confirmation:
            # La decisión final depende del usuario (fuera de este módulo)
            return SourceResolution(
                decision="skip",
                reason="Resolution requires user confirmation",
                requires_confirmation=True,
                metadata={
                    "source_type": preview.source_type,
                    "origin": preview.origin,
                },
            )

        # Resolución automática permitida
        return SourceResolution(
            decision="resolve",
            reason="Automatic resolution allowed by config",
            requires_confirmation=False,
            metadata={
                "source_type": preview.source_type,
                "origin": preview.origin,
            },
        )

    # ==========================
    # HELPERS
    # ==========================

    def _requires_confirmation(self) -> bool:
        """
        Determina si la resolución de fuentes requiere confirmación humana.
        """
        return bool(self.sources_config.get("resolve_requires_confirmation", True))
