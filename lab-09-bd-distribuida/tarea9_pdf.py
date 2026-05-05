from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted,
    HRFlowable, Image, Table, TableStyle
)

# ── Colores ───────────────────────────────────────────────────────────────────
BLUE   = colors.HexColor("#1565C0")
DGRAY  = colors.HexColor("#424242")
LGRAY  = colors.HexColor("#BDBDBD")
CODEBG = colors.HexColor("#F5F5F5")
BLACK  = colors.HexColor("#212121")
MGRAY  = colors.HexColor("#757575")

PAGE_W = A4[0] - 5 * cm

# ── Estilos ───────────────────────────────────────────────────────────────────
def build_styles():
    s_body = ParagraphStyle("body",
        fontName="Helvetica", fontSize=10.5,
        leading=16, textColor=BLACK,
        spaceAfter=8, alignment=TA_JUSTIFY)
    s_h1 = ParagraphStyle("h1",
        fontName="Helvetica-Bold", fontSize=17,
        textColor=BLUE, spaceBefore=6, spaceAfter=0, leading=22)
    s_h2 = ParagraphStyle("h2",
        fontName="Helvetica-Bold", fontSize=13,
        textColor=DGRAY, spaceBefore=14, spaceAfter=4)
    s_caption = ParagraphStyle("caption",
        fontName="Helvetica-Oblique", fontSize=9,
        textColor=MGRAY, spaceBefore=3, spaceAfter=10,
        alignment=TA_CENTER)
    s_footer = ParagraphStyle("footer",
        fontName="Helvetica", fontSize=8,
        textColor=LGRAY, alignment=TA_CENTER)
    return s_body, s_h1, s_h2, s_caption, s_footer

def sp(n):
    return Spacer(1, n)

def hr():
    return HRFlowable(width="100%", thickness=0.4,
                      color=LGRAY, spaceAfter=6, spaceBefore=4)

def h1_block(text, s_h1):
    p = Paragraph(text, s_h1)
    t = Table([[p]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0,0), (-1,-1), 1, BLUE),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
    ]))
    return t

def code(lines, font_size=8.2):
    text = "\n".join(lines)
    pre = Preformatted(text, ParagraphStyle("code",
        fontName="Courier", fontSize=font_size,
        leading=13, textColor=BLACK))
    t = Table([[pre]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CODEBG),
        ("BOX",           (0,0), (-1,-1), 0.5, LGRAY),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t

def img(path, width_cm=14, s_caption=None, caption_text=""):
    from PIL import Image as PILImage
    items = []
    try:
        orig = PILImage.open(path)
        orig_w, orig_h = orig.size
        w = width_cm * cm
        h = w * orig_h / orig_w
        im = Image(path, width=w, height=h)
        im.hAlign = "CENTER"
        items.append(im)
    except Exception:
        items.append(Paragraph(f"[Imagen no encontrada: {path}]",
                               ParagraphStyle("err", textColor=colors.red, fontSize=9)))
    if caption_text and s_caption:
        items.append(Paragraph(caption_text, s_caption))
    return items


def build_pdf(output_path):
    s_body, s_h1, s_h2, s_caption, s_footer = build_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm,  bottomMargin=2.5*cm,
    )

    story = []

    # ── Cabecera ──────────────────────────────────────────────────────────────
    story.append(h1_block("Tarea 9 — Simulación de base de datos distribuida y fragmentación", s_h1))
    story.append(sp(4))
    story.append(Paragraph(
        "Jhoan Camilo Arango Ortiz &nbsp;·&nbsp; 2º ASIR online &nbsp;·&nbsp; "
        "Administración de Sistemas Gestores de Bases de Datos", s_body))
    story.append(sp(14))

    # ── 1. Introducción ───────────────────────────────────────────────────────
    story.append(Paragraph("1. Introducción", s_h2))
    story.append(Paragraph(
        "Una base de datos distribuida es aquella cuyos datos se reparten físicamente entre "
        "varios nodos o servidores, aunque el sistema se gestione de forma lógicamente "
        "centralizada. En esta tarea se simula ese escenario dentro de un único servidor "
        "MySQL, usando distintas bases de datos para representar nodos independientes. "
        "Se trabajan dos tipos de fragmentación: horizontal, que divide las filas de una "
        "tabla entre nodos según algún criterio (en este caso, la ciudad de la sede), y "
        "vertical, que separa las columnas de una misma entidad en tablas distintas para "
        "aislar datos sensibles o de acceso menos frecuente.", s_body))
    story.append(sp(8))

    # ── 2. Fragmentación horizontal ───────────────────────────────────────────
    story.append(Paragraph("2. Fragmentación horizontal", s_h2))
    story.append(Paragraph(
        "Se crean dos bases de datos independientes — <b>empresa_madrid</b> y "
        "<b>empresa_barcelona</b> — que simulan los nodos de cada sede. Ambas contienen "
        "una tabla <b>empleados</b> con la misma estructura pero filas distintas, "
        "de modo que cada nodo almacena únicamente los registros que le corresponden "
        "geográficamente.", s_body))
    story.append(sp(4))

    story.append(Paragraph("Nodo Madrid — creación e inserción de datos:", s_h2))
    story.append(code([
        "CREATE DATABASE empresa_madrid;",
        "USE empresa_madrid;",
        "",
        "CREATE TABLE empleados (",
        "    id        INT PRIMARY KEY,",
        "    nombre    VARCHAR(100),",
        "    puesto    VARCHAR(100),",
        "    salario   DECIMAL(8,2),",
        "    ciudad    VARCHAR(50)",
        ");",
        "",
        "INSERT INTO empleados VALUES",
        "(1, 'Ana García',    'Desarrolladora',  2800.00, 'Madrid'),",
        "(2, 'Luis Martínez', 'Administrador',   2200.00, 'Madrid'),",
        "(3, 'Sara López',    'Analista',        3100.00, 'Madrid');",
    ]))
    story.append(sp(8))
    story += img("capturas/captura_01_empresa_madrid.png", 14, s_caption,
                 "Creación de empresa_madrid y carga de los tres empleados del nodo Madrid.")
    story.append(sp(8))

    story.append(Paragraph("Nodo Barcelona — creación e inserción de datos:", s_h2))
    story.append(code([
        "CREATE DATABASE empresa_barcelona;",
        "USE empresa_barcelona;",
        "",
        "CREATE TABLE empleados (",
        "    id        INT PRIMARY KEY,",
        "    nombre    VARCHAR(100),",
        "    puesto    VARCHAR(100),",
        "    salario   DECIMAL(8,2),",
        "    ciudad    VARCHAR(50)",
        ");",
        "",
        "INSERT INTO empleados VALUES",
        "(4, 'Marc Puig',     'Diseñador',       2600.00, 'Barcelona'),",
        "(5, 'Núria Soler',   'Project Manager', 3400.00, 'Barcelona'),",
        "(6, 'Jordi Vidal',   'Soporte',         2100.00, 'Barcelona');",
    ]))
    story.append(sp(8))
    story += img("capturas/captura_02_empresa_barcelona.png", 14, s_caption,
                 "Creación de empresa_barcelona y carga de los tres empleados del nodo Barcelona.")
    story.append(sp(8))

    # ── 3. Consulta UNION ─────────────────────────────────────────────────────
    story.append(Paragraph("3. Reconstrucción horizontal mediante UNION ALL", s_h2))
    story.append(Paragraph(
        "Para obtener el listado completo de empleados de la empresa se combinan ambas "
        "bases de datos con <b>UNION ALL</b>, que concatena los resultados sin eliminar "
        "duplicados (en este caso no los hay, ya que los IDs son disjuntos). "
        "La cláusula <b>ORDER BY id</b> garantiza un resultado ordenado y legible.", s_body))
    story.append(sp(4))
    story.append(code([
        "SELECT id, nombre, puesto, salario, ciudad",
        "FROM empresa_madrid.empleados",
        "UNION ALL",
        "SELECT id, nombre, puesto, salario, ciudad",
        "FROM empresa_barcelona.empleados",
        "ORDER BY id;",
    ]))
    story.append(sp(8))
    story += img("capturas/captura_03_union_horizontal.png", 14, s_caption,
                 "Resultado de la consulta UNION ALL: los seis empleados de ambos nodos ordenados por ID.")
    story.append(sp(8))

    # ── 4. Fragmentación vertical ─────────────────────────────────────────────
    story.append(Paragraph("4. Fragmentación vertical", s_h2))
    story.append(Paragraph(
        "La fragmentación vertical divide los atributos de una entidad entre tablas "
        "distintas, manteniendo la misma clave primaria para poder reconstruirla. "
        "En <b>empresa_vertical</b> se separan los datos de contacto personal "
        "(<b>empleados_personal</b>) de los datos laborales y salariales "
        "(<b>empleados_salario</b>). Esta estrategia es habitual cuando hay que "
        "restringir el acceso a información sensible — por ejemplo, que el departamento "
        "de soporte pueda ver nombre y teléfono sin acceder a los salarios.", s_body))
    story.append(sp(4))
    story.append(code([
        "CREATE DATABASE empresa_vertical;",
        "USE empresa_vertical;",
        "",
        "CREATE TABLE empleados_personal (",
        "    id        INT PRIMARY KEY,",
        "    nombre    VARCHAR(100),",
        "    email     VARCHAR(150),",
        "    telefono  VARCHAR(20)",
        ");",
        "",
        "CREATE TABLE empleados_salario (",
        "    id           INT PRIMARY KEY,",
        "    puesto       VARCHAR(100),",
        "    salario      DECIMAL(8,2),",
        "    departamento VARCHAR(80)",
        ");",
        "",
        "INSERT INTO empleados_personal VALUES",
        "(1, 'Ana García',    'ana.garcia@empresa.com',    '600111222'),",
        "(2, 'Luis Martínez', 'luis.martinez@empresa.com', '600333444'),",
        "(3, 'Sara López',    'sara.lopez@empresa.com',    '600555666');",
        "",
        "INSERT INTO empleados_salario VALUES",
        "(1, 'Desarrolladora', 2800.00, 'Tecnología'),",
        "(2, 'Administrador',  2200.00, 'Sistemas'),",
        "(3, 'Analista',       3100.00, 'Tecnología');",
    ]))
    story.append(sp(8))
    story += img("capturas/captura_04_empresa_vertical.png", 14, s_caption,
                 "Creación de las dos tablas fragmentadas verticalmente y carga de datos coherentes.")
    story.append(sp(8))

    # ── 5. Consulta JOIN ──────────────────────────────────────────────────────
    story.append(Paragraph("5. Reconstrucción vertical mediante JOIN", s_h2))
    story.append(Paragraph(
        "La operación <b>JOIN</b> sobre el campo <b>id</b> reconstituye la ficha "
        "completa de cada empleado a partir de sus fragmentos. El resultado incluye "
        "nombre, email, teléfono, puesto, salario y departamento en una única fila, "
        "como si los datos nunca hubieran estado separados.", s_body))
    story.append(sp(4))
    story.append(code([
        "SELECT",
        "    p.id,",
        "    p.nombre,",
        "    p.email,",
        "    p.telefono,",
        "    s.puesto,",
        "    s.salario,",
        "    s.departamento",
        "FROM empleados_personal  p",
        "JOIN empleados_salario   s ON p.id = s.id",
        "ORDER BY p.id;",
    ]))
    story.append(sp(8))
    story += img("capturas/captura_05_join_vertical.png", 14, s_caption,
                 "Resultado del JOIN: ficha completa de cada empleado reconstruida desde las dos tablas.")
    story.append(sp(8))

    # ── 6. Preguntas teóricas ─────────────────────────────────────────────────
    story.append(Paragraph("6. Preguntas teóricas", s_h2))

    story.append(Paragraph("¿Qué ventajas tiene la fragmentación?", s_h2))
    story.append(Paragraph(
        "Distribuir los datos entre nodos mejora el rendimiento porque cada servidor "
        "gestiona un subconjunto más pequeño y manejable. Las consultas que solo "
        "afectan a un nodo (por ejemplo, listar los empleados de Madrid) no necesitan "
        "acceder al resto, lo que reduce la carga de red y el tiempo de respuesta. "
        "Además, si un nodo cae, los datos del resto siguen accesibles, lo que aumenta "
        "la disponibilidad del sistema. La fragmentación vertical añade una ventaja "
        "adicional: permite controlar el acceso a columnas sensibles de forma "
        "granular, asignando permisos distintos a cada tabla sin necesidad de vistas "
        "o columnas cifradas.", s_body))
    story.append(sp(4))

    story.append(Paragraph("¿Qué problemas puede generar?", s_h2))
    story.append(Paragraph(
        "El principal inconveniente es la complejidad añadida al recuperar datos "
        "completos: cualquier consulta que necesite información de varios nodos "
        "requiere operaciones de tipo UNION o JOIN entre bases de datos, que son "
        "más costosas que una consulta local. Mantener la coherencia entre fragmentos "
        "también es un reto — si un registro se actualiza en un nodo pero no en "
        "otro, aparecen inconsistencias difíciles de detectar. Por otro lado, "
        "la gestión administrativa se complica: hay que monitorizar varios servidores, "
        "diseñar estrategias de backup coordinadas y asegurarse de que todos los "
        "nodos apliquen el mismo esquema cuando hay cambios estructurales. "
        "En entornos reales, estos problemas se abordan con middlewares de bases de "
        "datos distribuidas, pero añaden una capa de infraestructura que no siempre "
        "está justificada para sistemas pequeños.", s_body))
    story.append(sp(16))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(hr())
    story.append(Paragraph(
        "Tarea 9 — BD Distribuida y Fragmentación &nbsp;·&nbsp; "
        "Administración de SGBD &nbsp;·&nbsp; 2º ASIR online &nbsp;·&nbsp; Mayo 2025",
        s_footer))

    doc.build(story)
    print("PDF generado correctamente.")


if __name__ == "__main__":
    import os
    os.makedirs("capturas", exist_ok=True)
    build_pdf("tarea9_bd_distribuida.pdf")
