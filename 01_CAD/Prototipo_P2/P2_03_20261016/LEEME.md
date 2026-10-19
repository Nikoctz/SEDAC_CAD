# SEDAC P2.03 - entrega de prediseño

**Revisión:** 16/10/2026. **Escala maestra:** 1:1. **Carpeta de trabajo:** Documentos/SEDAC_CAD.

## Qué abrir

1. **Inventor:** [SEDAC_P2_03.iam](Entrega/Inventor_Optimizado/SEDAC_P2_03.iam). Todos los IPT necesarios están en la misma carpeta. Abrir el IAM, no cada pieza por separado.
2. **Vista previa:** [frente](Entrega/Inventor_Optimizado/VISTA_FRENTE.png), [espalda](Entrega/Inventor_Optimizado/VISTA_ESPALDA.png) y [estructura sin protector](Entrega/Inventor_Optimizado/VISTA_ESTRUCTURA.png).
3. **Intercambio CAD:** [STEP](Entrega/Inventor_Optimizado/SEDAC_P2_03_REVISION.step).
4. **Mathcad y PDF:** [guía de archivos](../../../06_DOCUMENTACION/Memoria_Calculo_P2_03/LEEME_MEMORIA.md). Usar el archivo que termina en **MC02_FINAL_EDITABLE.xmcd**.
5. **Resultados y decisiones:** [informe](INFORME_DISENO_P2_03.md).

## Resultado del aligeramiento

- Estructura, protector y herrajes: **2,333 kg**.
- Reducción equivalente respecto de P2.02: **26,0 %**, aproximadamente **0,820 kg**.
- Presupuesto completo con 0,50 kg de textiles y 0,08 kg de accesorios: **2,913 kg**.
- El objetivo conceptual de 2 kg **no se alcanza**. Las reservas no son masas medidas.
- Menor margen de los 33 modelos analíticos revisados: **2,254**, en el M6 del marco/X. No es un factor de seguridad global.
- Riel: margen nominal **2,447**, mínimo de pared **2,305** y flecha **2,038 mm**.

## Qué hay en cada carpeta

| Carpeta/archivo | Uso |
|---|---|
| Entrega/Inventor_Optimizado | Única revisión CAD final de P2.03; 51 IPT, IAM, STEP, vistas y registros |
| Soporte | Generadores y comprobaciones; archivos de trabajo, no otra entrega |
| Soporte/Iteraciones | Intentos intermedios conservados; no abrirlos como diseño vigente |
| PARAMETROS_P2_03.json | Dimensiones principales, cargas, materiales y reservas |
| ESPECIFICACION_P2_03.md | Alcance geométrico y datos pendientes |
| INFORME_DISENO_P2_03.md | Razones de diseño, masas, uniones y límites |

## Alcance

Los 25 kg del escenario son **masa total de equipo transportado**, incluyendo soporte y mochila. Se mantienen 3 g verticales totales, 1 g horizontal y reparto 70/30. Si cambia la masa, el brazo de carga o la posición del arnés, hay que recalcular.

El ensamblaje tiene 131 ocurrencias, 390 restricciones de posición y cero interferencias volumétricas nominales detectadas. Las restricciones a planos de referencia no simulan contacto ni apriete. Roscas nativas cosméticas: no hay una hélice sólida en el STEP.

**Sigue siendo un prediseño.** Faltan bomba real, arnés, tolerancias, referencias comerciales certificadas, contacto local, fatiga, temperatura y ensayos. La escotadura para la manguera cambió. No es una orden de fabricación para uso sobre una persona.

## Cómo modificarlo

Trabajar en una copia de revisión nueva. Las dimensiones principales están en el JSON; los detalles de la plantilla están en los generadores de Soporte. No todos los brazos ni las posiciones del arnés se deducen automáticamente de una dimensión general. Una modificación exige comprobar CAD y memoria juntos.

El generador usa Inventor 2027 instalado en este equipo. El cálculo usa Mathcad clásico de la instalación Mathcad 15. Editar el XMCD por sí solo no actualiza el IAM; editar el IAM por sí solo no actualiza la masa de la memoria.

P2.02 y su ZIP histórico se conservan sin cambios. No se publicó esta entrega en Notion ni se envió por correo.
