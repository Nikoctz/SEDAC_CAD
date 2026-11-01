import os
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

pptx = Path(r"C:\Users\nicol\OneDrive\Documentos\SEDAC_CAD\06_DOCUMENTACION\Soporte\Iteraciones\Pitch_SEDAC_20261101_R9\Output\SEDAC_Visual_Pitch_EN_90s_R9.pptx")
ns = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

with zipfile.ZipFile(pptx, "r") as z:
    files = {i.filename: (i, z.read(i.filename)) for i in z.infolist()}
presentation_text = files["ppt/presentation.xml"][1].decode("utf-8")
rels = ET.fromstring(files["ppt/_rels/presentation.xml.rels"][1])
relmap = {x.attrib["Id"]: x.attrib["Target"] for x in rels}
id_chunks = re.findall(r"<p:sldId\b[^>]*/>", presentation_text)
if len(id_chunks) != 10:
    raise RuntimeError(f"Expected 10 slide references, got {len(id_chunks)}")

def relationship_id(chunk):
    m = re.search(r'\br:id="([^"]+)"', chunk)
    if not m:
        raise RuntimeError("Slide reference missing relationship id")
    return m.group(1)

def part_for(chunk):
    target = relmap[relationship_id(chunk)]
    if target.startswith("/"):
        return target.lstrip("/")
    if target.startswith("../"):
        return target[3:]
    return "ppt/" + target

def slide_text(chunk):
    root = ET.fromstring(files[part_for(chunk)][1])
    return " ".join(t.text or "" for t in root.findall(".//a:t", ns))

texts = [(c, slide_text(c)) for c in id_chunks]
sensor = [c for c, t in texts if "COMPARE THE" in t and "MOVEMENT." in t]
status = [c for c, t in texts if "CURRENT STATUS" in t]
if len(sensor) != 1 or len(status) != 1:
    raise RuntimeError("Could not uniquely identify the sensor and current-status slides")
sensor_ref, status_ref = sensor[0], status[0]
id_chunks.remove(sensor_ref)
id_chunks.insert(id_chunks.index(status_ref) + 1, sensor_ref)

start = presentation_text.index("<p:sldIdLst>")
end = presentation_text.index("</p:sldIdLst>", start) + len("</p:sldIdLst>")
new_list = "<p:sldIdLst>" + "".join(id_chunks) + "</p:sldIdLst>"
presentation_text = presentation_text[:start] + new_list + presentation_text[end:]
files["ppt/presentation.xml"] = (files["ppt/presentation.xml"][0], presentation_text.encode("utf-8"))

hidden = {c for c in id_chunks if re.search(r'\bshow="0"', c)}
for chunk in id_chunks:
    if chunk in hidden:
        continue
    part = part_for(chunk)
    info, data = files[part]
    xml = data.decode("utf-8")
    xml = re.sub(r"<p:transition\b.*?</p:transition>", "", xml, flags=re.S)
    transition = '<p:transition advClick="1" spd="med"><p:fade/></p:transition>'
    if "</p:clrMapOvr>" in xml:
        xml = xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + transition, 1)
    elif "</p:cSld>" in xml:
        xml = xml.replace("</p:cSld>", "</p:cSld>" + transition, 1)
    else:
        raise RuntimeError(f"Missing slide insertion point: {part}")
    files[part] = (info, xml.encode("utf-8"))

tmp = pptx.with_name(pptx.stem + ".tmp.pptx")
with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for name, (info, data) in files.items():
        z.writestr(info, data)
os.replace(tmp, pptx)

with zipfile.ZipFile(pptx, "r") as z:
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    relmap = {x.attrib["Id"]: x.attrib["Target"] for x in rels}
    result = []
    for pos, item in enumerate(pres.findall(".//p:sldId", ns), 1):
        rid = item.attrib["{" + ns["r"] + "}id"]
        target = relmap[rid]
        part = target.lstrip("/") if target.startswith("/") else (target[3:] if target.startswith("../") else "ppt/" + target)
        root = ET.fromstring(z.read(part))
        text = " ".join(t.text or "" for t in root.findall(".//a:t", ns))
        tr = root.find("p:transition", ns)
        result.append({"position":pos,"part":part,"hidden":item.attrib.get("show")=="0","click_fade":tr is not None and tr.attrib.get("advClick")=="1" and tr.find("p:fade",ns) is not None,"title_text":text[:75]})
    if sum(not x["hidden"] for x in result) != 10:
        raise RuntimeError("Unexpected visible slide count")
    if not all(x["click_fade"] for x in result if not x["hidden"]):
        raise RuntimeError("A visible slide is missing click-to-Fade")
    sensor_pos = next(x["position"] for x in result if "COMPARE THE" in x["title_text"])
    status_pos = next(x["position"] for x in result if "CURRENT STATUS" in x["title_text"])
    if sensor_pos != status_pos + 1:
        raise RuntimeError("Sensor slide was not placed after current status")
print({"visible":10,"sensor_position":sensor_pos,"sequence":result})
