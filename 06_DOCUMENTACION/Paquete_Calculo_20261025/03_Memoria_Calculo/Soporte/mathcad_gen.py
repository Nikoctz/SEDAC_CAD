"""
mathcad_gen.py — generador de hojas de trabajo Mathcad en formato clasico XMCD.

Porta el generador ya validado del proyecto SEDAC (06_DOCUMENTACION/Memoria_Calculo_P2_03/Soporte
y 01_CAD/Prototipo_P2/P2_03_20261016/Soporte/mathcad_base.py) a la biblioteca estandar
xml.etree.ElementTree, porque en este equipo no esta disponible lxml.

No modifica nada del repositorio SEDAC_CAD: solo lee la plantilla que trae la propia
instalacion de Mathcad 15 y escribe el .xmcd en la carpeta de salida indicada.

Formato: XMCD clasico (worksheet30 / math30). La aplicacion instalada bajo Mathcad 15 se
identifica por automatizacion como 14.1.4.587 y abre estos archivos.
"""
from pathlib import Path
from copy import deepcopy
import ast
import math
import xml.etree.ElementTree as ET

MATHCAD_DIR = Path(r"C:\Program Files (x86)\Mathcad\Mathcad 15")
TEMPLATE = MATHCAD_DIR / "Resource Center/EN/qsheet/about_qs.xmcd"

W = "http://schemas.mathsoft.com/worksheet30"
M = "http://schemas.mathsoft.com/math30"
U = "http://schemas.mathsoft.com/units10"
P = "http://schemas.mathsoft.com/provenance10"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
XMLNS = "http://www.w3.org/XML/1998/namespace"

for prefix, uri in (("", W), ("ml", M), ("ws", W), ("u", U), ("p", P), ("xsi", XSI)):
    ET.register_namespace(prefix, uri)


def q(tag):
    return "{" + M + "}" + tag


def w(tag):
    return "{" + W + "}" + tag


def _ident(name):
    e = ET.Element(q("id"))
    e.set("{" + XMLNS + "}space", "preserve")
    e.text = "π" if name == "pi" else name
    return e


_PREC = {ast.Add: 10, ast.Sub: 10, ast.Mult: 20, ast.Div: 20, ast.Pow: 30}
_OP = {ast.Add: "plus", ast.Sub: "minus", ast.Mult: "mult", ast.Div: "div", ast.Pow: "pow"}


def _tree(node):
    if isinstance(node, ast.Constant):
        tag = "str" if isinstance(node.value, str) else "real"
        e = ET.Element(q(tag))
        e.text = str(node.value)
        return e
    if isinstance(node, ast.Name):
        return _ident(node.id)
    if isinstance(node, ast.BinOp):
        e = ET.Element(q("apply"))
        ET.SubElement(e, q(_OP[type(node.op)]))
        for side, child in (("left", node.left), ("right", node.right)):
            ce = _tree(child)
            if isinstance(child, ast.BinOp):
                need = (
                    _PREC[type(child.op)] < _PREC[type(node.op)]
                    or (side == "right" and isinstance(node.op, ast.Sub) and _PREC[type(child.op)] == 10)
                    or (isinstance(node.op, ast.Pow) and side == "left")
                )
                if need:
                    pe = ET.Element(q("parens"))
                    pe.append(ce)
                    ce = pe
            e.append(ce)
        return e
    if isinstance(node, ast.BoolOp):
        op = "and" if isinstance(node.op, ast.And) else "or"
        acc = _tree(node.values[-1])
        for value in reversed(node.values[:-1]):
            e = ET.Element(q("apply"))
            ET.SubElement(e, q(op))
            e.append(_tree(value))
            e.append(acc)
            acc = e
        return acc
    if isinstance(node, ast.UnaryOp):
        e = ET.Element(q("apply"))
        ET.SubElement(e, q("neg"))
        e.append(_tree(node.operand))
        return e
    if isinstance(node, ast.Call):
        e = ET.Element(q("apply"))
        if node.func.id in ("sqrt", "abs"):
            ET.SubElement(e, q("sqrt" if node.func.id == "sqrt" else "absval"))
            e.append(_tree(node.args[0]))
            return e
        e.append(_ident(node.func.id))
        if len(node.args) > 1:
            seq = ET.SubElement(e, q("sequence"))
            for a in node.args:
                seq.append(_tree(a))
        else:
            e.append(_tree(node.args[0]))
        return e
    if isinstance(node, ast.Compare):
        e = ET.Element(q("apply"))
        ET.SubElement(e, q({ast.GtE: "greaterOrEqual", ast.LtE: "lessOrEqual",
                             ast.Gt: "greaterThan", ast.Lt: "lessThan"}[type(node.ops[0])]))
        e.append(_tree(node.left))
        e.append(_tree(node.comparators[0]))
        return e
    if isinstance(node, ast.Subscript):
        e = ET.Element(q("apply"))
        ET.SubElement(e, q("index"))
        e.append(_tree(node.value))
        e.append(_tree(node.slice))
        return e
    raise TypeError(ast.dump(node))


def expr(source):
    """Expresion matematica en sintaxis Python -> arbol MathML de Mathcad."""
    return _tree(ast.parse(source, mode="eval").body)


class Worksheet:
    """Hoja de trabajo XMCD con regions de texto, definiciones, funciones y evals."""

    PAGE_H = 757.89

    def __init__(self, title, description, generator="SEDAC - paquete memoria 2026-10-25"):
        self.records = []
        self.inputs = {}
        self.values = {}
        self.units = {}
        self.pages = []
        self.env = {"mm": 0.001, "m": 1, "s": 1, "kg": 1, "N": 1, "MPa": 1e6, "Pa": 1, "pi": math.pi}
        self.env.update(sqrt=math.sqrt, max=max, min=min, abs=abs, floor=math.floor,
                        ceil=math.ceil, round=round, sign=lambda x: (x > 0) - (x < 0),
                        sin=math.sin, cos=math.cos, tan=math.tan, atan=math.atan,
                        ln=math.log, log=math.log10, exp=math.exp)
        self._page = -1
        self._y = 0

        template = ET.parse(str(TEMPLATE)).getroot()
        settings = deepcopy(template.find(w("settings")))
        for x in settings.findall(".//" + w("textStyle")):
            for e in x.findall(".//" + w("inlineAttr")):
                e.set("font-family", "Arial")
                e.set("font-size", "10")
        for e in settings.findall(".//" + w("mathStyle")):
            e.set("font-size", "10")
        pg = settings.find(".//" + w("pageModel"))
        pg.set("paper-code", "9")
        pg.set("page-width", "595.276")
        pg.set("page-height", "841.89")
        pg.set("print-single-page-width", "true")
        mar = pg.find(w("margins"))
        for a in ("left", "right", "top", "bottom"):
            mar.set(a, "42")
        pg.set("show-page-frame", "true")
        lang = settings.find(".//" + w("language"))
        if lang is not None:
            lang.set("math", "EN")
        gen = settings.find(".//" + w("general"))
        if gen is not None:
            gen.set("precision", "4")
        fmt = settings.find(".//" + w("fileFormat"))
        if fmt is not None:
            fmt.set("save-numeric-results", "true")
            fmt.set("save-text-images", "true")

        root = ET.Element(w("worksheet"), {"version": "3.0.3"})
        meta = ET.SubElement(root, w("metadata"))
        ET.SubElement(meta, w("generator")).text = generator
        ud = ET.SubElement(meta, w("userData"))
        ET.SubElement(ud, w("title")).text = title
        ET.SubElement(ud, w("description")).text = description
        root.append(settings)
        self.root = root
        self.regions = ET.SubElement(root, w("regions"))

    # --- infraestructura de regions -------------------------------------
    def _reg(self, tag, height=30, left=16, width=490, color="inherit"):
        rid = len(self.records) + 1
        top = self._page * self.PAGE_H + self._y
        e = ET.SubElement(self.regions, w("region"), {
            "region-id": str(rid), "left": str(left), "top": ("%.2f" % top),
            "width": str(width), "height": str(height),
            "align-x": str(left), "align-y": ("%.2f" % (top + height * 0.65)),
            "show-border": "false", "show-highlight": ("true" if color != "inherit" else "false"),
            "is-protected": "false", "z-order": "0", "background-color": color, "tag": tag})
        self.records.append(dict(id=rid, page=self._page + 1, y=self._y, height=height,
                                 left=left, width=width, tag=tag))
        return e

    def _math(self, parent):
        return ET.SubElement(parent, w("math"), {"optimize": "false", "disable-calc": "false"})

    # --- contenido -------------------------------------------------------
    def txt(self, text, size=10, bold=False, color="#253746", height=None):
        import textwrap
        lines = []
        for chunk in text.split("\n"):
            lines += textwrap.wrap(chunk, 92 if size <= 10 else 70, break_long_words=False) or [""]
        ht = height or (len(lines) * (size + 3) + 6)
        e = self._reg("texto", ht)
        tx = ET.SubElement(e, w("text"), {"use-page-width": "false", "push-down": "false", "lock-width": "true"})
        for line in lines:
            pp = ET.SubElement(tx, w("p"), {"style": "Normal"})
            f = ET.SubElement(pp, w("f"), {"family": "Arial", "charset": "0", "size": str(size)})
            if bold:
                f = ET.SubElement(f, w("b"))
            c = ET.SubElement(f, w("c"), {"val": color})
            c.text = line
        self.records[-1].update(kind="text", text=text)
        self._y += ht + 6

    def page(self, title, subtitle="", header="SEDAC / P2.04-P2.05 / MC01"):
        self._page += 1
        self._y = 16
        self.pages.append(title)
        self.txt(header, 9, True, "#687A88", 20)
        self.txt(title, 14, True, "#123B54", 28)
        if subtitle:
            self.txt(subtitle, 9, color="#687A88")

    def gap(self, n=8):
        self._y += n

    def define(self, name, source, unit="", height=48, wide=False, input=False, note=""):
        """Define una variable: name := source. 'input=True' la marca como entrada editable."""
        top = self._y
        e = self._reg(name, height, 16, 490 if wide else 330,
                      "#F0F6FC" if input else "inherit")
        de = ET.SubElement(self._math(e), q("define"))
        de.append(_ident(name))
        de.append(expr(source))
        try:
            value = self.calc(source)
        except Exception:
            value = None
        self.env[name] = value
        self.values[name] = value
        self.units[name] = unit
        self.records[-1].update(kind="define", name=name, expression=source, unit=unit,
                                value=value, input=input, note=note)
        if input:
            self.inputs[name] = source
        if not wide:
            self.output(name, unit, y=top, height=height)
        self._y = top + height + 4
        if wide:
            self.output(name, unit, left=20, y=self._y)
            self._y += 35

    def output(self, name, unit="", left=355, y=None, height=34):
        old = self._y
        if y is not None:
            self._y = y
        e = self._reg("eval_" + name, height, left, 150)
        ev = ET.SubElement(self._math(e), q("eval"))
        ev.append(_ident(name))
        if unit:
            un = ET.SubElement(ev, q("unitOverride"))
            un.append(expr(unit))
        self.records[-1].update(kind="eval", name=name, unit=unit)
        self._y = old

    def fun(self, name, args, source, height=56):
        e = self._reg(name, height)
        de = ET.SubElement(self._math(e), q("define"))
        fn = ET.SubElement(de, q("function"))
        fn.append(_ident(name))
        bv = ET.SubElement(fn, q("boundVars"))
        for a in args:
            ET.SubElement(bv, q("id")).text = a
        de.append(expr(source))
        self.records[-1].update(kind="function", name=name, args=args, expression=source)

        def _fn(*values, _s=source, _a=args):
            local = dict(self.env)
            local.update(dict(zip(_a, values)))
            return eval(compile(ast.parse(_s, mode="eval"), "<function>", "eval"),
                        {"__builtins__": {}}, local)

        self.env[name] = _fn
        self._y += height + 5

    # --- calculo de control (unidades SI) --------------------------------
    def calc(self, source):
        return eval(compile(ast.parse(source, mode="eval"), "<equation>", "eval"),
                    {"__builtins__": {}}, dict(self.env))

    def evaluate_all(self):
        """Recalcula las definiciones en orden, para el control numerico en Python."""
        for rec in self.records:
            if rec.get("kind") == "define":
                try:
                    value = self.calc(rec["expression"])
                except Exception:
                    value = None
                self.env[rec["name"]] = value
                self.values[rec["name"]] = value
                rec["value"] = value
        return self.values

    # --- escritura -------------------------------------------------------
    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tree = ET.ElementTree(self.root)
        tree.write(str(path), encoding="utf-8", xml_declaration=True)
        return path

    def manifest(self):
        return dict(regions=len(self.records), pages=len(self.pages),
                    defines=sum(1 for r in self.records if r.get("kind") == "define"),
                    functions=sum(1 for r in self.records if r.get("kind") == "function"),
                    evals=sum(1 for r in self.records if r.get("kind") == "eval"),
                    inputs=len(self.inputs), page_titles=list(self.pages))
