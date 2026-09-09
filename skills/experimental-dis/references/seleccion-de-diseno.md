# Selección del diseño

## Contenido

1. Árbol de decisión
2. Catálogo de diseños
3. Cuántas repeticiones hacen falta
4. Errores frecuentes al elegir

---

## 1. Árbol de decisión

Respondé todas las preguntas: estructura de tratamientos, restricciones de asignación y seguimiento son dimensiones combinables. Un factorial puede estar bloqueado y tener medidas repetidas.

**P1. ¿Cuántos factores se manipulan?**
Uno, seguí en P2. Dos o más, considerá un arreglo factorial para estimar efectos principales y las interacciones relevantes. Una variable de molestia no se convierte automáticamente en bloque: el bloqueo requiere formar conjuntos antes de aleatorizar dentro de ellos. También puede ajustarse como predictor categórico o covariable continua.

**P2. ¿Hay alguna fuente de variación conocida, ajena al tratamiento, que afecte la respuesta?**
Ejemplos: pendiente o fertilidad del terreno, estante de la incubadora, día de procesamiento, operario, lote de reactivo, camada, turno del hospital, máquina donde corre el benchmark.

- Sin restricción de asignación: **DCA**, aun con heterogeneidad, que puede reducir precisión.
- Se pueden formar conjuntos comparables que admiten todos los tratamientos: **DBCA**. Si no caben todos, considerar bloques incompletos conectados.
- Hay dos fuentes cruzadas con tantos niveles como tratamientos y una disposición compatible: **cuadrado latino**, evaluando su supuesto aditivo.
- Hay otras estructuras: considerar diseños fila-columna, bloques cruzados o anidados y modelos acordes. Una variable continua basal puede entrar como covariable; un operario o lote no se vuelve continuo por codificarlo con números. Ajustar después no recrea un bloqueo ausente.

**P3. ¿Todos los tratamientos se pueden asignar a unidades del mismo tamaño?**
Si A se asigna a unidades grandes y B se aleatoriza a subunidades dentro de ellas, es **parcelas divididas**. Si solo hay un factor aplicado a sectores, cámaras o aulas, puede ser un DCA o DBCA de esas unidades, con submuestreo. La escala de aplicación por sí sola no implica parcelas divididas.

**P4. ¿Cada unidad recibe un solo tratamiento?**
Medir varias veces una unidad introduce **medidas repetidas**, aunque siempre reciba el mismo tratamiento. Si recibe tratamientos sucesivos mediante secuencias asignadas, considerá un **cruzado** y justificá estabilidad, períodos y control del arrastre.

**P5. ¿Cuántas unidades hay disponibles de verdad?**
Evaluá potencia o precisión para el contraste de interés con los recursos reales. Si son insuficientes, revisá niveles, factores, medición y alcance. No sustituyas esta evaluación por un mínimo universal de réplicas; tampoco elimines un factor indispensable para responder la pregunta.

---

## 2. Catálogo de diseños

### Completamente aleatorizado (DCA)

**Cuándo.** Es viable asignar libremente los tratamientos a unidades del mismo nivel. La homogeneidad ayuda a la precisión, pero no es requisito de validez de la aleatorización.

**Modelo.** `y_ij = μ + τ_i + ε_ij`, donde `τ_i` es el efecto del tratamiento i.

**Grados de libertad.** En el modelo clásico balanceado con t tratamientos y r réplicas por tratamiento: tratamientos `t-1`, error `t(r-1)`, total `tr-1`. Sin balance, el error es `N-t` si el modelo tiene rango completo.

**Ventajas.** Es simple y admite número desigual de repeticiones por tratamiento. Para igual N y estructura de tratamientos, el modelo sin bloques reserva más grados de libertad residuales, aunque eso no garantiza mayor precisión.

**Precaución.** Una fuente basal predictiva puede justificar bloqueo o ajuste por covariables preespecificadas. El DCA no queda invalidado por heterogeneidad; revisá varianzas, dependencia y precisión.

### Bloques completos al azar (DBCA)

**Cuándo.** Se forman bloques antes de asignar y cada bloque puede incluir todos los tratamientos. Si hay un único día por tratamiento, día y tratamiento quedan confundidos: agregar día al modelo no resuelve el problema. Si cada tratamiento se asigna a varios días, estos pueden ser unidades experimentales, no bloques completos.

**Modelo.** `y_ij = μ + τ_i + β_j + ε_ij`, con `β_j` el efecto del bloque j.

**Grados de libertad.** Tratamientos `t-1`, bloques `r-1`, error `(t-1)(r-1)`.

**Ventajas.** Puede reducir la variación residual cuando el bloque predice la respuesta. El balance entre reducción de varianza y grados de libertad determina la ganancia.

**Reglas.** En el DBCA elemental cada bloque contiene cada tratamiento una vez y se aleatoriza dentro de cada bloque. Se busca similitud interna, sin exigir diferencias observadas entre bloques. Con una observación por celda no se separan interacción tratamiento×bloque y error puro; la prueba clásica usa el modelo aditivo. Las fórmulas anteriores no se trasladan sin cambios a datos faltantes o estructuras más complejas.

**Nota de interpretación.** Informá cómo se modeló el bloque, como fijo o aleatorio según el objetivo y la población de referencia. Su variación puede reportarse; no es automáticamente un efecto causal ni la hipótesis principal.

### Cuadrado latino

**Cuándo.** Dos fuentes de variación cruzadas, por ejemplo gradiente en dos direcciones del terreno, u orden de corrida cruzado con operario.

**Modelo.** `y_ijk = μ + τ_i + φ_j + γ_k + ε_ijk`, con fila y columna.

**Grados de libertad.** En un cuadrado completo bajo el modelo aditivo, error `(t-1)(t-2)`. Con t = 3 quedan 2: la varianza se estima con poca precisión, pero la prueba no es matemáticamente inválida por ello. Con t = 2 no hay error residual para la prueba F clásica.

**Precaución.** Las interacciones no se estiman separadamente en un único cuadrado. Si son plausibles y relevantes, revisá la estructura o replicá cuadrados con asignaciones independientes y modelo explícito. Aleatorizá etiquetas, filas y columnas dentro de las restricciones, documentando el procedimiento.

### Factorial

**Cuándo.** Interesa estimar efectos de dos o más factores, con o sin interacción como objetivo principal. La interacción expresa que el efecto de uno depende del otro en la escala del modelo; conviene preverla cuando sea científicamente relevante.

**Modelo, dos factores en DBCA.** `y_ijk = μ + α_i + β_j + (αβ)_ij + ρ_k + ε_ijk`.

**Notación.** Un factorial `a×b` tiene `a·b` combinaciones, y cada combinación es un tratamiento. Con 3 repeticiones, un 3×4 son 36 unidades.

**Reglas.** El arreglo factorial describe la estructura de tratamientos, pero no especifica por sí solo la asignación ni los errores. Indicá si se implementa con DCA, DBCA, parcelas divididas u otra estructura compatible. La expresión "diseño factorial" es habitual, pero necesita esa información para reconstruir el experimento.

**Interpretación.** Mostrá efectos simples y sus intervalos cuando la heterogeneidad sea importante. Los efectos marginales pueden interpretarse como promedios con ponderaciones explícitas, no como efectos constantes. Una p grande de interacción no demuestra aditividad, especialmente con poca potencia; una p pequeña no vuelve inútil todo promedio.

### Parcelas divididas

**Cuándo.** A se asigna a unidades grandes y B a subunidades dentro de ellas, generalmente por restricciones físicas o logísticas. Un único factor aplicado a unidades grandes no basta para definir este diseño.

**Modelo.** Dos términos de error: `ε_a` para la parcela grande y `ε_b` para la subparcela.
`y_ijk = μ + ρ_k + α_i + ε_a(ik) + β_j + (αβ)_ij + ε_b(ijk)`.

**Asignación.** En r bloques, aleatorizá los a niveles de A entre parcelas grandes de cada bloque y los b niveles de B entre subparcelas de cada parcela grande. Conservá identificadores únicos para ambos niveles. Hay `r·a` parcelas grandes y `r·a·b` subparcelas, no ese último número de réplicas independientes de A.

**Precisión.** En el caso balanceado clásico, A usa el error de parcela grande, con `(r-1)(a-1)` grados de libertad; B y A×B usan el error de subparcela, con `a(r-1)(b-1)`. Son fórmulas para esta estructura concreta, no para cualquier diseño jerárquico. El modelo mixto representa parcela grande dentro de bloque y la variación residual de subparcela.

**Decisión práctica.** La logística determina qué factor va arriba. Si hay libertad de elección, compará precisión y costos para los contrastes prioritarios. A suele disponer de menos información independiente; más subparcelas no sustituyen más parcelas grandes. Una sola cámara por temperatura confunde temperatura y cámara, aunque se midan muchas plantas.

**Error frecuente.** Analizarlo como si todos los factores se asignaran al mismo nivel. Los estratos de error son distintos; ignorar la correlación de parcela grande puede subestimar incertidumbre e inflar falsos positivos para A.

### Medidas repetidas

**Cuándo.** El mismo sujeto, parcela o servidor se mide en varios momentos.

**Problema.** Las observaciones de una unidad suelen estar correlacionadas. Pueden conservarse como filas separadas si el modelo representa esa dependencia; no deben analizarse como réplicas independientes del tratamiento.

**Análisis previsto.** ANOVA de medidas repetidas cuando sus condiciones sean adecuadas, con corrección de esfericidad si procede, o modelo mixto con estructura temporal justificada. Un intercepto aleatorio impone una correlación específica, no resuelve cualquier trayectoria. El manejo de faltantes depende de supuestos explícitos, no solo del software.

### Cruzado

**Cuándo.** Cada sujeto recibe los dos tratamientos en secuencia aleatoria. Frecuente en ensayos clínicos de fase temprana y en pruebas sensoriales.

**Requisito.** Efecto de arrastre despreciable, o un período de lavado suficientemente largo, que hay que justificar.

**Ventaja.** La comparación intraunidad puede aumentar precisión si la correlación es favorable. Incluí período, tratamiento y dependencia del sujeto, y evaluá secuencia según el diseño. No prometas una reducción fija del n ni uses un test de arrastre no significativo como garantía de ausencia de arrastre.

**Cuándo no.** Enfermedades o procesos que cambian de forma irreversible entre períodos.

### Factorial fraccionado y superficie de respuesta

**Cuándo.** Fase de tamizaje con muchos factores, o ajuste fino de una respuesta sobre variables continuas.

**Advertencia.** En un fraccionado declará generadores, resolución y estructura de alias, sin asumir despreciables interacciones importantes. En superficie de respuesta justificá región experimental, puntos centrales, capacidad de estimar curvatura y corridas de validación. Su pertinencia depende de la pregunta y los recursos, no del grado académico.

---

## 3. Cuántas repeticiones hacen falta

No hay mínimos universales de 12 grados de libertad ni de 3 réplicas. Distinguí identificabilidad del efecto, posibilidad de estimar el error, precisión de esa estimación y potencia para el contraste previsto. Dos réplicas pueden permitir una prueba en algunas estructuras, aunque con incertidumbre alta; tres no garantizan un ensayo informativo.

**Ejemplo.** Con 4 tratamientos y r bloques completos, el error clásico tiene `3(r-1)` grados de libertad. Con 3 bloques son 6 y con 5 son 12. Ninguno de esos números decide por sí solo si se detectará la diferencia relevante: también importan la varianza residual, el contraste y alfa.

**Dimensionamiento.** Usá `tamano-muestral.md`. Para factoriales, dimensioná el efecto o interacción prioritarios; para parcelas divididas, los dos estratos; para medidas repetidas, las correlaciones y el seguimiento. La potencia global de un ANOVA de una vía no sustituye estos cálculos.

Si los recursos son fijos, estimá precisión o efecto mínimo detectable bajo escenarios plausibles. Podés revisar niveles, mejorar medición, bloquear cuando tenga fundamento o limitar el objetivo a factibilidad. No cambies silenciosamente la potencia ni la diferencia relevante para justificar el presupuesto. Declarar baja potencia no elimina sesgos ni confusión estructural.

---

## 4. Errores frecuentes al elegir

**Confundir función en el diseño y en el análisis.** Un bloque controla la asignación; una covariable ajusta el modelo. Una variable puede tener interés secundario, pero eso no le confiere aleatorización ni exige incluir todas las interacciones posibles.

**Elegir factorial por costumbre.** Justificá los factores por sus efectos o interacciones de interés y verificá su costo en unidades y precisión.

**Bloquear sin fundamento.** Un bloqueo poco predictivo puede consumir grados de libertad sin mejorar precisión. Evaluá también sus razones operativas o de balance, sin eliminarlo retrospectivamente solo por una p grande.

**Ignorar el orden temporal.** Día o corrida pueden servir de bloques si la asignación lo permite. Distribuí tratamientos entre ellos y registrá orden; no supongas que agregar un predictor elimina una confusión perfecta.

**Confundir repetición con submuestra.** Ver `unidad-experimental.md`. Es el error que más caro sale.

**Proponer un diseño que la restricción física no permite.** Si el riego llega por sector, aleatorizá y replicá sectores. Pueden organizarse en DBCA; habrá parcelas divididas si además se asigna otro factor a subunidades dentro de ellos.
