#!/usr/bin/env python3
"""Generate Binai app icons for iOS home screen and PWA manifest."""
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG_TOP = (18, 18, 42)
BG_BOT = (13, 13, 26)
PURPLE = (155, 127, 232)
PURPLE_LIGHT = (210, 190, 255)
PURPLE_DARK = (108, 78, 198)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def load_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = size * 0.08
    radius = size * 0.21

    for y in range(size):
        t = y / max(size - 1, 1)
        c = lerp(BG_TOP, BG_BOT, t)
        draw.line([(0, y), (size, y)], fill=c + (255,))

    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = int(size * 0.5), int(size * 0.42)
    glow_r = int(size * 0.36)
    for r in range(glow_r, 0, -1):
        alpha = int(75 * (r / glow_r) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PURPLE + (alpha,))
    img = Image.alpha_composite(img.convert("RGBA"), glow)

    draw = ImageDraw.Draw(img)
    x0, y0 = pad, pad
    x1, y1 = size - pad, size - pad
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=radius,
        outline=(155, 127, 232, 45),
        width=max(1, size // 256),
    )

    letter_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(letter_layer)
    font_size = int(size * 0.56)
    font = load_font(font_size)
    text = "B"
    bbox = ld.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] - size * 0.02

    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    offset = max(int(size * 0.02), 1)
    sd.text((tx + offset, ty + offset), text, font=font, fill=PURPLE_DARK + (180,))
    letter_layer = Image.alpha_composite(letter_layer, shadow)

    main = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    md = ImageDraw.Draw(main)
    md.text((tx, ty), text, font=font, fill=PURPLE_LIGHT + (255,))
    letter_layer = Image.alpha_composite(letter_layer, main)

    highlight = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hld = ImageDraw.Draw(highlight)
    hld.text((tx - 1, ty - 1), text, font=font, fill=(245, 240, 255, 90))
    letter_layer = Image.alpha_composite(letter_layer, highlight)

    img = Image.alpha_composite(img, letter_layer)
    return img.convert("RGB")


def main():
    root = Path(__file__).resolve().parent
    project = root.parent
    sizes = {
        "apple-touch-icon.png": 180,
        "icon-152.png": 152,
        "icon-167.png": 167,
        "icon-192.png": 192,
        "icon-512.png": 512,
        "favicon-32.png": 32,
    }
    for name, px in sizes.items():
        path = root / name
        draw_icon(px).save(path, "PNG", optimize=True)
        print(f"wrote {path} ({px}x{px})")
        shutil.copy(path, project / name)
        www = project / "www" / name
        if www.parent.exists():
            shutil.copy(path, www)
        www_icons = project / "www" / "icons" / name
        if www_icons.parent.exists():
            shutil.copy(path, www_icons)


if __name__ == "__main__":
    main()