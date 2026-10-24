"""Redacta el informe a partir de los resultados de auditar_coherencia.py."""
import collections
import json
from pathlib import Path


def crear_informe(r,out,root,base,audit,gen,calc,param,hist,old):
    md=[]
    def p(s=''): md.extend([s,''])
    def fmt(v):
        if v is None:return 'sin correspondencia geométrica demostrada'
        return json.dumps(v,ensure_ascii=False) if not isinstance(v,str) else v
    def cell(v):return fmt(v).replace('|',' / ').replace('\n','<br>')
    def table(headers,rows):
        md.append('| '+' | '.join(headers)+' |')
        md.append('| '+' | '.join('---' for _ in headers)+' |')
        md.extend('| '+' | '.join(cell(v) for v in row)+' |' for row in rows)
        md.append('')
    def link(path,label=None,line=None):
        return '['+(label or path.name)+((':'+str(line)) if line else '')+'](<'+path.as_posix()+((':'+str(line)) if line else '')+'>)'
    def source(path,frag):
        n=next(i for i,s in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1) if frag in s)
        return link(path,path.name,n)
    def refs(items,path):
        return ', '.join(link(path,str(n),n) for n in sorted({v['linea'] for v in items})) or 'sin referencia directa'
    def resultfile(name):return link(out/name)
    counts=collections.Counter(x['estado_generador'] for x in r['cobertura'])
    d=r['bloque_D']
    p('# Auditoría de coherencia de P2.05 — 22/10/2026')
    p('**hecho — alcance:** lectura de fuentes, análisis AST y regeneración de descripciones JSON/CSV. No se ejecutó Inventor ni el cálculo; no se repitieron el banco de cierre ni la invariancia numérica del encargo anterior. No se adoptan decisiones técnicas ni correcciones.')
    p('## Respuesta a la pregunta del encargo')
    p('**hecho:** no toda dimensión o hipótesis sale de PARAMETROS_P2_05.json. Tampoco todo campo geométrico declarado controla directamente una cota del modelo. Hay campos exclusivos del cálculo, datos de presupuesto, literales declarados como fijos y conexiones parciales. Leer un campo y copiar el JSON completo dentro del manifiesto no demuestra que controle toda la geometría relacionada.')
    p('**hecho:** la regeneración actual coincide byte por byte con MODELO_API.json y BOM_FIJACIONES.csv de Nueva_20261019_060807. Esa coincidencia comprueba reproducibilidad de la descripción actual; no comprueba que cambiar un parámetro propague correctamente todas las dependencias, ni valida un sólido nativo.')
    p('**hecho:** se registran 13 hallazgos: 10 [I] informativos y 3 [C] a conservar, con severidad propuesta. No apareció una diferencia de regeneración que motive un nuevo [B] en este alcance. La aceptación nativa y física sigue pendiente; este resultado no autoriza una corrida de Inventor ni el cierre de P2.05.')
    p('## Método, fuentes y etiquetas')
    p('**hecho:** se leyó el contexto obligatorio del repositorio en el orden de AGENTS.md: CONTEXTO_SEDAC.md, ESTADO_ACTUAL.md, DECISIONES.md y CHANGELOG_SEDAC.md. Se usaron como fuentes de esta auditoría los archivos de la tabla; sus huellas de esta ejecución quedan en RESULTADOS.json → fuentes_sha256.')
    table(['Fuente leída','SHA-256 durante la auditoría'],[(link(root/rel,rel),sha) for rel,sha in r['fuentes_sha256'].items()])
    p('**hecho — método A:** recorrido recursivo del JSON, incluidos contenedores y elementos de listas; resolución de alias P/G/C/M y accesos por subíndice/get en AST. Además se trazaron lecturas en memoria con los mismos valores y sin ejecutar escrituras en ese tramo. Su manifiesto resultante coincide con el del generador original ejecutado después. No se hicieron perturbaciones de parámetros.')
    p('**hecho — método B:** inventario de todos los literales numéricos, comentarios y textos con cifras; clasificación automática por contexto, con revisión semántica de los grupos de interés en la tabla B. Las coincidencias numéricas del CSV son candidatos; la igualdad numérica por sí sola no prueba duplicación semántica. Los coeficientes de fórmula, índices, colores, alternativas de comparación, salidas y funciones no invocadas se separan de dimensiones e hipótesis efectivas.')
    p('**cálculo — método C:** extracción de contornos y profundidades de operaciones del JSON histórico y regenerado; diferencias geométricas simples identificadas en la tabla C. Se comparan descripciones y nominales, no mediciones de sólidos. Los mínimos de estudio no se presentan como tolerancias medidas.')
    p('**hecho — método D:** ejecución del generador original, en Python disponible y bajo PowerShell '+r['entorno']['powershell']+', con salida nueva dentro de esta auditoría. Se compararon árboles completos, filas CSV y bytes. Registro: '+resultfile('REGISTRO_GENERACION.json')+'. La ejecución final mediante ejecutar_auditoria.ps1 conserva también el proceso real y versión en REGISTRO_ENTORNO_POWERSHELL.json; las exploraciones anteriores registran 7.6.5 y no se presentan como ejecuciones de Windows PowerShell 5.1.')
    p('**hecho — etiquetas:** hecho = archivo/lectura/comando; cálculo = derivación identificada; supuesto = valor adoptado sin medir; hipótesis = condición física no comprobada. Las propuestas son pendientes, no decisiones adoptadas. Se normaliza el estado escrito como «no_leido Dale mas» en el encargo a no_leido_declarado. Se conserva sin_procultad como la etiqueta pedida para ausencia de origen geométrico verificable; no significa que el literal no tenga ubicación en el código.')
    p('## A. Parámetros → generador')
    p('**hecho:** '+str(len(r['cobertura']))+' nodos declarados, de los cuales '+str(sum(x['tipo']=='hoja' for x in r['cobertura']))+' son hojas (se cuenta una lista vacía como hoja). Estados de todos los nodos: '+fmt(dict(counts))+'. Ninguno se declara obsoleto solo por no leerse. La tabla completa con valores, notas, expresiones y referencias del cálculo está en '+resultfile('CAMPOS_PARAMETROS.csv')+'.')
    table(['Campo (contenedores incluidos)','Tipo','Estado AST del generador','Leído en control actual','Evidencia generador'],[(x['campo'],x['tipo'],x['estado_generador'],'sí' if x['leido_en_control'] else 'no',refs(x['referencias_generador'],gen)) for x in r['cobertura']])
    p('### Cruce con la revisión histórica y la declaración 10+4')
    p('**hecho:** '+source(root/'06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md','ancho_panel')+' enumera nueve campos geométricos antes no leídos. Los ocho siguientes tienen referencias nuevas en el generador P2.05. Profundidad_cuna queda pendiente, explícitamente no conectada. La presencia de una lectura no acredita propagación completa; H03/H13 precisan las limitaciones.')
    table(['Campo de la revisión del 17/10','Situación P2.05','Etiqueta'],[(k,'lectura geométrica incorporada; ver fila A y límites H03/H13','hecho') for k in r['conectados_desde_p204']]+[('profundidad_cuna','fuera de geometria, conservado en parametrizacion.pendiente[0]; no conectado','hecho')])
    p('**hecho:** los cuatro campos nuevos leídos son '+', '.join(r['nuevos_campos_leidos'])+'. El contraste AST entre ambos generadores respalda 8+4, no la frase 10+4 de '+source(base/'LEEME_P2_05.md','10 campos')+'. Espesor_anclaje y espesor_arandela ya tenían lecturas en P2.04; no son nuevas conexiones. Las reservas de masa 0,65/0,12 kg están fuera de geometría y no deben contarse como dimensiones conectadas. No se altera la frase histórica en este encargo; se documenta H01.')
    p('**hecho:** ancho_ventana_refuerzo y alto_ventana_refuerzo tienen referencia AST, pero no lectura efectiva con ventanas_refuerzo_y=[]. Los campos de cargas y materiales no generan geometría por sí mismos; los mínimos son de estudio. En cambio, luz_puente_cinta, alto_puente_cinta y separacion_pernos se usan en el cálculo sin gobernar los contornos/agujeros correspondientes (H02).')
    p('**hecho:** parametrizacion.fijo_en_generador reconoce textiles, radios de recortes y elementos M5 fijos. Su frase final sobre campos de geometria no se debe interpretar como garantía de control global: hay entradas exclusivamente analíticas y dependencias parciales. Evidencia: '+source(param,'fijo_en_generador')+'.')
    p('## B. Constantes y duplicaciones')
    p('**hecho:** '+str(len(r['literales']))+' registros entre literales, textos, comentarios y accesos a parámetros; inventario en '+resultfile('LITERALES.csv')+'. Clases automáticas por contexto: '+fmt(dict(collections.Counter(v['clase'] for v in r['literales'])))+'. Cada fila guarda ruta, línea y expresión. Las clases de contexto son propuestas de inventario; los hallazgos siguientes se fundamentan en relaciones revisadas, no en coincidencias numéricas accidentales.')
    b=[
      ('Canal, taladros y diámetros nominales','es_parametro',source(gen,"sec=dict(")+'; '+source(gen,"G['pasador_id']/2"),'B/D/t, raíz, pernos y nominales casquillo/pasador salen de G. Tolerancias de corte ±0,1/0,2 son literales auxiliares, no tolerancias de fabricación demostradas.'),
      ('Mejillas: 3, 6; pasador: +0,2/−0,4','literal_duplicado / literal_sin_parametro_cota',source(gen,'B+6-.4')+'; '+source(gen,'xx in [cx-B/2-3'),'El 3 de posicionamiento coincide semánticamente con EM actual y 6 con dos mejillas; no se derivan de EM.'),
      ('Inicio z −3,7 / −6,7 / −6,8, corte y capas','literal_sin_parametro_cota / literal_duplicado',source(gen,"op('z',-3.7,ECU")+'; '+source(gen,"op('z',-6.7,G['espesor_anclaje']"),'ECU y espesor_anclaje se leen, con coordenadas todavía fijas. Refuerzo local de cuna = 2×ECU actual, no un vínculo general con espesor_anclaje.'),
      ('Ranuras 52×8 y puentes locales','literal_duplicado / literal_sin_parametro_cota',source(gen,'Ventanas_cinturon_y_cuna')+'; '+source(calc,'cuna_sigma='),'52 tiene contraparte luz_puente_cinta; alto de ranura 8 no es un término independiente de la fórmula de cuna. 15 mínimo y 16 nominal se explican en C.'),
      ('Contornos, ventanas, radios de recorte, M5','literal_sin_parametro_cota',source(gen,'Cintas_y_aligeramiento')+'; '+source(gen,'Rosca parcial'),'Existen numerosos contornos fijos, incluidos estructurales y de referencia. Su declaración como fijos no los convierte en comprobados.'),
      ('Densidades y propiedades del modelo','literal_duplicado / hipotesis_sin_etiqueta',source(gen,'rho=')+'; '+source(gen,"mechanical']=dict(E_MPa=69000"),'E/Sy actuales coinciden con materiales; nu, Su y densidades están en código. No son certificados ni mediciones. El CSV distingue el contexto material.'),
      ('1,25 de borde y tres factores 1,5','es_parametro / literal ya etiquetado',source(calc,"C['K_borde']*mmax")+'; '+source(calc,"'factor_palanca_union'"),'K_borde proviene del JSON y tiene etiqueta; los tres 1,5 ya están en las 26 magnitudes. No se registran otra vez como ausentes.'),
      ('Precarga 1,25 / 0,75; Cj=0,2 / 0,8','hipotesis_sin_etiqueta',source(calc,'As=14.2')+'; '+source(calc,'joint_residual='),'Constantes explicadas en parte en textos, pero no incluidas individualmente en situacion_de_carga. El 1,25 de precarga es distinto de K_borde.'),
      ('M5 As=14,2; nu=0,33; k placa=0,43; K taladro=3','hipotesis_sin_etiqueta',source(calc,'As=14.2')+'; '+source(calc,'plate_sigma=')+'; '+source(calc,'Sy/(3*local_stress)'),'As y modelo de placa tienen interpretación física; 0,43 es el coeficiente adoptado para placa sobresaliente. El 3 del taladro no lee K_ventana. d=5 se asigna pero no interviene después.'),
      ('OD mínimo/ID máximo: ±0,1 y pin_id=5,6','literal_sin_parametro_cota',source(calc,'pin_od=')+'; '+source(calc,'Casquillo compresion'),'Nominales vienen del JSON; las tolerancias de estudio y el ID máximo están en código. No hay campo de tolerancias.'),
      ('Brazo 3,4; radio 4; AF8; hueco 5,5; mínimo cuna15','literal_duplicado / literal_sin_parametro_cota',source(calc,'pin_vm=')+'; '+source(calc,'washer_contact=')+'; '+source(calc,'cuna_Zin='),'3,4 no tiene origen geométrico unívoco; 4 coincide con AF/2 sin demostrar contacto; AF8 está fijo en ambos scripts; 5,5 de área difiere del agujero de arandela 5,3.'),
      ('Sy arandela 200; factor textil5','hipotesis_sin_etiqueta',source(calc,"200/washer_sigma")+'; '+source(calc,'resistencia_minima_conjunto_cuna_N='),'Mínimos/requisitos adoptados para prediseño. No se atribuye resistencia al textil representado ni al material real sin proveedor/ensayo.'),
      ('Ejemplos 0,35 / 3,4 / 2,3 del encargo','comprobación de contexto',source(gen,"edge_radius=G['radio_redondeo_refuerzo']")+'; '+source(calc,'pin_vm='),'0,35 es radio pedido desde JSON; 3,4 es brazo local literal distinto. No se encontró un mínimo tunnel=2,3 en estos dos scripts. No se inventa una relación entre esas cifras.'),
    ]
    table(['Grupo revisado','Clase semántica propuesta','Evidencia','Interpretación (hecho sobre el código; hipótesis físicas indicadas)'],b)
    p('**hecho:** los textos OD10/ID5,5, 35 grados, 52×8, espesor6/min5,8 y arandela16×3 pueden quedar desactualizados al cambiar los campos relacionados. Son textos descriptivos; no gobiernan el cálculo. Los factores geométricos de sección, π, raíces, exponentes y conversión de unidades no se convierten automáticamente en hipótesis pendientes solo por ser números.')
    p('### Cruce con las 26 magnitudes ya trazadas')
    table(['Magnitud existente','Unidad','Etiqueta actual','Fuente'],[(x['magnitud'],x['unidad'],x['etiqueta'],link(calc,calc.name,x['linea'])) for x in r['trazabilidad_26']])
    p('**hecho:** el brazo local 3,4, las tolerancias ±0,1 y pin_id máximo5,6, el mínimo cuna15, radio/área bajo arandela, Sy arandela200, As M5, coeficientes de junta y factor textil5 no están etiquetados individualmente en esa lista. También brazo_torsion_mm, K_ventana y Sy_perno_MPa provienen del JSON pero no tienen su propia entrada entre las 26. Se conserva lo trazado y se propone completar el resto; no se afirma que todos esos datos carezcan de explicación en otros textos.')
    p('## C. Cálculo ↔ descripción del modelo')
    p('**cálculo:** '+str(len(r['comparaciones_geometricas']))+' comparaciones. Las dos columnas de modelo se obtienen por separado con geometria() de auditar_coherencia.py. MODELO_API.parameters se excluye como prueba de conexión geométrica: es copia de entrada. Evidencias y notas completas en '+resultfile('COMPARACION_GEOMETRICA.csv')+'.')
    table(['Magnitud','Valor usado en cálculo','Modelo histórico','Modelo regenerado','Unidad','Relación','Etiqueta'],[(x['magnitud'],x['valor_calculo'],x['modelo_historico'],x['modelo_regenerado'],x['unidad'],x['estado'],x['etiqueta']) for x in r['comparaciones_geometricas']])
    for x in r['comparaciones_geometricas']:
        p('**'+x['etiqueta']+' — '+x['magnitud']+':** '+x['nota']+' Fuente: '+link(root/x['evidencia']['archivo'],Path(x['evidencia']['archivo']).name,x['evidencia']['linea'])+'.')
    p('**hipótesis — apoyos:** 55 y 435 mm son posiciones analíticas, L=380 mm. No existen entidades que demuestren contacto activo. Los pernos y=35/450 fuera del intervalo no prueban por sí solos omisión de carga: falta justificar resultantes y camino de transmisión. No se redefine el esquema ni se modifica la flecha.')
    p('**cálculo — nominales locales:** puente exterior de cinturón = 20 mm; entre ranuras superiores = 20 mm; superior de yugo = 24 mm; puente de cuna = 124−108=16 mm. El alto18 analítico no tiene identidad única con esos contornos. No se deduce su validez resistente por ser menor ni se propone reemplazarlo automáticamente.')
    p('### Recíproco: geometría sin comprobación individual correspondiente')
    p('**hecho:** '+resultfile('COTAS_MODELO.csv')+' inventaría '+str(len(r['cotas_modelo']))+' valores numéricos de operaciones y radios de piezas. No es una lista de '+str(len(r['cotas_modelo']))+' fallos: incluye cotas cubiertas parcialmente por C, coordenadas y detalles. Las dimensiones de interés sin comprobación individual están agrupadas aquí; la clasificación se basa en uso y crédito resistente explícito, no en que una pieza parezca cosmética.')
    table(['Detalle del modelo','Cobertura de cálculo / clasificación','Evidencia','Etiqueta'],[
      ('Ventanas lumbar/yugo y ligamentos de contornos','Estructural; solo se criban puentes idealizados. No se comprueban todos los ligamentos, esquinas, trayectorias ni apoyos de placa.',source(gen,'Ventanas_cinturon_y_cuna')+'; '+source(gen,'Cintas_y_aligeramiento'),'hecho'),
      ('Ventanas de mejillas 30×11, longitudes100/98 y posiciones','Estructural; bearing usa pared mínima del canal. No hay comprobación local individual de cada contorno.',source(gen,'Pasadores_y_ventana_mejillas')+'; '+source(calc,'Aplastamiento mejilla'),'hecho'),
      ('Pasador largo37,6, retranqueos0,2 y casquillo largo26','Fijación estructural; áreas/diámetros y brazo3,4 no verifican contacto, reparto, holgura ni todo el apoyo longitudinal.',source(gen,'B+6-.4')+'; '+source(gen,'B-2*t'),'hecho'),
      ('Roscas, cabeza, tuerca, penetración y montaje M5','Geometría fija de unión; no hay verificación individual de rosca, prueba de tuerca ni acceso de herramienta.',source(gen,'Rosca parcial')+'; '+source(gen,'No se modela deformacion'),'hecho'),
      ('Radio raíz2 y redondeos0,35/0,5/0,5','Acabado y contacto sin crédito de resistencia de radios en sección; aplicación nativa/desgaste pendiente.',source(gen,"r=G['radio_raiz']")+'; '+source(calc,'Conservative sharp-corner'),'hecho'),
      ('Panel HDPE, espumas, textiles y hebillas de referencia','Protección/representación sin crédito resistente de su geometría. Textiles y costuras requieren selección y ensayo, no se validan con el área dibujada.',source(gen,'No se cuenta como elemento resistente')+'; '+source(gen,'No presupone resistencia por area'),'hecho'),
      ('Recorridos de cuna y profundidad130 no conectada','Referencia no equivalente a dimensión validada. No se deduce contacto A/B/C ni dimensiones de la bomba desde esas curvas.',source(param,'profundidad_cuna')+'; '+source(gen,'path=[(156,30)'),'hecho'),
    ])
    p('## D. Regeneración ejecutada y conservación de evidencia')
    table(['Comprobación ejecutada','Resultado','Etiqueta'],[
      ('Entorno invocador',r['entorno']['powershell']+'; '+r['entorno']['python'],'hecho'),
      ('Archivos emitidos por generador',d['archivos_generados'],'hecho'),
      ('Diferencias MODELO_API',len(d['diferencias_modelo']),'hecho'),
      ('Diferencias BOM por filas',len(d['diferencias_bom']),'hecho'),
      ('Igualdad de bytes por archivo',d['igualdad_bytes'],'hecho'),
      ('Piezas / ocurrencias / uniones',[d['piezas'],d['ocurrencias'],d['uniones']],'hecho'),
      ('Trazado en memoria sin cambio de valores',d['instrumentacion_sin_cambio_de_valores'],'hecho'),
      ('Inventor y CAD nativo','no ejecutado / no modificado por este encargo','hecho'),
    ])
    p('**hecho:** resultados completos en '+resultfile('COMPARACION_GENERACION.json')+'; stdout/stderr y comando exacto en '+resultfile('REGISTRO_GENERACION.json')+'. Los dos archivos regenerados se conservan bajo Control_generacion_JSON con LEEME que indica que no son CAD nativo ni entrega aceptada. No se borra evidencia.')
    p('### Comandos completos (Windows PowerShell 5.1)')
    fence=chr(96)*3
    p('**hecho:** la herramienta de terminal inicia PowerShell 7 aunque se solicite otro shell. Para la ejecución final se invocó explícitamente el ejecutable de Windows PowerShell 5.1 con el siguiente archivo; el propio archivo rechaza otras versiones:')
    p(fence+'powershell\n& \'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe\' -NoProfile -ExecutionPolicy Bypass -File \''+str(audit/'ejecutar_auditoria.ps1')+"'\n"+fence)
    p('**hecho:** dentro de Windows PowerShell 5.1, estos comandos Python también reproducen el análisis:')
    cmd=["$env:PYTHONIOENCODING = 'utf-8'","$python = '"+r['entorno']['ejecutable']+"'","Set-Location -LiteralPath '"+str(root)+"'","$salida = Join-Path '"+str(audit)+"' ('Ejecucion_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))","& $python -B '"+str(audit/'auditar_coherencia.py')+"' --salida $salida --powershell $PSVersionTable.PSVersion.ToString()"]
    p(fence+'powershell\n'+'\n'.join(cmd)+'\n'+fence)
    p('**hecho:** el comando anterior reproduce A–D, genera una salida nueva y reescribe únicamente AUDITORIA.md de esta carpeta con el último resultado. El comando original del generador se conserva como vector de argumentos en REGISTRO_GENERACION.json; equivale al siguiente, con destino ya usado, por lo que para repetirlo debe elegirse otro destino nuevo:')
    p(fence+'powershell\n& $python -B \''+str(gen)+"' '"+str(out/'Control_generacion_JSON')+"'\n"+fence)
    p('## Hallazgos numerados y severidad propuesta')
    p('**hecho:** [B] bloqueante de corrida por evidencia incompatible; [I] informativo que requiere resolución según el alcance de la próxima modificación; [C] aceptable/conservar como distinción o limitación explícita. Ninguna severidad constituye una decisión adoptada ni autoriza fabricación o uso.')
    for h in r['hallazgos']:
        p('### '+h['id']+' ['+h['severidad_propuesta']+'] '+h['titulo'])
        p('**'+h['etiqueta']+' — evidencia:** '+'; '.join(link(root/e['archivo'],Path(e['archivo']).name,e['linea'])+' → '+e['expresion'] for e in h['evidencias'])+'.')
        p('**hecho — prueba reproducible:** RESULTADOS.json → hallazgos[id='+h['id']+'].prueba_reproducible: '+fmt(h['prueba_reproducible'])+'. El script reproduce esa extracción; filas de A/B/C y bloque D permiten contrastarla.')
        p('**pendiente — corrección propuesta, no aplicada:** '+h['correccion_propuesta_no_aplicada'])
    p('## Propuestas priorizadas y efecto sobre una próxima corrida')
    table(['Prioridad propuesta','Acción pendiente','Efecto propuesto, no adoptado'],[
      ('1','Antes de variar espesores/diámetros: resolver H02–H05 y H13; definir qué campo controla cota nominal, mínimo y dependencias.','Bloquear una corrida con parámetros modificados si no se demuestra coherencia. Con nominales actuales D no muestra desfase; no se inventa un fallo nativo.'),
      ('2','Justificar brazo3,4, alto18, mínimo15, contacto arandela y apoyos (H08/H09). Completar etiquetas y fuentes H06/H07.','Condiciona una nueva conclusión resistente y aceptación de entrega. Una regeneración idéntica no resuelve las hipótesis.'),
      ('3','Corregir el recuento documental 10+4 y precisar lectura parcial/ramas inactivas (H01/H11).','Corrección documental propuesta, sin cambiar ahora valores ni ecuaciones.'),
      ('4','Planificar comprobaciones locales/FEA/ensayos para H12 según geometría y datos físicos acordados.','Mantener prediseño y límites declarados. No declarar seguridad o cumplimiento demostrado.'),
    ])
    p('**pendiente real:** primera integración nativa del cierre nuevo en una carpeta nueva y con autorización; clasificación A/B/C de D-12 con recorrido/tensión reales; medidas de bomba llena/vacía, masas, centro de gravedad, reparto, excentricidad, apoyos y precarga; tolerancias/proveedores, ensayos de textiles/desgaste/radio0,5, revisión local y fatiga. Esta auditoría no los ejecuta ni los convierte en datos medidos. Se puede ordenar las fuentes y resolver decisiones documentales sin disponer todavía de la bomba; su validación física seguirá pendiente.')
    p('## Cambios permitidos y comprobación de integridad')
    p('**hecho:** los entregables nuevos están dentro de esta carpeta de auditoría. Fuera de ella solo se añadió una sección corta al LEEME_P2_05.md y una línea a CHANGELOG_SEDAC.md. Las ocho modificaciones rastreadas del encargo previo se conservaron; no se repitió su implementación. No se hace commit, no se toca DECISIONES.md ni ESTADO_ACTUAL.md en este encargo.')
    p('**hecho:** all.png queda excluido como insumo y sin abrir; se cotejan solo sus metadatos (0 bytes). Las dos carpetas ajenas de OpenCode Nueva_20261022_183218_837 y Calculo_20261022_183238_628 se conservaron intactas según autorización «sí, continúa». La línea base previa está en INTEGRIDAD_ANTES.json. El cotejo final de archivos previos, CAD, fuentes y evidencia histórica queda en VERIFICACION_INTEGRIDAD.json; consultar ese resultado para el estado al finalizar, no inferirlo de esta frase.')
    p('**hecho — resultados de ejecución:** '+link(out/'RESUMEN.json')+', '+link(out/'RESULTADOS.json')+'. La primera exploración Ejecucion_20261022_190100 se conserva; la ejecución enlazada aquí es la final, con clasificación afinada y este informe. No se elimina la exploración.')
    (audit/'AUDITORIA.md').write_text('\n'.join(md),encoding='utf-8')
