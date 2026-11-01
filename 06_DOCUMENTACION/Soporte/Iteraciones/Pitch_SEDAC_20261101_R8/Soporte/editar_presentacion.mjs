import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "file:///C:/Users/nicol/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const root = "C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/Soporte/Iteraciones/Pitch_SEDAC_20261101_R8";
const source = "C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/Soporte/Iteraciones/Pitch_SEDAC_20261101_R8/Soporte/Base_SEDAC_R7.pptx";
const output = path.join(root, "Output/SEDAC_Visual_Pitch_EN_90s_R8.pptx");
const presentation = await PresentationFile.importPptx(await FileBlob.load(source));

async function readBytes(file) {
  const b = await fs.readFile(file);
  return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
}
function addText(slide, name, text, position, style) {
  const s = slide.shapes.add({geometry:"textbox", name, position, fill:"none", line:{style:"solid", fill:"none", width:0}});
  s.text = text;
  s.text.style = {fontSize:style.fontSize, bold:style.bold??false, color:style.color??"#FFFFFF", alignment:"left", typeface:"Arial Narrow"};
  s.text.insets = 0;
  return s;
}

const sensors = presentation.slides.add();
sensors.background.fill = "#0F141B";
const cad = await readBytes(path.join(root,"Recursos/P204_VISTA_ESPALDA.png"));
sensors.images.add({blob:cad,contentType:"image/png",alt:"Original P2.04 CAD rear view; no sensors are installed in this pre-design",fit:"contain",position:{left:720,top:34,width:620,height:690}});
addText(sensors,"sensor-kicker","SEDAC · FUTURE SENSING",{left:70,top:66,width:580,height:34},{fontSize:21,bold:true,color:"#F6B744"});
addText(sensors,"sensor-title","MEASURE NOW.\nALERT NEXT.",{left:70,top:116,width:600,height:154},{fontSize:54,bold:true});
sensors.shapes.add({geometry:"rect",name:"sensor-title-accent",position:{left:72,top:286,width:88,height:5},fill:"#F6B744",line:{style:"solid",fill:"none",width:0}});
addText(sensors,"imu-status","THIS WEEK · PLANNED LAB SESSION",{left:72,top:324,width:590,height:32},{fontSize:20,bold:true,color:"#F6B744"});
addText(sensors,"imu-copy","IMU measurements\nMovement and orientation",{left:72,top:364,width:590,height:76},{fontSize:29,bold:true});
addText(sensors,"alert-status","FUTURE PRODUCT GOAL",{left:72,top:486,width:590,height:30},{fontSize:20,bold:true,color:"#F6B744"});
addText(sensors,"alert-copy","Sensor alerts for\ndefined risk conditions",{left:72,top:523,width:590,height:72},{fontSize:27,bold:true});
addText(sensors,"sensor-limits","IMUs track movement, not force.\nAlert rules and risk reduction still need testing.",{left:72,top:624,width:590,height:58},{fontSize:18,color:"#D4D9DF"});
addText(sensors,"cad-caption","P2.04 CAD PRE-DESIGN · SENSORS NOT INSTALLED",{left:744,top:718,width:590,height:28},{fontSize:15,bold:true,color:"#D4D9DF"});
sensors.speakerNotes.text="A professor is lending us the lab this week, and we plan to take IMU measurements. An IMU tracks movement and orientation; it does not measure force. Our future product goal is to add sensors and alerts for defined risk conditions. The alert rules and any risk reduction still need to be designed and tested. P2.04 remains a CAD pre-design, and the planned session is not a completed validation.";

const png=await presentation.export({slide:sensors,format:"png",scale:1});
await fs.writeFile(path.join(root,"Vista_previa/Diapositiva_Sensores.png"),new Uint8Array(await png.arrayBuffer()));
const pptx=await PresentationFile.exportPptx(presentation);
await pptx.save(output);
console.log(JSON.stringify({output,slideCount:presentation.slides.items.length,visibleSlideCount:presentation.slides.items.filter(s=>!s.hidden).length,sensorSlideId:sensors.id}));

