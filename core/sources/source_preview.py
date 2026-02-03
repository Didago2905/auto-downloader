from dataclasses import dataclass, field
from typing import List, Optional


# ==========================
# MODELOS
# ==========================


@dataclass(frozen=True)
class FilePreview:
    name: str
    extension: str
    size_bytes: Optional[int] = None
    size_human: Optional[str] = None


@dataclass(frozen=True)
class PatternInfo:
    common_prefix: Optional[str] = None
    common_suffix: Optional[str] = None
    numbering_detected: bool = False
    numbering_style: Optional[str] = None  # incremental | season_episode
    compressed_format: bool = False
    possible_episode_pack: bool = False


@dataclass(frozen=True)
class SourceSummary:
    total_files: int
    total_size_bytes: Optional[int] = None
    total_size_human: Optional[str] = None


@dataclass(frozen=True)
class SourcePreview:
    source_type: str
    origin: str
    summary: SourceSummary
    files: List[FilePreview] = field(default_factory=list)
    patterns: Optional[PatternInfo] = None
    warnings: List[str] = field(default_factory=list)
    resolvable: bool = True


# ==========================
# RENDERER
# ==========================


class SourcePreviewRenderer:
    MAX_FILES_PREVIEW = 5

    @staticmethod
    def render(preview: SourcePreview) -> None:
        print("=" * 50)
        print("📦 FUENTE DETECTADA")
        print("=" * 50)

        SourcePreviewRenderer._render_header(preview)
        SourcePreviewRenderer._render_summary(preview.summary)
        SourcePreviewRenderer._render_files(preview.files)
        SourcePreviewRenderer._render_patterns(preview.patterns)
        SourcePreviewRenderer._render_warnings(preview.warnings)
        SourcePreviewRenderer._render_resolvable(preview)

    # ----------------------

    @staticmethod
    def _render_header(preview: SourcePreview):
        print(f"📦 Tipo de fuente : {preview.source_type}")
        print(f"🔗 Origen        : {preview.origin}")

    # ----------------------

    @staticmethod
    def _render_summary(summary: SourceSummary):
        print("\n" + "-" * 50)
        print("📊 RESUMEN")
        print("-" * 50)
        print(f"📁 Archivos encontrados : {summary.total_files}")

        size = summary.total_size_human or "Desconocido"
        print(f"📐 Tamaño total         : {size}")

    # ----------------------

    @staticmethod
    def _render_files(files: List[FilePreview]):
        if not files:
            return

        print("\n" + "-" * 50)
        print("📄 ARCHIVOS (preview)")
        print("-" * 50)

        for file in files[: SourcePreviewRenderer.MAX_FILES_PREVIEW]:
            size = file.size_human or "?"
            print(f"• {file.name:<40} ({size})")

        remaining = len(files) - SourcePreviewRenderer.MAX_FILES_PREVIEW
        if remaining > 0:
            print(f"… y {remaining} archivo(s) más")

    # ----------------------

    @staticmethod
    def _render_patterns(patterns: Optional[PatternInfo]):
        if not patterns:
            return

        print("\n" + "-" * 50)
        print("🧠 PATRONES DETECTADOS")
        print("-" * 50)

        if patterns.common_prefix:
            print(f"✔ Prefijo común        : {patterns.common_prefix}")

        if patterns.common_suffix:
            print(f"✔ Sufijo común         : {patterns.common_suffix}")

        if patterns.numbering_detected:
            style = patterns.numbering_style or "desconocido"
            print(f"✔ Numeración detectada : {style}")

        if patterns.compressed_format:
            print("✔ Archivos comprimidos: sí")

        if patterns.possible_episode_pack:
            print("✔ Posible pack episodios")

    # ----------------------

    @staticmethod
    def _render_warnings(warnings: List[str]):
        if not warnings:
            return

        print("\n" + "-" * 50)
        print("⚠️ ADVERTENCIAS")
        print("-" * 50)

        for w in warnings:
            print(f"• {w}")

    # ----------------------

    @staticmethod
    def _render_resolvable(preview: SourcePreview):
        print("\n" + "-" * 50)
        print("🔓 ESTADO")
        print("-" * 50)

        if preview.resolvable:
            print("Resoluble automáticamente: SÍ")
        else:
            print("Resoluble automáticamente: NO")
