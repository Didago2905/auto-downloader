from core.sources.mega_source import MegaSource
from core.sources.source_preview import SourcePreviewRenderer
from core.sources.mega_source_interpreter import MegaSourceInterpreter
from core.sources.links_generator import LinksGenerator


def test_full_mega_flow():
    # 1. Metadata real (simulada)
    files_metadata = [
        {"name": "TBVT40104720.Hackstore.Net.rar", "size_bytes": 733_800_000},
        {"name": "TBVT40508720.Hackstore.Net.rar", "size_bytes": 711_200_000},
        {"name": "TBVT40912720.Hackstore.Net.rar", "size_bytes": 712_700_000},
    ]

    folder_url = "https://mega.nz/folder/REAL_FOLDER_ID"

    # 2. Construir fuente
    source = MegaSource(
        folder_url=folder_url,
        files_metadata=files_metadata,
    )

    preview = source.build_preview()

    # 3. Mostrar preview (decisión humana)
    SourcePreviewRenderer.render(preview)

    # 4. Interpretar fuente
    config = {
        "sources": {"resolve_requires_confirmation": False}  # para la prueba automática
    }

    interpreter = MegaSourceInterpreter(config)
    resolution = interpreter.interpret(preview)

    print("\n📌 DECISIÓN FINAL:")
    print(f"Decision: {resolution.decision}")
    print(f"Reason  : {resolution.reason}")
    print(f"Items   : {len(resolution.resolved_items)}")

    # 5. Generar links.generated.txt
    generator = LinksGenerator()
    output = generator.generate(resolution)

    if output:
        print(f"\n✅ Archivo generado: {output}")
    else:
        print("\n⏭️ No se generó archivo de links")


if __name__ == "__main__":
    test_full_mega_flow()
