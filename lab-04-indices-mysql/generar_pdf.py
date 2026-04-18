from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted,
    HRFlowable, Image, Table, TableStyle
)

BLUE   = colors.HexColor("#1565C0")
DGRAY  = colors.HexColor("#424242")
LGRAY  = colors.HexColor("#BDBDBD")
CODEBG = colors.HexColor("#F5F5F5")
BLACK  = colors.HexColor("#212121")
MGRAY  = colors.HexColor("#757575")

def build_styles():
    s_body = ParagraphStyle("body",
        fontName="Helvetica", fontSize=10.5,
        leading=16, textColor=BLACK,
        spaceAfter=8, alignment=TA_JUSTIFY)
    s_h1 = ParagraphStyle("h1",
        fontName="Helvetica-Bold", fontSize=17,
        textColor=BLUE, spaceBefore=6, spaceAfter=2)
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

def code(lines, font_size=8.5):
    text = "\n".join(lines)
    pre = Preformatted(text, ParagraphStyle("code",
        fontName="Courier", fontSize=font_size,
        leading=13, textColor=BLACK))
    t = Table([[pre]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CODEBG),
        ("BOX",        (0,0), (-1,-1), 0.5, LGRAY),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t

def img(path, width_cm=14):
    try:
        im = Image(path, width=width_cm*cm)
        im.hAlign = "CENTER"
        return im
    except Exception:
        return Paragraph(f"[Imagen no encontrada: {path}]",
                         ParagraphStyle("err", textColor=colors.red, fontSize=9))

def main():
    s_body, s_h1, s_h2, s_caption, s_footer = build_styles()

    doc = SimpleDocTemplate(
        "Tarea7_Indices_MySQL.pdf",
        pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm,  bottomMargin=2.5*cm,
    )

    story = []

    # Cabecera
    story += [
        Paragraph("Tarea 7 — Creación y análisis de índices en MySQL", s_h1),
        HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=4, spaceBefore=2),
        Paragraph("Jhoan Camilo Arango Ortiz &nbsp;·&nbsp; 2º ASIR online", s_body),
        sp(16),
    ]

    # 1. Creación del entorno
    story += [
        Paragraph("1. Creación del entorno de trabajo", s_h2),
        Paragraph(
            "Se ha creado la base de datos <b>empresa_indices</b> y dentro de ella una tabla "
            "llamada <b>empleados</b> con los campos id (clave primaria), nombre, departamento y salario. "
            "A continuación se insertaron 10 registros con datos variados repartidos entre los "
            "departamentos IT, RRHH, Contabilidad y Marketing.",
            s_body),
        sp(6),
        code([
            "CREATE DATABASE empresa_indices;",
            "USE empresa_indices;",
            "",
            "CREATE TABLE empleados (",
            "    id INT AUTO_INCREMENT PRIMARY KEY,",
            "    nombre VARCHAR(100),",
            "    departamento VARCHAR(50),",
            "    salario DECIMAL(8,2)",
            ");",
            "",
            "INSERT INTO empleados (nombre, departamento, salario) VALUES",
            "('Ana Garcia', 'IT', 2500.00),",
            "('Carlos Lopez', 'RRHH', 1800.00),",
            "('Maria Martinez', 'IT', 3200.00),",
            "('Pedro Sanchez', 'Contabilidad', 2100.00),",
            "('Laura Fernandez', 'IT', 2800.00),",
            "('Jorge Ruiz', 'RRHH', 1950.00),",
            "('Sofia Torres', 'Contabilidad', 2300.00),",
            "('Andres Molina', 'IT', 1750.00),",
            "('Elena Castro', 'Marketing', 2200.00),",
            "('Raul Herrera', 'Marketing', 2600.00);",
        ]),
        sp(10),
    ]

    # 2. Análisis sin índices
    story += [
        Paragraph("2. Análisis sin índices", s_h2),
        Paragraph(
            "Antes de crear ningún índice se ejecutó la consulta de filtrado por departamento "
            "para obtener los empleados del departamento IT. La consulta devolvió 4 registros correctamente.",
            s_body),
        sp(6),
        code(["SELECT * FROM empleados WHERE departamento = 'IT';"]),
        sp(8),
        img("capturas/captura_01_select_sin_indice.png"),
        Paragraph("Resultado de la consulta sin índice: 4 empleados del departamento IT.", s_caption),
        sp(8),
        Paragraph(
            "A continuación se analizó la consulta con <b>EXPLAIN</b>. El resultado mostró un "
            "<b>Table scan</b> sobre la tabla completa, lo que indica que MySQL recorrió las 10 filas "
            "una a una para encontrar las que cumplían el filtro. No se utilizó ningún índice. "
            "El coste estimado fue de 1.25 y las filas analizadas 10.",
            s_body),
        sp(6),
        code(["EXPLAIN SELECT * FROM empleados WHERE departamento = 'IT';"]),
        sp(8),
        img("capturas/captura_02_explain_sin_indice.png"),
        Paragraph("EXPLAIN sin índice: Table scan sobre las 10 filas de la tabla.", s_caption),
        sp(10),
    ]

    # 3. Creación del índice
    story += [
        Paragraph("3. Creación de índice sobre departamento", s_h2),
        Paragraph(
            "Se creó un índice simple sobre la columna <b>departamento</b> con el nombre "
            "<b>idx_departamento</b>. Este índice permite a MySQL localizar directamente "
            "las filas que coinciden con un valor concreto de departamento, sin necesidad "
            "de recorrer la tabla completa.",
            s_body),
        sp(6),
        code(["CREATE INDEX idx_departamento ON empleados(departamento);"]),
        sp(10),
    ]

    # 4. Análisis con índice
    story += [
        Paragraph("4. Análisis con índice", s_h2),
        Paragraph(
            "Tras crear el índice se volvió a ejecutar el mismo EXPLAIN. El resultado cambió "
            "radicalmente: en lugar de un Table scan, MySQL realizó un <b>Index lookup</b> "
            "usando <b>idx_departamento</b>. El número de filas estimadas bajó de 10 a 4 y "
            "el coste se redujo de 1.25 a 0.9. MySQL ya no recorre toda la tabla sino que "
            "va directamente a las entradas del índice que corresponden al departamento IT.",
            s_body),
        sp(6),
        img("capturas/captura_03_explain_con_indice.png"),
        Paragraph("EXPLAIN con índice: Index lookup con coste 0.9 sobre 4 filas.", s_caption),
        sp(10),
    ]

    # 5. Índice compuesto
    story += [
        Paragraph("5. Índice compuesto (departamento + salario)", s_h2),
        Paragraph(
            "Se creó un índice compuesto sobre las columnas <b>departamento</b> y <b>salario</b>. "
            "Este tipo de índice es útil cuando las consultas filtran habitualmente por ambas "
            "columnas a la vez, ya que permite descartar filas usando los dos criterios "
            "directamente desde el índice.",
            s_body),
        sp(6),
        code(["CREATE INDEX idx_dep_sal ON empleados(departamento, salario);"]),
        sp(8),
        Paragraph(
            "Se ejecutó la consulta con doble filtro y se analizó con EXPLAIN. MySQL usó "
            "<b>idx_departamento</b> para el filtro de departamento y aplicó el filtro de "
            "salario como paso adicional. Con una tabla de solo 10 registros el optimizador "
            "considera suficiente el índice simple, pero el coste bajó aún más hasta 0.633 "
            "y las filas estimadas a 1.33, lo que demuestra que el índice compuesto aporta "
            "información adicional al planificador de consultas. En tablas de gran volumen "
            "el índice compuesto sería seleccionado directamente.",
            s_body),
        sp(6),
        code([
            "SELECT * FROM empleados",
            "WHERE departamento = 'IT' AND salario > 2000;",
        ]),
        sp(8),
        img("capturas/captura_04_explain_indice_compuesto.png"),
        Paragraph("EXPLAIN con índice compuesto: coste 0.633, filtro aplicado sobre 4 filas del índice.", s_caption),
        sp(10),
    ]

    # 6. Reflexión final
    story += [
        Paragraph("6. Reflexión final", s_h2),

        Paragraph("<b>¿Para qué sirven los índices?</b>", s_body),
        Paragraph(
            "Los índices sirven para que MySQL localice los datos sin tener que escanear "
            "toda la tabla. Funcionan de forma similar al índice de un libro: en lugar de "
            "leer todas las páginas para encontrar un término, el índice apunta directamente "
            "a la posición correcta.",
            s_body),
        sp(4),

        Paragraph("<b>¿En qué casos mejoran el rendimiento?</b>", s_body),
        Paragraph(
            "Los índices son especialmente útiles en tablas con un volumen alto de registros "
            "y en columnas que se usan frecuentemente en cláusulas WHERE, JOIN u ORDER BY. "
            "A pequeña escala la mejora es marginal, pero en tablas con miles o millones de "
            "filas la diferencia en tiempo de respuesta es muy significativa.",
            s_body),
        sp(4),

        Paragraph("<b>¿En qué casos pueden perjudicarlo?</b>", s_body),
        Paragraph(
            "Los índices ocupan espacio en disco adicional y tienen un coste de mantenimiento: "
            "cada vez que se inserta, modifica o elimina un registro, MySQL tiene que actualizar "
            "también todos los índices de esa tabla. En tablas con operaciones de escritura muy "
            "frecuentes, tener demasiados índices puede ralentizar esas operaciones más de lo "
            "que mejoran las consultas de lectura.",
            s_body),
        sp(10),
    ]

    # Footer
    story += [
        hr(),
        Paragraph(
            "Tarea 7 — Índices en MySQL &nbsp;·&nbsp; Gestión de Bases de Datos "
            "&nbsp;·&nbsp; 2º ASIR online &nbsp;·&nbsp; Abril 2025",
            s_footer),
    ]

    doc.build(story)
    print("PDF generado: Tarea7_Indices_MySQL.pdf")

if __name__ == "__main__":
    main()
