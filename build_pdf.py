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

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8, textColor=colors.HexColor("#1b4332")))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#2d6a4f")))
styles.add(ParagraphStyle(name="H3", parent=styles["Heading3"], spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#40916c")))
styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], alignment=TA_JUSTIFY, spaceAfter=8, leading=14))
styles.add(ParagraphStyle(name="Caption", parent=styles["Normal"], alignment=TA_CENTER, fontSize=9, textColor=colors.grey, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=26, leading=32))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=14, alignment=TA_CENTER, spaceAfter=6))

story = []

# ---------- CARATULA (formato UVG estándar) ----------
caratula_center = ParagraphStyle(name="CaratulaCenter", parent=styles["Normal"], alignment=TA_CENTER, fontSize=12, leading=16)

story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph("UNIVERSIDAD DEL VALLE DE GUATEMALA", ParagraphStyle(name="UniName", parent=styles["Normal"], fontSize=14, alignment=TA_CENTER, spaceAfter=20)))
story.append(Paragraph("CC2017 — Modelación y Simulación", caratula_center))
story.append(Spacer(1, 0.5 * inch))

story.append(Image("assets/uvg_logo.png", width=2.1 * inch, height=2.1 * inch * (448 / 301)))
story.append(Spacer(1, 0.5 * inch))

story.append(Paragraph("Laboratorio 5", ParagraphStyle(name="CoverTitle2", parent=styles["Normal"], fontSize=16, alignment=TA_CENTER, spaceAfter=2)))
story.append(Paragraph("Informe", ParagraphStyle(name="CoverInforme", parent=styles["Normal"], fontSize=13, alignment=TA_CENTER, spaceAfter=4)))
story.append(Paragraph("Modelo espacial de cobertura hospitalaria — Indiana (IN)",
                        ParagraphStyle(name="Subtitle2", parent=styles["Normal"], fontSize=11, alignment=TA_CENTER, textColor=colors.HexColor("#2d6a4f"), spaceAfter=30)))

story.append(Paragraph("Leonardo Dufrey Mejía Mejía", caratula_center))
story.append(Paragraph("María José Girón Isidro", caratula_center))
story.append(Spacer(1, 0.6 * inch))

story.append(Paragraph(f'Repositorio de GitHub: <link href="{GITHUB_URL}">{GITHUB_URL}</link>',
                        ParagraphStyle(name="GHLink", parent=styles["Normal"], fontSize=10.5, alignment=TA_CENTER, textColor=colors.HexColor("#1a73e8"), spaceAfter=20)))

story.append(Paragraph("6 de octubre de 2026", caratula_center))

story.append(PageBreak())

# ---------- NOTA SOBRE USO DE IA ----------
story.append(Paragraph("Nota sobre uso de IA generativa", styles["H1"]))
story.append(Paragraph(
    "Este laboratorio se desarrolló con apoyo extensivo de Claude Code (Anthropic), usado como asistente "
    "de programación dentro de un entorno Docker con GeoPandas y OSMnx, siguiendo la instrucción del "
    "enunciado de documentar su uso. El prompt inicial fue pedirle que leyera el enunciado del laboratorio "
    "y los datos provistos en Canvas, y que implementara cada task en un notebook de Jupyter, ejecutando "
    "el código real contra los datos reales (no solo generando código sin probar) y verificando cada "
    "resultado antes de continuar con el siguiente task. Este prompt funcionó bien porque forzó una "
    "verificación empírica constante: en vez de aceptar código generado a ciegas, cada tabla, mapa y "
    "número que aparece en este documento fue efectivamente calculado ejecutando el notebook contra los "
    "cuatro archivos de datos, lo que permitió detectar y corregir sobre la marcha columnas con nombres "
    "distintos a los esperados, tipos de datos inconsistentes, y errores de sintaxis. "
    "Para el Task 3.1 se le pidió adicionalmente diagnosticar por qué OSMnx no lograba conectarse a la "
    "API de Overpass, lo que llevó a una investigación de red (pruebas con curl, con suplantación de "
    "huella de navegador, y verificación independiente del estado del servicio) documentada en el propio "
    "notebook. Para el Task 3.2 se le pidió buscar en la web un paper académico real publicado entre 2022 "
    "y 2026 sobre accesibilidad espacial a servicios de salud y citarlo en formato APA verificando los "
    "datos bibliográficos contra Crossref antes de usarlos.",
    styles["Body"]))

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

cell_style = ParagraphStyle(name="CellBody", parent=styles["Normal"], fontSize=8.5, leading=11, alignment=TA_CENTER)
cell_header_style = ParagraphStyle(name="CellHeader", parent=styles["Normal"], fontSize=9, leading=11, alignment=TA_CENTER, textColor=colors.white, fontName="Helvetica-Bold")

def simple_table(headers, rows, col_widths=None):
    header_cells = [Paragraph(str(h), cell_header_style) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), cell_style) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d6a4f")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
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
