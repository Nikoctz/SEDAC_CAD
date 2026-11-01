import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "file:///C:/Users/nicol/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const root = "C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/Soporte/Iteraciones/Pitch_SEDAC_20261101_R10";
const source = path.join(root, "Output/SEDAC_Visual_Pitch_EN_90s_R9.pptx");
const output = path.join(root, "Output/SEDAC_Visual_Pitch_EN_90s_R10_Final5.pptx");
const presentation = await PresentationFile.importPptx(await FileBlob.load(source));

async function readBytes(file) {
  const b = await fs.readFile(file);
  return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
}
function addText(slide, name, text, position, style = {}) {
  const shape = slide.shapes.add({ geometry: "textbox", name, position, fill: "none", line: { style: "solid", fill: "none", width: 0 } });
  shape.text = text;
  shape.text.style = { fontSize: style.fontSize ?? 22, bold: style.bold ?? false, color: style.color ?? "#FFFFFF", alignment: style.alignment ?? "left", typeface: "Arial Narrow" };
  shape.text.insets = 0;
  return shape;
}

const slide = presentation.slides.add();
slide.background.fill = "#0F141B";
const cadPath = path.join(root, "Recursos/P204_VISTA_ESPALDA.png");
const imuPath = path.join(root, "Recursos/IMU_modulo_conceptual.png");
const tempPath = path.join(root, "Recursos/Sonda_temperatura_conceptual.png");
await slide.images.add({ blob: await readBytes(cadPath), contentType: "image/png", alt: "Original P2.04 CAD rear view; unchanged; candidate sensor locations are conceptual", fit: "contain", position: { left: 60, top: 124, width: 740, height: 590 } });

addText(slide, "sensor-map-kicker", "SEDAC · SENSOR INTEGRATION CONCEPT", { left: 62, top: 36, width: 720, height: 28 }, { fontSize: 19, bold: true, color: "#F6B744" });
addText(slide, "sensor-map-title", "WHERE SENSORS COULD GO", { left: 62, top: 68, width: 740, height: 54 }, { fontSize: 40, bold: true });

const imuCard = slide.shapes.add({ geometry: "rect", name: "imu-candidate-card", position: { left: 842, top: 164, width: 470, height: 178 }, fill: "#1B222A", line: { style: "solid", fill: "#46515D", width: 1 } });
const tempCard = slide.shapes.add({ geometry: "rect", name: "temperature-candidate-card", position: { left: 842, top: 383, width: 470, height: 178 }, fill: "#1B222A", line: { style: "solid", fill: "#46515D", width: 1 } });

await slide.images.add({ blob: await readBytes(imuPath), contentType: "image/png", alt: "AI-generated conceptual IMU enclosure, not selected hardware", fit: "contain", position: { left: 855, top: 199, width: 152, height: 105 } });
addText(slide, "imu-label", "IMU · MOVEMENT", { left: 1020, top: 188, width: 270, height: 30 }, { fontSize: 23, bold: true, color: "#FFFFFF" });
addText(slide, "imu-use", "Tracks movement\nand orientation", { left: 1020, top: 224, width: 270, height: 52 }, { fontSize: 20, color: "#D4D9DF" });
addText(slide, "imu-location", "CANDIDATE · UPPER FRAME", { left: 1020, top: 296, width: 275, height: 24 }, { fontSize: 16, bold: true, color: "#F6B744" });

await slide.images.add({ blob: await readBytes(tempPath), contentType: "image/png", alt: "AI-generated conceptual temperature probe, not selected hardware", fit: "contain", position: { left: 855, top: 416, width: 152, height: 105 } });
addText(slide, "temperature-label", "TEMPERATURE", { left: 1020, top: 407, width: 270, height: 30 }, { fontSize: 23, bold: true, color: "#FFFFFF" });
addText(slide, "temperature-use", "Reads local surface\ntemperature", { left: 1020, top: 443, width: 270, height: 52 }, { fontSize: 20, color: "#D4D9DF" });
addText(slide, "temperature-location", "CANDIDATE · BELT CONTACT ZONE", { left: 1020, top: 515, width: 280, height: 24 }, { fontSize: 16, bold: true, color: "#F6B744" });

slide.shapes.add({ geometry: "line", name: "imu-location-arrow-line", position: { left: 480, top: 255, width: 360, height: 0 }, fill: "none", line: { style: "solid", fill: "#F6B744", width: 3 } });
addText(slide, "imu-location-arrow-tip", "◀", { left: 452, top: 243, width: 28, height: 25 }, { fontSize: 24, bold: true, color: "#F6B744" });
slide.shapes.add({ geometry: "line", name: "temperature-location-arrow-line", position: { left: 480, top: 557, width: 360, height: 0 }, fill: "none", line: { style: "solid", fill: "#F6B744", width: 3 } });
addText(slide, "temperature-location-arrow-tip", "◀", { left: 452, top: 545, width: 28, height: 25 }, { fontSize: 24, bold: true, color: "#F6B744" });

addText(slide, "sensor-map-caveat", "CONCEPT ONLY · LOCATIONS TO CONFIRM WITH THE PROFESSOR", { left: 842, top: 596, width: 480, height: 30 }, { fontSize: 17, bold: true, color: "#F6B744" });
addText(slide, "sensor-map-footer", "AI SENSOR VISUALS · P2.04 CAD PRE-DESIGN · NO SENSORS INSTALLED", { left: 62, top: 724, width: 900, height: 22 }, { fontSize: 15, bold: true, color: "#D4D9DF" });
slide.speakerNotes.text = "Concept placement only. The sensor hardware renders were generated for this pitch and are not selected components or detailed designs. The IMU is a candidate at the upper frame to record movement and orientation during the planned comparative test. A temperature probe is shown at the belt contact zone as a future option for local surface temperature only; it does not measure body temperature, comfort, or risk. The candidate locations and the sensor mount must be confirmed with the professor. P2.04 has no sensors installed. The IMU session is planned; no results are available. Do not infer force distribution, ergonomic improvement, safety, or risk prevention from this concept image.";

const png = await presentation.export({ slide, format: "png", scale: 1 });
const preview = path.join(root, "Vista_previa/Mapa_sensores_R10_Final5.png");
await fs.writeFile(preview, new Uint8Array(await png.arrayBuffer()));
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
console.log(JSON.stringify({ output, preview, totalSlides: presentation.slides.items.length, addedSlideId: slide.id }));
