# Kit de montaje geometrico SEDAC V0.1

Estado: reglas preparadas, no ejecutadas ni compiladas en Inventor en esta sesion. El usuario ya genero los modelos de anclaje y base. La nueva regla del kit crea una carpeta de salida independiente y un ensamblaje nuevo; no modifica esos modelos fuente.

STL del separador generado independientemente del CAD: 01_CAD/Exportaciones/SEDAC_Separador_18x5p5x6_V01.stl. Verificado como malla cerrada, orientacion consistente, 1024 triangulos y envolvente18x18x6 mm. No laminado; encaje y resistencia pendientes. Importar con unidades mm.

## Alcance y limite de impresion

Se mantienen TRES disenos imprimibles: anclaje, base y separador. El montaje representado utiliza SIETE unidades: 2 anclajes + 1 base + 4 separadores. No equivale a tres objetos fisicos. Puede imprimirse primero un separador para comprobar su ajuste.

El usuario CONFIRMO un limite de 40 x 40 x 70 MILIMETROS. Solo el separador cabe a escala real. El anclaje de 90 x 75 x 8 y la base de 280 x 140 x 66 no caben; no se deben exportar como si pudieran fabricarse en esta maquina. Se mantienen a escala real para el ensamblaje digital. Recomendacion de impresion: separadores solamente; probar primero una unidad. Una maqueta reducida seria solo visual y requeriria decision explicita, pues perderia compatibilidad con cinta y tornilleria. No se han dividido ni escalado las piezas. La cabida geometrica no sustituye comprobar margen, orientacion y tiempo en el laminador.

Cuatro separadores de diametro18 en una grilla de 2x2, centros separados20 mm, ocupan 38x38 mm y dejan solo1 mm de margen por lado. No recomendar esa distribucion sin revisar las exclusiones y la adhesion del equipo. Una unidad ocupa18x18x6; dos unidades en fila separadas20 mm ocupan38x18x6. Preferir comenzar con una unidad y repetir segun el laminador.

## Lista provisional para dos anclajes y una base

| Elemento | Cantidad | Especificacion inicial | Origen |
|---|---:|---|---|
| Anclaje | 2 | Modelo existente 90 x 75 x 8 mm | Impresion PLA, ajuste |
| Base | 1 | Modelo existente 280 x 140 x 66 mm | Impresion PLA, ajuste |
| Separador | 4 | Exterior 18; agujero 5,5; largo 6 mm | Impresion de prueba o pieza comercial equivalente |
| Tornillo anclaje | 4 | M5 x 30, paso 0,8; longitud bajo cabeza; rosca completa | Comprar metalico |
| Tornillo base | 4 | M5 x 20, paso 0,8; longitud bajo cabeza; rosca completa | Comprar metalico |
| Arandela ancha | 16 | M5, interior 5,3; exterior 15; espesor 1,2 mm | Comprar metalica |
| Tuerca autofrenante | 8 | M5, paso 0,8; envolvente usada: 8 entre caras, 5 alto | Comprar metalica con inserto, verificar ficha |
| Panel de ensayo | 1 | 360 x 420 x 3 mm; 8 agujeros de 5,5 mm | Referencia provisional, material pendiente |
| Cinta | Pendiente | 50 x 2 mm supuestos; lazo cosido o cierre comercial adecuado | Textil comercial; terminacion pendiente |
| Acolchados | Pendiente | Superficie y espesor segun bolsa real | Pendiente |

No se ha comprado nada. Esta lista es para montaje geometrico; grado resistente, material final, par de apriete, bloqueo frente a deslizamiento y proteccion de extremos roscados no estan validados.

## Por que estas dimensiones

- Separacion de 6 mm: deja espacio nominal para el retorno de una cinta supuesta de 2 mm; debe probarse tambien con el espesor de costura. Exterior de 18 mm aporta una superficie de apoyo mayor que el agujero y cabe alrededor de los centros de las ranuras. Es una hipotesis de montaje, no un resultado estructural.
- Arandela de 15 mm: la ranura tiene 6,2 mm de ancho en su garganta; el redondeo R2 puede ampliar la boca a unos 10,2 mm. Una arandela de 10 mm no es apropiada como referencia de apoyo plano sobre esa boca; se propone 15 mm. El apoyo restante sigue sin dimensionamiento resistente.
- Tornillo de anclaje: 1,2 + 8 + 6 + 3 + 1,2 + 5 = 24,4 mm de apilamiento nominal hasta final de tuerca. M5x30 deja 5,6 mm de salida nominal.
- Tornillo de base: 1,2 + 6 + 3 + 1,2 + 5 = 16,4 mm. M5x20 deja 3,6 mm de salida nominal.
- Si cambia el panel, el separador, la tuerca o las arandelas, recalcular longitudes. Verificar que la rosca atraviese el elemento de bloqueo y que el extremo no roce la bolsa, cinta o usuario. La tuerca evita aflojamiento; no convierte por si sola la ranura en bloqueo positivo.

## Esquema de montaje por tornillo

Cabeza -> arandela -> anclaje (8) -> separador (6) -> panel (3) -> arandela -> tuerca.

En la base se omite el separador y se sustituye el anclaje por su pared posterior de 6 mm. El kit situa base y anclajes del mismo lado del panel para inspeccion geometrica; no es la arquitectura definitiva de bolsa y arnes, que se montaran en caras funcionales distintas segun el diseno final. No representa contacto humano ni el recorrido completo de las cintas.

## Referencias comerciales consultadas

- [Arandela DIN9021/ISO7093 M5 5,3 x 15 x 1,2, Ettinger](https://www.ettinger.de/en/product-datasheet/152942d7ad166326986e390641f06c1d/create).
- [Tuerca DIN985 M5, ficha Bollhoff](https://eshop.boellhoff.de/out/media/pdf/DIN_985_Stahl_010_gv___en.pdf). Elegir segun dimensiones del producto suministrado; no asumir equivalencia dimensional exacta con otra norma.
- [Tornillo M5 paso 0,8 y cabeza de 3,5 mm, catalogo Aspen](https://www.aspenfasteners.com/m5-0-8-x-35mm-din-933-iso-4017-metric-hex-head-cap-screws-bolts-full-thread-brass/). Referencia de geometria, no recomendacion de comprar ese material o largo.

## Alcance del CAD automatico

La regla genera 40 ocurrencias fijas: 1 panel, 2 anclajes, 1 base, 4 separadores, 8 tornillos, 16 arandelas y 8 tuercas. Las piezas REF_ son envolventes simplificadas, no componentes normalizados del Content Center ni modelos de rosca. No imprimir las piezas REF_. El anillo de la tuerca tiene un agujero de visualizacion, no una rosca fabricable. El modelo no incluye cintas ni acolchados.

Las posiciones estan fijadas con Grounded. No hay restricciones de movimiento ni actualizacion automatica de posiciones al modificar piezas; para nuevas cotas hay que adaptar y regenerar el kit. La regla comprueba parametros y envolventes de origen antes de montarlo. No realiza un analisis de interferencias completo ni un calculo de resistencia.
