# Plan de análisis previo

## 1. Partir del estimando

Un plan no es una lista de pruebas. Definí qué cantidad se quiere estimar: diferencia media al final, cambio respecto del inicio, razón de riesgos, efecto de una dosis, interacción o diferencia de rendimiento sobre una población de tareas.

Para cada objetivo completá: población, variable, escala, momento, comparador, resumen o contraste, unidad de asignación, modelo e intervalo. Marcá cuáles son confirmatorios y cuáles exploratorios. No todos los objetivos descriptivos necesitan una prueba de hipótesis.

En intervenciones con abandono, rescate o falta de adherencia, especificá qué resultado interesa pese a esos eventos. El conjunto de datos disponible no debe definir retrospectivamente el estimando.

## 2. Estructura de datos

Prepará un diccionario con identificadores únicos, tratamiento asignado y recibido, bloque, unidad superior, subunidad, tiempo, respuesta, denominador o exposición, covariables basales y razones de faltantes. Una fila representa una observación definida, no necesariamente una réplica independiente.

Conservá datos originales y reglas de derivación. Predefiní unidades, rangos plausibles, duplicados, límites de detección y conversiones. Separá una medición errónea de un valor extremo biológicamente posible.

## 3. Correspondencia diseño-modelo

Las expresiones siguientes son plantillas conceptuales, no código ejecutable ni una elección universal de efectos aleatorios.

| Diseño o respuesta | Modelo inicial | Punto crítico |
|---|---|---|
| DCA, respuesta continua | `y = mu + tratamiento + error` | Independencia y varianzas; considerar Welch si corresponde |
| DBCA | `y = mu + tratamiento + bloque + error` | Bloque fijo o aleatorio justificado; respetar asignación |
| Cuadrado latino | `y = mu + tratamiento + fila + columna + error` | Aditividad y limitada estimación de interacciones |
| Factorial A×B | `y = mu + A + B + A:B + error` | Añadir estructura de bloques o jerarquía real |
| Parcelas divididas en bloques | `y = mu + bloque + A + B + A:B + u_parcela + error` | `u_parcela` identifica parcela grande dentro de bloque |
| Seguimiento longitudinal | `y = tratamiento + tiempo + tratamiento:tiempo + dependencia` | Correlación y forma temporal explícitas |
| Resultado binario | Modelo binomial con enlace apropiado | Distinguir odds ratio, riesgo y diferencia de riesgos |
| Conteo con exposición | Poisson o binomial negativa con offset de exposición | Sobredispersión, ceros y dependencia |
| Tiempo hasta evento | Modelo de supervivencia pertinente | Censura, riesgos competitivos y escala del efecto |

Una proporción basada en éxitos sobre ensayos requiere su denominador; una fracción continua entre 0 y 1 no es automáticamente binomial. Datos acotados, ordinales o censurados requieren una familia coherente con su generación.

En parcelas divididas, el factor A no se prueba contra el error de observaciones individuales. En diseños desbalanceados, usá inferencia del modelo con método de grados de libertad documentado, por ejemplo Satterthwaite o Kenward-Roger cuando esté disponible y sea pertinente. No apliques fórmulas balanceadas después de perder unidades sin revisar.

## 4. Contrastes e interacciones

Escribí el contraste principal antes de medir: por ejemplo, diferencia entre dosis alta y control, tendencia lineal según dosis reales o diferencia de diferencias entre niveles de A y B. Para dosis desigualmente espaciadas, no uses coeficientes que presupongan igual separación sin justificación.

Con interacción, mostrá predicciones por combinación, efectos simples y sus intervalos cuando respondan la pregunta. Un efecto marginal promedia sobre niveles del otro factor; explicá si se pondera por igual o por una población objetivo. En modelos no lineales, la interacción depende de la escala del enlace o de respuesta.

No retires automáticamente interacciones por p > 0,05 ni concluyas que hay interacción porque un efecto es significativo en un subgrupo y no en otro. Compará los efectos directamente. Conservá términos inferiores cuando son necesarios para interpretar una interacción incluida.

## 5. Multiplicidad

Definí la familia de inferencias. Para todas las comparaciones por pares, Tukey puede ser adecuado bajo su modelo; para varios tratamientos contra un control, Dunnett; para una familia general de pruebas, Holm es una opción de control del error familiar. En exploración de muchas señales puede interesar controlar FDR, declarando su alcance.

Un contraste primario preespecificado no siempre requiere un ANOVA global significativo como puerta de entrada. Tampoco una prueba global autoriza todas las comparaciones sin ajuste. La estrategia depende de las hipótesis y de cómo se controlará el error.

Informá estimaciones, intervalos, p y escala del efecto. No traduzcas p > alfa como «sin efecto» ni p < alfa como «importancia práctica demostrada». Para equivalencia, predefiní márgenes y método específico.

## 6. Diagnósticos y alternativas

Evaluá residuos frente a predichos, dispersión por grupo, colas, observaciones influyentes y patrones temporales o espaciales. La independencia se sustenta principalmente en el diseño; no se demuestra con Shapiro-Wilk.

No uses una prueba de normalidad como interruptor automático entre ANOVA y Kruskal-Wallis. Considerá tamaño, balance, tipo de respuesta, magnitud de desviaciones y estimando. Kruskal-Wallis no es una prueba universal de medianas y no repara dependencia.

Ante heterocedasticidad, considerá modelar varianzas, Welch en casos simples o inferencia robusta adecuada. Ante correlación, especificá estructuras mixtas, marginales o errores por conglomerado con correcciones apropiadas. Pocos conglomerados limitan las aproximaciones asintóticas.

Una prueba por permutaciones debe reproducir la asignación: dentro de bloques, por conglomerados o por secuencias según corresponda. Un bootstrap debe remuestrear el nivel de independencia, no hojas o lecturas ignorando su agrupación.

## 7. Faltantes y atípicos

Predefiní razones de exclusión verificables, idealmente evaluadas sin conocer tratamiento. Conservá trazabilidad de correcciones y exclusiones. No elimines observaciones solo porque cambian la significancia.

Describí faltantes por grupo, momento y causa. Un análisis de casos completos puede sesgar; un modelo mixto o imputación múltiple requiere supuestos, a menudo MAR condicional a información incluida, y un modelo adecuado. Ninguno garantiza validez ante faltantes informativos.

La imputación debe respetar jerarquía, interacciones y variables del análisis. Evitá reemplazar por la media o arrastrar la última observación por defecto. Prevé sensibilidad ante supuestos MNAR cuando el abandono pueda depender de resultados no observados.

## 8. Entregable reproducible

1. Tabla objetivo-estimando-variable-modelo-contraste.
2. Diccionario de datos y reglas de derivación y exclusión.
3. Modelo principal, covariables basales y estructura de dependencia.
4. Diagnósticos y alternativas justificadas, con criterios de decisión.
5. Estrategia de multiplicidad, faltantes y sensibilidad.
6. Software, versiones, semilla cuando corresponda y estado de validación del código.
7. Fecha y versión del plan, con registro posterior de enmiendas.

Si el software elegido no implementa un método requerido, indicá la limitación en lugar de sustituirlo silenciosamente por un ANOVA más simple. Ver `seleccion-de-diseno.md` y `unidad-experimental.md` antes de cerrar el modelo.
