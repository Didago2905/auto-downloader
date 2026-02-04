from core.sources.source_interpreter import SourceInterpreter
from core.sources.source_preview import (
    SourcePreview,
    SourceSummary,
)


def make_basic_preview(resolvable=True):
    return SourcePreview(
        source_type="TEST_SOURCE",
        origin="test://source",
        summary=SourceSummary(
            total_files=3,
            total_size_human="1.2 GB",
        ),
        files=[],
        patterns=None,
        warnings=[],
        resolvable=resolvable,
    )


def test_requires_confirmation_by_default():
    config = {
        "sources": {
            "resolve_requires_confirmation": True
        }
    }

    interpreter = SourceInterpreter(config)
    preview = make_basic_preview(resolvable=True)

    resolution = interpreter.interpret(preview)

    assert resolution.decision == "skip"
    assert resolution.requires_confirmation is True
    assert "confirmation" in resolution.reason.lower()


def test_automatic_resolution_allowed():
    config = {
        "sources": {
            "resolve_requires_confirmation": False
        }
    }

    interpreter = SourceInterpreter(config)
    preview = make_basic_preview(resolvable=True)

    resolution = interpreter.interpret(preview)

    assert resolution.decision == "resolve"
    assert resolution.requires_confirmation is False
    assert "automatic" in resolution.reason.lower()


def test_blocked_source():
    config = {
        "sources": {
            "resolve_requires_confirmation": False
        }
    }

    interpreter = SourceInterpreter(config)
    preview = make_basic_preview(resolvable=False)

    resolution = interpreter.interpret(preview)

    assert resolution.decision == "blocked"
    assert resolution.requires_confirmation is False
    assert "not resolvable" in resolution.reason.lower()


if __name__ == "__main__":
    test_requires_confirmation_by_default()
    test_automatic_resolution_allowed()
    test_blocked_source()
    print("✅ SourceInterpreter tests passed")
