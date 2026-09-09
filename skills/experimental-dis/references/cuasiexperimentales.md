# Diseños cuasiexperimentales

## 1. Clasificar sin prometer causalidad

Una intervención no aleatorizada puede evaluarse con comparaciones cuasiexperimentales si existe una estrategia defendible para aproximar el contrafactual. El nombre del diseño no elimina confusión, selección ni cambios temporales.

Un grupo ya formado puede ser aleatorizado como conglomerado. No clasifiques automáticamente escuelas, hospitales o comunidades como cuasiexperimentales. Si no se asigna intervención, describí el estudio observacional; algunas estrategias siguientes también se aplican a políticas o experimentos naturales cuya asignación no controla el investigador.

Antes de elegir, preguntá quién recibe la intervención, mediante qué regla, cuándo comienza, qué información previa existe y qué grupo o trayectoria aproxima lo que habría ocurrido sin ella.

## 2. Elegir una estructura

| Datos y asignación | Estrategia candidata | Supuesto decisivo |
|---|---|---|
| Un grupo antes y después | Comparación pre-post descriptiva | No separa intervención de historia o maduración |
| Intervenidos y comparables, antes y después | Diferencias en diferencias | Tendencias contrafactuales paralelas |
| Serie con inicio conocido | Serie temporal interrumpida | Ausencia de cambios simultáneos que expliquen la ruptura |
| Elegibilidad por umbral | Discontinuidad en la regresión | Continuidad cerca del corte y ausencia de manipulación relevante |
| Una unidad tratada y varios donantes | Control sintético | Donantes pertinentes y buen contrafactual preintervención |
| Grupos seleccionados por variables medidas | Ajuste, emparejamiento o ponderación | Intercambiabilidad condicional y positividad |

No elijas el método por cuál entrega una p pequeña. Si falta información para sostener la identificación, reducí el alcance a asociación o descripción y explicitá la limitación.

## 3. Pre-post y diferencias en diferencias

Una mejora dentro del grupo tratado puede deberse a recuperación espontánea, aprendizaje, regresión a la media o cambios externos. Comparar dos p de pruebas pre-post, una por grupo, no prueba que las mejoras difieran.

Con dos grupos y dos momentos, el estimando básico es:

`DiD = (media_tratado_post - media_tratado_pre) - (media_control_post - media_control_pre)`

Un modelo lineal simple incluye grupo, período y su interacción. La inferencia debe reconocer seguimiento de individuos y nivel de asignación o exposición. Una comunidad tratada y otra control no se convierten en muchas réplicas causales por incluir cientos de residentes.

Justificá tendencias paralelas sin intervención, ausencia de anticipación, estabilidad de composición y ausencia de contaminación relevante. Varios momentos previos ayudan a evaluar plausibilidad, pero una prueba no significativa de pre-tendencias no demuestra el supuesto.

Con adopción escalonada y efectos heterogéneos, una regresión estándar de efectos fijos de unidad y tiempo puede mezclar comparaciones inadecuadas. Elegí un estimador de efectos por cohorte y período compatible con la pregunta. No extrapoles automáticamente la fórmula de dos períodos.

## 4. Serie temporal interrumpida

Predefiní fecha de intervención, demora esperada y si interesa un cambio de nivel, pendiente o ambos. Un modelo segmentado orientativo es:

`y_t = beta0 + beta1·tiempo + beta2·post + beta3·tiempo_desde_intervencion + error_t`

La variable `tiempo_desde_intervencion` vale cero antes del cambio. Definí claramente la codificación en el punto de corte. Para tasas o conteos, incorporá distribución, denominador o exposición apropiados.

Modelá autocorrelación, estacionalidad, cambios de medición y otras políticas. Una serie control puede fortalecer la comparación si comparte shocks relevantes sin recibir la intervención. Elegir suficientes puntos antes y después requiere considerar frecuencia, ciclos y potencia por simulación; no hay un mínimo universal que garantice identificación.

No selecciones la fecha de ruptura buscando el máximo efecto si la hipótesis confirmatoria era una intervención con fecha conocida. Una exploración de cambios desconocidos debe declararse como tal.

## 5. Discontinuidad en la regresión

Documentá variable de asignación, umbral, cumplimiento de la regla y efecto local de interés. Distinguí diseño nítido, donde el corte determina tratamiento, de difuso, donde cambia su probabilidad.

Evaluá manipulación o acumulación cerca del umbral, continuidad de covariables basales y otras reglas que cambien en el mismo punto. Especificá ventana, modelo local y sensibilidad a anchos de banda. Evitá polinomios globales de alto grado como opción automática.

El resultado se refiere a unidades cercanas al corte. En un diseño difuso, la interpretación requiere supuestos instrumentales adicionales, como exclusión y monotonicidad. No lo presentes como efecto medio de toda la población.

## 6. Ajuste y control sintético

Seleccioná confusores por conocimiento causal y temporalidad, no solo por asociación estadística. Ajustar por mediadores o colisionadores puede introducir sesgo. Usá un esquema causal cuando ayude a explicitar qué se asume.

Emparejamiento y ponderación por puntaje de propensión requieren solapamiento y confusores medidos suficientes. Revisá balance con diferencias estandarizadas y distribución de pesos, no solo p. Definí si el objetivo es ATE, ATT u otra población y registrá qué unidades quedan fuera. No eliminan confusión no medida.

Para control sintético, justificá donantes no afectados, variables y período de ajuste, desempeño previo y análisis de sensibilidad a donantes. Un ajuste previo excelente ayuda, pero no garantiza que el contrafactual posterior sea válido. Las comparaciones placebo necesitan un conjunto de referencia defendible.

## 7. Amenazas y acciones

| Amenaza | Acción de diseño o análisis | Límite que persiste |
|---|---|---|
| Selección basal | Comparador pertinente, medición de confusores | Variables no medidas |
| Historia y estacionalidad | Series previas, controles contemporáneos | Shocks diferenciales |
| Regresión a la media | Varias mediciones basales, criterio de selección explícito | Selección por extremos |
| Cambio de instrumento | Calibración y protocolo constante | Rupturas no documentadas |
| Contaminación | Medir exposición y relaciones entre grupos | Interferencia no registrada |
| Abandono diferencial | Seguimiento y sensibilidad de faltantes | Dependencia de resultados no observados |

## 8. Redacción y dimensionamiento

Escribí «se estimará el efecto bajo los supuestos de…» si hay una estrategia causal defendible, o «se compararán cambios asociados con…» cuando corresponda. No uses «se demostró causalidad» por obtener significancia tras ajuste.

Dimensioná para el estimador real, considerando número de grupos, períodos, correlación serial y pérdidas. El script de ANOVA de una vía no calcula potencia de DiD, discontinuidad ni series interrumpidas. Entregá supuestos de identificación separados de supuestos estadísticos, más análisis de sensibilidad y amenazas no resueltas.
