from pathlib import Path

from core.sources.links_generator import LinksGenerator
from core.sources.source_interpreter import SourceResolution, ResolvedItem


def test_generate_links_file(tmp_path: Path = Path("tmp_test_links")):
    tmp_path.mkdir(exist_ok=True)

    resolution = SourceResolution(
        decision="resolve",
        reason="Test resolution",
        resolved_items=[
            ResolvedItem(
                link="https://mega.nz/file/AAA",
                name="file1.rar",
            ),
            ResolvedItem(
                link="https://mega.nz/file/BBB",
                name="file2.rar",
            ),
        ],
    )

    generator = LinksGenerator(output_path=tmp_path / "links.generated.txt")
    output = generator.generate(resolution)

    assert output is not None
    assert output.exists()

    content = output.read_text().strip().splitlines()
    assert content == [
        "https://mega.nz/file/AAA",
        "https://mega.nz/file/BBB",
    ]

    print("✅ LinksGenerator test passed")


if __name__ == "__main__":
    test_generate_links_file()
