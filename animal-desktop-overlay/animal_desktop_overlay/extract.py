from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from rembg import remove


@dataclass(frozen=True)
class ExtractionResult:
    input_path: Path
    output_path: Path


def extract_animal_cutout(input_path: str | Path, output_path: str | Path) -> ExtractionResult:
    """
    Extract a foreground cutout (typically the animal) as a transparent PNG.

    This is a best-effort background removal using `rembg` (U2Net). For photos with
    multiple objects, it may keep more than the animal.
    """
    in_path = Path(input_path).expanduser().resolve()
    out_path = Path(output_path).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("rb") as f:
        inp = f.read()

    out_bytes = remove(inp)
    out_path.write_bytes(out_bytes)

    # Normalize to RGBA PNG for downstream display.
    img = Image.open(out_path).convert("RGBA")
    img.save(out_path)

    return ExtractionResult(input_path=in_path, output_path=out_path)

