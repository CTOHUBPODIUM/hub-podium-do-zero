from pathlib import Path
from tempfile import gettempdir

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from services.card_tiers import get_card_tier

OUTPUT = Path(gettempdir()) / "hub_podium_report.pdf"
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 42
RIGHT = PAGE_WIDTH - 42
TOP = PAGE_HEIGHT - 42
BOTTOM = 42


def safe_text(value, fallback=""):
    text = str(value or fallback).strip()
    return text or fallback


def wrap_text_to_width(c, text, max_width, font_name="Helvetica", font_size=10):
    words = safe_text(text).split()
    if not words:
        return [""]

    lines = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if c.stringWidth(candidate, font_name, font_size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate

    lines.append(current)
    return lines


def get_photo_path(data):
    photo = data.get("athlete_photo") or {}
    path = photo.get("stored_path") or data.get("athlete_photo_path")
    if not path:
        return None
    photo_path = Path(path)
    return photo_path if photo_path.exists() else None


class ReportLayout:
    def __init__(self, c, data):
        self.c = c
        self.data = data
        self.page = 0
        self.y = TOP
        self.new_page()

    def new_page(self):
        if self.page:
            self.draw_footer()
            self.c.showPage()
        self.page += 1
        self.y = TOP
        self.draw_page_header()

    def draw_page_header(self):
        self.c.setFillColorRGB(0.06, 0.07, 0.08)
        self.c.rect(0, PAGE_HEIGHT - 74, PAGE_WIDTH, 74, stroke=0, fill=1)
        self.c.setFillColorRGB(0.83, 0.69, 0.22)
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(LEFT, PAGE_HEIGHT - 32, "Relatório HUB-PODIUM")
        self.c.setFillColorRGB(1, 1, 1)
        self.c.setFont("Helvetica", 10)
        self.c.drawRightString(
            RIGHT,
            PAGE_HEIGHT - 32,
            f"Análise {safe_text(self.data.get('analysis_id'), 'beta')}",
        )
        self.y = PAGE_HEIGHT - 96

    def draw_footer(self):
        self.c.setStrokeColorRGB(0.82, 0.84, 0.88)
        self.c.line(LEFT, BOTTOM + 18, RIGHT, BOTTOM + 18)
        self.c.setFillColorRGB(0.33, 0.37, 0.43)
        self.c.setFont("Helvetica", 9)
        self.c.drawString(LEFT, BOTTOM + 4, "HUB-PODIUM · Relatório gerado para uso orientativo no desenvolvimento esportivo.")
        self.c.drawRightString(RIGHT, BOTTOM + 4, f"Página {self.page}")

    def ensure_space(self, height_needed):
        if self.y - height_needed < BOTTOM + 28:
            self.new_page()

    def section_title(self, title, min_content_space=22):
        self.ensure_space(32 + min_content_space)
        self.c.setFillColorRGB(0.08, 0.10, 0.14)
        self.c.setFont("Helvetica-Bold", 15)
        self.c.drawString(LEFT, self.y, title)
        self.y -= 18
        self.c.setStrokeColorRGB(0.83, 0.69, 0.22)
        self.c.line(LEFT, self.y, RIGHT, self.y)
        self.y -= 16

    def body_text(self, text, max_width=None, leading=14, gap=5, x=None):
        font_name = "Helvetica"
        font_size = 10
        lines = wrap_text_to_width(
            self.c,
            text,
            max_width or (RIGHT - LEFT),
            font_name=font_name,
            font_size=font_size,
        )
        self.ensure_space(len(lines) * leading + gap)
        self.c.setFillColorRGB(0.18, 0.20, 0.24)
        self.c.setFont(font_name, font_size)
        text_x = x or LEFT
        for line in lines:
            self.c.drawString(text_x, self.y, line)
            self.y -= leading
        self.y -= gap

    def sub_label(self, label):
        self.ensure_space(18)
        self.c.setFont("Helvetica-Bold", 10)
        self.c.setFillColorRGB(0.08, 0.10, 0.14)
        self.c.drawString(LEFT, self.y, f"{label}:")
        self.y -= 16

    def key_value(self, label, value, fallback="Não informado"):
        label_text = f"{label}:"
        label_font = "Helvetica-Bold"
        value_font = "Helvetica"
        font_size = 10
        inline_threshold = 150
        indent = LEFT + 158

        label_width = self.c.stringWidth(label_text, label_font, font_size)
        value_text = safe_text(value, fallback) if fallback is not None else safe_text(value, "")
        value_width = RIGHT - max(indent, LEFT + label_width + 10)
        value_lines = (
            wrap_text_to_width(
                self.c,
                value_text,
                max(80, value_width),
                font_name=value_font,
                font_size=font_size,
            )
            if value_text
            else []
        )
        stack_value = label_width > inline_threshold or max(indent, LEFT + label_width + 10) > RIGHT - 160
        line_count = max(1, len(value_lines))
        height_needed = 16
        if value_lines:
            height_needed += (line_count - (0 if stack_value else 1)) * 14
            if stack_value:
                height_needed += 14
        self.ensure_space(max(18, height_needed + 4))

        self.c.setFont(label_font, font_size)
        self.c.setFillColorRGB(0.08, 0.10, 0.14)
        self.c.drawString(LEFT, self.y, label_text)

        if not value_lines:
            self.y -= 16
            return

        self.c.setFont(value_font, font_size)
        self.c.setFillColorRGB(0.22, 0.24, 0.28)
        if stack_value:
            self.y -= 16
            for line in value_lines:
                self.c.drawString(LEFT + 12, self.y, line)
                self.y -= 14
            self.y -= 2
            return

        value_x = max(indent, LEFT + label_width + 10)
        current_y = self.y
        for index, line in enumerate(value_lines):
            self.c.drawString(value_x, current_y, line)
            if index < len(value_lines) - 1:
                current_y -= 14
        self.y = current_y - 16

    def bullets(self, items):
        for item in items:
            text = safe_text(item)
            if not text:
                continue
            lines = wrap_text_to_width(
                self.c,
                text,
                RIGHT - (LEFT + 12),
                font_name="Helvetica",
                font_size=10,
            )
            self.ensure_space(len(lines) * 14 + 4)
            self.c.setFont("Helvetica", 10)
            self.c.setFillColorRGB(0.18, 0.20, 0.24)
            self.c.drawString(LEFT, self.y, "•")
            current_y = self.y
            for index, line in enumerate(lines):
                self.c.drawString(LEFT + 12, current_y, line)
                current_y -= 14
            self.y = current_y - 4

    def stat_row(self, stats):
        box_height = 38
        box_width = 95
        gap = 10
        needed = box_height + 10
        self.ensure_space(needed)
        x = LEFT
        for label, value in stats:
            self.c.setStrokeColorRGB(0.83, 0.69, 0.22)
            self.c.roundRect(x, self.y - box_height, box_width, box_height, 8, stroke=1, fill=0)
            self.c.setFont("Helvetica-Bold", 9)
            self.c.setFillColorRGB(0.10, 0.12, 0.15)
            self.c.drawString(x + 9, self.y - 14, label)
            self.c.setFont("Helvetica-Bold", 16)
            self.c.drawRightString(x + box_width - 9, self.y - 28, str(value))
            x += box_width + gap
        self.y -= box_height + 12


def draw_cover(layout, data):
    c = layout.c
    name = safe_text(data.get("athlete_name"), "Atleta HUB-PODIUM")
    category = safe_text(data.get("category"), "sub-12").upper()
    position = safe_text(data.get("position"), "meia").title()
    track = "Feminino" if data.get("competition_track") == "feminino" else "Masculino"
    overall = data.get("overall", 74)
    supporter_club = safe_text(data.get("supporter_club"), "Não informado")
    responsible_whatsapp = safe_text(data.get("responsible_whatsapp"), "Não informado")
    algorithm = safe_text(data.get("algorithm"), "HUB-ELITE")
    card_tier = data.get("card_tier") or get_card_tier(overall)
    photo_path = get_photo_path(data)

    c.setFillColorRGB(0.08, 0.10, 0.14)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(LEFT, layout.y, name)
    layout.y -= 22
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.22, 0.24, 0.28)
    c.drawString(LEFT, layout.y, f"Categoria: {category} · Posição: {position} · Trilha: {track}")
    layout.y -= 18
    c.drawString(LEFT, layout.y, f"Algoritmo: {algorithm} · Overall: {overall} · Card: {safe_text(card_tier.get('label'), 'CARD')}")
    layout.y -= 24

    if photo_path:
        try:
            frame_x = RIGHT - 128
            frame_y = layout.y - 116
            frame_width = 106
            frame_height = 122
            image_padding = 8
            c.drawImage(
                ImageReader(str(photo_path)),
                frame_x + image_padding,
                frame_y + image_padding,
                width=frame_width - (image_padding * 2),
                height=frame_height - (image_padding * 2),
                preserveAspectRatio=True,
                anchor="c",
            )
            c.setStrokeColorRGB(0.83, 0.69, 0.22)
            c.roundRect(frame_x, frame_y, frame_width, frame_height, 10, stroke=1, fill=0)
            layout.y = min(layout.y, frame_y - 18)
        except Exception:
            pass

    layout.section_title("Resumo executivo")
    executive_summary = data.get("executive_summary", {})
    profile_match = data.get("elite_profile_match", {})
    layout.body_text(executive_summary.get("profile_reading", profile_match.get("comparison_text", "")))
    layout.body_text(executive_summary.get("development_recommendation", ""))

    layout.section_title("Dados principais")
    layout.key_value("Clube do coração", supporter_club)
    layout.key_value("WhatsApp do responsável", responsible_whatsapp)
    layout.key_value("Identificador da análise", safe_text(data.get("analysis_id"), "beta"))

    recognition = data.get("recognition", {})
    layout.section_title("Reconhecimento do atleta")
    layout.key_value("Status facial", recognition.get("video_identity_check", "Pendente"))
    layout.key_value("Confiança estimada", f"{recognition.get('match_confidence', 0) or 0}%")
    layout.body_text(recognition.get("message", "Foto usada como referência visual para o fluxo de vídeo."))

    layout.section_title("Indicadores HUB-ELITE")
    layout.stat_row([
        ("VEL", data.get("speed", 78)),
        ("TEC", data.get("technique", 72)),
        ("QI", data.get("game_iq", 70)),
        ("FÍS", data.get("physical", 76)),
        ("POT", data.get("potential", 82)),
    ])


def draw_analysis_pages(layout, data):
    executive_summary = data.get("executive_summary", {})
    profile_match = data.get("elite_profile_match", {})
    category_profile = data.get("category_profile", {})
    calibration = data.get("calibration", {})
    position_consistency = calibration.get("position_consistency", {})
    functional_family = calibration.get("functional_family_coherence", {})
    similarity = calibration.get("similarity_refinement", {})
    category_gap = calibration.get("category_gap_matrix", {})
    development_gaps = calibration.get("development_gaps", {})
    comparative = calibration.get("comparative_explainability", {})
    golden_ball = calibration.get("golden_ball_map", {})

    layout.section_title("Leitura de perfil esportivo")
    layout.key_value("Referência principal", profile_match.get("reference_athlete", "Não definida"))
    layout.key_value("Similaridade base", f"{profile_match.get('similarity_score', 0)}%")
    style_tags = profile_match.get("style_tags", [])
    if style_tags:
        layout.key_value("Marcas do perfil", ", ".join(style_tags))
    layout.body_text(executive_summary.get("profile_reading", profile_match.get("comparison_text", "")))
    layout.body_text(profile_match.get("development_note", ""))

    layout.section_title("Direção evolutiva")
    layout.key_value("Perfil da categoria", category_profile.get("experience_profile", "evolutivo"))
    layout.body_text(executive_summary.get("category_guidance", category_profile.get("message", "")))
    layout.body_text(executive_summary.get("development_recommendation", ""))

    layout.section_title("Calibração do algoritmo")
    layout.key_value("Consistência posicional", f"{position_consistency.get('score', 0)} · {safe_text(position_consistency.get('band'), 'n/a')}")
    layout.key_value("Coerência funcional", f"{functional_family.get('score', 0)} · {safe_text(functional_family.get('canonical_position_code'), 'n/a')}")
    layout.key_value("Similaridade refinada", f"{similarity.get('overall_score', profile_match.get('similarity_score', 0))}%")
    if similarity.get("shared_style_tags"):
        layout.key_value("Encaixe de estilo", ", ".join(similarity.get("shared_style_tags", [])))
    layout.body_text(executive_summary.get("calibration_summary", position_consistency.get("summary", "")))
    layout.body_text(category_gap.get("summary", executive_summary.get("category_gap_summary", "")))

    priorities = development_gaps.get("top_priorities", [])
    if priorities:
        items = []
        for item in priorities:
            if isinstance(item, dict):
                label = safe_text(item.get("label"), "prioridade").title()
                gap = item.get("gap", 0)
                focus = safe_text(item.get("focus"), "")
                if focus:
                    items.append(f"{label}: gap {gap} · foco em {focus}.")
                else:
                    items.append(f"{label}: gap {gap}.")
            elif item:
                items.append(safe_text(item))
        if items:
            layout.section_title("Prioridades de evolução", min_content_space=54)
            layout.bullets(items)

    if comparative.get("parent_summary") or comparative.get("club_summary"):
        layout.section_title("Leitura para famílias e clubes", min_content_space=40)
        if comparative.get("parent_summary"):
            layout.sub_label("Pais e responsáveis")
            layout.body_text(comparative.get("parent_summary"))
        if comparative.get("club_summary"):
            layout.sub_label("Clubes e treinadores")
            layout.body_text(comparative.get("club_summary"))

    layout.section_title("Mapa Golden Ball")
    layout.key_value("Estágio atual", golden_ball.get("current_stage", "Fundação competitiva"))
    layout.key_value("Próximo estágio", golden_ball.get("next_stage", "n/a"))
    layout.key_value("Stage score", golden_ball.get("stage_score", 0))
    next_checkpoint = golden_ball.get("next_cycle_checkpoint") or {}
    if next_checkpoint:
        layout.key_value(
            "Próximo checkpoint",
            f"{safe_text(next_checkpoint.get('label'), 'n/a')} · distância {next_checkpoint.get('distance', 0)}",
        )
    layout.body_text(executive_summary.get("golden_ball_summary", golden_ball.get("summary", "")))


def draw_roadmap_pages(layout, data):
    calibration = data.get("calibration", {})
    training_roadmap = calibration.get("training_roadmap", {})
    evolution_subscription = calibration.get("evolution_subscription", {})
    onboarding_journey = calibration.get("onboarding_journey", {})
    executive_summary = data.get("executive_summary", {})
    profile_match = data.get("elite_profile_match", {})
    facial_verification = data.get("facial_verification") or {}

    cycles = training_roadmap.get("cycles", [])
    if cycles:
        layout.section_title("Roadmap de treino", min_content_space=120)
        layout.body_text(training_roadmap.get("summary", ""))
        for cycle in cycles:
            layout.ensure_space(80)
            layout.key_value(
                f"Ciclo {safe_text(cycle.get('cycle'), '1')}",
                safe_text(cycle.get("label"), "").title(),
            )
            layout.body_text(cycle.get("goal", ""))
            if cycle.get("training_blocks"):
                layout.body_text(f"Blocos: {', '.join(cycle.get('training_blocks', []))}")
            layout.body_text(cycle.get("checkpoint", ""))

    if evolution_subscription:
        layout.section_title("Acompanhamento em estudo", min_content_space=40)
        layout.key_value("Frente atual", evolution_subscription.get("plan_name", "Acompanhamento em estudo"))
        layout.key_value("Módulo base", evolution_subscription.get("module_name", "Módulo evolutivo"))
        layout.key_value("Contexto competitivo", evolution_subscription.get("program_tier", "Desenvolvimento competitivo"))
        layout.body_text(evolution_subscription.get("sales_summary", ""))

    if onboarding_journey:
        layout.section_title("Roteiro da beta", min_content_space=40)
        layout.body_text(onboarding_journey.get("summary", ""))
        for step in onboarding_journey.get("steps", []):
            layout.key_value(f"Etapa {step.get('step', '')}", step.get("title", ""))
            layout.body_text(step.get("description", ""))

    layout.section_title("Recomendações HUB-PODIUM", min_content_space=54)
    recommendations = [
        "Manter rotina de treinos técnicos, tomada de decisão e intensidade sem bola.",
        executive_summary.get("development_recommendation", ""),
        "Enviar novos vídeos periodicamente para acompanhar a evolução do atleta.",
        "Sem comercialização ativa nesta fase. O foco atual é validação técnica, clareza da devolutiva e teste assistido.",
        profile_match.get("disclaimer", ""),
        executive_summary.get("institutional_note", ""),
        facial_verification.get("disclaimer", ""),
    ]
    layout.bullets([item for item in recommendations if safe_text(item)])


def generate_report(data):
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    layout = ReportLayout(c, data)
    draw_cover(layout, data)
    draw_analysis_pages(layout, data)
    draw_roadmap_pages(layout, data)
    layout.draw_footer()
    c.save()
    return str(OUTPUT)

