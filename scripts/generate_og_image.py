from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static/images/og-image.png"
WIDTH, HEIGHT = 1200, 630
FONT_DIRECTORIES = (
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts"),
)


def font(size: int, *, bold: bool = False) -> Any:
    filename = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = tuple(directory / filename for directory in FONT_DIRECTORIES)
    for candidate in candidates:
        if candidate.is_file():
            from PIL import ImageFont

            return ImageFont.truetype(str(candidate), size=size)
    raise RuntimeError(
        f"Required font {filename} was not found. Install the fonts-dejavu-core "
        "package and rerun scripts/generate_og_image.py."
    )


def draw_centered_text(
    draw: Any,
    bounds: tuple[int, int, int, int],
    text: str,
    *,
    fill: str,
    text_font: Any,
) -> None:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=text_font)
    width = right - left
    height = bottom - top
    x = bounds[0] + ((bounds[2] - bounds[0] - width) / 2) - left
    y = bounds[1] + ((bounds[3] - bounds[1] - height) / 2) - top
    draw.text((x, y), text, fill=fill, font=text_font)


def main() -> None:
    from PIL import Image, ImageDraw

    paper = "#F4F1E9"
    ink = "#111827"
    muted = "#566274"
    grid = "#DDE2E8"
    blue = "#245BDC"

    image = Image.new("RGB", (WIDTH, HEIGHT), paper)
    draw = ImageDraw.Draw(image)

    for x in range(0, WIDTH, 64):
        draw.line((x, 0, x, HEIGHT), fill=grid, width=1)
    for y in range(0, HEIGHT, 64):
        draw.line((0, y, WIDTH, y), fill=grid, width=1)

    draw.rectangle((0, 0, 18, HEIGHT), fill=blue)
    monogram_bounds = (72, 58, 140, 126)
    draw.ellipse(monogram_bounds, fill="#FFFFFF", outline=blue, width=3)
    draw_centered_text(
        draw,
        monogram_bounds,
        "AS",
        fill=blue,
        text_font=font(19, bold=True),
    )

    draw.text((72, 166), "AVISHEK SAHA", fill=blue, font=font(23, bold=True))
    draw.text((72, 216), "Applied AI &", fill=ink, font=font(74, bold=True))
    draw.text((72, 302), "ML Engineer", fill=ink, font=font(74, bold=True))
    draw.text(
        (72, 422),
        "LLM systems · evaluation · predictive ML · APIs · cloud",
        fill=muted,
        font=font(27),
    )
    draw.rectangle((72, 510, 1128, 515), fill=blue)
    draw.text((72, 548), "avisheksaha.com", fill=muted, font=font(24))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
