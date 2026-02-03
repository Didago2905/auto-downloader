from core.sources.source_preview import (
    SourcePreview,
    SourceSummary,
    FilePreview,
    PatternInfo,
    SourcePreviewRenderer,
)


def test_mega_folder_preview():
    preview = SourcePreview(
        source_type="MEGA (carpeta)",
        origin="https://mega.nz/folder/bkAiTDbQ#example",
        summary=SourceSummary(
            total_files=6,
            total_size_bytes=4665000000,
            total_size_human="4.35 GB",
        ),
        files=[
            FilePreview(
                name="TBVT40104720.Hackstore.Net.rar",
                extension=".rar",
                size_human="733.8 MB",
            ),
            FilePreview(
                name="TBVT40508720.Hackstore.Net.rar",
                extension=".rar",
                size_human="711.2 MB",
            ),
            FilePreview(
                name="TBVT40912720.Hackstore.Net.rar",
                extension=".rar",
                size_human="712.7 MB",
            ),
            FilePreview(
                name="TBVT41316720.Hackstore.Net.rar",
                extension=".rar",
                size_human="702.6 MB",
            ),
            FilePreview(
                name="TBVT41720720.Hackstore.Net.rar",
                extension=".rar",
                size_human="753.2 MB",
            ),
            FilePreview(
                name="TBVT42124720.Hackstore.Net.rar",
                extension=".rar",
                size_human="724.1 MB",
            ),
        ],
        patterns=PatternInfo(
            common_prefix="TBVT",
            common_suffix="Hackstore.Net",
            numbering_detected=True,
            numbering_style="incremental",
            compressed_format=True,
            possible_episode_pack=True,
        ),
        warnings=[
            "No se puede inspeccionar el contenido interno sin descargar",
            "Fuente grande (> 4 GB)",
        ],
        resolvable=True,
    )

    SourcePreviewRenderer.render(preview)


if __name__ == "__main__":
    test_mega_folder_preview()