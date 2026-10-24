"""Verificación en memoria: no ejecutar las escrituras del cálculo ni Inventor."""
from pathlib import Path
import argparse
import ast
import contextlib
import io
import json
import subprocess

PRUEBAS = Path(__file__).resolve().parent
BASE = PRUEBAS.parents[2]
FUENTE = BASE / 'Soporte/calcular_p2_05.py'
RAIZ = BASE.parents[2]


def calcular_en_memoria(texto):
    arbol = ast.parse(texto)
    tramo = []
    for nodo in arbol.body:
        if isinstance(nodo, ast.Expr) and isinstance(nodo.value, ast.Call):
            llamada = nodo.value.func
            if isinstance(llamada, ast.Attribute) and llamada.attr == 'mkdir':
                continue
        tramo.append(nodo)
        if isinstance(nodo, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'result' for t in nodo.targets):
            break
    else:
        raise AssertionError('No se encontró la asignación de result')
    for nodo in tramo:
        for llamada in ast.walk(nodo):
            if isinstance(llamada, ast.Call) and isinstance(llamada.func, ast.Attribute):
                assert llamada.func.attr not in {'write_text', 'write_bytes', 'mkdir', 'open'}, 'Escritura antes del resultado'
    variables = {'__file__': str(FUENTE)}
    exec(compile(ast.Module(body=tramo, type_ignores=[]), str(FUENTE), 'exec'), variables)
    return variables, arbol


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    salida = args.salida.resolve()
    assert salida.parent.is_relative_to(PRUEBAS / 'Ejecuciones'), 'Salida fuera del banco'
    assert not salida.exists(), 'No se sobrescriben resultados anteriores'
    anterior = subprocess.check_output(['git', 'show', 'HEAD:' + FUENTE.relative_to(RAIZ).as_posix()], cwd=RAIZ).decode('utf-8-sig')
    actuales, arbol = calcular_en_memoria(FUENTE.read_text(encoding='utf-8-sig'))
    previas, _ = calcular_en_memoria(anterior)
    resultado = actuales['result']
    sin_metadatos = {k: v for k, v in resultado.items() if k != 'situacion_de_carga'}
    assert sin_metadatos == previas['result'], 'Se alteraron resultados o datos anteriores'
    assert resultado['alcance'] == previas['result']['alcance'], 'Se alteró el alcance'
    datos = resultado['situacion_de_carga']['magnitudes']
    for nombre, dato in datos.items():
        assert set(dato) == {'valor', 'unidad', 'origen', 'etiqueta'}, nombre
        assert dato['etiqueta'] in {'supuesto', 'hipótesis', 'cálculo'}, nombre
        assert dato['origen'], nombre
    salida_print = io.StringIO()
    nodo_print = next(n for n in arbol.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id == 'print')
    with contextlib.redirect_stdout(salida_print):
        exec(compile(ast.Module(body=[nodo_print], type_ignores=[]), str(FUENTE), 'exec'), actuales)
    assert json.loads(salida_print.getvalue())['situacion_de_carga'] == resultado['situacion_de_carga']
    informe = dict(etiqueta='hecho', metodo='AST en memoria, omitiendo mkdir y toda escritura original', resultados_anteriores_identicos=True, verificaciones=len(resultado['verificaciones']), minimo_margen=resultado['minimo_margen'], magnitudes_trazadas=len(datos), alcance_conservado=True, bloque_presente_en_print=True, inventor_ejecutado=False)
    salida.write_text(json.dumps(informe, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(informe, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
