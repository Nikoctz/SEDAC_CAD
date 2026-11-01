import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "file:///C:/Users/nicol/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const root = "C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/Soporte/Iteraciones/Pitch_SEDAC_20261101_R9";
const source = "C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/Soporte/Iteraciones/Pitch_SEDAC_20261101_R8/Output/SEDAC_Visual_Pitch_EN_90s_R8.pptx";
const output = path.join(root, "Output/SEDAC_Visual_Pitch_EN_90s_R9.pptx");
const presentation = await PresentationFile.importPptx(await FileBlob.load(source));

function shapeNamed(slide, name) {
  const shape = slide.shapes.items.find(item => item.name === name);
  if (!shape) throw new Error(`Missing expected shape: ${name}`);
  return shape;
}

const sensorSlide = presentation.slides.items.find(slide =>
  slide.shapes.items.some(shape => shape.name === "sensor-title")
);
if (!sensorSlide) throw new Error("Could not locate the IMU slide.");

shapeNamed(sensorSlide, "sensor-kicker").text = "SEDAC · IMU TEST PLAN";
shapeNamed(sensorSlide, "sensor-title").text = "COMPARE THE\nMOVEMENT.";
shapeNamed(sensorSlide, "imu-status").text = "PLANNED LAB SESSION · THIS WEEK";
shapeNamed(sensorSlide, "imu-copy").text = "Pump only vs. pump + SEDAC\nSame pump · load · task · conditions";
shapeNamed(sensorSlide, "alert-status").text = "IMU MEASUREMENTS";
shapeNamed(sensorSlide, "alert-copy").text = "Movement · orientation · sway";
shapeNamed(sensorSlide, "sensor-limits").text = "IMUs do not measure force · results pending\nFuture risk alerts need design and testing.";
sensorSlide.speakerNotes.text = "This week, a professor is lending us the lab for a planned IMU session. We plan to compare the pump alone with the same pump plus SEDAC, keeping the pump, load, task, and conditions the same. The sensor mounting, attachment, calibration, and protocol must be agreed with the professor before measuring. IMUs record movement, orientation, and oscillation (sway); they do not measure force or pressure. Results are pending, and this planned session is not a completed validation. Sensor alerts for possible risk conditions are a future product goal. Alert rules and any effect on risk still need to be designed and tested. The P2.04 image is CAD pre-design and has no sensors installed.";

const preview = await presentation.export({ slide: sensorSlide, format: "png", scale: 1 });
const previewPath = path.join(root, "Vista_previa/Diapositiva_IMU_R9.png");
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
console.log(JSON.stringify({ output, preview: previewPath, slideCount: presentation.slides.items.length }));
