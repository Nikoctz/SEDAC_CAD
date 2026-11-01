import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "file:///C:/Users/nicol/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const root="C:/Users/nicol/OneDrive/Documentos/SEDAC_CAD/06_DOCUMENTACION/Soporte/Iteraciones/Pitch_SEDAC_20261101_R10";
const file=path.join(root,"Output/SEDAC_Visual_Pitch_EN_90s_R10_Final5.pptx");
const deck=await PresentationFile.importPptx(await FileBlob.load(file));
const visible=deck.slides.items.filter(s=>!s.hidden);
if(visible.length!==11) throw new Error("Expected 11 visible slides, got "+visible.length);
for(let i=0;i<visible.length;i++){
  const png=await deck.export({slide:visible[i],format:"png",scale:1});
  const number=String(i+1).padStart(2,"0");
  const out=path.join(root,"Vista_previa/Final_"+number+".png");
  await fs.writeFile(out,new Uint8Array(await png.arrayBuffer()));
}
console.log(JSON.stringify({visible:visible.length,previews:11,imported:true}));
