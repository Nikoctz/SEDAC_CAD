# Corrección de dependencias H03 y parte de H13 — alcance previo

## UNIDADES:

- **hecho:** milímetros; sin conversiones ni cambios de escala.

## TIPO DE PIEZA/PLANO:

- **hecho:** mantenimiento del generador descriptivo P2.05. Interfaz lumbar, yugos, mejillas y pasadores existentes. No es un diseño nuevo ni una corrida de Inventor.

## PARÁMETROS GEOMÉTRICOS:

- **hecho:** EM = geometria.espesor_mejilla = 3 mm; B = ancho_refuerzo = 32 mm. Se conserva PARAMETROS_P2_05.json.
- **cálculo propuesto:** inicio de mejilla izquierda = cx−B/2−EM; agarre = B+2×EM; pasador = agarre−0,4; corte transversal = agarre+0,2. Sustituyen los 3/6 embebidos de la misma función geométrica.
- **cálculo propuesto:** cara superior lumbar = Z0+ECU; comienzo de corte = Z0−0,1; placa de yugo = Z0. Conservan las caras actuales −3,7/−6,8/−6,7 mm con los parámetros presentes. No se cambia el espesor ECU de la segunda capa de cuna ni se equipara por decreto 2×ECU con espesor_anclaje.
- **supuesto existente:** retranqueo de pasador 0,2 por extremo y sobrepaso de corte 0,1 por extremo. Se conservan; no son tolerancias de fabricación validadas.
- **hecho:** roscas M5 esquemáticas y demás cotas existentes fuera de esta corrección; sin cambio de su definición.

## OPERACIONES:

- **hecho:** edición de expresiones del generador y documentación; conservación de su fuente anterior y huellas. No se ejecutan operaciones CAD.
- **pendiente:** comparar descripciones antes/después y comprobar variaciones de parámetros cuando se autorice verificar la implementación. No se añaden ni ejecutan pruebas en este paso.

## MATERIAL Y FABRICACIÓN:

- **supuesto existente:** 6061-T6 para elementos resistentes; sin cambios de propiedades.
- **pendiente:** certificados, proceso definitivo, tolerancias, contacto y desgaste. El radio 0,5 mm continúa sin ensayo.

## ENTREGABLES:

- **hecho:** fuente del generador corregida, copia de la fuente anterior, ficha, informe de cambios, diff, huellas e inserciones documentales. No se emite CAD ni entrega aceptada.

## DATOS FALTANTES CRÍTICOS:

- **pendiente:** origen de alto de puente18 y brazo3,4; mínimo independiente de mejilla; tolerancias de pasador/casquillo; apoyos y transmisión de fuerzas. Bloquean justificar nuevos valores o aceptación resistente, no la sustitución de expresiones equivalentes de esta ficha.

## SUPUESTOS:

- **hipótesis:** las relaciones actuales definen la intención de posicionar mejillas externas al canal y retraer el pasador respecto de sus caras exteriores. La corrección enlaza esas dependencias; no demuestra ajuste físico ni propagación completa de cualquier cambio futuro.
