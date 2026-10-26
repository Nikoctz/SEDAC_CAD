# A.2 · Protocolo de laboratorio (propuesta, sujeta a revisión del profesor)

> **Estado:** propuesta. No habilita por sí mismo ningún ensayo. Los ensayos con personas solo
> proceden tras el piloto, la revisión del profesor, autorización escrita y consentimiento.
> Los valores numéricos marcados como *referencia* son rangos de trabajo, no criterios aceptados.

## 1. Antes de la sesión

- [ ] Verificar el estado del prototipo: apriete de las 8 uniones, integridad de aristas, estado de
      cintas y acolchados, ausencia de juego en los apoyos.
- [ ] Registrar la versión del prototipo (P2.04) y la configuración concreta de cada ensayo.
- [ ] Confirmar que el instrumento está calibrado y vigente. Sin calibración vigente, el ensayo no
      se registra como válido.
- [ ] Tener escrito el criterio de parada y el canal para detenerlo.
- [ ] Tener el consentimiento firmado, si el ensayo es con personas.

## 2. Montaje

| Elemento | Criterio propuesto | Por qué |
|---|---|---|
| IMU principal | En el canal, junto al apoyo de hombro, eje z alineado con el eje longitudinal del canal | Punto de mayor desplazamiento y de menor curvatura de la IMU |
| IMU secundaria | En la bomba o en el yugo, si hay sensor disponible | Permite estimar el movimiento relativo, que es lo comparable con la predicción |
| Fijación | Soporte rígido y continuo, sin cinta ni espuma intermedias; documentar con fotografías | Una IMU con base flexible mide el soporte, no el cuerpo |
| Célula de fuerza | En la correa de carga, si el laboratorio dispone | Sin ella no hay cadena cerrada entre movimiento y fuerzas |
| Sincronización | Evento común visible por todas las instrumentaciones | Sin sincronización la comparación no es interpretable |
| Cableado | Fijado al prototipo, sin bucles sueltos ni enganches en la zona de carga | Los tirones de cable falsean la señal |

## 3. Parámetros de registro

| Parámetro | Referencia propuesta | Estado |
|---|---|---|
| Frecuencia de muestreo efectiva | ≥ 100 Hz (registrar la tasa real, que puede ser menor que la nominal) | Por acordar |
| Duración por repetición | ≥ 60 s | Por acordar |
| Repeticiones por condición | 5, más 3 de control sin carga | Por acordar |
| Condiciones de carga | Sin carga, carga estática en 3 niveles, ciclo de carga y descarga | Por acordar |
| Intervalo entre repeticiones | Para detectar deriva y cambio de montaje | Por acordar |
| Tiempo de estabilización tras aplicar carga | Antes de cada ventana de registro | Por acordar |

## 4. Secuencia de un ensayo

1. Registrar configuración, estado del prototipo e identificador de ensayo.
2. Colocar el lastre en los incrementos acordados; en cada incremento, esperar la estabilización y registrar.
3. Registrar de forma continua todas las instrumentaciones, marcando el evento de sincronización.
4. Medir la holgura axial del casquillo y el estado de las uniones antes y después, con comparador.
5. Descargar el lastre de forma controlada y registrar el comportamiento de retorno.
6. Anotar todo evento: deformación permanente, marca de desgarro, deslizamiento, pérdida de precarga,
   giro del pasador, ruido o vibración.
7. Cerrar: fotografías, hoja de registro firmada y copia de los datos crudos con su carpeta de origen.

## 5. Criterios de interrupción

- Deformación permanente visible o marca de desgarro en cualquier pieza, unión o cinta.
- Aumento medible de la holgura axial del casquillo o giro del pasador en una unión.
- Pérdida de precarga perceptible o aflojamiento de una unión durante la carga.
- Fallo de instrumentación o pérdida de sincronización: el registro no es válido y se repite.
- Alcanzar el límite de carga definido por el profesor.

## 6. Personas: consentimiento y tratamiento de datos

- [ ] Autorización escrita del responsable del proyecto para ensayos con personas.
- [ ] Consentimiento informado, con posibilidad de detenerse en cualquier momento y sin explicación.
- [ ] Datos pseudonimizados; la clave de identificación se guarda separada de los datos.
- [ ] Sin datos personales ni antropométricos en herramientas de IA externas: es una regla vigente del
      proyecto y aplica a todo el pipeline de análisis.
- [ ] Ninguna medición aislada declara validación ergonómica, clínica o normativa.

## 7. Revisión del profesor antes de ensayos con personas

| Ítem | Respuesta del profesor | Fecha |
|---|---|---|
| ¿El montaje y el protocolo son aceptables? | | |
| ¿La carga máxima y los incrementos son aceptables? | | |
| ¿Los criterios de parada son suficientes? | | |
| ¿Hace falta instrumentación adicional? | | |
| ¿Se autoriza el paso a ensayo con personas? | | |

---

**Relación con la planilla:** este protocolo se ejecuta ensayo por ensayo; cada ejecución se registra
en `02_Planilla/Planilla_SEDAC_Captura_y_Seguimiento_v0.1.xlsx`, hoja `03_Registro_Ensayos`, con su
identificador de ensayo, su configuración y su estado.
