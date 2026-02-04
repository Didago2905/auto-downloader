from core.sources.mega_source_interpreter import MegaSourceInterpreter
from core.sources.source_preview import (
    SourcePreview,
    SourceSummary,
    FilePreview,
)


def make_mega_preview():
    return SourcePreview(
        source_type="MEGA (carpeta)",
        origin="https://mega.nz/folder/example",
        summary=SourceSummary(
            total_files=3,
            total_size_human="2.1 GB",
        ),
        files=[
            FilePreview(
                name="TBVT40104720.Hackstore.Net.rar",
                extension=".rar",
                size_human="700 MB",
            ),
            FilePreview(
                name="TBVT40508720.Hackstore.Net.rar",
                extension=".rar",
                size_human="710 MB",
            ),
            FilePreview(
                name="TBVT40912720.Hackstore.Net.rar",
                extension=".rar",
                size_human="690 MB",
            ),
        ],
        patterns=None,
        warnings=[],
        resolvable=True,
    )


def test_mega_interpreter_auto_resolution():
    config = {"sources": {"resolve_requires_confirmation": False}}

    interpreter = MegaSourceInterpreter(config)
    preview = make_mega_preview()

    resolution = interpreter.interpret(preview)

    assert resolution.decision == "resolve"
    assert len(resolution.resolved_items) == 3

    for item in resolution.resolved_items:
        assert item.link.startswith("mega://download/")
        assert item.name.endswith(".rar")


def test_mega_interpreter_requires_confirmation():
    config = {"sources": {"resolve_requires_confirmation": True}}

    interpreter = MegaSourceInterpreter(config)
    preview = make_mega_preview()

    resolution = interpreter.interpret(preview)

    assert resolution.decision == "skip"
    assert resolution.resolved_items == []


if __name__ == "__main__":
    test_mega_interpreter_auto_resolution()
    test_mega_interpreter_requires_confirmation()
    print("✅ MegaSourceInterpreter tests passed")
