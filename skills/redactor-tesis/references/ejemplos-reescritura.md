# Ejemplos de reescritura

Cada par muestra una regla concreta. La versión corregida no es más larga que la original.

## Palabras que no comunican

> ❌ Es importante señalar que, de alguna manera, los resultados obtenidos en el marco del
> experimento parecen indicar una cierta mejora a nivel de rendimiento.

> ✅ Los resultados del experimento indican una mejora del rendimiento.

Fórmulas que casi siempre sobran: *cabe destacar que*, *es preciso mencionar que*,
*en el presente trabajo se procede a*, *a nivel de*, *en términos de*, *el hecho de que*,
*de cara a*, *proceder a + infinitivo*.

## Repetición

> ❌ El modelo se entrenó con el conjunto de datos completo. El modelo alcanzó una
> precisión del 86 %. El modelo se comparó después con la línea base.

> ✅ El modelo se entrenó con el conjunto de datos completo y alcanzó una precisión del
> 86 %, que se comparó después con la línea base.

Excepción: los términos técnicos se repiten literalmente. Si el trabajo llama *codificador
visual* a un componente, no debe alternarse con *extractor de rasgos* ni *backbone*.

## Frases largas y coloquiales

> ❌ Al final del día, lo que se ve es que cuando congelas el encoder el modelo aprende
> bastante menos, algo que ya se intuía y que además encaja con un montón de trabajos
> previos que apuntaban en esa dirección desde hacía tiempo.

> ✅ El codificador congelado reduce el aprendizaje del modelo. El resultado coincide con
> la evidencia previa [4].

## Discurso despersonalizado

| ❌ Personal | ✅ Impersonal |
|---|---|
| En este trabajo he analizado… | En este trabajo se analizan… |
| Nuestros resultados demuestran… | Los resultados demuestran… |
| Como puede observar el lector… | Como se observa en la Figura 4… |
| Creo que esto se debe a… | Este comportamiento se atribuye a… |
| Vamos a ver a continuación… | A continuación se presentan… |

## Conectores

> ❌ El modelo V1 obtuvo 0,668. El modelo V0 obtuvo 0,865. El preentrenamiento no aporta
> ventaja en esta tarea.

> ✅ El modelo V1 obtuvo 0,668, frente a los 0,865 de V0. Por tanto, el preentrenamiento no
> aporta ventaja en esta tarea.

## Metáforas, eufemismos y léxico recargado

| ❌ | ✅ |
|---|---|
| El modelo devora los datos | El modelo procesa el conjunto de datos completo |
| Los resultados no fueron del todo óptimos | Los resultados quedaron por debajo de la línea base |
| Se produjo una situación de no consecución del objetivo | No se alcanzó el objetivo |
| Un paradigma disruptivo que revoluciona el campo | Un enfoque que reduce el error en un 12 % |

## Presentar un resultado numérico

> ❌ Se probaron varias variantes y algunas fueron bastante mejores que otras, sobre todo
> la primera, que dio un resultado muy bueno comparado con las demás.

> ✅ De las tres variantes evaluadas, V0 alcanzó la mejor puntuación (0,8645), seguida de
> V1 (0,668) y V2 (0,6477). La Tabla 2 recoge los valores por época.

Regla: la comparación va en la tabla; el texto interpreta, no repite la tabla.

## Raya y guion largo

La raya (`—`) no se usa como signo de puntuacion. Cada caso tiene un sustituto natural.

> ❌ El modelo V0 — el unico entrenado desde cero — alcanzo la mejor puntuacion.

> ✅ El modelo V0, el unico entrenado desde cero, alcanzo la mejor puntuacion.

> ❌ Los tres codificadores congelados fallaron — el preentrenamiento no basta.

> ✅ Los tres codificadores congelados fallaron: el preentrenamiento no basta.

> ❌ Se evaluaron cinco variantes — V0 a V4 — sobre la misma tarea.

> ✅ Se evaluaron cinco variantes (V0 a V4) sobre la misma tarea.

El guion medio (`–`) se reserva para rangos numericos: `pp. 627–635`, `15–25 palabras`.
