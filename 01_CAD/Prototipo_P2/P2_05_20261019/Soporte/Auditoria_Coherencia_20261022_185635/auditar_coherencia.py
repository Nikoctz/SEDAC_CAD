"""Auditoría de coherencia: fuentes en lectura, salidas nuevas y sin Inventor."""
from pathlib import Path
import argparse
import ast
import copy
import csv
import datetime
import hashlib
import io
import json
import math
import re
import subprocess
import sys
import tokenize
from collections import Counter

AUDIT = Path(__file__).resolve().parent
BASE = AUDIT.parents[1]
ROOT = BASE.parents[2]
GEN = BASE / 'Soporte/generar_p2_05.py'
CALC = BASE / 'Soporte/calcular_p2_05.py'
PARAM = BASE / 'PARAMETROS_P2_05.json'
HIST = BASE / 'Soporte/Iteraciones/Nueva_20261019_060807'
OLD = ROOT / '01_CAD/Prototipo_P2/P2_04_20261016/Soporte/generar_p2_04.py'


def cargar(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def guardar(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def linea(path, fragment):
    return next(i for i, s in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1) if fragment in s)


def ruta(path):
    return path.relative_to(ROOT).as_posix()


def cita(path, fragment):
    n = linea(path, fragment)
    return dict(archivo=ruta(path), linea=n, expresion=fragment)


def nombre_camino(parts):
    out = ''
    for p in parts:
        out += ('[' + str(p) + ']') if isinstance(p, int) else ('.' if out else '') + p
    return out


def campos(value, prefix=()):
    if prefix:
        yield prefix, value
    if isinstance(value, dict):
        for k, v in value.items():
            yield from campos(v, prefix + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from campos(v, prefix + (i,))


def hojas(value, prefix=()):
    if isinstance(value, dict) and value:
        for k, v in value.items():
            yield from hojas(v, prefix + (k,))
    elif isinstance(value, list) and value:
        for i, v in enumerate(value):
            yield from hojas(v, prefix + (i,))
    else:
        yield prefix, value


def accesos(path):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    aliases = {'P': ()}
    def resolver(n):
        if isinstance(n, ast.Name):
            return aliases.get(n.id)
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, (str, int)):
            a = resolver(n.value)
            return None if a is None else a + (n.slice.value,)
        return None
    # Solo alias de contenedor; las cotas escalares se siguen en su propia tabla.
    for node in tree.body:
        if isinstance(node, ast.Assign):
            p = resolver(node.value)
            if p in {('geometria',), ('cargas',), ('materiales',)}:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        aliases[target.id] = p
    rows = []
    meta_node = next((n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'situacion_de_carga' for t in n.targets)), None)
    meta = (meta_node.lineno, meta_node.end_lineno) if meta_node else (10**9, 10**9)
    for n in ast.walk(tree):
        p = resolver(n)
        if isinstance(n, ast.Subscript) and p:
            rows.append(dict(camino=p, linea=n.lineno, expresion=ast.unparse(n), solo_trazabilidad=meta[0] <= n.lineno <= meta[1]))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'get' and n.args and isinstance(n.args[0], ast.Constant):
            a = resolver(n.func.value)
            if a is not None:
                rows.append(dict(camino=a + (n.args[0].value,), linea=n.lineno, expresion=ast.unparse(n), solo_trazabilidad=meta[0] <= n.lineno <= meta[1]))
    return tree, sorted(rows, key=lambda x: (x['linea'], x['expresion']))


class DiccionarioTrazado(dict):
    def __init__(self, data, camino, log):
        self.camino, self.log = camino, log
        super().__init__((k, envolver(v, camino + (k,), log)) for k, v in data.items())
    def __getitem__(self, k):
        self.log.add(self.camino + (k,))
        return super().__getitem__(k)
    def get(self, k, default=None):
        return self[k] if k in self else default


class ListaTrazada(list):
    def __init__(self, data, camino, log):
        self.camino, self.log = camino, log
        super().__init__(envolver(v, camino + (i,), log) for i, v in enumerate(data))
    def __getitem__(self, k):
        if isinstance(k, slice):
            return [self[i] for i in range(*k.indices(len(self))) ]
        self.log.add(self.camino + (k,))
        return super().__getitem__(k)
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


def envolver(value, camino, log):
    if isinstance(value, dict):
        return DiccionarioTrazado(value, camino, log)
    if isinstance(value, list):
        return ListaTrazada(value, camino, log)
    return value


def lecturas_sin_escritura(params):
    tree = ast.parse(GEN.read_text(encoding='utf-8-sig'))
    selected, log = [], set()
    for original in tree.body:
        n = copy.deepcopy(original)
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == 'mkdir':
            continue
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'P' for t in n.targets):
            n.value = ast.Name(id='_parametros_trazados', ctx=ast.Load())
            ast.fix_missing_locations(n)
        selected.append(n)
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'manifest' for t in n.targets):
            break
    for n in selected:
        for v in ast.walk(n):
            if isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute):
                assert v.func.attr not in {'mkdir', 'write_text', 'write_bytes', 'open'}, 'Escritura no permitida en el tramo instrumentado'
    namespace = {'__file__': str(GEN), '_parametros_trazados': envolver(params, (), log)}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(GEN), 'exec'), namespace)
    reads = set(log)
    # La normalización conserva todos los valores; no se perturba ningún parámetro.
    plain = json.loads(json.dumps(namespace['manifest'], ensure_ascii=True))
    return reads, plain


def refs_de(camino, refs):
    result = []
    for ref in refs:
        r = ref['camino']
        if camino == r or (len(camino) > len(r) and camino[:len(r)] == r and isinstance(camino[len(r)], int)):
            result.append(ref)
    return result


def cobertura(params, genrefs, calcrefs, runtime):
    rows = []
    analytical = {'pared_minima','apoyo_hombro_y','apoyo_cinturon_y','separacion_pernos','distancia_borde_perno','espesor_minimo_anclaje','espesor_arandela_minimo','alto_puente_cinta','luz_puente_cinta'}
    for p, value in campos(params):
        gs, cs = refs_de(p, genrefs), refs_de(p, calcrefs)
        leaf = not isinstance(value, (dict, list)) or not value
        declared = p[:2] == ('parametrizacion','pendiente')
        state = 'leido' if gs else ('no_leido_declarado' if declared else 'no_leido')
        note = 'Copiado dentro de manifest.parameters; esa propagación no constituye uso geométrico.'
        if p[0] == 'geometria' and len(p) > 1:
            if p[1] in analytical:
                note += ' Campo analítico; distinguirlo de una cota nominal del modelo.'
            if p[1] in {'alto_puente_cinta','luz_puente_cinta','separacion_pernos','distancia_borde_perno'}:
                note += ' La relación con geometría se revisa en C; no la gobierna directamente.'
            if p[1] in {'ancho_ventana_refuerzo','alto_ventana_refuerzo'}:
                note += ' Referencia AST condicional; no se ejecuta con ventanas_refuerzo_y=[].'
        if p[0] in {'cargas','reservas_masa','referencias_historicas','materiales'}:
            note += ' No todo dato de carga/material/presupuesto debe crear geometría; su ausencia del generador no es por sí sola un error.'
        if declared:
            note += ' Profundidad de cuna declarada expresamente no conectada; no se reclasifica como resuelta.'
        rows.append(dict(campo=nombre_camino(p), valor=value, tipo='contenedor' if isinstance(value,(dict,list)) and value else 'hoja', estado_generador=state, leido_en_control=p in runtime, referencias_generador=gs, referencias_calculo=cs, etiqueta='hecho', nota=note))
    return rows


def inventario_literales(path, tree, params):
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    parent = {child: n for n in ast.walk(tree) for child in ast.iter_child_nodes(n)}
    values = [(nombre_camino(k), v) for k, v in hojas(params) if isinstance(v, (int,float)) and not isinstance(v,bool)]
    meta_node = next((n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='situacion_de_carga' for t in n.targets)),None)
    meta = (meta_node.lineno,meta_node.end_lineno) if meta_node else (10**9,10**9)
    rows = []
    physical_calc = {'nu','As','d','pin_id','pin_od','pin_vm','washer_sigma','washer_contact','sbri','cuna_sigma','cuna_Zin','cuna_Zout','R','fb','joint_residual','result','Tstrap'}
    for n in ast.walk(tree):
        if not isinstance(n, ast.Constant) or isinstance(n.value,bool) or not isinstance(n.value,(int,float)):
            continue
        v = n.value
        if isinstance(parent.get(n),ast.UnaryOp) and isinstance(parent[n].op,ast.USub):
            v = -v
        cur = n
        while cur in parent and not isinstance(cur,(ast.Assign,ast.Expr,ast.Return,ast.FunctionDef,ast.For)):
            cur = parent[cur]
        expression = ast.unparse(cur)
        owner = n
        while owner in parent and not isinstance(owner,ast.FunctionDef):
            owner = parent[owner]
        function = owner.name if isinstance(owner,ast.FunctionDef) else None
        assignment = set(t.id for t in cur.targets if isinstance(t,ast.Name)) if isinstance(cur,ast.Assign) else set()
        matching = [k for k, pv in values if pv == v]
        line = lines[n.lineno-1].strip()
        if meta[0] <= n.lineno <= meta[1]:
            category = 'solo_trazabilidad'
        elif path == CALC and n.lineno >= linea(CALC,'for b,d,t in'):
            category = 'alternativa_de_comparacion_o_salida'
        elif path == GEN and function == 'strap_segment':
            category = 'funcion_no_invocada'
        elif 'colors' in assignment:
            category = 'control_o_visual'
        elif isinstance(parent.get(n),ast.Subscript) or (function in {'rect','circle','poly','op','part','hexagon','ribbon_path'} and n.value in {0,1,2,3,6}):
            category = 'coeficiente_o_control'
        elif path == CALC and assignment == {'d'}:
            category = 'variable_sin_uso'
        elif path == CALC:
            if assignment & physical_calc:
                if v == 1.5 and assignment & {'R','sbri','cuna_sigma'}:
                    category = 'literal_ya_etiquetado'
                elif assignment & {'fb','joint_residual','nu','As','result'} or (v == 200 and 'check(' in line):
                    category = 'hipotesis_sin_etiqueta'
                else:
                    category = 'literal_duplicado' if matching else 'literal_sin_parametro_cota'
            elif ('check(' in line and v in {200,3}) or (v == .43 and 'plate_sigma=' in line):
                category = 'hipotesis_sin_etiqueta'
            else:
                category = 'coeficiente_de_formula'
        elif assignment & {'rho'}:
            category = 'hipotesis_material_no_parametrizada'
        elif v == 0 or v in {-1,1} or isinstance(cur,ast.For):
            category = 'origen_o_control'
        else:
            category = 'literal_duplicado' if matching else 'literal_sin_parametro_cota'
        rows.append(dict(archivo=ruta(path),linea=n.lineno,columna=n.col_offset,valor=v,clase=category,coincidencias_numericas=matching,funcion=function,contexto=line,etiqueta='hecho',nota='La igualdad de valor no demuestra identidad semántica; clases de contexto propuestas, hallazgos verificados aparte.'))
    for n in ast.walk(tree):
        if isinstance(n,ast.Constant) and isinstance(n.value,str) and re.search(r'\d',n.value) and len(n.value)>8:
            rows.append(dict(archivo=ruta(path),linea=n.lineno,columna=n.col_offset,valor=n.value,clase='texto_no_operativo',coincidencias_numericas=[],funcion=None,contexto=lines[n.lineno-1].strip(),etiqueta='hecho',nota='Texto literal: no gobierna cotas por sí mismo; comprobar que no quede obsoleto al cambiar entradas.'))
    for token in tokenize.generate_tokens(io.StringIO('\n'.join(lines)).readline):
        if token.type == tokenize.COMMENT and re.search(r'\d',token.string):
            rows.append(dict(archivo=ruta(path),linea=token.start[0],columna=token.start[1],valor=token.string,clase='comentario_no_ejecutable',coincidencias_numericas=[],funcion=None,contexto=token.string,etiqueta='hecho',nota='Declaración en comentario; no se confunde con una ecuación ejecutada.'))
    return sorted(rows,key=lambda r:(r['archivo'],r['linea'],r['columna']))


def diferencias(a,b,path='$'):
    if isinstance(a,bool) or isinstance(b,bool):
        return [] if type(a)==type(b) and a==b else [dict(ruta=path,antes=a,despues=b)]
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        return [] if a==b else [dict(ruta=path,antes=a,despues=b)]
    if type(a)!=type(b):
        return [dict(ruta=path,antes=a,despues=b)]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out.append(dict(ruta=path+'.'+k,antes=a.get(k),despues=b.get(k)))
            else:out+=diferencias(a[k],b[k],path+'.'+k)
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [dict(ruta=path+'.longitud',antes=len(a),despues=len(b))]
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in diferencias(x,y,path+'['+str(i)+']')]
    return [] if a==b else [dict(ruta=path,antes=a,despues=b)]


def geometria(model, params):
    parts={p['name']:p for p in model['parts']}
    def op(name,label):return next(x for x in parts[name]['ops'] if x['label']==label)
    ch=op('Refuerzo_C_I','Canal_abierto');sec=ch['loops'][0]
    holes=op('Refuerzo_C_I','Alojamiento_pasador_hueco')['loops']
    cs=op('Casquillo_I_35','Separador_compresion');pin=op('Pasador_hueco_I_35','Pasador_cortante')
    ws=op('Arandela_M5_16x3_GN6341','Arandela_gruesa')
    lumbar=op('Interfaz_lumbar_aligerada','Placa_lumbar');slots=op('Interfaz_lumbar_aligerada','Ventanas_cinturon_y_cuna')['loops']
    yoke=op('Yugo_superior_I','Placa_yugo')['loops'][0];ys=op('Yugo_superior_I','Cintas_y_aligeramiento')['loops']
    nut=op('Tuerca_M5_autofreno_metalica','Tuerca')['loops'][0]['pts']
    return dict(B=sec['B'],D=sec['D'],pared=sec['t'],altura=ch['depth'],raiz=sec['r'],eje_pernos=holes[0]['y'],pernos=[x['x'] for x in holes],casquillo_OD=2*cs['loops'][0]['r'],casquillo_ID=2*cs['loops'][1]['r'],casquillo_largo=cs['depth'],pasador_OD=2*pin['loops'][0]['r'],pasador_ID=2*pin['loops'][1]['r'],pasador_largo=pin['depth'],mejilla=op('Interfaz_lumbar_aligerada','Mejilla_apoyo')['depth'],anclaje_yugo=op('Yugo_superior_I','Placa_yugo')['depth'],anclaje_cuna=lumbar['depth']+op('Interfaz_lumbar_aligerada','Refuerzos_locales_cuna')['depth'],ranuras_cuna=[[s['w'],s['h']] for s in slots[-2:]],luz_cinturon=slots[1]['h'],luz_yugo=ys[0]['w'],puente_cuna_nominal=lumbar['loops'][0]['y']+lumbar['loops'][0]['h']-(slots[-1]['y']+slots[-1]['h']),puentes_nominales=[slots[1]['x']-lumbar['loops'][0]['x'],ys[0]['y']-(ys[1]['y']+ys[1]['h']),yoke['y']+yoke['h']-(ys[0]['y']+ys[0]['h'])],arandela_t=ws['depth'],arandela_OD=2*ws['loops'][0]['r'],arandela_ID=2*ws['loops'][1]['r'],tuerca_AF=max(p[1] for p in nut)-min(p[1] for p in nut),radios=[parts[k]['edge_radius'] for k in ['Refuerzo_C_I','Interfaz_lumbar_aligerada','Yugo_superior_I']],E_cad=parts['Refuerzo_C_I']['mechanical']['E_MPa'],Sy_cad=parts['Refuerzo_C_I']['mechanical']['Sy_MPa'])


def comparaciones(params, historic, regenerated):
    G,C,M=params['geometria'],params['cargas'],params['materiales'];a,b=geometria(historic,params),geometria(regenerated,params)
    rows=[]
    def add(nombre,valor,key,estado,fuente,nota,unidad='mm'):
        rows.append(dict(magnitud=nombre,valor_calculo=valor,modelo_historico=a.get(key),modelo_regenerado=b.get(key),unidad=unidad,estado=estado,evidencia=cita(CALC,fuente),origen_modelo=key,etiqueta='cálculo' if estado!='sin_procultad' else 'hipótesis',nota=nota))
    for name,key in [('ancho_refuerzo','B'),('profundidad_refuerzo','D')]:add(name,G[name],key,'coincide_nominal',"S=section(",'Coincide con el perfil nominal de la descripción; no lectura del sólido nativo.')
    add('Pared mínima canal',G['pared_minima'],'pared','minimo_frente_a_nominal','S=section(','2,8 frente a 3 nominal; mínimo de estudio explícito, no error de identidad ni tolerancia medida.')
    add('Altura total (masa de comparación)',G['alto_refuerzo'],'altura','coincide_nominal',"G['alto_refuerzo']",'Solo aparece en la comparación de masas de secciones, no sustituye la luz L.')
    add('L entre apoyos',G['apoyo_hombro_y']-G['apoyo_cinturon_y'],None,'hipotesis_sin_anclaje_CAD','L=G[','Los parámetros 55/435 están copiados en parameters; no crean apoyos geométricos efectivos.')
    a['separaciones_pares']=[a['pernos'][1]-a['pernos'][0],a['pernos'][3]-a['pernos'][2]]
    b['separaciones_pares']=[b['pernos'][1]-b['pernos'][0],b['pernos'][3]-b['pernos'][2]]
    a['borde_boca']=a['D']-a['eje_pernos'];b['borde_boca']=b['D']-b['eje_pernos']
    a['radio_inscrito_tuerca']=a['tuerca_AF']/2;b['radio_inscrito_tuerca']=b['tuerca_AF']/2
    add('Separación de pernos',G['separacion_pernos'],'separaciones_pares','coincidencia_derivada_independiente',"sp=G[",'El modelo usa pernos_y: las diferencias 95−35 y 450−390 son 60. El campo separacion_pernos no gobierna esos agujeros.')
    add('Eje de taladro',G['eje_pernos_z'],'eje_pernos','coincide_nominal',"local_z=G[",'Coordenada z de los centros en el perfil y en el cribado de agujeros.')
    add('Distancia de borde',G['distancia_borde_perno'],'borde_boca','coincidencia_derivada_independiente',"G['distancia_borde_perno']",'D−eje_pernos_z=24−12=12 hasta la boca del canal; el campo distancia_borde_perno no gobierna la geometría. La dirección del arrancamiento sigue siendo una hipótesis del cribado.')
    add('Anclaje mínimo',G['espesor_minimo_anclaje'],'anclaje_yugo','minimo_frente_a_nominal','tt=G.get','5,8 mínimo frente a placa yugo nominal de 6; mínimo de estudio.')
    add('Anclaje de cuna mínimo',G['espesor_minimo_anclaje'],'anclaje_cuna','minimo_frente_a_nominal','cuna_Zin=','Dos capas nominales de 3 forman 6 en el refuerzo local; el cálculo usa 5,8. No se prueba contacto físico.')
    add('Mejilla efectiva mínima',G['pared_minima'],'mejilla','acoplamiento_analitico',"Aplastamiento mejilla",'Usa pared_minima del canal, no espesor_mejilla ni un mínimo independiente. Nominal actual 3; relación mínima 2,8 no controlada por ese campo.')
    add('Luz de puente anclaje',G['luz_puente_cinta'],'luz_yugo','coincide_pero_literal',"bridge_M=",'52 coincide con la ranura de yugo; también con la altura de ranura de cinturón. El generador escribe 52 literal.')
    add('Alto de puente anclaje',G['alto_puente_cinta'],'puentes_nominales','sin_vinculo_univoco',"Z_bridge=",'18 no identifica un puente único: candidatos nominales de contorno 20, 20 y 24. Su elección conservadora o reducción mínima queda pendiente de justificación local.')
    add('Luz de puente cuna',52,'ranuras_cuna','coincide_pero_literal','cuna_sigma=','52 usado en la fórmula; 8 es alto nominal de ranura descrito en el texto, no un término independiente de esa fórmula.')
    add('Alto mínimo de puente cuna',15,'puente_cuna_nominal','minimo_literal_sin_parametro','cuna_Zin=','Nominal geométrico 16; el mínimo 15 está en código/texto, sin campo de tolerancia o mínimo propio.')
    add('OD casquillo mínimo',G['casquillo_od']-.1,'casquillo_OD','minimo_literal_sin_parametro',"Casquillo compresion",'OD nominal 12,5; resta 0,1 embebida para estudiar 12,4, sin tolerancia en parámetros.')
    add('ID casquillo máximo',G['taladro_union']+.1,'casquillo_ID','maximo_literal_sin_parametro',"Casquillo compresion",'ID nominal 10,2; suma 0,1 embebida para estudiar 10,3.')
    add('OD pasador mínimo',G['pasador_od']-.1,'pasador_OD','minimo_literal_sin_parametro','pin_od=','OD nominal 10; mínimo 9,9 por tolerancia literal.')
    add('ID pasador máximo',5.6,'pasador_ID','literal_no_derivado_del_parametro','pin_od=','El nominal sí sale de pasador_id=5,5 en el generador; el cálculo mantiene 5,6 literal y no lee pasador_id.')
    add('Brazo local de pasador',3.4,None,'sin_procultad','pin_vm=','Constante de brazo local sin campo ni correspondencia geométrica demostrada. No basta encontrar un número parecido en el modelo.')
    add('Espesor mínimo arandela',G['espesor_arandela_minimo'],'arandela_t','minimo_frente_a_nominal','washer_sigma=','2,9 de estudio frente a 3 nominal; mínimo explícito en parámetros.')
    add('AF de apoyo bajo tuerca',8,'tuerca_AF','coincide_pero_literal','washer_contact=','AF medido analíticamente del polígono nominal: 8; valor embebido en ambos scripts.')
    add('Radio de carga arandela',4,'radio_inscrito_tuerca','hipotesis_relacion_geometrica','washer_sigma=','Coincide con AF/2=4 como radio inscrito posible; el contacto y la distribución de presión no se derivan del modelo ni están validados.')
    add('Agujero usado en área bajo tuerca',5.5,'arandela_ID','idealizacion_distinta_de_nominal','washer_contact=','El nominal de arandela es 5,3. El cálculo resta un agujero de 5,5: idealización conservadora de área, pero sin campo ni trazabilidad del apoyo real.')
    add('Radios de contacto y raíz','sin crédito resistente','radios','acabado_sin_credito',"Conservative sharp-corner",'Radios pedidos 0,35/0,5/0,5 y raíz 2; se calcula esquina ideal sin crédito de esos radios. MODELO_API no prueba su aplicación nativa.')
    add('E aluminio',M['E_6061_MPa'],'E_cad','coincide_pero_literal',"E=M[",'69 000 coincide hoy; el material del modelo se escribe como literal, sin leer materiales.E_6061_MPa.',unidad='MPa')
    add('Sy aluminio',M['Sy_6061_MPa'],'Sy_cad','coincide_pero_literal',"Sy=M[",'240 coincide hoy; el material del modelo se escribe como literal, sin leer materiales.Sy_6061_MPa.',unidad='MPa')
    add('Brazo de torsión',C['brazo_torsion_mm'],None,'hipotesis_parametrizada_sin_linea_de_carga_CAD',"T=Q*C[",'Existe en parámetros, pero no una línea de acción de carga en el JSON que demuestre este brazo. No deducirlo solo por coincidir con D/2.')
    add('Ancho de ventana opcional',G['ancho_ventana_refuerzo'],None,'rama_inactiva_actual',"ss=section(",'Las dos ramas generador/cálculo leen este campo solo al recorrer ventanas_refuerzo_y; lista vacía actual, sin ranuras de refuerzo activas.')
    return rows


def escribir_csv(path, rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        for r in rows:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list,tuple)) else v for k,v in r.items()})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida',type=Path,required=True)
    parser.add_argument('--powershell',required=True)
    args=parser.parse_args();out=args.salida.resolve()
    assert out.is_relative_to(AUDIT) and out!=AUDIT and not out.exists(),'Usar una carpeta nueva dentro de la auditoría'
    out.mkdir(parents=True)
    inputs=[PARAM,GEN,CALC,OLD,OLD.parents[1]/'PARAMETROS_P2_04.json',HIST/'MODELO_API.json',HIST/'BOM_FIJACIONES.csv',BASE/'LEEME_P2_05.md',ROOT/'06_DOCUMENTACION/REVISION_P2_04_Y_SKILLS_20261017.md']
    hashes={ruta(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    params=cargar(PARAM);historic=cargar(HIST/'MODELO_API.json')
    gt,gr=accesos(GEN);ct,cr=accesos(CALC);_,oldrefs=accesos(OLD)
    runtime,instrumented=lecturas_sin_escritura(params)
    genout=out/'Control_generacion_JSON';genout.mkdir()
    cmd=[sys.executable,'-B',str(GEN),str(genout)]
    execution=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    guardar(out/'REGISTRO_GENERACION.json',dict(etiqueta='hecho',fecha=datetime.datetime.now().astimezone().isoformat(),comando=cmd,powershell_invocador=args.powershell,python=sys.version,retorno=execution.returncode,stdout=execution.stdout,stderr=execution.stderr,alcance='Solo descripción JSON y CSV; no CAD nativo ni Inventor'))
    assert execution.returncode==0,execution.stderr
    regen=cargar(genout/'MODELO_API.json')
    assert not diferencias(instrumented,regen),'La instrumentación cambió la descripción'
    coverage=cobertura(params,gr,cr,runtime)
    literals=inventario_literales(GEN,gt,params)+inventario_literales(CALC,ct,params)
    literals += [dict(archivo=ruta(GEN if group is gr else CALC),linea=r['linea'],columna=0,valor=nombre_camino(r['camino']),clase='es_parametro',coincidencias_numericas=[],funcion=None,contexto=r['expresion'],etiqueta='hecho',nota='Lectura de parámetro; distinguir cálculo efectivo y salida de trazabilidad.') for group in [gr,cr] for r in group]
    oldkeys={r['camino'][1] for r in oldrefs if r['camino'][0]=='geometria' and len(r['camino'])==2}
    newkeys={r['camino'][1] for r in gr if r['camino'][0]=='geometria' and len(r['camino'])==2}
    oldparams=cargar(OLD.parents[1]/'PARAMETROS_P2_04.json')
    connected=sorted(k for k in newkeys-oldkeys if k in oldparams['geometria'])
    newfields=sorted(k for k in newkeys if k not in oldparams['geometria'])
    comparisons=comparaciones(params,historic,regen)
    diffs=diferencias(historic,regen)
    csv_before=list(csv.DictReader((HIST/'BOM_FIJACIONES.csv').open(encoding='utf-8-sig',newline='')))
    csv_after=list(csv.DictReader((genout/'BOM_FIJACIONES.csv').open(encoding='utf-8-sig',newline='')))
    extra=sorted(p.name for p in genout.iterdir())
    d=dict(etiqueta='hecho',archivos_generados=extra,diferencias_modelo=diffs,diferencias_bom=diferencias(csv_before,csv_after),igualdad_bytes={name:(HIST/name).read_bytes()==(genout/name).read_bytes() for name in extra},piezas=len(regen['parts']),ocurrencias=len(regen['instances']),uniones=len(regen['bolts']),instrumentacion_sin_cambio_de_valores=True)
    # Inventario recíproco completo de cotas: no se asume que todo lo no comparado sea cosmético.
    reciprocal=[]
    for i,p in enumerate(regen['parts']):
        for key,v in hojas(p):
            if isinstance(v,(int,float)) and not isinstance(v,bool) and (key[0]=='ops' or key[0]=='edge_radius'):
                role='referencia_o_proteccion_sin_credito_resistente' if p['reference'] or p['group']=='protecciones' else ('acabado_sin_credito' if key[-1]=='r' or key[0]=='edge_radius' else 'detalle_estructural_o_fijacion_revisar_cobertura_en_C')
                reciprocal.append(dict(pieza=p['name'],ruta_modelo='parts['+str(i)+'].'+nombre_camino(key),valor=v,unidad='mm',grupo=p['group'],clasificacion=role,etiqueta='hecho',nota='El inventario no atribuye verificación individual a todas las coordenadas; consultar magnitudes comparadas en C. Sin inspección nativa.'))
    rows_trace=[]
    node=next(n for n in ct.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='situacion_de_carga' for t in n.targets))
    mag=next(k.value for k in node.value.keywords if k.arg=='magnitudes')
    for k,v in zip(mag.keys,mag.values):
        rows_trace.append(dict(magnitud=k.value,valor_expresion=ast.unparse(v.args[0]),unidad=ast.literal_eval(v.args[1]),origen=ast.literal_eval(v.args[2]),etiqueta=ast.literal_eval(v.args[3]),linea=v.lineno))
    assert hashes=={ruta(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'Una fuente cambió durante el análisis'
    result=dict(alcance='Auditoría de código y descripciones; sin rediseño, sin cambio de valores ni CAD nativo',entorno=dict(powershell=args.powershell,python=sys.version,ejecutable=sys.executable),fuentes_sha256=hashes,cobertura=coverage,conectados_desde_p204=connected,nuevos_campos_leidos=newfields,literales=literals,comparaciones_geometricas=comparisons,cotas_modelo=reciprocal,trazabilidad_26=rows_trace,bloque_D=d)
    # Las conclusiones interpretativas se construyen con pruebas explícitas y severidad propuesta.
    hallazgos=[]
    def finding(id,severity,title,evidence,proof,proposal):
        hallazgos.append(dict(id=id,severidad_propuesta=severity,etiqueta='hecho' if severity!='B' else 'hipótesis',titulo=title,evidencias=evidence,prueba_reproducible=proof,correccion_propuesta_no_aplicada=proposal))
    finding('H01','I','La declaración 10+4 no coincide con las nuevas lecturas del código',[cita(BASE/'LEEME_P2_05.md','10 campos'),cita(GEN,'ECU=G['),cita(OLD,"wt=G[")],dict(conectados_anteriores=connected,nuevos=newfields),'Rectificar en una revisión autorizada el recuento histórico: ocho campos antes no leídos y cuatro nuevos. No contar como nuevos espesor_anclaje ni espesor_arandela, ya leídos en P2.04.')
    finding('H02','I','Luz/alto de puentes y separación de pernos no gobiernan la geometría',[cita(CALC,'bridge_M='),cita(GEN,'Ventanas_cinturon_y_cuna'),cita(CALC,"sp=G[")],dict(campos=[k for k in coverage if k['campo'] in {'geometria.luz_puente_cinta','geometria.alto_puente_cinta','geometria.separacion_pernos'}]),'Conectar o separar explícitamente esas hipótesis y cotas; comprobar las relaciones antes de permitir cambios de parámetros. No sustituir ahora 18 por otra dimensión.')
    finding('H03','I','Espesor de mejilla leído, pero posiciones, grip y pasador conservan 3/6 embebidos',[cita(GEN,'xx in [cx-B/2-3'),cita(GEN,'B+6-.4'),cita(GEN,"B+6,'Lumbar_")],dict(nominal_actual=params['geometria']['espesor_mejilla'],expresiones=['inicio cx-B/2-3','grip B+6','longitud pasador B+6-.4']),'En una revisión posterior derivar las posiciones y longitudes del espesor nominal, con tolerancias justificadas. La lectura de EM no demuestra control global.')
    finding('H13','I','Espesores lumbar/anclaje leídos con inicios y cortes todavía fijos',[cita(GEN,"Z0=-(G['espesor_anclaje']+0.7)"),cita(GEN,"op('z',-3.7,ECU"),cita(GEN,"op('z',-6.8,G['espesor_anclaje']+.2")],dict(cuna_dos_capas='ECU+ECU=6 actual',inicio_capa_local=-3.7,inicio_corte=-6.8,inicio_yugo=-6.7),'Revisar dependencia conjunta de espesores, coordenadas z y profundidad de corte antes de variar estos parámetros; la configuración actual no demuestra propagación general.')
    finding('H04','I','Pasador ID de cálculo desconectado de pasador_id y tolerancias embebidas',[cita(GEN,"G['pasador_id']/2"),cita(CALC,'pin_od=')],dict(nominal=params['geometria']['pasador_id'],maximo_codigo=5.6,tolerancias_literales=0.1),'Declarar mínimos/máximos y su origen; derivar el extremo de estudio desde el nominal autorizado. Mantener por ahora 5,6 y los valores actuales.')
    finding('H05','I','Mejilla mínima se calcula con la pared mínima del canal',[cita(CALC,'Aplastamiento mejilla'),cita(GEN,"xx,EM,")],dict(canal_minimo=params['geometria']['pared_minima'],mejilla_nominal=params['geometria']['espesor_mejilla']),'Separar el mínimo de mejilla o justificar expresamente su vínculo con el canal antes de variar espesores; no inventar una tolerancia.')
    finding('H06','I','Constantes de unión, material y textil no cubiertas por las 26 magnitudes',[cita(CALC,'As=14.2'),cita(CALC,'joint_residual='),cita(CALC,'pin_vm='),cita(CALC,'resistencia_minima_conjunto_cuna_N='),cita(CALC,'plate_sigma='),cita(CALC,"Sy/(3*local_stress)")],dict(pendientes=['As M5=14,2 mm²','dispersión de precarga 1,25 / 0,75','rigidez de junta 0,2 y pérdida 0,8','brazo local 3,4 mm','Sy arandela 200 MPa','factor textil 5','nu=0,33','mínimo de puente cuna 15 mm','coeficiente de placa k=0,43','K local de taladro=3 literal, independiente de K_ventana'],factores_1_5_ya_etiquetados=['factor_palanca_union','factor_puente_anclaje','factor_puente_cuna']),'Incorporar los supuestos faltantes con unidad, origen y etiqueta en una revisión autorizada. No confundir el 1,25 de borde con el 1,25 de dispersión de precarga; tener texto explicativo no equivale a estar en las 26 magnitudes.')
    finding('H07','I','Propiedades del modelo y del cálculo coinciden hoy pero tienen fuentes separadas',[cita(GEN,'mechanical\']=dict(E_MPa=69000'),cita(CALC,"E=M["),cita(PARAM,'E_6061_MPa')],dict(E=params['materiales']['E_6061_MPa'],Sy=params['materiales']['Sy_6061_MPa']),'Unificar o verificar explícitamente propiedades de estudio y propiedades escritas en CAD; los certificados físicos siguen pendientes.')
    finding('H08','I','Apoyos ideales no equivalen a entidades o contactos demostrados del modelo',[cita(CALC,'L=G['),cita(GEN,"G['pernos_y']")],dict(apoyos=[params['geometria']['apoyo_cinturon_y'],params['geometria']['apoyo_hombro_y']],pernos=params['geometria']['pernos_y'],fuera_luz=[v for v in params['geometria']['pernos_y'] if not params['geometria']['apoyo_cinturon_y']<=v<=params['geometria']['apoyo_hombro_y']]),'Documentar resultantes/apoyos y transmisión por grupos de pernos. Tener pernos fuera de la luz no demuestra por sí solo una carga externa omitida; no redefinir el esquema sin evidencia.')
    finding('H09','I','Brazo de pasador 3,4 y mínimos locales no se obtienen del modelo',[cita(CALC,'pin_vm='),cita(CALC,'cuna_Zin='),cita(CALC,'washer_sigma=')],dict(brazo_pasador='sin_procultad: sin origen geométrico unívoco',puente_cuna_nominal=16,puente_cuna_minimo_literal=15,radio_carga_arandela_literal=4),'Justificar brazo efectivo, mínimo de puente y contacto de arandela; parametrizarlos si se adopta su uso. No atribuirlos a una medición del CAD nativo.')
    finding('H10','C','Los mínimos de estudio no deben confundirse con nominales distintos por error',[cita(CALC,'S=section('),cita(CALC,'tt=G.get'),cita(CALC,'washer_sigma=')],dict(canal=[2.8,3],anclaje=[5.8,6],arandela=[2.9,3]),'Conservar nominal/mínimo separados y las etiquetas de prediseño. La aceptación de fabricación requiere evidencia posterior.')
    finding('H11','C','Profundidad de cuna no conectada y ventanas opcionales inactivas están declaradas',[cita(PARAM,'profundidad_cuna'),cita(GEN,"enumerate(G['ventanas_refuerzo_y'])")],dict(ventanas=params['geometria']['ventanas_refuerzo_y'],profundidad=params['parametrizacion']['pendiente']),'Conservar pendiente la profundidad; no etiquetar como obsoletos automáticamente los parámetros de una rama opcional vacía.')
    finding('H12','C','Hay geometría estructural local sin comprobación individual de sus contornos',[cita(GEN,'Ventanas_cinturon_y_cuna'),cita(GEN,'Cintas_y_aligeramiento'),cita(CALC,'FEA local, pandeo distorsional')],dict(detalles=['ventanas y ligamentos de placas lumbar/yugos','ventanas de mejillas 30×11','longitud de pasador 37,6 y condiciones de apoyo','roscas, contacto, acceso y tolerancias','radios sin crédito y referencias textiles']), 'Conservar el alcance parcial del cribado; preparar revisión local, tolerancias y ensayos cuando existan los datos. No dar por calculadas todas las ventanas por existir K_ventana.')
    if diffs or d['diferencias_bom']:
        finding('H14','B','La regeneración descriptiva difiere de la corrida histórica',[cita(GEN,'manifest=dict(')],d,'Investigar el desfase de fuentes/parámetros antes de una nueva corrida nativa; no sobrescribir la evidencia anterior.')
    hallazgos.sort(key=lambda h:h['id'])
    result['hallazgos']=hallazgos
    guardar(out/'RESULTADOS.json',result)
    escribir_csv(out/'CAMPOS_PARAMETROS.csv',coverage)
    escribir_csv(out/'LITERALES.csv',literals)
    escribir_csv(out/'COMPARACION_GEOMETRICA.csv',comparisons)
    escribir_csv(out/'COTAS_MODELO.csv',reciprocal)
    guardar(out/'COMPARACION_GENERACION.json',d)
    (genout/'LEEME.md').write_text('Descripción JSON/CSV regenerada para auditoría. No es CAD nativo ni evidencia de entrega. Se conserva sin borrar; no confundir con Entrega ni con una corrida de Inventor.\n',encoding='utf-8')
    (out/'RESUMEN.json').write_text(json.dumps(dict(etiqueta='hecho',campos=len(coverage),hojas=sum(r['tipo']=='hoja' for r in coverage),conectados_desde_p204=connected,nuevos_campos=newfields,literales=len(literals),magnitudes_geometricas=len(comparisons),cotas_inventariadas=len(reciprocal),diferencias_modelo=len(diffs),diferencias_bom=len(d['diferencias_bom']),hallazgos_por_severidad=dict(Counter(h['severidad_propuesta'] for h in hallazgos)),inventor_ejecutado=False),ensure_ascii=False,indent=2),encoding='utf-8')
    print((out/'RESUMEN.json').read_text(encoding='utf-8'))
    from informe_coherencia import crear_informe
    crear_informe(result,out,ROOT,BASE,AUDIT,GEN,CALC,PARAM,HIST,OLD)


if __name__=='__main__':
    main()
