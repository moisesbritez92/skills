# Salud y nutrición

## 1. Delimitar la pregunta clínica

Definí población, intervención, comparador, desenlace y momento, junto con el efecto que cambiaría una decisión clínica o de salud pública. Distinguí eficacia, efectividad, seguridad, factibilidad y adherencia.

Un ensayo no necesita siempre placebo: un tratamiento activo o la atención habitual pueden ser el comparador pertinente. La elección requiere fundamento clínico y ético. No retires atención eficaz solo para obtener un control «puro».

## 2. Elegir la unidad y el diseño

| Situación | Diseño candidato | Riesgo principal |
|---|---|---|
| Intervención individual sin contaminación importante | Paralelo aleatorizado | Pérdidas o desviaciones de asignación |
| Programa entregado por centro, escuela o comunidad | Aleatorización por conglomerados | Pocos grupos, ICC y contaminación |
| Efectos reversibles y condición estable | Cruzado con secuencias aleatorizadas | Arrastre, período y abandono |
| Seguimiento de la misma persona | Estructura longitudinal sobre el diseño base | Dependencia y faltantes |
| Implementación no aleatorizada | Estrategia cuasiexperimental justificada | Confusión y tendencias temporales |

Los centros preexistentes pueden aleatorizarse; su existencia no obliga a un diseño cuasiexperimental. Si se aleatoriza una familia y la dieta se comparte, sus integrantes no son asignaciones independientes.

En nutrición, precisá dosis, composición, sustituciones, duración, suministro y verificación de consumo. Comparar alimentos puede implicar diferencias de energía total, sabor y adherencia; definí qué se mantiene constante y qué forma parte de la intervención.

## 3. Asignación, ocultación y cegamiento

La generación aleatoria crea la secuencia. La ocultación impide anticipar la próxima asignación antes de incorporar a la persona. El cegamiento limita conocimiento después de asignar. Ninguno sustituye a los otros.

Predefiní razón de asignación y estratos basales relevantes, evitando demasiados estratos pequeños. Si se usan bloques permutados, protegé sus tamaños y la secuencia frente a quienes reclutan. Una semilla pública antes de cerrar la asignación puede hacer predecible el plan; archivarla no exige publicarla durante el reclutamiento.

Indicá quién genera, quién recluta y quién asigna. Si no es viable cegar participantes o aplicadores, evaluá medición objetiva, evaluadores cegados y análisis con códigos protegidos. No llames «doble ciego» a un procedimiento sin describir roles.

## 4. Desenlace y estimando

Elegí un desenlace principal con instrumento validado para la población y momento predefinido. Múltiples escalas y tiempos aumentan oportunidades de selección; fijá qué inferencia será confirmatoria.

Definí cómo se interpretarán abandono, tratamiento de rescate, cambio de dieta, cirugía u otros eventos posteriores. El enfoque de intención de tratar conserva la comparación por asignación, pero no determina por sí solo cómo imputar faltantes o definir el resultado tras un evento.

Un análisis por protocolo puede complementar, pero excluir no adherentes sin más puede introducir sesgo. Si interesa el efecto bajo adherencia, especificá estimando, supuestos y método; no lo presentes como equivalente al efecto de asignación.

Para un resultado continuo final, ANCOVA con ajuste basal preespecificado suele ser útil. Analizar cambios también puede responder una pregunta válida; elegí según estimando, medición y eficiencia, no según cuál p resulte menor.

## 5. Tamaño de muestra

La diferencia relevante debe tener significado clínico, no solo estadístico. Para no inferioridad o equivalencia, justificá margen y método; un resultado no significativo de superioridad no basta.

En conglomerados, necesitás número de centros, tamaños, ICC y variación de tamaños. El efecto de diseño simple puede orientar, pero no corrige inferencia basada en muy pocos centros. En cruzados, usá variabilidad intraindividual y contemplá pares o secuencias incompletos.

Para eventos raros, supervivencia, diseños adaptativos o interinos, recurrí a un cálculo específico. Los casos simples de `tamano_muestral.py` no cubren estos diseños. Una revisión de resultados intermedia exige reglas de parada y control de error acordes, no mirar cada semana hasta alcanzar p < 0,05.

## 6. Medición y seguimiento

Estandarizá horarios, ayuno, postura, equipos, entrenamiento y condiciones pertinentes. En ingesta dietaria, diferenciá variación diaria, error de recuerdo y cambio real; varios recordatorios de una persona no crean más participantes.

Registrá adherencia, exposición concomitante, eventos adversos y razones de pérdida sin convertirlos automáticamente en covariables de ajuste. Algunos son mediadores de la intervención, y ajustarlos puede cambiar el efecto estimado.

Predefiní procedimientos de contacto y seguimiento proporcionados al riesgo y a la privacidad. Inflar el n por pérdidas no elimina sesgo por abandono diferencial; el plan debe incluir análisis de sensibilidad cuando corresponda.

## 7. Ética y reporte

Verificá revisión por el comité competente antes del inicio, consentimiento informado o dispensa autorizada, capacidad para consentir, asentimiento cuando corresponda y protección de datos. Una exención debe provenir de la instancia competente, no de una decisión informal del investigador.

Documentá registro prospectivo del ensayo cuando sea aplicable, antes de incorporar al primer participante según los requisitos pertinentes. Describí vigilancia de seguridad, acceso a atención y reglas de suspensión proporcionales al riesgo. No inventes números de registro o aprobación.

CONSORT orienta el reporte de ensayos aleatorizados; SPIRIT, el contenido de protocolos. Usá la versión y extensión pertinentes, por ejemplo para conglomerados, cruzados o pilotos. Son guías de reporte, no sustitutos de diseño, aprobación ética ni análisis válido.

Documentación localizable en EQUATOR: [CONSORT](https://www.equator-network.org/reporting-guidelines/consort/) y [SPIRIT](https://www.equator-network.org/reporting-guidelines/spirit-2013-statement-defining-standard-protocol-items-for-clinical-trials/). Comprobá la versión vigente y sus metadatos antes de incorporarla como referencia formal; la ruta histórica no determina qué edición debe citarse.

## 8. Salida mínima

Entregá criterios de selección, tabla de intervenciones, cronograma de evaluaciones, unidad de asignación, secuencia protegida, justificación muestral y plan de análisis. Incluí un flujo previsto de participantes y responsables de seguridad y datos.

Antes de cerrar, verificá coherencia entre registro, protocolo y desenlace principal. Para estudios no aleatorizados, consultá `../cuasiexperimentales.md`; para dependencia y faltantes, `../plan-de-analisis.md`.
