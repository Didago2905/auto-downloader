from core.sources.mega_source import MegaSource
from core.sources.source_preview import SourcePreviewRenderer


def test_mega_folder_source():
    # Simulación de metadata obtenida de una carpeta MEGA
    files_metadata = [
        {
            "name": "TBVT40104720.Hackstore.Net.rar",
            "size_bytes": 733_800_000,
        },
        {
            "name": "TBVT40508720.Hackstore.Net.rar",
            "size_bytes": 711_200_000,
        },
        {
            "name": "TBVT40912720.Hackstore.Net.rar",
            "size_bytes": 712_700_000,
        },
        {
            "name": "TBVT41316720.Hackstore.Net.rar",
            "size_bytes": 702_600_000,
        },
        {
            "name": "TBVT41720720.Hackstore.Net.rar",
            "size_bytes": 753_200_000,
        },
        {
            "name": "TBVT42124720.Hackstore.Net.rar",
            "size_bytes": 724_100_000,
        },
    ]

    source = MegaSource(
        folder_url="https://mega.nz/folder/bkAiTDbQ#example",
        files_metadata=files_metadata,
    )

    preview = source.build_preview()

    SourcePreviewRenderer.render(preview)


if __name__ == "__main__":
    test_mega_folder_source()
