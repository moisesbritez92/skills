---
name: experimental-dis
description: Diseña experimentos y estudios para tesis, TFG, TFM, proyectos finales de grado y artículos científicos. Elige el diseño correcto (completamente aleatorizado, bloques al azar, cuadrado latino, factorial, parcelas divididas, medidas repetidas, cruzado, cuasiexperimental), define la unidad experimental y las repeticiones, calcula el tamaño de muestra con potencia estadística, genera el plan de aleatorización con su croquis, deja escrito el plan de análisis antes de tomar datos y redacta la sección de materiales y métodos. Sirve en agronomía, ambiental y laboratorio, en salud y nutrición, y en informática e ingeniería. Usa esta skill siempre que aparezcan las palabras diseño experimental, diseño de investigación, DCA, DBCA, bloques al azar, factorial, split plot, parcelas divididas, medidas repetidas, tratamientos, testigo, grupo control, réplicas, repeticiones, unidad experimental, aleatorización, tamaño de muestra, cuántas muestras necesito, potencia estadística, variables independientes y dependientes, operacionalización de variables, hipótesis estadística, ensayo, ensayo clínico, prueba de campo, experimento de laboratorio, benchmark, prueba A/B, o cuando alguien pregunte cómo montar o dimensionar un experimento para su tesis, aunque no nombre ningún diseño. Úsala también para auditar un diseño que el tutor objetó, para arreglar un experimento mal replicado, o para decidir qué prueba estadística habrá que aplicar a los datos que todavía no se tomaron.
---

# Diseño experimental para tesis e investigaciones

Esta skill cubre el tramo que va desde una pregunta de investigación hasta un experimento montado, dimensionado, aleatorizado y con su plan de análisis escrito. Termina antes del análisis de datos reales: la salida es el protocolo, no los resultados.

Lo que se entrega, según lo que pida el usuario: la sección de materiales y métodos, el plan de aleatorización con croquis, la justificación del tamaño de muestra, y el esqueleto del script de análisis que el tesista correrá cuando tenga los datos.

## Lo que hunde un diseño experimental

Cuatro fallas frecuentes comprometen la inferencia. Algunas permiten un análisis más limitado; otras exigen nuevas unidades o un rediseño:

1. **Pseudorreplicación.** Si el tratamiento se asigna independientemente a tres plantas, treinta hojas no equivalen a treinta réplicas del tratamiento. Si las plantas comparten una única maceta tratada, la unidad puede ser la maceta. Un modelo jerárquico puede representar el submuestreo, pero no crear replicación inexistente.
2. **Asignación confundida con el ambiente.** Ordenar tratamientos por comodidad puede confundirlos con gradientes. La aleatorización protege frente a sesgos de asignación; el bloqueo puede mejorar la precisión, pero no es obligatorio ni sustituye la aleatorización.
3. **Tamaño de muestra sin justificación.** "Se tomarán 30 muestras" sin explicar potencia, precisión o un objetivo explícito de factibilidad.
4. **Plan de análisis que no corresponde al diseño.** Comparaciones sin control de multiplicidad cuando corresponde, ANOVA independiente sobre medidas correlacionadas o efectos promedio presentados como constantes pese a una interacción relevante.

El flujo ataca cada una en un paso distinto. No saltees ninguno.

## Flujo de trabajo

### 1. Separar experimento de estudio observacional

Preguntá si el investigador asigna los tratamientos a las unidades o solo observa lo que ya ocurrió.

- Asigna al azar: experimento aleatorizado, sigue todo este flujo. Los grupos ya formados también pueden aleatorizarse como conglomerados si es viable.
- Asigna sin aleatorizar: estudio de intervención no aleatorizado, con alcance cuasiexperimental según su estructura de comparación. Leé `references/cuasiexperimentales.md`: las estrategias de identificación requieren supuestos y no equivalen a la protección de la aleatorización.
- No asigna nada: habitualmente es un estudio observacional (transversal, cohorte, casos y controles, correlacional). No llames experimental a una encuesta. Si una política o mecanismo externo genera una comparación cuasiexperimental o un experimento natural, explicitá esa estrategia y sus supuestos en lugar de atribuir aleatorización al investigador.

Resolvé esta bifurcación antes de hablar de tratamientos, porque cambia todo lo que sigue.

### 2. Identificar el área y leer su referencia

La lógica del diseño es la misma en todas las áreas, pero la unidad experimental, la jerga, las restricciones y las normas de reporte no. Leé la que corresponda:

- `references/areas/agro-ambiental-laboratorio.md`: ensayos de campo, invernadero, bioensayos, corridas de laboratorio.
- `references/areas/salud-nutricion.md`: ensayos clínicos y comunitarios, sujetos humanos, CONSORT, ética.
- `references/areas/informatica-ingenieria.md`: benchmarks, pruebas A/B, experimentos con usuarios, ensayos de materiales y procesos.

Si el trabajo cruza áreas, leé las dos que apliquen. Si el usuario no dice de qué área es, deducilo de la variable respuesta antes de preguntar.

### 3. Reunir los datos mínimos

En un solo turno, no de a una pregunta, pedí lo que falte:

- Pregunta de investigación e hipótesis, en palabras del usuario.
- Variable respuesta principal, con su unidad y el instrumento con que se mide.
- Factores a estudiar y niveles de cada uno, incluido el testigo o control.
- Qué es una unidad experimental en su contexto: maceta, parcela, animal, paciente, lote, corrida, servidor, alumno.
- Cuántas unidades puede conseguir de verdad, cuánto tiempo tiene, y qué presupuesto o espacio lo limita.
- Fuentes de variación conocidas que no son de interés: pendiente del terreno, estante de la incubadora, día de procesamiento, operario, camada, turno, máquina.
- Si hay sujetos humanos o animales, si ya cuenta con aval del comité de ética.

Sin la restricción real de unidades disponibles no se puede recomendar nada honesto. Un diseño con seis repeticiones que el usuario no puede montar no sirve de nada.

### 4. Fijar la unidad experimental y la replicación real

La unidad experimental es la entidad a la que se asigna un tratamiento mediante el procedimiento previsto, aleatorio o no. Las observaciones dentro de ella no son réplicas independientes de ese tratamiento. En parcelas divididas hay unidades distintas para cada factor; distinguí también unidad de observación y unidad de muestreo.

Escribilo explícitamente antes de seguir, con esta forma: "unidad experimental = una maceta con tres plantas; se miden las tres y se promedia; n = número de macetas por tratamiento". Si el n real es menor que el supuesto, revisá identificabilidad y precisión antes de decidir si hace falta rediseñar.

Casos límite por área y las trampas más comunes en `references/unidad-experimental.md`.

### 5. Elegir el diseño

Leé `references/seleccion-de-diseno.md`, que trae el árbol de decisión y el catálogo con el modelo de cada diseño. En resumen:

| Situación | Diseño |
|---|---|
| Asignación libre a unidades del mismo nivel | Completamente aleatorizado (DCA), con ajuste de covariables si corresponde |
| Bloques definidos antes de asignar, cada uno admite todos los tratamientos | Bloques completos al azar (DBCA) |
| Dos fuentes de variación cruzadas, tantos niveles como tratamientos | Cuadrado latino |
| Dos o más factores cuyos efectos se quieren estimar | Arreglo factorial, con estructura de asignación explícita |
| Factores asignados en dos niveles, a unidades grandes y subunidades | Parcelas divididas |
| Mismos sujetos medidos en varios momentos | Medidas repetidas |
| Dos tratamientos y cada sujeto recibe ambos, sin arrastre | Cruzado |
| Muchos factores, etapa de tamizaje | Factorial fraccionado |
| Optimizar una respuesta sobre variables continuas | Superficie de respuesta |

Elegí el más simple que responda la pregunta y respete las restricciones. Un factorial 3×4 con 3 repeticiones por combinación requiere 36 unidades si todas se asignan al mismo nivel. Su viabilidad depende de los recursos y de la precisión requerida, no del nivel académico.

Justificá la elección en una o dos frases que digan qué fuente de variación controla el diseño. Esa frase va después a la tesis.

### 6. Calcular el tamaño de muestra

Justificá el tamaño por potencia para un efecto relevante, precisión del intervalo o viabilidad explícita en un piloto. Para potencia, fijá el contraste, la diferencia de interés, la variabilidad, alfa, la potencia, la asignación y la dependencia entre observaciones. Un coeficiente de variación requiere una media y una escala compatibles para obtener un desvío estándar.

```bash
python scripts/tamano_muestral.py --caso anova --grupos 4 --dme 2.5 --sd 3.0 --potencia 0.80
```

Ejecutá los comandos desde el directorio de esta skill o resolvé la ruta del script desde allí. Dependencias del planificador: Python 3, `scipy` para `scripts/tamano_muestral.py` y `matplotlib` para los croquis de `scripts/aleatorizar.py`; la asignación sin croquis usa la biblioteca estándar. `requirements.txt` declara las versiones mínimas. No instales paquetes sin autorización. Verificá las opciones actuales con `--help`, ya que los scripts pueden evolucionar.

Casos disponibles: `dos-medias`, `medias-pareadas`, `anova`, `dos-proporciones`, `correlacion`. Revisá el n, su unidad, los redondeos y los supuestos antes de usar el párrafo generado. Los ejemplos son ilustrativos, no recomendaciones de tamaño.

El caso `anova` calcula potencia de la prueba global de una vía, balanceada, con errores independientes y varianza común. En la implementación auditada, `--dme` separa dos medias extremas y las restantes se suponen en el punto medio. Esto no garantiza potencia para comparaciones específicas, interacciones, DBCA, parcelas divididas, conglomerados ni medidas repetidas. Para esos diseños, usá métodos específicos o simulación del modelo previsto; no presentes la salida de una vía como cálculo definitivo.

Si el usuario no tiene ninguna estimación de variabilidad, decilo y proponé un piloto o un rango de escenarios. No inventes un desvío estándar.

Fórmulas, escenarios, correlación intraclase y ajustes por pérdidas en `references/tamano-muestral.md`. No hay un descuento universal del n por bloquear.

### 7. Aleatorizar y dejar constancia

Documentá el procedimiento y conservá el registro de asignación. Una semilla permite reproducir un algoritmo determinado, pero no demuestra por sí sola que el plan se haya aplicado:

```bash
python scripts/aleatorizar.py --diseno dbca --tratamientos T1,T2,T3,T4 --bloques 4 --semilla 2026 --salida plan.csv --croquis croquis.png
```

Revisá la tabla y, si se solicitó y está disponible `matplotlib`, el croquis. Archivá semilla, versión, orden inicial de unidades, restricciones y desviaciones de la asignación. Contrastá el dibujo con el CSV: en diseños jerárquicos debe mostrar todas las parcelas grandes y subparcelas, sin superposiciones ni omisiones. No confundas número de filas con réplicas de cada factor.

Con sujetos humanos, agregá la ocultación de la secuencia de asignación y el cegamiento cuando sea posible.

### 8. Escribir el plan de análisis antes de tomar los datos

Este paso separa un trabajo defendible de uno que sale a buscar significancia. Dejá escrito, antes de la primera medición:

- Variable respuesta principal y cuáles son secundarias.
- Modelo estadístico con todos sus términos, incluido el de bloque o el error de parcela grande.
- Prueba principal, nivel de significancia y prueba de comparaciones múltiples elegida.
- Cómo se verificarán los supuestos y qué se hará si no se cumplen.
- Qué se hará con datos faltantes y con valores atípicos.

La correspondencia entre diseño y modelo está en `references/plan-de-analisis.md`. Interpretá la magnitud e incertidumbre de las interacciones, no solo su p. Los efectos marginales siguen siendo estimables si se explican su ponderación y alcance; los efectos simples responden preguntas condicionadas a niveles. El bloque puede reportarse como componente de variación, sin atribuirle causalidad por defecto. Elegí distribución y enlace según cómo se generó la respuesta, no por transformaciones automáticas.

Si se solicita un esqueleto de análisis, la estructura actual incluye este generador:

```bash
python scripts/esqueleto_analisis.py --diseno dbca --lenguaje r --datos plan.csv --salida analisis.R
```

Leé su alcance antes de usarlo: genera plantillas para respuestas continuas gaussianas y planes completos balanceados, no un análisis universal. En Python, parcelas divididas y medidas repetidas producen estimación REML sin pruebas implementadas de efectos fijos; en R, parcelas divididas usa estratos del ANOVA balanceado y medidas repetidas solo estimación con intercepto aleatorio. El cruzado se limita a AB/BA, dos períodos y ausencia de arrastre. Los CSV longitudinales y cruzados son externos: el aleatorizador no los genera.

El generador usa la biblioteca estándar; ejecutar sus salidas Python requiere `pandas`, `numpy` y `statsmodels`, no incluidos en las dependencias del planificador. Las salidas R usan R básico salvo medidas repetidas, que requiere `nlme`. Completá contrastes, diagnósticos, multiplicidad y sensibilidad según el plan científico. Si no se ejecutó con datos de prueba, entregá el esqueleto como borrador no validado, no como análisis terminado.

### 9. Redactar materiales y métodos

Seguí `references/redaccion-metodologia.md`. El orden que espera un tribunal es: lugar y período, material experimental, diseño y su justificación, tratamientos, unidad experimental y número de repeticiones, variables con su forma de medición, manejo del ensayo, y análisis estadístico previsto con el software y su versión.

Preferí prosa clara, futuro para procedimientos previstos y pasado para los realizados, con persona gramatical consistente. Usá tablas o listas cuando mejoren la reproducibilidad y el formato institucional lo permita.

Si el usuario está armando un anteproyecto o proyecto final de la FCyT UNCA, esta sección alimenta la metodología de ese documento. Coordiná con esa skill en vez de duplicar el formato.

### 10. Verificar antes de entregar

Recorré `references/checklist.md`. Lo esencial: el n está declarado por nivel de asignación, el comparador responde a la pregunta, la asignación está documentada, el modelo respeta el diseño, cada objetivo tiene un estimando y un análisis o resumen apropiado, y la sección de ética está si corresponde.

## Reglas que no se negocian

**El n se declara por nivel.** Las submuestras pueden resumirse o modelarse con su dependencia; no cuentan como asignaciones independientes del tratamiento aplicado a la unidad superior.

**Toda comparación necesita un referente definido.** Puede ser otro tratamiento activo, práctica habitual, placebo o ausencia de intervención, según pregunta y ética. No todo experimento necesita un grupo sin tratamiento.

**La asignación se documenta.** Para generación computacional, conservá semilla, algoritmo o versión y lista de partida. En un sorteo físico, registrá el procedimiento y el resultado. Separá reproducibilidad, ocultación y cegamiento.

**El análisis confirmatorio se preespecifica.** Documentá cambios y separá análisis exploratorios, sin ocultarlos ni prohibirlos.

**No se inventan estimaciones de variabilidad.** Si no hay dato previo, se dice que no lo hay y se propone un piloto.

**La revisión ética precede a la intervención cuando corresponde.** En humanos, verificá aprobación o exención formal, consentimiento o dispensa autorizada y protección de datos. En animales, verificá autorización aplicable, bienestar y las 3R; no se habla de consentimiento del animal. No declares aprobaciones que no constan.

**Ningún guion largo ni guion medio como signo de inciso** en el texto que se entrega. Para incisos, comas o paréntesis.

## Referencias de la skill

- `references/seleccion-de-diseno.md`: árbol de decisión y catálogo con el modelo de cada diseño.
- `references/unidad-experimental.md`: unidad experimental, submuestreo y pseudorreplicación.
- `references/tamano-muestral.md`: potencia por tipo de diseño y qué hacer sin datos previos.
- `references/plan-de-analisis.md`: correspondencia diseño a modelo, supuestos y comparaciones múltiples.
- `references/cuasiexperimentales.md`: diseños sin aleatorización y amenazas a la validez.
- `references/redaccion-metodologia.md`: estructura, plantillas de párrafo y pares antes y después.
- `references/checklist.md`: verificación final.
- `references/areas/`: particularidades de agronomía y laboratorio, salud, e informática e ingeniería.
