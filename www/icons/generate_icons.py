#!/usr/bin/env python3
"""Generate Binai app icons for iOS home screen and PWA manifest."""
from PIL import Image, ImageDraw

BG_TOP = (18, 18, 42)
BG_BOT = (13, 13, 26)
PURPLE = (155, 127, 232)
PURPLE_LIGHT = (196, 176, 255)
PURPLE_DARK = (123, 95, 212)
HEART = (232, 75, 154)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = size * 0.08
    radius = size * 0.21

    for y in range(size):
        t = y / max(size - 1, 1)
        c = lerp(BG_TOP, BG_BOT, t)
        draw.line([(0, y), (size, y)], fill=c + (255,))

    glow_r = int(size * 0.42)
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = int(size * 0.5), int(size * 0.36)
    for r in range(glow_r, 0, -1):
        alpha = int(70 * (r / glow_r) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PURPLE + (alpha,))
    img = Image.alpha_composite(img.convert("RGBA"), glow)

    draw = ImageDraw.Draw(img)
    x0, y0 = pad, pad
    x1, y1 = size - pad, size - pad
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=(155, 127, 232, 40), width=max(1, size // 256))

    s = size / 512.0
    bx, by = int(168 * s), int(136 * s)
    bw, bh = int(176 * s), int(240 * s)
    thick = max(int(44 * s), 2)

    def bar(rect, fill):
        draw.rounded_rectangle(rect, radius=max(int(10 * s), 1), fill=fill)

    # Stylized B: vertical spine + two bowls
    bar((bx, by, bx + thick, by + bh), PURPLE_LIGHT)
    mid_y = by + int(bh * 0.46)
    bowl_h = mid_y - by - int(8 * s)
    bar((bx + thick - int(6 * s), by + int(6 * s), bx + bw, by + bowl_h), PURPLE)
    bar((bx + thick - int(6 * s), mid_y + int(8 * s), bx + bw, by + bh - int(6 * s)), PURPLE_DARK)

    # Heart accent (Binai 💜)
    hx, hy = int(392 * s), int(372 * s)
    hr = max(int(18 * s), 2)
    draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=HEART + (245,))
    gr = int(hr * 1.5)
    draw.ellipse([hx - gr, hy - gr, hx + gr, hy + gr], fill=PURPLE + (55,))

    return img.convert("RGB")


def main():
    root = __file__.rsplit("/", 1)[0]
    sizes = {
        "apple-touch-icon.png": 180,
        "icon-152.png": 152,
        "icon-167.png": 167,
        "icon-192.png": 192,
        "icon-512.png": 512,
        "favicon-32.png": 32,
    }
    for name, px in sizes.items():
        path = f"{root}/{name}"
        draw_icon(px).save(path, "PNG", optimize=True)
        print(f"wrote {path} ({px}x{px})")

    # Root copies for Flask static serving
    import shutil
    for name in ("apple-touch-icon.png", "icon-192.png", "icon-512.png", "favicon-32.png"):
        shutil.copy(f"{root}/{name}", f"{root}/../{name}")


if __name__ == "__main__":
    main()