# Base SEDAC V0.1: maqueta geometrica

La regla SEDAC_Cuna_Base_V01.iLogicVb esta preparada pero NO ejecutada ni compilada en Inventor. La captura aportada confirma visualmente la creacion del anclaje anterior, no la de esta base.

## Uso

1. Guardar la pieza del anclaje con un nombre identificable.
2. File > New > Standard (mm).ipt: abrir OTRA pieza estandar vacia.
3. Manage > iLogic > Add Rule > Text. Nombre sugerido: SEDAC_Generar_Base.
4. Pegar TODO el archivo iLogic, incluidos Sub Main y las funciones auxiliares al final.
5. Save & Run. Guardar resultado como SEDAC_Cuna_Base_V0.1.ipt.
6. Si hay error, copiar etapa y mensaje completos. La transaccion intenta revertir los cambios de esa ejecucion.

No pegar en la regla del anclaje ni ejecutar en esa pieza. El generador rechaza documentos con geometria ajena. No guarda ni sobrescribe archivos automaticamente.

## Dimensiones iniciales asumidas (mm)

| Parametro | Valor | Significado |
|---|---:|---|
| CB_Ancho | 280 | Ancho total |
| CB_Fondo | 140 | Fondo total |
| CB_Espesor | 6 | Piso y paredes de maqueta |
| CB_AlturaPosterior | 60 | Sobre la superficie del piso; altura exterior total 66 |
| CB_AlturaLabio | 15 | Sobre el piso; altura exterior lateral total 21 |
| CB_AberturaAncho | 60 | Ancho de abertura en U |
| CB_AberturaProfundidad | 90 | Profundidad total desde frente, incluido extremo R30 |
| CB_DiametroAgujero | 6,2 | Cuatro agujeros pasantes, herrajes por confirmar |
| CB_SeparacionHorizontal | 180 | Distancia horizontal entre centros |
| CB_AgujeroInferiorZ | 30 | Cota vertical desde cara inferior del piso |
| CB_SeparacionVertical | 20 | Filas en Z=30 y Z=50 |
| CB_RadioBorde | 1 | Redondeo de aristas |

Los centros de agujeros son X=50/230, Z=30/50. La pared posterior esta en Y=134..140. Frente Y=0; la abertura llega a Y=90. Los dos apoyos laterales quedan conectados por un puente posterior. No hay labio frontal: se conserva libre la entrada de la manguera. Se omiten acolchados, pernos, arandelas y panel; deben incorporarse y definirse en el ensamblaje.

Estas dimensiones son decisiones preliminares de modelado autorizadas por el usuario. No se deducen de los 635 x 419,1 mm oficiales de la bolsa vacia. No se conoce aun su perfil lleno, profundidad, posicion exacta del racor ni superficie de apoyo necesaria. La bolsa podria sobresalir o deformarse hacia la abertura; el ajuste real sigue pendiente.

## Parametros y regeneracion

Cambiar CB_* en Manage > Parameters y volver a ejecutar la regla. Los bocetos se reconstruyen desde los parametros; no son bocetos completamente restringidos con actualizacion automatica. No agregar operaciones manuales si se desea seguir regenerando. El generador verifica nombres y cantidades antes de borrar sus propias operaciones. Guardar una copia antes de extender manualmente el modelo.

## Impresion y alcance

Es una maqueta en PLA de una posible base futura metalica, no un modelo de chapa desplegable ni una base estructural calculada. Los 6 mm no especifican el espesor de metal futuro. No demuestra resistencia, rigidez ni seguridad bajo la carga real.

Se requiere espacio de impresion para 280 x 140 mm mas margenes que determine el laminador. Si no cabe, decidir entre una maqueta reducida (que no comprueba encaje a escala real) o un diseno dividido; la regla no divide automaticamente la base. No escalar silenciosamente.

Empezar con UN tamano de anclaje (el existente, pensado para cinta supuesta de 50 mm) y UNA maqueta de base. Dos copias identicas del anclaje servirian para un montaje simetrico futuro, pero son dos unidades del mismo tamano, no dos variantes. No imprimir variantes de tallas sin una pregunta de ajuste concreta.
