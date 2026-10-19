# Maqueta SEDAC adaptada 1:12

## UNIDADES
Milímetros. El archivo 3MF declara las unidades. Importar el STL en mm.

## TIPO DE PIEZA/PLANO
Maqueta integrada de una sola pieza, para explicar el montaje del kit.
Reconstruida a partir de las cotas y posiciones del código que generó el kit.
No es una conversión ni una lectura del archivo SEDAC_Kit_Montaje_V01.iam.

## PARÁMETROS GEOMÉTRICOS
- Panel: 30 × 35 × 1.6 mm (ancho y alto a 1:12).
- Envolvente prevista: 30 × 35 × 13.267 mm.
- Cuna: ancho 23.333 mm, piso 1.4 mm, labios laterales 1.2 mm.
- Dos anclajes: 8.5 × 7.25 × 1.4 mm; borde aumentado 0.5 mm.
- Cuatro separadores integrados: diámetro 2.2 mm, luz nominal bajo placas 1.2 mm.
- Ranuras superiores ampliadas a 1.2 mm de ancho para conservar su lectura.
- Ocho fijaciones representadas con arandelas y cabezas hexagonales aumentadas.
- Herrajes posteriores integrados en el panel y representados mediante contornos
  grabados de 0.25 mm de profundidad; el respaldo queda plano.
- Tornillos macizos sin roscas, tuercas sin función mecánica. No desmontable.
- Tolerancias funcionales: no aplica a la maqueta. Resolución de máquina desconocida.

## OPERACIONES
Unión booleana de panel, cuna, anclajes, separadores y detalles de fijación;
recorte de escotadura U y ranuras; exportación a malla de un volumen conectado.
El generador comprueba la envolvente antes de escribir los archivos.
Los originales se conservan sin cambios.

## MATERIAL Y FABRICACIÓN
PLA según lo pedido. Supuesto de preparación: boquilla habitual de 0.4 mm;
confirmar configuración con el centro de impresión. Orientación propuesta:
respaldo plano sobre la cama (Z=0). Puede requerir soportes bajo los anclajes;
revisar accesibilidad para retirarlos y posibilidad de puentes en el laminador.
La cuna se construye como paredes verticales con esta orientación.
Un borde de adhesión de hasta 2 mm por lado ocuparía aproximadamente 34 × 39 mm;
los soportes y recorridos auxiliares también deben mantenerse dentro del límite.
No hay soportes, perfil de impresión ni G-code incluidos. No se ha laminado ni
impreso; no se garantiza impresión con cualquier equipo/configuración.

## ENTREGABLES
- SEDAC_Kit_Maqueta_1a12_ADAPTADA_mm.3mf: geometría con unidades explícitas.
- SEDAC_Kit_Maqueta_1a12_ADAPTADA_mm.stl: geometría; importar en milímetros.
- VISTA_MAQUETA.png: vista calculada de la malla exportada.
- DIMENSIONES_Y_ALCANCE.json: dimensiones y alcance de la generación.
- Generador Python en la carpeta Automatizacion: no pegar en iLogic.

## DATOS FALTANTES CRÍTICOS
Ninguno para generar la maqueta. Antes de imprimir: laminador, boquilla,
altura de capa y estrategia de soportes del centro de impresión.

## SUPUESTOS
Se conserva la disposición demostrativa del kit (base y anclajes en la misma
cara). Escala de disposición 1:12, con espesores y herrajes deliberadamente
aumentados; no es una reducción uniforme ni sirve para validar cargas o ajuste.
Esta entrega contiene solo la maqueta: el separador de 18 × 18 × 6 mm sigue
siendo otro archivo. No se ha preparado una disposición conjunta de ambos.
