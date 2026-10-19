# Revisión de cálculos — MC01 frente al prediseño P2.02

Fecha: 15/10/2026. El CAD no se ha modificado en esta tarea.

## 1. Sección redondeada

Se sustituyó el contorno discretizado por expresiones analíticas exactas de área y segundos momentos. El efecto en el margen del riel es mínimo: aproximadamente 2,2526 en ambos métodos. Se conservaron las hipótesis de carga y amplificaciones locales del prediseño.

En los tubos de refuerzo inferior se incorporaron también los radios de esquina al cálculo de sección. La aproximación previa usaba un tubo de esquinas rectas.

## 2. Tornillos de cartela

El cálculo anterior combinaba la magnitud de la fuerza directa y la contribución del momento mediante una raíz de suma de cuadrados. Para el tornillo crítico en el plano YZ deben sumarse antes las componentes coincidentes en Z.

Antes:
R = 1,2 × sqrt[(sqrt(Vy²+Vz²)/2)² + (M/pitch)²]

Ahora:
R = 1,2 × sqrt[(Vy/2)² + (Vz/2 + M/pitch)²]

Resultado: aproximadamente **1691 N -> 1789 N** por tornillo crítico. El margen de aplastamiento de cartela pasa de aproximadamente **2,46 -> 2,32**. Aún deben verificarse palanca, apertura, precarga y demás modos de la unión.

## 3. Piso: carga localizada en el borde

El cálculo anterior añadía la contribución de un parche usando un brazo correspondiente al tramo interior, incluso al revisar el voladizo. Se incorporó por separado el momento de una carga localizada en el extremo delantero.

Además, la memoria toma como líneas de apoyo los **ejes de los refuerzos**:
- Separación entre ejes: 65 mm.
- Voladizo hasta el borde delantero: 40 mm.

Es una idealización conservadora respecto del apoyo repartido sobre la superficie plana del tubo. Ese contacto efectivo deberá medirse o modelarse con más detalle.

En una franja de 50 mm, para un parche supuesto de 100 N:

M_borde = q × voladizo²/2 + P_parche × voladizo / ancho_franja
sigma = 6 × M_borde / espesor²

Con el piso de 2,5 mm:
- Tensión aproximada: **106,94 MPa**.
- Margen frente a 130 MPa: **1,22**.
- Objetivo adoptado: **2,2**.

El cálculo previo de aproximadamente 38,55 MPa / margen 3,37 **no cubría este caso y no debe usarse para aceptarlo**.

La hoja compara:
- Espesor orientativo necesario: **3,36 mm**.
- Propuesta a estudiar: **3,5 mm**, tensión aproximada **54,56 MPa**, margen **2,38**.
- Alternativas: reducir el voladizo, adelantar/reforzar el apoyo o justificar otra distribución de contacto.

Estas cifras son resultados de un escenario elegido, no valores obtenidos de la bomba real.

## 4. Qué significa el resultado

La memoria registra comprobaciones parciales y muestra el resultado desfavorable. El margen del riel no representa el margen de todas las piezas, y el menor margen parcial tampoco certifica por sí solo el sistema.

Se mantiene pendiente la validación de fatiga, geometría de uniones, textiles, temperatura, retención de bolsa y comodidad. No se declaró una capacidad de carga de uso.

