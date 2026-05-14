from pathlib import Path
from tempfile import gettempdir

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from services.card_tiers import get_card_tier
from services.face_recognition import detect_largest_face_box

OUTPUT = Path(gettempdir()) / "hub_podium_card.png"


def load_font(size, bold=False):
    candidates = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            continue
    return ImageFont.load_default()


def get_photo_path(data):
    photo = data.get("athlete_photo") or {}
    path = photo.get("stored_path") or data.get("athlete_photo_path")
    if not path:
        return None

    photo_path = Path(path)
    return photo_path if photo_path.exists() else None


def fit_text(draw, text, max_width, start_size, bold=True):
    size = start_size
    while size >= 18:
        font = load_font(size, bold=bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 3
    return load_font(18, bold=bold)


def center_text(draw, box, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = box[0] + ((box[2] - box[0] - text_width) / 2)
    y = box[1] + ((box[3] - box[1] - text_height) / 2) - 2
    draw.text((x, y), text, fill=fill, font=font)


def wrap_text_to_width(draw, text, font, max_width, max_lines=2):
    words = str(text or "").split()
    if not words:
        return [""]

    lines = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
            continue
        lines.append(current)
        current = word
        if len(lines) == max_lines - 1:
            break

    remaining_words = words[len(" ".join(lines + [current]).split()):]
    if remaining_words and len(lines) == max_lines - 1:
        current = f"{current} {' '.join(remaining_words)}".strip()
    lines.append(current)
    return lines[:max_lines]


def fit_multiline_text(draw, text, max_width, start_size, max_lines=2, bold=True):
    size = start_size
    while size >= 18:
        font = load_font(size, bold=bold)
        lines = wrap_text_to_width(draw, text, font, max_width, max_lines=max_lines)
        longest = max(
            (draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]) for line in lines
        )
        if longest <= max_width and len(lines) <= max_lines:
            return font, lines
        size -= 2
    fallback = load_font(18, bold=bold)
    return fallback, wrap_text_to_width(draw, text, fallback, max_width, max_lines=max_lines)


def center_multiline_text(draw, box, lines, font, fill, line_gap=4):
    line_heights = []
    line_widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])

    total_height = sum(line_heights) + max(0, len(lines) - 1) * line_gap
    y = box[1] + ((box[3] - box[1] - total_height) / 2) - 2
    for index, line in enumerate(lines):
        x = box[0] + ((box[2] - box[0] - line_widths[index]) / 2)
        draw.text((x, y), line, fill=fill, font=font)
        y += line_heights[index] + line_gap


def draw_pill(draw, box, text, fill, outline, text_fill, font_size=20):
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=2)
    center_text(draw, box, text, load_font(font_size, bold=True), text_fill)


def draw_stat_block(draw, x, y, label, value, accent, fill):
    draw.rounded_rectangle((x, y, x + 182, y + 82), radius=14, fill=fill, outline=accent, width=3)
    draw.text((x + 18, y + 14), label, fill=(235, 235, 235), font=load_font(27, bold=True))
    value_text = str(value)
    value_font = fit_text(draw, value_text, 74, 34, bold=True)
    value_bbox = draw.textbbox((0, 0), value_text, font=value_font)
    value_width = value_bbox[2] - value_bbox[0]
    value_height = value_bbox[3] - value_bbox[1]
    value_x = x + 182 - 18 - value_width
    value_y = y + ((82 - value_height) / 2) - 3
    draw.text((value_x, value_y), value_text, fill=accent, font=value_font)


def normalize_position_label(position):
    return " ".join(str(position or "").replace("_", " ").split()).strip().upper()


def get_position_badge(position):
    normalized = normalize_position_label(position)
    position_map = {
        "GOLEIRO": "GK",
        "LATERAL DIREITO": "LD",
        "LATERAL ESQUERDO": "LE",
        "ZAGUEIRO": "ZAG",
        "VOLANTE": "VOL",
        "MEIA CENTRAL": "MC",
        "MEIA OFENSIVO": "MO",
        "PONTA DIREITA": "PD",
        "PONTA ESQUERDA": "PE",
        "SEGUNDO ATACANTE": "SA",
        "CENTROAVANTE": "9",
    }
    return position_map.get(normalized, normalized[:3] or "ATL")


def draw_empty_photo_state(draw, box, accent, fill):
    inner = (box[0] + 24, box[1] + 24, box[2] - 24, box[3] - 24)
    draw.rounded_rectangle(inner, radius=24, outline=(86, 92, 102), width=2)
    center_x = (box[0] + box[2]) // 2
    head_radius = 42
    head_box = (center_x - head_radius, box[1] + 84, center_x + head_radius, box[1] + 84 + (head_radius * 2))
    draw.ellipse(head_box, outline=accent, width=5)
    body_top = head_box[3] + 22
    draw.rounded_rectangle(
        (center_x - 116, body_top, center_x + 116, body_top + 146),
        radius=48,
        outline=accent,
        width=5,
    )
    center_text(draw, (box[0] + 48, body_top + 168, box[2] - 48, body_top + 214), "AGUARDANDO FOTO OFICIAL", load_font(24, bold=True), accent)
    center_text(draw, (box[0] + 60, body_top + 216, box[2] - 60, body_top + 266), "ENVIE UMA IMAGEM NITIDA PARA GERAR O CARD FINAL", load_font(16, bold=True), (214, 218, 224))


def get_club_initials(club_name):
    words = [
        word for word in str(club_name or "HUB").replace("-", " ").split()
        if word.strip()
    ]
    if not words:
        return "HUB"
    if len(words) == 1:
        return words[0][:3].upper()
    return "".join(word[0] for word in words[:3]).upper()


def draw_club_shield(draw, box, club_name, accent):
    x0, y0, x1, y1 = box
    center_x = (x0 + x1) // 2
    points = [
        (center_x, y0),
        (x1, y0 + 18),
        (x1 - 10, y1 - 26),
        (center_x, y1),
        (x0 + 10, y1 - 26),
        (x0, y0 + 18),
    ]
    draw.polygon(points, fill=(18, 20, 24), outline=accent)
    draw.line(points + [points[0]], fill=accent, width=4)
    center_text(draw, (x0 + 8, y0 + 18, x1 - 8, y1 - 18), get_club_initials(club_name), load_font(28, bold=True), accent)


def build_neutral_backdrop(size, accent=(226, 190, 76), panel=(31, 34, 40)):
    backdrop = Image.new("RGB", size, panel)
    backdrop_draw = ImageDraw.Draw(backdrop)
    for y in range(size[1]):
        ratio = y / max(1, size[1])
        color = (
            min(255, int(panel[0] + (18 * ratio))),
            min(255, int(panel[1] + (18 * ratio))),
            min(255, int(panel[2] + (18 * ratio))),
        )
        backdrop_draw.line((0, y, size[0], y), fill=color)
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse(
        (-int(size[0] * 0.12), -int(size[1] * 0.04), int(size[0] * 1.12), int(size[1] * 1.08)),
        fill=(235, 238, 242, 42),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=18))
    backdrop = Image.alpha_composite(backdrop.convert("RGBA"), glow).convert("RGB")
    backdrop_draw = ImageDraw.Draw(backdrop)
    backdrop_draw.ellipse((-80, -50, size[0] + 80, size[1] + 120), outline=accent, width=5)
    backdrop_draw.ellipse((22, 28, size[0] - 22, size[1] - 28), outline=(255, 255, 255), width=1)
    return backdrop


def crop_portrait_region(photo):
    cv_image = cv2.cvtColor(np.array(photo), cv2.COLOR_RGB2BGR)
    face_box = detect_largest_face_box(cv_image)
    min_face_width = max(140, int(photo.size[0] * 0.12))
    min_face_height = max(140, int(photo.size[1] * 0.10))

    if face_box is None or face_box[2] < min_face_width or face_box[3] < min_face_height:
        crop_width = min(photo.size[0], int(photo.size[0] * 0.82))
        crop_height = min(photo.size[1], int(photo.size[1] * 0.86))
        left = max(0, (photo.size[0] - crop_width) // 2)
        top = max(0, int((photo.size[1] - crop_height) * 0.18))
        return photo.crop((left, top, left + crop_width, top + crop_height))

    x, y, width, height = face_box
    center_x = x + (width / 2)
    center_y = y + (height * 1.22)
    crop_width = min(photo.size[0], int(width * 2.85))
    crop_height = min(photo.size[1], int(height * 3.95))
    left = max(0, int(center_x - (crop_width / 2)))
    top = max(0, int(center_y - (crop_height * 0.40)))
    right = min(photo.size[0], left + crop_width)
    bottom = min(photo.size[1], top + crop_height)

    if right - left < crop_width:
        left = max(0, right - crop_width)
    if bottom - top < crop_height:
        top = max(0, bottom - crop_height)

    return photo.crop((left, top, right, bottom))


def build_focus_mask(size, focus_x_ratio=0.5, focus_y_ratio=0.5):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    center_x = int(size[0] * focus_x_ratio)
    center_y = int(size[1] * focus_y_ratio)
    radius_x = int(size[0] * 0.36)
    radius_y = int(size[1] * 0.40)
    draw.ellipse(
        (
            center_x - radius_x,
            center_y - radius_y,
            center_x + radius_x,
            center_y + radius_y,
        ),
        fill=255,
    )
    return mask.filter(ImageFilter.GaussianBlur(radius=20))


def prepare_card_portrait(photo_path, target_size):
    if not photo_path:
        return None

    try:
        photo = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGB")
        portrait_region = crop_portrait_region(photo)
        portrait = ImageOps.fit(
            portrait_region,
            target_size,
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.28),
        )
        portrait = ImageEnhance.Sharpness(portrait).enhance(1.35)
        portrait = ImageEnhance.Contrast(portrait).enhance(1.08)
        portrait = ImageEnhance.Color(portrait).enhance(1.02)
        softened = portrait.filter(ImageFilter.GaussianBlur(radius=8))
        softened = ImageEnhance.Color(softened).enhance(0.24)
        softened = ImageEnhance.Brightness(softened).enhance(0.82)
        neutral_fill = Image.new("RGB", target_size, (126, 132, 140))
        softened = Image.blend(softened, neutral_fill, 0.58)
        focused = Image.composite(portrait, softened, build_focus_mask(target_size, 0.5, 0.48))
        return focused.convert("RGBA")
    except Exception:
        return None


def paste_athlete_photo(img, draw, photo_path, box, accent, panel):
    draw.rounded_rectangle(box, radius=24, fill=panel, outline=accent, width=5)

    if not photo_path:
        draw_empty_photo_state(draw, box, accent, panel)
        return

    try:
        frame_width = box[2] - box[0] - 16
        frame_height = box[3] - box[1] - 16
        fitted = build_neutral_backdrop((frame_width, frame_height), accent, panel)
        portrait_width = min(int(frame_width * 0.44), int(frame_height * 0.82))
        portrait_height = int(frame_height * 0.88)
        portrait = prepare_card_portrait(photo_path, (portrait_width, portrait_height))
        if portrait is not None:
            fitted = fitted.convert("RGBA")
            portrait_x = (frame_width - portrait_width) // 2
            portrait_y = int(frame_height * 0.06)
            portrait_mask = Image.new("L", portrait.size, 0)
            portrait_mask_draw = ImageDraw.Draw(portrait_mask)
            portrait_mask_draw.rounded_rectangle((0, 0, portrait.size[0] - 1, portrait.size[1] - 1), radius=24, fill=255)
            portrait.putalpha(portrait_mask)
            portrait_shadow = Image.new("RGBA", portrait.size, (0, 0, 0, 0))
            portrait_shadow.putalpha(portrait_mask.filter(ImageFilter.GaussianBlur(radius=12)))
            fitted.alpha_composite(portrait_shadow, (portrait_x + 6, portrait_y + 10))
            fitted.alpha_composite(portrait, (portrait_x, portrait_y))
            fitted = fitted.convert("RGB")

        mask = Image.new("L", fitted.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, fitted.size[0], fitted.size[1]), radius=20, fill=255)
        img.paste(fitted, (box[0] + 8, box[1] + 8), mask)
    except Exception:
        draw_empty_photo_state(draw, box, accent, panel)


def generate_card(data):
    width, height = 900, 1260
    tier = data.get("card_tier") or get_card_tier(data.get("overall", 74))
    accent = tuple(tier.get("accent_rgb", [226, 190, 76]))
    secondary = tuple(tier.get("secondary_rgb", [130, 96, 28]))
    dark = tuple(tier.get("dark_rgb", [10, 12, 16]))
    panel = tuple(tier.get("panel_rgb", [24, 27, 32]))
    light = (245, 244, 238)

    img = Image.new("RGB", (width, height), color=dark)
    draw = ImageDraw.Draw(img)
    draw.polygon([(42, 210), (42, 92), (210, 42), (365, 42)], fill=secondary)
    draw.polygon([(858, 1048), (858, 1218), (640, 1218), (770, 1048)], fill=secondary)
    draw.rectangle((74, 276, 826, 286), fill=accent)

    for offset, color in [(0, accent), (14, secondary), (26, accent)]:
        draw.rounded_rectangle((42 + offset, 38 + offset, width - 42 - offset, height - 38 - offset), radius=48, outline=color, width=8)

    name = data.get("athlete_name", "ATLETA").upper()
    category = data.get("category", "SUB-12").upper()
    track = "FEM" if data.get("competition_track") == "feminino" else "MASC"
    raw_position = data.get("position", "meia central")
    position_badge = get_position_badge(raw_position)
    position_label = normalize_position_label(raw_position) or "ATLETA DE LINHA"
    overall = str(data.get("overall", 74))
    profile_match = data.get("elite_profile_match", {})
    reference = profile_match.get("reference_athlete", "Gilberto Silva").upper()
    supporter_club = data.get("supporter_club") or "HUB-PODIUM"
    recognition = data.get("recognition") or {}
    face_confidence = recognition.get("match_confidence", 0) or 0
    face_confidence_value = f"{face_confidence}%" if face_confidence and face_confidence > 0 else "--"
    photo_path = get_photo_path(data)

    draw.rounded_rectangle((82, 82, 288, 265), radius=20, fill=panel, outline=accent, width=4)
    center_text(draw, (82, 88, 288, 176), overall, load_font(72, bold=True), accent)
    center_text(draw, (82, 168, 288, 224), position_badge, load_font(38, bold=True), light)
    center_text(draw, (82, 215, 288, 260), f"{category} | {track}", load_font(22, bold=True), (210, 214, 220))

    draw.rounded_rectangle((322, 82, 818, 150), radius=16, fill=panel, outline=accent, width=3)
    center_text(draw, (322, 82, 818, 150), f"CARD {tier.get('label', 'HUB-ELITE')}", load_font(34, bold=True), accent)
    draw.rounded_rectangle((322, 170, 676, 232), radius=16, fill=panel, outline=(80, 84, 92), width=2)
    reference_font = fit_text(draw, f"REFERENCIA: {reference}", 320, 22, bold=True)
    center_text(draw, (322, 170, 676, 232), f"REFERENCIA: {reference}", reference_font, light)
    draw.rounded_rectangle((322, 244, 676, 276), radius=12, fill=accent)
    center_text(draw, (322, 244, 676, 276), tier.get("headline", "Perfil esportivo").upper(), load_font(18, bold=True), dark)
    draw_club_shield(draw, (702, 162, 818, 270), supporter_club, accent)

    paste_athlete_photo(img, draw, photo_path, (132, 290, 768, 690), accent, panel)

    draw.rounded_rectangle((100, 714, 800, 816), radius=18, fill=panel, outline=accent, width=4)
    name_font = fit_text(draw, name, 640, 44, bold=True)
    center_text(draw, (116, 718, 784, 772), name, name_font, light)
    draw_pill(draw, (232, 778, 668, 808), position_label, fill=(19, 22, 28), outline=(84, 90, 100), text_fill=(224, 228, 232), font_size=18)

    stats = [
        ("VEL", data.get("speed", 78)),
        ("TEC", data.get("technique", 72)),
        ("QI", data.get("game_iq", 70)),
        ("FIS", data.get("physical", 76)),
        ("POT", data.get("potential", 82)),
        ("FAC", face_confidence_value),
    ]

    x_positions = [112, 360, 608]
    y_positions = [846, 948]
    for index, (label, value) in enumerate(stats):
        draw_stat_block(draw, x_positions[index % 3], y_positions[index // 3], label, value, accent, panel)

    draw.rounded_rectangle((102, 1060, 798, 1162), radius=18, fill=panel, outline=accent, width=3)
    headline = profile_match.get("profile_headline", "perfil esportivo em desenvolvimento").upper()
    headline_font, headline_lines = fit_multiline_text(draw, headline, 608, 29, max_lines=2, bold=True)
    center_multiline_text(draw, (122, 1068, 778, 1128), headline_lines, headline_font, light, line_gap=5)
    center_text(
        draw,
        (120, 1126, 780, 1156),
        f"{tier.get('label', 'CARD')} | SIM {profile_match.get('similarity_score', 0)}% | {category}",
        load_font(22, bold=True),
        accent,
    )

    img.save(OUTPUT)
    return str(OUTPUT)
