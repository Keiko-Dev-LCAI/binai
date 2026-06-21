#!/usr/bin/env python3
"""Generate Binai app icons for iOS home screen and PWA manifest."""
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

BG_TOP = (18, 18, 42)
BG_BOT = (13, 13, 26)
PURPLE = (155, 127, 232)
PURPLE_LIGHT = (210, 190, 255)
PURPLE_DARK = (108, 78, 198)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def heart_points(cx, cy, scale):
    pts = []
    for deg in range(0, 360, 2):
        t = math.radians(deg)
        x = 16 * math.sin(t) ** 3
        y = -(
            13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t)
        )
        pts.append((cx + x * scale / 16, cy + y * scale / 16))
    return pts


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
    cx, cy = int(size * 0.5), int(size * 0.48)
    glow_r = int(size * 0.38)
    for r in range(glow_r, 0, -1):
        alpha = int(85 * (r / glow_r) ** 2)
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

    heart_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(heart_layer)
    heart_scale = size * 0.34
    heart_cx, heart_cy = size * 0.5, size * 0.52
    pts = heart_points(heart_cx, heart_cy, heart_scale)
    hd.polygon(pts, fill=PURPLE_DARK + (255,))

    shade = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    shade_pts = heart_points(heart_cx, heart_cy + heart_scale * 0.08, heart_scale * 0.92)
    sd.polygon(shade_pts, fill=PURPLE + (220,))
    heart_layer = Image.alpha_composite(heart_layer, shade)

    highlight = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hld = ImageDraw.Draw(highlight)
    hl_pts = heart_points(
        heart_cx - heart_scale * 0.1,
        heart_cy - heart_scale * 0.16,
        heart_scale * 0.42,
    )
    hld.polygon(hl_pts, fill=PURPLE_LIGHT + (110,))
    heart_layer = Image.alpha_composite(heart_layer, highlight)

    img = Image.alpha_composite(img, heart_layer)
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