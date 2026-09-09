---
name: analista-datos
description: Analiza los datos de un experimento ya ejecutado y produce la sección de resultados de una tesis, TFG, TFM o artículo. Recupera el diseño con que se tomaron los datos, audita la planilla contra ese diseño, ajusta el modelo que corresponde (ANOVA de una vía, con bloques, factorial con interacción, parcelas divididas con sus dos errores, medidas repetidas, modelo mixto, modelo lineal generalizado para conteos y proporciones), verifica los supuestos sobre los residuos, aplica comparaciones múltiples de Tukey o Dunnett, calcula tamaños de efecto e intervalos de confianza, arma las tablas y figuras publicables, redacta la sección de resultados y propone las líneas de la discusión. Usa esta skill siempre que aparezcan las palabras analizar mis datos, procesar los datos, ANOVA, análisis de varianza, prueba de Tukey, Dunnett, Duncan, LSD, letras de significancia, cuadro de ANOVA, coeficiente de variación, supuestos, normalidad, Shapiro Wilk, homocedasticidad, Levene, residuos, transformación de datos, Kruskal Wallis, prueba no paramétrica, modelo mixto, medidas repetidas, p valor, significancia estadística, tamaño de efecto, intervalo de confianza, gráfico de barras con error, sección de resultados, o cuando alguien traiga una planilla de un ensayo y pregunte qué prueba corresponde o por qué no le dio significativo. Úsala también para auditar un análisis ya hecho que el tutor objetó, para detectar pseudorreplicación en datos ya tomados, y para rehacer en R o Python un análisis salido de InfoStat o SPSS.

compatibility: Requiere Python 3 con pandas, numpy, scipy, statsmodels y matplotlib. Instalá las dependencias en un entorno virtual; no uses --break-system-packages.
---

# Análisis de datos experimentales

Esta skill toma los datos de un experimento ya ejecutado, corre el análisis y devuelve los resultados: tablas, figuras, la sección de resultados redactada y las líneas sugeridas para la discusión.

Es la continuación de la skill `diseno-experimental`. Cuando existe el protocolo que aquella genera, el modelo ya está decidido y este flujo se limita a ejecutarlo con honestidad. Cuando no existe, el primer trabajo es reconstruirlo, y ahí es donde aparecen la mayoría de los problemas.

## Lo que hunde un análisis

1. **Modelo que no corresponde al diseño.** Analizar parcelas divididas como factorial común, o ignorar el bloque, cambia los grados de libertad del error y con eso todos los valores p.
2. **Pseudorreplicación heredada.** La planilla trae tres mediciones por parcela y el software informa n = 72 cuando el n real es 24. Casi siempre llega así.
3. **Elegir la prueba después de ver el resultado.** Probar ANOVA, no dar significativo, y pasarse a no paramétrica buscando el p que convenga.
4. **Reportar sólo el valor p.** Sin medias, sin dispersión declarada, sin tamaño de efecto y sin intervalo de confianza, el resultado no se puede interpretar ni comparar con nada.

## Flujo de trabajo

### 1. Recuperar el diseño

Buscá el archivo `diseno.json` que produce la skill `diseno-experimental`. Si está, leelo: trae el diseño, la unidad experimental, las submuestras por unidad, el modelo previsto, el alfa, la prueba post hoc elegida y la lista de desviaciones registradas. Con eso el modelo no se discute, se ejecuta.

Si no está, reconstruilo antes de tocar los datos. Preguntá en un solo turno:

- Qué es una unidad experimental y cuántas hubo por tratamiento.
- Si hubo bloques, y qué representaban.
- Si cada fila de la planilla es una unidad o una medición dentro de una unidad.
- Si el mismo sujeto o parcela aparece más de una vez.
- Qué tratamientos hubo y si son combinación de dos factores.
- Si el análisis estaba decidido de antemano o se está eligiendo ahora.

Esa última pregunta importa: un análisis elegido después de ver los datos es exploratorio, y así hay que declararlo. No lo escondas.

Escribí el protocolo reconstruido a un `diseno.json` para que el resto del flujo lo use y quede constancia.

### 2. Auditar los datos contra el diseño

Nunca ajustes un modelo sin este paso.

```bash
python3 scripts/verificar_datos.py datos.csv --protocolo diseno.json
```

Reporta: filas por unidad experimental, n real por tratamiento, desbalance, celdas vacías del cruce de factores, unidades faltantes respecto del plan, valores fuera de rango, tipos de columna mal leídos y duplicados. Si el número de filas no coincide con el número de unidades, avisa que hay submuestreo y cuál es el n verdadero.

Resolvé todo lo que reporte antes de seguir. Si hay submuestras, decidí explícitamente entre promediarlas por unidad, que es lo habitual y lo más defendible, o modelarlas como término anidado, y dejá dicho cuál se usó.

### 3. Explorar antes de probar

Medias, desvíos, coeficiente de variación y conteos por tratamiento. Gráfico de dispersión de los datos crudos por tratamiento, no de las medias. Un valor extremo o un tratamiento con varianza muy distinta se ven acá y no en la tabla de ANOVA.

No descartes valores atípicos por ser atípicos. Se descartan sólo con una causa documentada (falla del instrumento, planta arrancada, sujeto que abandonó), y se declara en la tesis cuántos y por qué.

### 4. Ajustar el modelo que dicta el diseño

La correspondencia está en `references/modelo-por-diseno.md`. En resumen:

| Diseño | Modelo |
|---|---|
| DCA | ANOVA de una vía |
| DBCA | ANOVA con bloque como término, no como hallazgo |
| Cuadrado latino | ANOVA con fila y columna |
| Factorial | ANOVA con interacción |
| Parcelas divididas | Modelo mixto, parcela grande como término aleatorio |
| Medidas repetidas | Modelo mixto con sujeto aleatorio, o ANOVA con corrección de esfericidad |
| Respuesta de conteo | Poisson o binomial negativa |
| Respuesta binaria o proporción | Regresión logística |
| Tiempo hasta un evento | Análisis de supervivencia |

```bash
python3 scripts/analizar.py datos.csv --protocolo diseno.json --respuesta rendimiento
```

Con interacción significativa no se interpretan efectos principales por separado, se analizan efectos simples. El término de bloque no se reporta como resultado.

### 5. Verificar los supuestos sobre los residuos

Los supuestos son del modelo, no de los datos crudos. Se verifican sobre los residuos del modelo ajustado, nunca sobre la variable respuesta sin ajustar. Es un error muy extendido y fácil de detectar en una defensa.

Qué mirar: normalidad de residuos con gráfico cuantil cuantil y Shapiro Wilk como apoyo, homogeneidad de varianzas con residuos contra ajustados y Levene, independencia por el diseño y por el orden de toma de datos, y aditividad cuando hay bloques.

Con n chico, Shapiro tiene poca potencia y no detecta nada; con n grande, detecta desvíos irrelevantes. El gráfico manda sobre la prueba. Decilo así en la tesis.

### 6. Cuando los supuestos fallan

Mostrá las rutas con lo que cada una cuesta, en vez de aplicar una en silencio:

- **Transformación.** Raíz cuadrada para conteos, arcoseno o logit para proporciones, logaritmo para varianza proporcional a la media. Costo: las conclusiones quedan en la escala transformada y las medias hay que retransformarlas con cuidado.
- **Modelo lineal generalizado.** Casi siempre preferible a transformar, porque respeta la naturaleza de la variable. Costo: interpretación de coeficientes menos directa.
- **Prueba no paramétrica.** Kruskal Wallis, Friedman. Costo: pierde potencia, no maneja diseños complejos ni interacciones, y cambia la hipótesis que se está probando.
- **Aceptar el desvío.** El ANOVA tolera desvíos moderados de normalidad si el diseño es balanceado. Decirlo con la evidencia a la vista es legítimo.

Detalle en `references/supuestos-y-alternativas.md`.

### 7. Comparaciones múltiples y tamaño de efecto

Sólo si el efecto global resultó significativo, salvo que las comparaciones estuvieran planificadas de antemano.

Esta skill trabaja con dos pruebas, y la elección depende de la pregunta:

- **Tukey**, cuando interesan todas las comparaciones entre tratamientos.
- **Dunnett**, cuando todas las comparaciones son contra el testigo. Es más potente que Tukey para ese caso porque hace menos comparaciones, así que cuando el diseño tiene un control claro, conviene.

**Duncan y LSD no se usan.** Ambas controlan el error por comparación y no por familia, de modo que con varios tratamientos la probabilidad de declarar una diferencia falsa se dispara. Siguen circulando por costumbre en manuales viejos y en las salidas por defecto de algunos programas. Si el usuario las pide porque su facultad las usa, explicale el problema en una o dos frases, ofrecé Tukey o Dunnett según corresponda, y si insiste, decile que la skill no las produce y que puede correrlas por su cuenta. No las implementes en silencio.

Reportá siempre, además del valor p: la media de cada tratamiento con su medida de dispersión declarada, la diferencia entre medias con su intervalo de confianza, y un tamaño de efecto (eta cuadrado parcial, omega cuadrado, o d según el caso). Un resultado significativo con una diferencia sin relevancia práctica hay que decirlo.

### 8. Tablas y figuras

Tabla de ANOVA con fuente de variación, grados de libertad, cuadrados medios, F y p, más el coeficiente de variación. Tabla de medias con letras de significancia, indicando siempre qué prueba las produjo y con qué alfa.

En las figuras, declarar qué representa la barra de error: desvío estándar, error estándar o intervalo de confianza. Una barra de error sin identificar no significa nada. Preferí mostrar los puntos crudos junto a la media cuando el n lo permite.

Formato y estilo en `references/tablas-y-figuras.md`.

### 9. Redactar los resultados

Los resultados describen, no interpretan. La explicación de por qué ocurrió va en discusión. Seguí `references/redaccion-resultados.md`.

La redacción cita cada tabla y figura en el texto, informa el estadístico completo (F con sus dos grados de libertad, el p y el tamaño de efecto), y no repite en prosa todos los números que ya están en la tabla.

### 10. Sugerir la discusión

La discusión no se redacta entera acá, porque depende de literatura que hay que leer. Lo que sí corresponde es entregar las líneas sobre las que se construye, en forma de lista breve:

- Qué resultado responde a cada objetivo específico, y si lo hace en el sentido esperado o en el contrario.
- Qué hallazgo pide contraste con antecedentes, y con qué tipo de trabajo habría que compararlo.
- Qué explicación biológica, técnica o de proceso es plausible para el patrón observado, planteada como hipótesis y no como conclusión.
- Las limitaciones reales del estudio: potencia insuficiente, un solo sitio o una sola campaña, rango estrecho de niveles probados, submuestreo, pérdidas.
- Qué resultado no debe sobreinterpretarse, en particular las diferencias significativas de magnitud irrelevante y las no significativas con n chico.

**Nunca inventes referencias ni atribuyas hallazgos a autores.** Si no hay búsqueda disponible, dejá marcadores explícitos del tipo `[CONTRASTAR CON: estudios sobre respuesta a dosis de nitrógeno en suelos arenosos]` y avisá al usuario qué tiene que buscar.

Dejá claro al entregar que la discusión es del tesista y que estas son entradas para escribirla, no la sección terminada.

### 11. Registrar el software

Anotá el nombre y la versión de cada paquete usado, porque va en la tesis y porque los valores por defecto cambian entre versiones y entre programas. Si el tesista corrió antes lo mismo en InfoStat o SPSS y los números no coinciden, revisá primero el tipo de suma de cuadrados y el manejo del desbalance antes de suponer un error.

### 12. Verificar antes de entregar

Recorré `references/checklist.md`. Lo esencial: el n del análisis es de unidades experimentales, el modelo tiene los mismos términos que el diseño, los supuestos se verificaron sobre residuos, las letras de significancia dicen de qué prueba salieron, toda desviación respecto del plan está declarada, cada objetivo específico tiene su resultado, y ninguna conclusión afirma la hipótesis nula.

## Reglas que no se negocian

**El modelo lo dicta el diseño, no el resultado que se busca.** Si el usuario pide una prueba que no corresponde a cómo se tomaron los datos, decilo antes de correr nada.

**Toda desviación respecto del plan se declara.** Cambiar de prueba, descartar datos o agregar una covariable después de ver los resultados es legítimo si se declara, y es fraude si se oculta.

**Nunca escribir p = 0,000.** Se escribe p < 0,001.

**No se acepta la hipótesis nula.** "No se detectaron diferencias significativas" es correcto; "los tratamientos son iguales" no lo es. Con n chico, la ausencia de significancia suele ser falta de potencia y conviene decirlo.

**Toda media va con su dispersión y esa dispersión va identificada.**

**Significancia estadística no es relevancia práctica.** Un aumento de rendimiento de 20 kg por hectárea puede ser significativo y no valer nada para el productor.

**Las submuestras no inflan los grados de libertad.**

**Ningún guion largo ni guion medio como signo de inciso** en el texto que se entrega.

## Contrato con la skill de diseño

`diseno-experimental` produce tres archivos que esta skill consume:

- `diseno.json`: diseño, unidad experimental, submuestras, factores, modelo previsto, alfa, post hoc y desviaciones.
- `plan_aleatorizacion.csv`: la asignación con su semilla, que sirve para verificar que los datos llegaron completos.
- La planilla de carga con las columnas correctas.

Cuando los datos vienen sin ninguno de los tres, funcioná igual pero reconstruí el protocolo en el paso 1 y advertí al usuario que el diseño reconstruido a posteriori es más frágil ante un tribunal.

## Referencias de la skill

- `references/modelo-por-diseno.md`: qué modelo corresponde a cada diseño, con su sintaxis en R y en Python.
- `references/supuestos-y-alternativas.md`: verificación de supuestos y qué hacer cuando fallan.
- `references/comparaciones-multiples.md`: Tukey y Dunnett, control del error por familia, y por qué quedan afuera Duncan y LSD.
- `references/tamano-de-efecto.md`: cuál corresponde a cada modelo y cómo se interpreta.
- `references/tablas-y-figuras.md`: formato de la tabla de ANOVA, letras de significancia y figuras.
- `references/redaccion-resultados.md`: plantillas de párrafo, pares antes y después, y armado de las líneas de discusión.
- `references/checklist.md`: verificación final.
