# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, HRFlowable
)

GITHUB_URL = "https://github.com/DufreyM/CC2017-Laboratorio5"
OUT = "Laboratorio5_Respuestas.pdf"

FONT = "Times-Roman"
FONT_BOLD = "Times-Bold"
FONT_ITALIC = "Times-Italic"

styles = getSampleStyleSheet()
for _name in styles.byName:
    styles[_name].fontName = FONT
styles["Heading1"].fontName = FONT_BOLD
styles["Heading2"].fontName = FONT_BOLD
styles["Heading3"].fontName = FONT_BOLD
styles["Title"].fontName = FONT_BOLD

styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontName=FONT_BOLD, spaceBefore=18, spaceAfter=8, textColor=colors.black))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontName=FONT_BOLD, spaceBefore=12, spaceAfter=6, textColor=colors.black))
styles.add(ParagraphStyle(name="H3", parent=styles["Heading3"], fontName=FONT_BOLD, spaceBefore=8, spaceAfter=4, textColor=colors.black))
styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], fontName=FONT, alignment=TA_JUSTIFY, spaceAfter=8, leading=14))
styles.add(ParagraphStyle(name="Caption", parent=styles["Normal"], fontName=FONT_ITALIC, alignment=TA_CENTER, fontSize=9, textColor=colors.black, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName=FONT_BOLD, fontSize=26, leading=32))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontName=FONT, fontSize=14, alignment=TA_CENTER, spaceAfter=6))

story = []

# ---------- CARATULA (formato UVG estándar) ----------
caratula_center = ParagraphStyle(name="CaratulaCenter", parent=styles["Normal"], fontName=FONT, alignment=TA_CENTER, fontSize=12, leading=16)

story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph("UNIVERSIDAD DEL VALLE DE GUATEMALA", ParagraphStyle(name="UniName", parent=styles["Normal"], fontName=FONT, fontSize=14, alignment=TA_CENTER, spaceAfter=20)))
story.append(Paragraph("CC2017 — Modelación y Simulación", caratula_center))
story.append(Spacer(1, 0.5 * inch))

story.append(Image("assets/uvg_logo.png", width=2.1 * inch, height=2.1 * inch * (448 / 301)))
story.append(Spacer(1, 0.5 * inch))

story.append(Paragraph("Laboratorio 5", ParagraphStyle(name="CoverTitle2", parent=styles["Normal"], fontName=FONT, fontSize=16, alignment=TA_CENTER, spaceAfter=2)))
story.append(Paragraph("Informe", ParagraphStyle(name="CoverInforme", parent=styles["Normal"], fontName=FONT, fontSize=13, alignment=TA_CENTER, spaceAfter=4)))
story.append(Paragraph("Modelo espacial de cobertura hospitalaria — Indiana (IN)",
                        ParagraphStyle(name="Subtitle2", parent=styles["Normal"], fontName=FONT, fontSize=11, alignment=TA_CENTER, textColor=colors.black, spaceAfter=30)))

story.append(Paragraph("Leonardo Dufrey Mejía Mejía", caratula_center))
story.append(Paragraph("María José Girón Isidro", caratula_center))
story.append(Spacer(1, 0.6 * inch))

story.append(Paragraph(f'Repositorio de GitHub: <link href="{GITHUB_URL}"><u>{GITHUB_URL}</u></link>',
                        ParagraphStyle(name="GHLink", parent=styles["Normal"], fontName=FONT, fontSize=10.5, alignment=TA_CENTER, textColor=colors.black, spaceAfter=20)))

story.append(Paragraph("6 de octubre de 2026", caratula_center))

story.append(PageBreak())

def h1(text): story.append(Paragraph(text, styles["H1"]))
def h2(text): story.append(Paragraph(text, styles["H2"]))
def h3(text): story.append(Paragraph(text, styles["H3"]))
def p(text): story.append(Paragraph(text, styles["Body"]))
def img(path, width=5.5 * inch, caption=None):
    story.append(Spacer(1, 6))
    story.append(Image(path, width=width, height=width * 0.78))
    if caption:
        story.append(Paragraph(caption, styles["Caption"]))

cell_style = ParagraphStyle(name="CellBody", parent=styles["Normal"], fontName=FONT, fontSize=8.5, leading=11, alignment=TA_CENTER)
cell_header_style = ParagraphStyle(name="CellHeader", parent=styles["Normal"], fontName=FONT_BOLD, fontSize=9, leading=11, alignment=TA_CENTER, textColor=colors.white)

def simple_table(headers, rows, col_widths=None):
    header_cells = [Paragraph(str(h), cell_header_style) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), cell_style) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e8e8e8")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

with open("build_pdf_content.py", encoding="utf-8") as f:
    exec(f.read())

doc = SimpleDocTemplate(OUT, pagesize=letter,
                         topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                         leftMargin=0.9 * inch, rightMargin=0.9 * inch)
doc.build(story)
print("PDF generado:", OUT)
