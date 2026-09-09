# Informática e ingeniería

## 1. Definir qué población representa el experimento

Precisá si interesa rendimiento en una máquina concreta, generalización a tareas nuevas, comportamiento de usuarios o calidad de una población de piezas. Un benchmark reproducible no es automáticamente representativo de todos los sistemas de producción.

Definí factor, configuración, métrica, carga o material, comparador y diferencia práctica relevante. Distinguí experimentos de exactitud predictiva, rendimiento computacional, experiencia de usuario y procesos físicos: no comparten necesariamente unidad ni modelo.

## 2. Unidad y replicación

| Caso | Unidad o nivel relevante | Pseudorreplicación frecuente |
|---|---|---|
| A/B de interfaz asignada a cuentas | Cuenta o usuario según asignación | Sesiones y clics como usuarios independientes |
| Intervención sobre servidores | Servidor o instancia-período con reinicio válido | Peticiones como réplicas de servidor |
| Algoritmos sobre varios conjuntos de datos | Conjunto o tarea para generalizar a tareas | Folds o semillas como conjuntos nuevos |
| Algoritmo estocástico en tarea fija | Corrida con semilla y condiciones definidas | Confundir variación de optimización con generalización |
| Proceso aplicado a lotes | Lote asignado | Probetas del mismo lote como lotes distintos |
| Tratamiento individual de piezas | Pieza asignada | Lecturas repetidas del mismo sensor |

Una corrida puede ser unidad de una intervención controlada si se restablece el sistema y se asigna la configuración de forma pertinente. Aun así, varias corridas de la misma máquina no representan variabilidad entre máquinas. Declará el alcance condicional.

## 3. Benchmarks comparables

Ejecutar todos los métodos sobre las mismas tareas permite comparaciones pareadas. Registrá dificultad, tamaño, origen y criterio de selección de las tareas; no elijas solo aquellas donde el método propuesto gana.

Distribuí el orden de métodos entre días o máquinas para evitar confundir método con calentamiento, carga externa o deriva. Controlá versiones, compilador, bibliotecas, hardware, energía, concurrencia, caché, calentamiento y reinicio según el objetivo de producción. No elimines variabilidad real del entorno si precisamente se pretende generalizar a ella.

Separá tiempo de preparación, entrenamiento e inferencia cuando tengan significados distintos. Definí política de timeout, fallos, memoria agotada y resultados inválidos antes de comparar. Excluir ejecuciones fallidas puede favorecer al método menos fiable.

Si el resultado de interés es una razón de tiempos, especificá cómo se agregará y por qué. Un promedio de razones y una razón de promedios no estiman lo mismo. Distribuciones asimétricas o colas largas requieren intervalos y métodos adecuados, no solo el mejor tiempo observado.

## 4. Aprendizaje automático y semillas

Separá entrenamiento, selección de hiperparámetros y evaluación. Evitá fuga por sujetos, dispositivos, sitios o tiempo: si observaciones del mismo paciente aparecen en entrenamiento y prueba, una división aleatoria por filas puede sobreestimar generalización.

La validación cruzada anidada puede separar selección y evaluación cuando sea apropiada. Los folds comparten datos de entrenamiento y sus resultados no son réplicas independientes para una prueba t ordinaria. Repetir particiones no crea nuevas poblaciones de prueba.

Varias semillas miden variabilidad del algoritmo condicionada a datos y configuración. Usar las mismas particiones y un emparejamiento justificado puede mejorar comparabilidad, pero un mismo número de semilla en algoritmos diferentes no garantiza perturbaciones equivalentes.

Predefiní presupuesto de ajuste comparable, métricas, particiones y política de selección. Informá incertidumbre entre tareas, sujetos o sitios según el objetivo, además de variación entre corridas. No dimensiones solo el número de semillas con una fórmula de dos medias si la pregunta trata de generalización a nuevas tareas.

## 5. Pruebas A/B y usuarios

Elegí asignación estable a usuario, cuenta, organización o dispositivo según interferencia y uso compartido. Un usuario expuesto a ambas variantes por cambios de dispositivo puede contaminar la comparación. Medí esa situación y justificá el nivel.

Fijá métrica principal, ventana de exposición, denominador y métricas de seguridad. Para conversión binaria por usuario, usá usuarios como unidades; para ingresos por usuario, considerá asimetría y ceros. Las métricas de razón y los eventos repetidos requieren métodos que representen su dependencia.

Predefiní duración, horizonte de análisis y reglas de parada. Revisar significancia continuamente con una prueba de tamaño fijo aumenta falsos positivos; usá un diseño secuencial válido si se necesita monitoreo inferencial. Las revisiones de seguridad no deben ocultarse por esta regla.

Comprobá integridad de asignación, proporciones observadas frente a las previstas y fallos de instrumentación. Una discrepancia de tamaños puede indicar problemas de elegibilidad, registro o exposición; no se corrige excluyendo usuarios hasta equilibrar.

En experimentos con tareas de usuarios, aleatorizá o contrabalanceá orden cuando sea viable y modelá aprendizaje, fatiga y dependencia de participante. Si el aprendizaje es irreversible, un cruzado puede no ser adecuado.

## 6. Procesos y materiales

Identificá lote, materia prima, máquina, herramienta, operador y día. Bloqueá o distribuí tratamientos para evitar confusión; un código numérico de operador sigue siendo categórico salvo que represente una cantidad real.

Si temperatura se cambia por corrida de horno y composición dentro de ella, considerá parcelas divididas. La réplica de temperatura es la corrida de horno asignada, con efectos de horno y período si corresponde. Aumentar probetas dentro de una corrida mejora medición interna, no replica temperatura.

En factoriales fraccionados registrá alias y resolución. No declares un efecto como aislado si está confundido con otro plausible. Para superficies de respuesta, justificá región segura, curvatura y ensayos de confirmación; un óptimo predicho fuera de la región estudiada requiere validación, no solo extrapolación.

Predefiní acondicionamiento, ensayo destructivo, calibración, tolerancias y fallos. No atribuyas a una norma un procedimiento sin comprobar código, edición y aplicabilidad.

## 7. Potencia y análisis

Dimensioná para diferencia o razón práctica, variabilidad en el nivel adecuado y comparación principal. En benchmarks pareados, la variabilidad de diferencias entre tareas puede importar más que la dispersión de tiempos individuales. Para múltiples algoritmos o métricas, definí la familia de inferencias.

El ANOVA de una vía del script no cubre automáticamente tareas cruzadas con métodos, efectos de máquina, latencias correlacionadas, métricas de razón ni parcelas divididas industriales. Usá contrastes pareados, modelos jerárquicos, remuestreo por unidad o simulación según el diseño y el estimando.

Para costo y rendimiento, informá intervalos y compromiso entre métricas relevantes, no solo rankings por p. Si interesa equivalencia de rendimiento dentro de un margen operativo, planificá una prueba de equivalencia en lugar de interpretar no significancia como empate.

## 8. Entrega reproducible y límites

Archivá identificadores de datos, versiones, configuración, semillas, plan de ejecución, logs y reglas de exclusión, con permisos y privacidad adecuados. Separá variabilidad de repetición, variabilidad entre tareas y generalización a producción.

La [guía de diseño experimental del NIST/SEMATECH e-Handbook](https://www.itl.nist.gov/div898/handbook/pri/pri.htm) ofrece documentación conocida para diseños de procesos. Verificá la sección concreta antes de citarla; no sustituye la validación de supuestos del experimento.

Consultá `../unidad-experimental.md` para jerarquías y `../plan-de-analisis.md` para contrastes, faltantes y remuestreo. Si hay participantes humanos o telemetría personal, incorporá revisión ética y protección de datos según la jurisdicción y el riesgo.
