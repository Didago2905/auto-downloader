from typing import List, Dict, Optional
import re

from core.sources.source_preview import (
    SourcePreview,
    SourceSummary,
    FilePreview,
    PatternInfo,
)


class MegaSource:
    """
    Fuente MEGA (carpeta).
    Este módulo SOLO construye un SourcePreview.
    No descarga ni resuelve enlaces.
    """

    def __init__(self, folder_url: str, files_metadata: List[Dict]):
        """
        files_metadata: lista de dicts con claves esperadas:
        - name: str
        - size_bytes: int | None
        """
        self.folder_url = folder_url
        self.files_metadata = files_metadata

    # ==========================
    # API PÚBLICA
    # ==========================

    def build_preview(self) -> SourcePreview:
        files = self._build_file_previews()
        summary = self._build_summary(files)
        patterns = self._detect_patterns(files)
        warnings = self._build_warnings(summary, patterns)

        return SourcePreview(
            source_type="MEGA (carpeta)",
            origin=self.folder_url,
            summary=summary,
            files=files,
            patterns=patterns,
            warnings=warnings,
            resolvable=True,
        )

    # ==========================
    # HELPERS
    # ==========================

    def _build_file_previews(self) -> List[FilePreview]:
        previews = []

        for f in self.files_metadata:
            name = f.get("name")
            size_bytes = f.get("size_bytes")

            previews.append(
                FilePreview(
                    name=name,
                    extension=self._get_extension(name),
                    size_bytes=size_bytes,
                    size_human=self._human_size(size_bytes),
                )
            )

        return previews

    def _build_summary(self, files: List[FilePreview]) -> SourceSummary:
        total_files = len(files)
        sizes = [f.size_bytes for f in files if f.size_bytes is not None]

        total_size_bytes = sum(sizes) if sizes else None
        total_size_human = (
            self._human_size(total_size_bytes) if total_size_bytes else None
        )

        return SourceSummary(
            total_files=total_files,
            total_size_bytes=total_size_bytes,
            total_size_human=total_size_human,
        )

    def _detect_patterns(self, files: List[FilePreview]) -> Optional[PatternInfo]:
        names = [f.name for f in files]

        if not names:
            return None

        prefix = self._common_prefix(names)
        suffix = self._common_suffix(names)

        numbering_style = self._detect_numbering_style(names)
        numbering_detected = numbering_style is not None

        compressed = all(f.extension == ".rar" for f in files)

        possible_pack = numbering_detected and len(files) >= 3

        return PatternInfo(
            common_prefix=prefix,
            common_suffix=suffix,
            numbering_detected=numbering_detected,
            numbering_style=numbering_style,
            compressed_format=compressed,
            possible_episode_pack=possible_pack,
        )

    def _build_warnings(
        self,
        summary: SourceSummary,
        patterns: Optional[PatternInfo],
    ) -> List[str]:
        warnings = []

        if patterns and patterns.compressed_format:
            warnings.append(
                "No se puede inspeccionar el contenido interno sin descargar"
            )

        if summary.total_size_bytes and summary.total_size_bytes > 4 * 1024**3:
            warnings.append("Fuente grande (> 4 GB)")

        return warnings

    # ==========================
    # UTILIDADES
    # ==========================

    @staticmethod
    def _get_extension(name: str) -> str:
        if "." not in name:
            return ""
        return "." + name.split(".")[-1].lower()

    @staticmethod
    def _human_size(size: Optional[int]) -> Optional[str]:
        if size is None:
            return None

        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return "?"

    @staticmethod
    def _common_prefix(names: List[str]) -> Optional[str]:
        if not names:
            return None

        prefix = names[0]
        for name in names[1:]:
            while not name.startswith(prefix) and prefix:
                prefix = prefix[:-1]

        return prefix if len(prefix) >= 3 else None

    @staticmethod
    def _common_suffix(names: List[str]) -> Optional[str]:
        reversed_names = [name[::-1] for name in names]
        suffix = MegaSource._common_prefix(reversed_names)

        if not suffix:
            return None

        suffix = suffix[::-1]
        return suffix if len(suffix) >= 3 else None

    @staticmethod
    def _detect_numbering_style(names: List[str]) -> Optional[str]:
        # Detecta patrones tipo 01, 02, 03 o 1.1, 1.2, etc.
        numeric = 0
        dot_numeric = 0

        for name in names:
            if re.search(r"\b\d{1,3}\b", name):
                numeric += 1
            if re.search(r"\b\d+\.\d+\b", name):
                dot_numeric += 1

        if dot_numeric == len(names):
            return "incremental"

        if numeric == len(names):
            return "numeric"

        return None
