from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT = Path("/tmp/hub_podium_card.png")

def generate_card(data):
    img = Image.new("RGB", (800, 1100), color=(212, 175, 55))
    draw = ImageDraw.Draw(img)

    try:
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 90)
        font_med = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 36)
    except Exception:
        font_big = font_med = font_small = None

    name = data.get("athlete_name", "ATLETA")
    position = data.get("position", "MEI").upper()[:3]
    overall = str(data.get("overall", 74))

    draw.rounded_rectangle((60, 60, 740, 1040), radius=40, outline=(20,20,20), width=8)
    draw.text((90, 110), overall, fill=(20,20,20), font=font_big)
    draw.text((100, 220), position, fill=(20,20,20), font=font_med)
    draw.text((150, 500), name.upper(), fill=(20,20,20), font=font_med)

    stats = [
        ("VEL", data.get("speed", 78)),
        ("TEC", data.get("technique", 72)),
        ("QI", data.get("game_iq", 70)),
        ("FIS", data.get("physical", 76)),
        ("POT", data.get("potential", 82)),
    ]

    y = 650
    for label, value in stats:
        draw.text((180, y), f"{label}  {value}", fill=(20,20,20), font=font_small)
        y += 70

    draw.text((210, 970), "HUB-PODIUM", fill=(20,20,20), font=font_med)
    img.save(OUTPUT)
    return str(OUTPUT)
