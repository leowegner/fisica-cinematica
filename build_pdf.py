"""
Genera examen_cinematica.pdf usando reportlab.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import (
    Drawing, Line, PolyLine, String, Rect, Circle, Polygon
)


# ---------- Page numbers ----------
def add_page_chrome(canv, doc):
    canv.saveState()
    canv.setFont("Times-Italic", 8.5)
    canv.setFillColor(HexColor("#6c757d"))
    # Top right
    canv.drawRightString(A4[0] - 2*cm, A4[1] - 1.2*cm,
                         "Cinemática · 1º Bachillerato")
    # Bottom center
    canv.drawCentredString(A4[0]/2, 1.2*cm,
                           f"Página {doc.page}")
    canv.restoreState()


# ---------- Styles ----------
styles = getSampleStyleSheet()

C_PRIMARY = HexColor("#1864ab")
C_RED     = HexColor("#c92a2a")
C_GREY_BG = HexColor("#f1f3f5")
C_YELLOW_BG = HexColor("#fff9db")
C_YELLOW_BORDER = HexColor("#fab005")
C_TAG_T_BG = HexColor("#d0ebff")
C_TAG_T_FG = HexColor("#1864ab")
C_TAG_P_BG = HexColor("#d3f9d8")
C_TAG_P_FG = HexColor("#2b8a3e")
C_BORDER = HexColor("#adb5bd")
C_DARK = HexColor("#212529")
C_MUTED = HexColor("#495057")

title_style = ParagraphStyle(
    "title", parent=styles["Title"],
    fontName="Times-Bold", fontSize=22, leading=26,
    textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=4,
)
subtitle_style = ParagraphStyle(
    "subtitle", parent=styles["Normal"],
    fontName="Times-Italic", fontSize=11, leading=14,
    textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=14,
)
problem_style = ParagraphStyle(
    "problem", parent=styles["Heading2"],
    fontName="Times-Bold", fontSize=14, leading=18,
    textColor=C_RED, alignment=TA_LEFT,
    spaceBefore=14, spaceAfter=6,
)
instr_style = ParagraphStyle(
    "instr", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=10.5, leading=14,
    textColor=C_DARK, alignment=TA_JUSTIFY,
)
context_style = ParagraphStyle(
    "context", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=10.5, leading=14,
    textColor=C_DARK, alignment=TA_JUSTIFY,
)
body_style = ParagraphStyle(
    "body", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=11, leading=15,
    textColor=C_DARK, alignment=TA_JUSTIFY,
)
sub_style = ParagraphStyle(
    "sub", parent=body_style,
    leftIndent=18, bulletIndent=4, spaceAfter=8,
)
footer_note_style = ParagraphStyle(
    "footer_note", parent=styles["Normal"],
    fontName="Times-Italic", fontSize=9.5, leading=12,
    textColor=C_MUTED, alignment=TA_CENTER, spaceBefore=16,
)


def tag(kind):
    """Return inline HTML for a TEORÍA/PRÁCTICA tag."""
    if kind == "T":
        return (f'<font name="Helvetica-Bold" size="8.5" color="#1864ab" '
                f'backColor="#d0ebff">&nbsp;TEORÍA&nbsp;</font>')
    else:
        return (f'<font name="Helvetica-Bold" size="8.5" color="#2b8a3e" '
                f'backColor="#d3f9d8">&nbsp;PRÁCTICA&nbsp;</font>')


def pts(text="1 punto"):
    return f'<font name="Times-Italic" size="9.5" color="#6c757d">  ({text})</font>'


def vec(letter):
    """Render a vector with an overarrow approximation."""
    return f'<b>{letter}</b><super><font size="7">→</font></super>'


# ---------- Build document ----------
doc = SimpleDocTemplate(
    "examen_cinematica.pdf",
    pagesize=A4,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    leftMargin=2*cm, rightMargin=2*cm,
    title="Examen de Cinemática",
    author="Física · 1º Bachillerato",
)

flow = []

# Title block
flow.append(Paragraph("Examen de Cinemática", title_style))
flow.append(HRFlowable(width="100%", thickness=1.4, color=C_PRIMARY,
                       spaceBefore=0, spaceAfter=4))
flow.append(Paragraph("Física · 1º de Bachillerato", subtitle_style))

# Meta table (name, date, grade)
meta_data = [[
    Paragraph("<b>Nombre y apellidos:</b> _______________________________",
              ParagraphStyle("m", fontName="Times-Roman", fontSize=10, leading=13)),
    Paragraph("<b>Fecha:</b> __________",
              ParagraphStyle("m", fontName="Times-Roman", fontSize=10, leading=13)),
    Paragraph("<b>Nota:</b> ____ / 15",
              ParagraphStyle("m", fontName="Times-Roman", fontSize=10, leading=13)),
]]
meta_table = Table(meta_data, colWidths=[9.0*cm, 3.6*cm, 4.4*cm])
meta_table.setStyle(TableStyle([
    ("BOX",        (0,0), (-1,-1), 0.5, C_BORDER),
    ("INNERGRID",  (0,0), (-1,-1), 0.5, C_BORDER),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",(0,0), (-1,-1), 6),
    ("RIGHTPADDING",(0,0),(-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
flow.append(meta_table)
flow.append(Spacer(1, 10))

# Instructions box
instr_text = (
    "<b><font color='#1864ab'>Instrucciones.</font></b> El examen consta de "
    "<b>3 problemas</b>, cada uno con <b>5 subapartados</b>. "
    "Cada subapartado vale <b>1 punto</b> (15 en total; la nota final se reescala sobre 10). "
    "Justifica todas las respuestas teóricas y muestra el procedimiento completo "
    "en los apartados de aplicación práctica, indicando claramente las unidades en el "
    "Sistema Internacional. La etiqueta " + tag("T") + " indica preguntas conceptuales y "
    + tag("P") + " indica ejercicios numéricos."
)
instr_table = Table(
    [[Paragraph(instr_text, instr_style)]],
    colWidths=[17.0*cm],
)
instr_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), C_GREY_BG),
    ("LINEBEFORE", (0,0), (0,-1), 3, C_PRIMARY),
    ("LEFTPADDING",(0,0), (-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
]))
flow.append(instr_table)
flow.append(Spacer(1, 14))

# ================== PROBLEMA 1 ==================
flow.append(Paragraph("Problema 1 — Conceptos fundamentales, posición y velocidad",
                      problem_style))
flow.append(HRFlowable(width="100%", thickness=1, color=C_RED,
                       spaceBefore=0, spaceAfter=6))

# Context box (with embedded data table)
p1_intro = Paragraph(
    "<b>Enunciado.</b> Un ciclista circula por una pista. Su posición a lo largo de un eje "
    "recto viene dada por las siguientes mediciones, tomadas con un sistema de referencia "
    "fijo en la línea de salida:",
    context_style
)

data_tbl = Table(
    [
        ["t (s)", "0", "2", "5", "8", "12"],
        ["x (m)", "0", "10", "28", "52", "96"],
    ],
    colWidths=[2.0*cm] + [1.6*cm]*5,
)
data_tbl.setStyle(TableStyle([
    ("BOX",         (0,0), (-1,-1), 0.5, C_BORDER),
    ("INNERGRID",   (0,0), (-1,-1), 0.5, C_BORDER),
    ("BACKGROUND",  (0,0), (0,-1),  HexColor("#e9ecef")),
    ("FONTNAME",    (0,0), (0,-1),  "Times-Bold"),
    ("FONTNAME",    (1,0), (-1,-1), "Times-Roman"),
    ("FONTSIZE",    (0,0), (-1,-1), 10),
    ("ALIGN",       (0,0), (-1,-1), "CENTER"),
    ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",  (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
]))

p1_outro = Paragraph(
    "Más adelante, el ciclista entra en una <b>curva de radio R = 20 m</b> manteniendo "
    "el módulo de la velocidad alcanzada en el instante <i>t</i> = 12 s.",
    context_style
)

context1 = Table(
    [[p1_intro], [data_tbl], [p1_outro]],
    colWidths=[17.0*cm],
)
context1.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), C_YELLOW_BG),
    ("BOX",        (0,0), (-1,-1), 0.7, C_YELLOW_BORDER),
    ("LEFTPADDING",(0,0), (-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ("ALIGN",      (0,0), (-1,-1), "CENTER"),
]))
flow.append(context1)
flow.append(Spacer(1, 10))

# Subapartados Problema 1
p1_items = [
    (
        "T",
        "Enumera y define brevemente los <b>tres elementos fundamentales</b> que "
        "necesitamos para estudiar el movimiento de un cuerpo. Justifica además, "
        "con un ejemplo cotidiano, la afirmación: <i>«no existe el movimiento "
        "absoluto, sólo el relativo»</i>."
    ),
    (
        "T",
        "Define con precisión los conceptos de <b>vector de posición " + vec("r") + "</b>, "
        "<b>desplazamiento " + vec("ΔL") + "</b> y <b>espacio recorrido (s)</b>. "
        "Explica, mediante un dibujo esquemático, en qué caso particular el módulo "
        "del desplazamiento coincide con el espacio recorrido y por qué."
    ),
    (
        "P",
        "A partir de la tabla, calcula la <b>velocidad media</b> del ciclista en los "
        "siguientes intervalos: "
        "<b>(a)</b> entre <i>t</i> = 0 s y <i>t</i> = 5 s; "
        "<b>(b)</b> entre <i>t</i> = 5 s y <i>t</i> = 12 s; "
        "<b>(c)</b> en el intervalo total (0–12 s). "
        "Expresa los resultados en m/s y en km/h."
    ),
    (
        "P",
        "Razona si el movimiento del ciclista entre 0 s y 12 s puede considerarse "
        "uniforme. ¿Es la <b>velocidad media</b> del intervalo total igual a la "
        "<b>media aritmética</b> de las velocidades medias de los apartados (a) y (b)? "
        "Explica matemáticamente por qué."
    ),
    (
        "P",
        "Suponiendo que en <i>t</i> = 12 s el ciclista entra en la curva de radio "
        "<i>R</i> = 20 m manteniendo el módulo de la velocidad media calculada entre "
        "<i>t</i> = 8 s y <i>t</i> = 12 s, calcula el módulo de la <b>aceleración "
        "centrípeta</b>. Indica además su dirección y sentido sobre un esquema."
    ),
]

list_items_1 = []
for kind, html in p1_items:
    para = Paragraph(tag(kind) + pts() + " " + html, body_style)
    list_items_1.append(ListItem(para, leftIndent=18, value=None))

flow.append(ListFlowable(
    list_items_1,
    bulletType="1",
    bulletFormat="%s.",
    bulletFontName="Times-Bold",
    bulletFontSize=11,
    bulletColor=C_PRIMARY,
    leftIndent=22,
    spaceBefore=2,
))

# ================== PROBLEMA 2 ==================
flow.append(Spacer(1, 8))
flow.append(Paragraph("Problema 2 — Aceleración y sus componentes intrínsecas",
                      problem_style))
flow.append(HRFlowable(width="100%", thickness=1, color=C_RED,
                       spaceBefore=0, spaceAfter=6))

p2_text = Paragraph(
    "<b>Enunciado.</b> Un coche entra en una rotonda circular de <b>radio R = 25 m</b>. "
    "En el instante inicial (<i>t</i><sub>0</sub> = 0) lleva una velocidad de módulo "
    "<i>v</i><sub>0</sub> = 10 m/s, y al cabo de <i>t</i> = 5 s su velocidad ha aumentado "
    "uniformemente hasta <i>v</i> = 20 m/s, conservando el mismo sentido de giro. "
    "Considera el movimiento contenido en un plano horizontal.",
    context_style
)
context2 = Table([[p2_text]], colWidths=[17.0*cm])
context2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), C_YELLOW_BG),
    ("BOX",        (0,0), (-1,-1), 0.7, C_YELLOW_BORDER),
    ("LEFTPADDING",(0,0), (-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
]))
flow.append(context2)
flow.append(Spacer(1, 10))

p2_items = [
    (
        "T",
        "Define el concepto de <b>aceleración</b> como magnitud vectorial. Distingue entre "
        "<b>aceleración media</b> y <b>aceleración instantánea</b>, escribiendo la "
        "expresión matemática correspondiente y explicando el significado físico de cada una."
    ),
    (
        "T",
        "Explica qué son las <b>componentes intrínsecas</b> de la aceleración: "
        "<b>tangencial " + vec("a") + "<sub>t</sub></b> y <b>centrípeta (o normal) "
        + vec("a") + "<sub>c</sub></b>. Indica para cada una su <i>dirección</i>, su "
        "<i>sentido</i> y qué <i>cambio físico</i> en el vector velocidad mide. "
        "Razona por qué en un movimiento rectilíneo uniforme ambas son nulas."
    ),
    (
        "P",
        "Calcula el módulo de la <b>aceleración tangencial</b> del coche durante el "
        "intervalo de 0 a 5 s. Razona, basándote en el sentido de " + vec("a") + "<sub>t</sub> "
        "respecto al de " + vec("v") + ", si el coche está acelerando o frenando."
    ),
    (
        "P",
        "Calcula el módulo de la <b>aceleración centrípeta</b> en los instantes "
        "<i>t</i> = 0 s y <i>t</i> = 5 s. ¿Es constante? Justifica el resultado utilizando "
        "la fórmula <font face='Times-Italic'>a<sub>c</sub> = v² / R</font>."
    ),
    (
        "P",
        "En el instante <i>t</i> = 5 s, dibuja en un esquema la rotonda con el coche, el "
        "vector velocidad " + vec("v") + " y los vectores " + vec("a") + "<sub>t</sub> y "
        + vec("a") + "<sub>c</sub>. Calcula a continuación el <b>módulo de la aceleración "
        "total</b> en ese instante (composición de " + vec("a") + "<sub>t</sub> y "
        + vec("a") + "<sub>c</sub>, que son perpendiculares entre sí) y el <b>ángulo</b> "
        "que dicho vector forma con la dirección de la velocidad."
    ),
]

list_items_2 = []
for kind, html in p2_items:
    para = Paragraph(tag(kind) + pts() + " " + html, body_style)
    list_items_2.append(ListItem(para, leftIndent=18, value=None))

flow.append(ListFlowable(
    list_items_2,
    bulletType="1",
    bulletFormat="%s.",
    bulletFontName="Times-Bold",
    bulletFontSize=11,
    bulletColor=C_PRIMARY,
    leftIndent=22,
    spaceBefore=2,
))

# ================== PROBLEMA 3 ==================
def build_xt_graph():
    """
    Gráfico x(t) por tramos para el Problema 3.

    Tramos:
      A (0–4 s):   x: 0  → 20 m   (MRU, v = +5 m/s)
      B (4–6 s):   x: 20 → 20 m   (reposo)
      C (6–10 s):  x: 20 → 40 m   (MRU, v = +5 m/s)
      D (10–14 s): x: 40 → 10 m   (MRU, v = -7,5 m/s)
    """
    # Plot box dimensions (points)
    W, H = 420, 240          # canvas
    PL, PR, PT, PB = 50, 18, 20, 36   # paddings
    plot_w = W - PL - PR
    plot_h = H - PT - PB

    t_min, t_max = 0, 14
    x_min, x_max = 0, 50

    def sx(t):  # screen x for time
        return PL + (t - t_min) / (t_max - t_min) * plot_w

    def sy(x):  # screen y for position (y axis inverted: bigger x → higher pos)
        return PB + (x - x_min) / (x_max - x_min) * plot_h

    d = Drawing(W, H)

    # ---- Grid ----
    # Vertical gridlines every 2 s
    for t in range(0, 15, 2):
        d.add(Line(sx(t), PB, sx(t), PB + plot_h,
                   strokeColor=HexColor("#e9ecef"), strokeWidth=0.5))
    # Horizontal gridlines every 10 m
    for x in range(0, 51, 10):
        d.add(Line(PL, sy(x), PL + plot_w, sy(x),
                   strokeColor=HexColor("#e9ecef"), strokeWidth=0.5))

    # ---- Axes ----
    d.add(Line(PL, PB, PL + plot_w + 8, PB,
               strokeColor=HexColor("#495057"), strokeWidth=1.2))
    d.add(Line(PL, PB, PL, PB + plot_h + 10,
               strokeColor=HexColor("#495057"), strokeWidth=1.2))
    # Arrow heads
    d.add(Polygon([PL + plot_w + 8, PB,
                   PL + plot_w + 2, PB - 4,
                   PL + plot_w + 2, PB + 4],
                  fillColor=HexColor("#495057"),
                  strokeColor=HexColor("#495057")))
    d.add(Polygon([PL, PB + plot_h + 10,
                   PL - 4, PB + plot_h + 4,
                   PL + 4, PB + plot_h + 4],
                  fillColor=HexColor("#495057"),
                  strokeColor=HexColor("#495057")))

    # ---- Tick labels ----
    # X-axis ticks every 2 s
    for t in range(0, 15, 2):
        d.add(Line(sx(t), PB, sx(t), PB - 4,
                   strokeColor=HexColor("#495057"), strokeWidth=0.8))
        d.add(String(sx(t), PB - 14, str(t),
                     fontName="Times-Roman", fontSize=9,
                     fillColor=HexColor("#212529"), textAnchor="middle"))
    # Y-axis ticks every 10 m
    for x in range(0, 51, 10):
        d.add(Line(PL, sy(x), PL - 4, sy(x),
                   strokeColor=HexColor("#495057"), strokeWidth=0.8))
        d.add(String(PL - 8, sy(x) - 3, str(x),
                     fontName="Times-Roman", fontSize=9,
                     fillColor=HexColor("#212529"), textAnchor="end"))

    # ---- Axis labels ----
    d.add(String(PL + plot_w + 4, PB - 14, "t (s)",
                 fontName="Times-Italic", fontSize=10,
                 fillColor=HexColor("#212529"), textAnchor="start"))
    d.add(String(PL - 30, PB + plot_h + 4, "x (m)",
                 fontName="Times-Italic", fontSize=10,
                 fillColor=HexColor("#212529"), textAnchor="start"))

    # ---- Curve x(t) ----
    pts_curve = [
        (0, 0), (4, 20), (6, 20), (10, 40), (14, 10)
    ]
    poly = []
    for (t, x) in pts_curve:
        poly.extend([sx(t), sy(x)])
    d.add(PolyLine(poly, strokeColor=HexColor("#1864ab"),
                   strokeWidth=2.2))

    # ---- Vertices ----
    for (t, x) in pts_curve:
        d.add(Circle(sx(t), sy(x), 3.2,
                     fillColor=HexColor("#1864ab"),
                     strokeColor=HexColor("#1864ab")))

    # ---- Point labels A,B,C,D,E ----
    labels = [
        ("A", 0, 0,   +6,  +10),
        ("B", 4, 20,  +6,  +8),
        ("C", 6, 20,  +6,  +8),
        ("D", 10, 40, +6,  +8),
        ("E", 14, 10, +6,  +8),
    ]
    for (name, t, x, dx, dy) in labels:
        d.add(String(sx(t) + dx, sy(x) + dy, name,
                     fontName="Times-Bold", fontSize=10,
                     fillColor=HexColor("#c92a2a"), textAnchor="start"))

    return d


flow.append(PageBreak())
flow.append(Paragraph("Problema 3 — Interpretación de un gráfico posición–tiempo",
                      problem_style))
flow.append(HRFlowable(width="100%", thickness=1, color=C_RED,
                       spaceBefore=0, spaceAfter=6))

p3_intro = Paragraph(
    "<b>Enunciado.</b> La siguiente gráfica representa la posición <i>x</i> (en metros) "
    "de un móvil que se desplaza a lo largo de una recta, en función del tiempo "
    "<i>t</i> (en segundos). Los puntos <b>A, B, C, D</b> y <b>E</b> señalan los "
    "instantes en los que cambia el tipo de movimiento.",
    context_style
)

# Centered drawing inside the yellow box
graph_table = Table([[build_xt_graph()]], colWidths=[17.0*cm])
graph_table.setStyle(TableStyle([
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))

context3 = Table(
    [[p3_intro], [graph_table]],
    colWidths=[17.0*cm],
)
context3.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), C_YELLOW_BG),
    ("BOX",        (0,0), (-1,-1), 0.7, C_YELLOW_BORDER),
    ("LEFTPADDING",(0,0), (-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
]))
flow.append(KeepTogether(context3))
flow.append(Spacer(1, 10))

p3_items = [
    (
        "T",
        "Identifica el <b>tipo de movimiento</b> que tiene el móvil en cada uno de los "
        "tramos AB, BC, CD y DE. Justifica tu respuesta a partir de la <i>forma del "
        "gráfico</i> en cada tramo (por ejemplo, qué representa una recta horizontal "
        "o un tramo de pendiente negativa)."
    ),
    (
        "P",
        "Calcula el <b>desplazamiento total</b> " + vec("Δx") + " del móvil entre el "
        "instante inicial (punto A, <i>t</i> = 0 s) y el final (punto E, <i>t</i> = 14 s). "
        "Indica también si el desplazamiento entre A y D es igual al desplazamiento "
        "entre A y E, razonando la respuesta."
    ),
    (
        "P",
        "Calcula el <b>espacio recorrido</b> total <i>s</i> entre A y E. Explica por qué, "
        "en este movimiento, el espacio recorrido <b>no coincide</b> con el módulo "
        "del desplazamiento."
    ),
    (
        "P",
        "Calcula la <b>velocidad media</b> del móvil en los siguientes intervalos: "
        "<b>(a)</b> tramo AB (0–4 s); "
        "<b>(b)</b> tramo DE (10–14 s); "
        "<b>(c)</b> recorrido completo A → E (0–14 s). "
        "Indica el signo de cada valor y qué significa físicamente."
    ),
    (
        "P",
        "Calcula la <b>celeridad media</b> (rapidez media) del móvil en el recorrido "
        "completo A → E, definida como el cociente entre el espacio recorrido y el "
        "tiempo total empleado. Compara este resultado con el del apartado anterior "
        "(velocidad media en A → E) y explica a qué se debe la diferencia."
    ),
]

list_items_3 = []
for kind, html in p3_items:
    para = Paragraph(tag(kind) + pts() + " " + html, body_style)
    list_items_3.append(ListItem(para, leftIndent=18, value=None))

flow.append(ListFlowable(
    list_items_3,
    bulletType="1",
    bulletFormat="%s.",
    bulletFontName="Times-Bold",
    bulletFontSize=11,
    bulletColor=C_PRIMARY,
    leftIndent=22,
    spaceBefore=2,
))

# Footer note
flow.append(Spacer(1, 12))
flow.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER,
                       dash=(2,2), spaceBefore=4, spaceAfter=4))
flow.append(Paragraph(
    "Fin del examen · Revisa todos tus cálculos y las unidades antes de entregar · ¡Mucho ánimo!",
    footer_note_style
))


doc.build(flow, onFirstPage=add_page_chrome, onLaterPages=add_page_chrome)
print("OK: examen_cinematica.pdf generado")
