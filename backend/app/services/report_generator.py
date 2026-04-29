from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

OUTPUT = Path("/tmp/hub_podium_report.pdf")

def generate_report(data):
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    width, height = A4

    name = data.get("athlete_name", "Atleta HUB-PODIUM")
    position = data.get("position", "meia")

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 70, "Relatório de Análise HUB-PODIUM")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 110, f"Atleta: {name}")
    c.drawString(50, height - 130, f"Posição: {position}")
    c.drawString(50, height - 150, f"Overall: {data.get('overall', 74)}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 200, "Indicadores")

    c.setFont("Helvetica", 12)
    lines = [
        f"Velocidade: {data.get('speed', 78)}",
        f"Técnica: {data.get('technique', 72)}",
        f"Inteligência de Jogo: {data.get('game_iq', 70)}",
        f"Físico: {data.get('physical', 76)}",
        f"Potencial: {data.get('potential', 82)}",
    ]

    y = height - 230
    for line in lines:
        c.drawString(70, y, line)
        y -= 22

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 20, "Recomendação HUB-PODIUM")
    c.setFont("Helvetica", 12)
    c.drawString(70, y - 50, "Manter rotina de treinos técnicos, tomada de decisão e intensidade sem bola.")
    c.drawString(70, y - 70, "A avaliação completa deve ser validada por scout/profissional em fase posterior.")

    c.save()
    return str(OUTPUT)
