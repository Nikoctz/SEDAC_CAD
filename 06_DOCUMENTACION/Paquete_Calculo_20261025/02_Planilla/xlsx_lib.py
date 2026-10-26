"""
xlsx_lib.py — escritor minimo de libros de Excel (.xlsx, OOXML) sin dependencias externas.

Soporta: varias hojas, cadenas en linea, numeros, formulas, estilos basicos (negrita, relleno,
ajuste de texto, anchos de columna, panel congelado) y una hoja de estilos con formato de fecha.
Se valida abriendo el libro con Excel y comprobando que no se repara.
"""
from pathlib import Path
import zipfile
from xml.sax.saxutils import escape

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="1"><numFmt numFmtId="164" formatCode="dd/mm/yyyy"/></numFmts>
<fonts count="3">
<font><sz val="10"/><name val="Calibri"/></font>
<font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><color rgb="FF123B54"/><name val="Calibri"/></font>
</fonts>
<fills count="4">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF123B54"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFF0F6FC"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="2">
<border><left/><right/><top/><bottom/><diagonal/></border>
<border><left style="thin"><color rgb="FFB8C6D1"/></left><right style="thin"><color rgb="FFB8C6D1"/></right><top style="thin"><color rgb="FFB8C6D1"/></top><bottom style="thin"><color rgb="FFB8C6D1"/></bottom><diagonal/></border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="7">
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"><alignment vertical="center"/></xf>
<xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""

STYLE_NORMAL = 0
STYLE_HEADER = 1
STYLE_TITLE = 2
STYLE_INPUT = 3
STYLE_DATE = 4
STYLE_CALC = 5


def col_letter(index):
    letters = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


class Sheet:
    def __init__(self, name, widths=None, freeze=None):
        self.name = name
        self.rows = []
        self.widths = widths or []
        self.freeze = freeze

    def add_row(self, cells):
        """cells: lista de (valor, estilo) o valores simples."""
        row = []
        for cell in cells:
            if isinstance(cell, tuple):
                value, style = cell
            else:
                value, style = cell, STYLE_NORMAL
            row.append((value, style))
        self.rows.append(row)
        return self

    def blank(self, n=1):
        for _ in range(n):
            self.rows.append([])
        return self


def _cell_xml(ref, value, style):
    if value is None:
        return ""
    if isinstance(value, str) and value.startswith("="):
        return '<c r="%s" s="%d"><f>%s</f></c>' % (ref, style, escape(value[1:]))
    if isinstance(value, bool):
        value = "VERDADERO" if value else "FALSO"
        return '<c r="%s" s="%d" t="inlineStr"><is><t>%s</t></is></c>' % (ref, style, escape(value))
    if isinstance(value, (int, float)):
        return '<c r="%s" s="%d"><v>%s</v></c>' % (ref, style, repr(value))
    return '<c r="%s" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (
        ref, style, escape(str(value)))


def _sheet_xml(sheet):
    parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">']
    if sheet.freeze:
        parts.append('<sheetViews><sheetView workbookViewId="0"><pane ySplit="%d" topLeftCell="A%d" '
                     'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>' % (sheet.freeze, sheet.freeze + 1))
    if sheet.widths:
        parts.append("<cols>")
        for i, width in enumerate(sheet.widths):
            parts.append('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (i + 1, i + 1, width))
        parts.append("</cols>")
    parts.append("<sheetData>")
    for r, row in enumerate(sheet.rows, start=1):
        if not row:
            continue
        cells = []
        for c, (value, style) in enumerate(row):
            cells.append(_cell_xml("%s%d" % (col_letter(c), r), value, style))
        parts.append('<row r="%d">%s</row>' % (r, "".join(cells)))
    parts.append("</sheetData></worksheet>")
    return "".join(parts)


def write_xlsx(path, sheets):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = len(sheets)
    content_types = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
                     '<Default Extension="xml" ContentType="application/xml"/>',
                     '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
                     '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
                     '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
                     '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>']
    for i in range(1, n + 1):
        content_types.append('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % i)
    content_types.append("</Types>")

    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                 '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                 '</Relationships>')

    workbook = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
                "<sheets>"]
    for i, sheet in enumerate(sheets, start=1):
        workbook.append('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (escape(sheet.name), i, i))
    workbook.append("</sheets></workbook>")

    wb_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i in range(1, n + 1):
        wb_rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i, i))
    wb_rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' % (n + 1))
    wb_rels.append("</Relationships>")

    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>Planilla de captura y seguimiento SEDAC</dc:title>'
            '<dc:creator>Paquete documental SEDAC 2026-10-25</dc:creator>'
            '<cp:lastModifiedBy>Paquete documental SEDAC</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-10-25T00:00:00Z</dcterms:created>'
            '</cp:coreProperties>')

    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Application>OpenCode</Application></Properties>')

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(content_types))
        z.writestr("_rels/.rels", root_rels)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("xl/workbook.xml", "".join(workbook))
        z.writestr("xl/_rels/workbook.xml.rels", "".join(wb_rels))
        z.writestr("xl/styles.xml", STYLES)
        for i, sheet in enumerate(sheets, start=1):
            z.writestr("xl/worksheets/sheet%d.xml" % i, _sheet_xml(sheet))
    return path
