# Verificación del protocolo

## 1. Cómo usar esta lista

Marcá cada punto como cumplido, pendiente, no aplicable o limitación aceptada. Para cada pendiente registrá evidencia requerida, responsable y momento de resolución. No conviertas la lista en un puntaje: un único problema de asignación puede comprometer la pregunta principal.

Distinguí tres resultados: listo para ejecutar, listo con limitaciones explícitas o requiere rediseño. Una aprobación formal del documento no demuestra validez estadística.

## 2. Pregunta y alcance

- [ ] Se distingue experimento aleatorizado, intervención no aleatorizada y observación.
- [ ] La población objetivo y la población accesible están identificadas.
- [ ] Existe una respuesta principal con escala y momento definidos.
- [ ] El estimando y el contraste principal responden a la pregunta científica.
- [ ] Superioridad, estimación, equivalencia, no inferioridad o factibilidad están diferenciadas.
- [ ] Los objetivos secundarios y exploratorios no se presentan como confirmatorios por defecto.
- [ ] El comparador es pertinente; no se exige un grupo sin tratamiento cuando un comparador activo responde mejor o es éticamente necesario.

## 3. Unidades y asignación

- [ ] Se identifican unidad experimental, unidad de observación y unidad de muestreo.
- [ ] n se informa por tratamiento y por cada nivel de asignación.
- [ ] Submuestras, lecturas técnicas y momentos no inflan la replicación del tratamiento.
- [ ] Se evaluaron contaminación, interferencia y aplicación compartida.
- [ ] Los bloques se definieron antes de asignar y la composición permite el diseño anunciado.
- [ ] Bloques, predictores categóricos y covariables continuas no se confunden.
- [ ] Ningún tratamiento queda perfectamente confundido con cámara, día, máquina, aula o lote sin reconocerlo.
- [ ] En parcelas divididas hay dos asignaciones y los identificadores conservan la jerarquía.
- [ ] En un cruzado se justifican secuencias, períodos, estabilidad y lavado.
- [ ] Se documentan procedimiento, restricciones, lista inicial y resultado de la asignación.
- [ ] Para generación computacional se archivan semilla y algoritmo o versión; para sorteo físico se conserva el registro pertinente.
- [ ] Ocultación, cegamiento y aleatorización se describen como procedimientos distintos.

## 4. Tamaño y recursos

- [ ] El tamaño se justifica por potencia, precisión o factibilidad explícita.
- [ ] La diferencia relevante y la variabilidad tienen fundamento y unidades compatibles.
- [ ] No se usan 12 grados de libertad ni 3 réplicas como umbrales universales.
- [ ] Se especifican alfa, potencia o ancho de intervalo y su justificación.
- [ ] Se distingue potencia global ANOVA de potencia para un contraste o interacción.
- [ ] Para bloques, conglomerados, parcelas divididas o seguimiento se considera la estructura real.
- [ ] En pares se usa la variabilidad de diferencias o una correlación justificada.
- [ ] Se evaluó sensibilidad a parámetros inciertos, sin inventar fuentes.
- [ ] Pérdidas y redondeos se aplican al nivel correcto y el total coincide con la suma por grupos.
- [ ] El presupuesto y el calendario permiten realizar las unidades previstas.
- [ ] Una restricción de recursos no se oculta cambiando silenciosamente la potencia o el efecto de interés.

## 5. Medición y análisis

- [ ] Cada variable tiene definición, unidad, instrumento, momento y derivación.
- [ ] Se prevén calibración, control de calidad y registro de fallos.
- [ ] El modelo incluye la dependencia y los estratos de error pertinentes.
- [ ] Se justifican efectos fijos, aleatorios, distribución y enlace.
- [ ] Los contrastes primarios y la familia de multiplicidad están definidos.
- [ ] Las interacciones se interpretarán por magnitud, incertidumbre y escala, no solo mediante un umbral de p.
- [ ] Los efectos marginales tienen ponderación y población de referencia explícitas.
- [ ] Los diagnósticos no se reducen a una prueba de normalidad.
- [ ] Las alternativas robustas, transformaciones o modelos alternativos tienen fundamento.
- [ ] Las reglas de atípicos y exclusiones no dependen de conseguir significancia.
- [ ] El tratamiento de faltantes tiene supuestos y sensibilidad apropiados.
- [ ] Permutaciones o remuestreo respetan bloques, conglomerados y jerarquía.
- [ ] Se informarán estimaciones e intervalos, evitando equiparar no significancia con equivalencia.

## 6. Identificación cuasiexperimental

- [ ] El contrafactual y la regla de exposición o asignación están descritos.
- [ ] Se distinguen supuestos causales de supuestos del modelo estadístico.
- [ ] Hay una justificación de tendencias paralelas, continuidad o estabilidad temporal, según el método.
- [ ] Se consideran historia, selección, regresión a la media, contaminación y cambios de medición.
- [ ] El ajuste por variables medidas no se presenta como eliminación de toda confusión.
- [ ] La cantidad de individuos no oculta un número insuficiente de grupos para la inferencia propuesta.
- [ ] El alcance causal y las amenazas no resueltas quedan explícitos.

## 7. Ética y reproducibilidad

- [ ] Se verificó revisión ética, aprobación o exención según normativa y población.
- [ ] En humanos se documentan consentimiento o dispensa autorizada y protección de datos.
- [ ] En animales se documentan bienestar, autorización y las 3R cuando corresponde.
- [ ] Permisos ambientales, bioseguridad y manejo de residuos están previstos si aplican.
- [ ] No se inventaron números de aprobación, referencias ni versiones de software.
- [ ] El plan tiene fecha, versión y procedimiento de enmiendas.
- [ ] Se archivan diccionario, asignación y reglas de transformación sin exponer información sensible.
- [ ] Los comandos apuntan a archivos existentes y se declaran dependencias.
- [ ] Se distingue código ejecutado y validado de borrador no probado.
- [ ] El croquis representa todas las unidades del CSV y no redefine la disposición física sin documentarlo.

## 8. Motivos para detener y revisar

Requieren resolver o limitar el alcance antes de ejecutar: confusión perfecta tratamiento-unidad superior, imposibilidad de estimar el contraste principal, falta de autorización necesaria o intervención no viable. No se arreglan aumentando submuestras ni cambiando la prueba.

Una muestra pequeña, incertidumbre de parámetros o limitaciones de generalización requieren evaluación específica, no rechazo automático. Si se aceptan, explicá qué conclusiones serán posibles y cuáles no.

**Acta breve de cierre.** «Estado: [resultado]. Evidencia revisada: [archivos y versión]. Pendientes: [lista o ninguno]. Limitaciones aceptadas: [alcance]. Verificaciones realizadas: [métodos y salidas]. No verificado: [aspectos pendientes]».
