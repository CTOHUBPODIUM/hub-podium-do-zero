from math import sin, pi
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERO_WIDTH = 1800
HERO_HEIGHT = 1200
OG_WIDTH = 1200
OG_HEIGHT = 630
MARK_SIZE = 512
BG_TOP = (3, 5, 9)
BG_BOTTOM = (11, 15, 24)
GOLD = (214, 175, 55)
GOLD_SOFT = (161, 118, 28)
WHITE = (245, 247, 250)


def load_font(size, bold=False):
    candidates = []
    if bold:
        candidates.extend(
            [
                "C:/Windows/Fonts/arialbd.ttf",
                "C:/Windows/Fonts/calibrib.ttf",
                "C:/Windows/Fonts/segoeuib.ttf",
            ]
        )
    candidates.extend(
        [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
    )

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def vertical_gradient(width, height):
    image = Image.new("RGB", (width, height), BG_TOP)
    pixels = image.load()
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(
            int(BG_TOP[index] + (BG_BOTTOM[index] - BG_TOP[index]) * ratio)
            for index in range(3)
        )
        for x in range(width):
            pixels[x, y] = color
    return image.convert("RGBA")


def draw_network(draw):
    random.seed(11)
    points = []
    for _ in range(82):
        x = random.randint(-120, 760)
        y = random.randint(-80, 520)
        points.append((x, y))

    for index, point in enumerate(points):
        distances = sorted(
            (
                (other, (point[0] - other[0]) ** 2 + (point[1] - other[1]) ** 2)
                for other in points
                if other != point
            ),
            key=lambda item: item[1],
        )
        for other, distance in distances[:4]:
            if distance < 120000:
                alpha = 64 if index % 2 == 0 else 42
                draw.line([point, other], fill=(*GOLD, alpha), width=2)

    for point in points:
        radius = random.randint(3, 6)
        draw.ellipse(
            [point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius],
            fill=(*GOLD, 228),
        )


def draw_wave(draw):
    base_y = HERO_HEIGHT - 170
    for layer in range(12):
        amplitude = 22 + layer * 5
        offset_y = base_y + layer * 12
        phase = layer * 0.28
        color = (
            max(90, GOLD_SOFT[0] - layer * 5),
            max(58, GOLD_SOFT[1] - layer * 4),
            max(24, GOLD_SOFT[2] - layer * 2),
            108,
        )
        points = []
        for x in range(-60, HERO_WIDTH + 60, 12):
            y = offset_y + sin((x / HERO_WIDTH) * pi * 2.1 + phase) * amplitude
            points.append((x, y))
        draw.line(points, fill=color, width=3)
        for x, y in points[::3]:
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(*GOLD, 88))


def shield_outline_points(width, height, scale=1.0):
    center_x = width * 0.84
    top_y = height * 0.16
    shield_w = 260 * scale
    shield_h = 310 * scale
    left = center_x - shield_w / 2
    top = top_y
    return [
        (left + shield_w * 0.18, top),
        (left + shield_w * 0.82, top),
        (left + shield_w * 0.94, top + shield_h * 0.14),
        (left + shield_w * 0.92, top + shield_h * 0.62),
        (left + shield_w * 0.50, top + shield_h * 0.98),
        (left + shield_w * 0.08, top + shield_h * 0.62),
        (left + shield_w * 0.06, top + shield_h * 0.14),
    ]


def draw_shield(draw, width, height, scale=1.0, alpha=255):
    points = shield_outline_points(width, height, scale=scale)
    draw.polygon(points, outline=(*GOLD, alpha), width=max(4, int(10 * scale)))

    px = [point[0] for point in points]
    py = [point[1] for point in points]
    left = min(px)
    top = min(py)
    shield_w = max(px) - left
    shield_h = max(py) - top

    draw.line(
        [
            (left + shield_w * 0.24, top + shield_h * 0.64),
            (left + shield_w * 0.82, top + shield_h * 0.34),
        ],
        fill=(*GOLD, alpha),
        width=max(4, int(12 * scale)),
    )

    bar_width = shield_w * 0.08
    bars = [
        (left + shield_w * 0.26, top + shield_h * 0.52, left + shield_w * 0.26 + bar_width, top + shield_h * 0.72),
        (left + shield_w * 0.42, top + shield_h * 0.41, left + shield_w * 0.42 + bar_width, top + shield_h * 0.72),
        (left + shield_w * 0.58, top + shield_h * 0.31, left + shield_w * 0.58 + bar_width, top + shield_h * 0.72),
        (left + shield_w * 0.74, top + shield_h * 0.18, left + shield_w * 0.74 + bar_width, top + shield_h * 0.72),
    ]
    for rect in bars:
        draw.rounded_rectangle(rect, radius=max(4, int(8 * scale)), fill=(*GOLD, max(180, alpha - 10)))

    circuit_points = [
        (left + shield_w * 0.78, top + shield_h * 0.10),
        (left + shield_w * 0.92, top + shield_h * 0.04),
        (left + shield_w * 1.03, top + shield_h * 0.12),
        (left + shield_w * 1.12, top + shield_h * 0.05),
    ]
    draw.line(circuit_points, fill=(*GOLD, max(150, alpha - 20)), width=max(3, int(5 * scale)))
    for x, y in circuit_points:
        r = max(3, int(6 * scale))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*GOLD, alpha))


def draw_mark_shape(draw, size, padding=72, alpha=255):
    shield_w = size - padding * 2
    shield_h = shield_w * 1.16
    left = padding
    top = (size - shield_h) / 2

    outline = [
        (left + shield_w * 0.18, top),
        (left + shield_w * 0.82, top),
        (left + shield_w * 0.94, top + shield_h * 0.14),
        (left + shield_w * 0.92, top + shield_h * 0.62),
        (left + shield_w * 0.50, top + shield_h * 0.98),
        (left + shield_w * 0.08, top + shield_h * 0.62),
        (left + shield_w * 0.06, top + shield_h * 0.14),
    ]
    draw.polygon(outline, outline=(*GOLD, alpha), width=10)

    draw.line(
        [
            (left + shield_w * 0.24, top + shield_h * 0.64),
            (left + shield_w * 0.82, top + shield_h * 0.34),
        ],
        fill=(*GOLD, alpha),
        width=12,
    )

    bar_width = shield_w * 0.08
    bars = [
        (left + shield_w * 0.26, top + shield_h * 0.52, left + shield_w * 0.26 + bar_width, top + shield_h * 0.72),
        (left + shield_w * 0.42, top + shield_h * 0.41, left + shield_w * 0.42 + bar_width, top + shield_h * 0.72),
        (left + shield_w * 0.58, top + shield_h * 0.31, left + shield_w * 0.58 + bar_width, top + shield_h * 0.72),
        (left + shield_w * 0.74, top + shield_h * 0.18, left + shield_w * 0.74 + bar_width, top + shield_h * 0.72),
    ]
    for rect in bars:
        draw.rounded_rectangle(rect, radius=8, fill=(*GOLD, max(210, alpha - 10)))

    circuit_points = [
        (left + shield_w * 0.78, top + shield_h * 0.10),
        (left + shield_w * 0.92, top + shield_h * 0.04),
        (left + shield_w * 1.03, top + shield_h * 0.12),
        (left + shield_w * 1.12, top + shield_h * 0.05),
    ]
    draw.line(circuit_points, fill=(*GOLD, max(180, alpha - 20)), width=5)
    for x, y in circuit_points:
        draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(*GOLD, alpha))


def add_glows(canvas):
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow, "RGBA")
    draw.ellipse(
        [HERO_WIDTH - 620, 80, HERO_WIDTH - 40, 660],
        fill=(214, 175, 55, 34),
    )
    draw.ellipse(
        [-120, HERO_HEIGHT - 260, 900, HERO_HEIGHT + 340],
        fill=(214, 175, 55, 18),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(52))
    return Image.alpha_composite(canvas, glow)


def add_mark_glow(canvas):
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow, "RGBA")
    draw.ellipse([60, 60, MARK_SIZE - 60, MARK_SIZE - 60], fill=(214, 175, 55, 28))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(canvas, glow)


def render_hero(output_dir):
    canvas = vertical_gradient(HERO_WIDTH, HERO_HEIGHT)
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw_network(draw)
    draw_wave(draw)
    draw_shield(draw, HERO_WIDTH, HERO_HEIGHT, scale=1.65, alpha=64)

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay, "RGBA")
    overlay_draw.rectangle(
        [0, 0, HERO_WIDTH, HERO_HEIGHT],
        fill=(0, 0, 0, 18),
    )
    canvas = Image.alpha_composite(canvas, overlay)
    canvas = add_glows(canvas)

    brand_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    brand_draw = ImageDraw.Draw(brand_layer, "RGBA")
    label_font = load_font(24, bold=True)
    brand_draw.text((126, 126), "HUB-PODIUM", font=label_font, fill=(*GOLD, 188))
    canvas = Image.alpha_composite(canvas, brand_layer)

    hero_path = output_dir / "hub-podium-site-hero-v2.png"
    canvas.convert("RGB").save(hero_path, format="PNG", optimize=True)
    return hero_path


def render_mark(output_dir):
    canvas = Image.new("RGBA", (MARK_SIZE, MARK_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_mark_shape(draw, MARK_SIZE, padding=88, alpha=255)

    mark_path = output_dir / "hub-podium-mark-v2.png"
    canvas.save(mark_path, format="PNG", optimize=True)
    return mark_path


def render_icon(output_dir, size):
    canvas = Image.new("RGBA", (size, size), BG_TOP + (255,))
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow, "RGBA")
    glow_draw.ellipse(
        [size * 0.12, size * 0.12, size * 0.88, size * 0.88],
        fill=(214, 175, 55, 18),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(max(8, size // 18)))
    canvas = Image.alpha_composite(canvas, glow)

    draw = ImageDraw.Draw(canvas, "RGBA")
    padding = max(32, int(size * 0.17))
    draw_mark_shape(draw, size, padding=padding, alpha=255)

    icon_path = output_dir / f"hub-podium-icon-{size}.png"
    canvas.save(icon_path, format="PNG", optimize=True)
    return icon_path


def render_og_card(output_dir):
    canvas = vertical_gradient(OG_WIDTH, OG_HEIGHT)
    draw = ImageDraw.Draw(canvas, "RGBA")

    random.seed(13)
    points = []
    for _ in range(56):
        x = random.randint(-60, 420)
        y = random.randint(-40, 230)
        points.append((x, y))

    for point in points:
        distances = sorted(
            (
                (other, (point[0] - other[0]) ** 2 + (point[1] - other[1]) ** 2)
                for other in points
                if other != point
            ),
            key=lambda item: item[1],
        )
        for other, distance in distances[:4]:
            if distance < 50000:
                draw.line([point, other], fill=(*GOLD, 58), width=2)
        radius = random.randint(3, 5)
        draw.ellipse([point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius], fill=(*GOLD, 220))

    base_y = OG_HEIGHT - 78
    for layer in range(8):
        amplitude = 12 + layer * 3
        offset_y = base_y + layer * 9
        phase = layer * 0.35
        color = (
            max(92, GOLD_SOFT[0] - layer * 4),
            max(60, GOLD_SOFT[1] - layer * 4),
            max(24, GOLD_SOFT[2] - layer * 2),
            112,
        )
        points = []
        for x in range(-24, OG_WIDTH + 24, 10):
            y = offset_y + sin((x / OG_WIDTH) * pi * 2.1 + phase) * amplitude
            points.append((x, y))
        draw.line(points, fill=color, width=2)

    shield_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shield_draw = ImageDraw.Draw(shield_layer, "RGBA")
    draw_shield(shield_draw, OG_WIDTH, OG_HEIGHT, scale=1.0, alpha=236)
    shield_layer = shield_layer.filter(ImageFilter.GaussianBlur(0.3))
    canvas = Image.alpha_composite(canvas, shield_layer)

    text = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text, "RGBA")
    label_font = load_font(24, bold=True)
    title_font = load_font(62, bold=True)
    body_font = load_font(24)
    text_draw.text((78, 74), "HUB-PODIUM", font=label_font, fill=(*GOLD, 220))
    text_draw.text((78, 140), "Onde talento vira performance", font=title_font, fill=(*WHITE, 255))
    text_draw.text((78, 230), "Futebol, dados, scouting e alta performance.", font=body_font, fill=(228, 231, 236, 228))
    text_draw.text((78, 268), "Site institucional pré-produto", font=body_font, fill=(228, 231, 236, 166))
    canvas = Image.alpha_composite(canvas, text)

    og_path = output_dir / "hub-podium-og-1200x630.png"
    canvas.convert("RGB").save(og_path, format="PNG", optimize=True)
    return og_path


def main():
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "landing-page" / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)

    hero_path = render_hero(output_dir)
    mark_path = render_mark(output_dir)
    icon_192 = render_icon(output_dir, 192)
    icon_512 = render_icon(output_dir, 512)
    og_path = render_og_card(output_dir)

    print(hero_path)
    print(mark_path)
    print(icon_192)
    print(icon_512)
    print(og_path)


if __name__ == "__main__":
    main()
