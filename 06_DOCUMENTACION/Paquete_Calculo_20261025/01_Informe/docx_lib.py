"""
docx_lib.py — escritor minimo de documentos Word (.docx, OOXML) sin dependencias externas.

Soporta: titulo, encabezados, parrafos con formato, vinetas, tablas con fila de encabezado,
saltos de pagina y notas al pie simplificadas como texto entre parentesis.
"""
from pathlib import Path
import zipfile
from xml.sax.saxutils import escape

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def esc(text):
    return escape(str(text))


class Doc:
    def __init__(self):
        self.body = []

    # --- bloques ---
    def para(self, text="", style="Normal", bold=False, size=None, color=None, align=None,
             space_after=120, keep=False):
        runs = []
        for i, chunk in enumerate(str(text).split("\n")):
            if i:
                runs.append("<w:r><w:br/></w:r>")
            props = ""
            if bold:
                props += "<w:b/>"
            if size:
                props += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size * 2, size * 2)
            if color:
                props += '<w:color w:val="%s"/>' % color
            runs.append('<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (props, esc(chunk)))
        # El orden de los hijos de w:pPr lo exige el esquema: pStyle, keepNext, spacing, jc.
        ppr = "<w:pPr>"
        ppr += '<w:pStyle w:val="%s"/>' % style
        if keep:
            ppr += "<w:keepNext/>"
        ppr += '<w:spacing w:after="%d"/>' % space_after
        if align:
            ppr += '<w:jc w:val="%s"/>' % align
        ppr += "</w:pPr>"
        self.body.append("<w:p>%s%s</w:p>" % (ppr, "".join(runs)))

    def heading(self, text, level=1):
        self.para(text, style="Heading%d" % level, space_after=140, keep=True)

    def title(self, text):
        self.para(text, style="Title", space_after=200)

    def bullet(self, text, level=0):
        self.para("• " + text, style="Normal", space_after=60)

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def table(self, rows, widths=None, header=True, font_size=8):
        ncols = max(len(r) for r in rows)
        if widths is None:
            widths = [round(9600 / ncols)] * ncols
        # Normaliza el ancho total al area imprimible (A4 con margenes de 1134 twips = 9638 utiles).
        max_total = 9500
        total = sum(widths)
        if total > max_total:
            factor = max_total / total
            widths = [max(400, int(round(w * factor))) for w in widths]
            total = sum(widths)
        grid = "".join('<w:gridCol w:w="%d"/>' % w for w in widths)
        out = ['<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/>' % total,
               '<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:color="9FB6C6"/>'
               '<w:left w:val="single" w:sz="4" w:color="9FB6C6"/>'
               '<w:bottom w:val="single" w:sz="4" w:color="9FB6C6"/>'
               '<w:right w:val="single" w:sz="4" w:color="9FB6C6"/>'
               '<w:insideH w:val="single" w:sz="4" w:color="C7D5DE"/>'
               '<w:insideV w:val="single" w:sz="4" w:color="C7D5DE"/>'
               '</w:tblBorders>',
               '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="70" w:type="dxa"/>'
               '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tblCellMar>',
               '<w:tblLook w:val="0000" w:firstRow="0" w:lastRow="0" w:firstColumn="0" '
               'w:lastColumn="0" w:noHBand="0" w:noVBand="0"/>',
               '</w:tblPr><w:tblGrid>%s</w:tblGrid>' % grid]
        for r, row in enumerate(rows):
            is_head = header and r == 0
            cells = []
            for c in range(ncols):
                value = row[c] if c < len(row) else ""
                shade = '<w:shd w:val="clear" w:color="auto" w:fill="123B54"/>' if is_head else ""
                color = '<w:color w:val="FFFFFF"/>' if is_head else ""
                runs = []
                for i, chunk in enumerate(str(value).split("\n")):
                    if i:
                        runs.append("<w:r><w:br/></w:r>")
                    runs.append('<w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>%s'
                                '<w:sz w:val="%d"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'
                                % (("<w:b/>" + color) if is_head else "", font_size * 2, esc(chunk)))
                cells.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s'
                             '<w:vAlign w:val="top"/></w:tcPr><w:p><w:pPr><w:spacing w:after="20"/></w:pPr>%s</w:p></w:tc>'
                             % (widths[c], shade, "".join(runs)))
            header_row = '<w:trPr><w:tblHeader/></w:trPr>' if is_head else ""
            out.append("<w:tr>%s%s</w:tr>" % (header_row, "".join(cells)))
        out.append("</w:tbl>")
        self.body.append("".join(out))
        self.para("", space_after=80)

    # --- escritura ---
    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<w:document xmlns:w="%s"><w:body>%s'
                    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                    '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
                    'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>'
                    '</w:body></w:document>' % (W, "".join(self.body)))
        styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                  '<w:styles xmlns:w="%s">'
                  '<w:docDefaults><w:rPrDefault><w:rPr>'
                  '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="20"/></w:rPr></w:rPrDefault>'
                  '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
                  '</w:docDefaults>'
                  '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
                  '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
                  '<w:pPr><w:spacing w:before="240" w:after="200"/></w:pPr>'
                  '<w:rPr><w:b/><w:color w:val="123B54"/><w:sz w:val="40"/></w:rPr></w:style>'
                  '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
                  '<w:pPr><w:keepNext/><w:spacing w:before="320" w:after="140"/>'
                  '<w:pBdr><w:bottom w:val="single" w:sz="6" w:color="123B54"/></w:pBdr></w:pPr>'
                  '<w:rPr><w:b/><w:color w:val="123B54"/><w:sz w:val="30"/></w:rPr></w:style>'
                  '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
                  '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="100"/></w:pPr>'
                  '<w:rPr><w:b/><w:color w:val="1F5673"/><w:sz w:val="24"/></w:rPr></w:style>'
                  '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>'
                  '<w:pPr><w:keepNext/><w:spacing w:before="180" w:after="80"/></w:pPr>'
                  '<w:rPr><w:b/><w:color w:val="2E6C86"/><w:sz w:val="22"/></w:rPr></w:style>'
                  '</w:styles>' % W)
        content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                         '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                         '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                         '<Default Extension="xml" ContentType="application/xml"/>'
                         '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                         '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                         '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
                         '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
                         '</Types>')
        root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                     '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                     '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                     '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                     '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                     '</Relationships>')
        doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                    '</Relationships>')
        core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                'xmlns:dc="http://purl.org/dc/elements/1.1/">'
                '<dc:title>Informe SEDAC: memoria de cálculo y ensayos</dc:title>'
                '<dc:creator>Paquete documental SEDAC 2026-10-25</dc:creator>'
                '<cp:lastModifiedBy>Paquete documental SEDAC</cp:lastModifiedBy>'
                '</cp:coreProperties>')
        app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
               '<Application>OpenCode</Application></Properties>')
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types)
            z.writestr("_rels/.rels", root_rels)
            z.writestr("docProps/core.xml", core)
            z.writestr("docProps/app.xml", app)
            z.writestr("word/document.xml", document)
            z.writestr("word/styles.xml", styles)
            z.writestr("word/_rels/document.xml.rels", doc_rels)
        return path
