"""Logo tròn từ assets/logo-bird.png."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
LOGO_SRC = ROOT / "assets" / "logo-bird.png"


def _bird_rgba(src: Image.Image) -> Image.Image:
    src = src.convert("RGBA")
    px = src.load()
    w, h = src.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > 235 and g > 235 and b > 235:
                px[x, y] = (0, 0, 0, 0)
    return src


def render_circular(size: int, *, bg: str = "#0a0a0a") -> Image.Image:
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse((0, 0, size - 1, size - 1), fill=bg)
    if not LOGO_SRC.is_file():
        return out
    pad = max(3, size // 18)
    inner = size - 2 * pad
    bird = _bird_rgba(Image.open(LOGO_SRC)).resize((inner, inner), Image.Resampling.LANCZOS)
    out.paste(bird, (pad, pad), bird)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out.putalpha(mask)
    return out