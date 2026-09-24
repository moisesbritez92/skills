# Estilo: de voz de tesis a voz de artículo

Índice: el cambio de voz · residuos de tesis · densidad · lo que delata texto generado ·
español y traducción al inglés · pares antes/después.

## El cambio de voz

La tesis le habla a un tribunal que evalúa al autor; el artículo le habla a colegas que
evalúan un resultado. De ahí salen casi todos los ajustes de redacción:

| En la tesis | En el artículo |
|---|---|
| Explica para demostrar que se entendió | Afirma y cita |
| Anuncia lo que va a hacer en cada capítulo | Lo hace |
| Justifica cada decisión metodológica | Justifica solo lo discutible |
| Recorre la literatura autor por autor | Agrupa por enfoques y señala el hueco |
| Reserva la conclusión para el final | Adelanta el hallazgo en resumen e introducción |
| Tono cauteloso y deferente | Tono directo, con las cautelas donde tocan |

Tiempos verbales, que en español académico se descuidan mucho: lo que hiciste, en pasado
(`se midieron`, `se aplicó`); lo que muestran los datos y las figuras, en presente (`la
figura 2 muestra`, `el modelo predice`); lo que se sabe de forma establecida, en presente
(`el ensuciamiento reduce la producción`).

Persona: sigue a la revista. Muchas ya aceptan `we` o `nosotros` en trabajos con varios
autores, y en inglés es lo dominante fuera de algunas áreas. En español, la impersonal con
`se` sigue siendo lo más seguro. Lo que no funciona es mezclar las tres en la misma sección
ni el `yo` de la tesis de grado.

## Residuos de tesis

Estas expresiones son la huella de copiar y pegar. `scripts/check_articulo.py` las busca,
pero conviene reconocerlas al escribir:

- Autorreferencias al documento: `en el presente capítulo`, `en el apartado anterior`,
  `como se vio en el capítulo 2`, `a lo largo de esta tesis`, `el presente trabajo de fin de
  máster`, `en el Anexo A`.
- Aparato académico de grado: `objetivo general`, `objetivos específicos`, `hipótesis de
  investigación` numeradas al estilo de un anteproyecto, `justificación`, `alcance y
  limitaciones` como sección propia, `marco teórico` como título de sección.
- Dirigirse al tribunal: `se espera que este trabajo contribuya a`, `queda a criterio del
  lector`, `se recomienda a la institución`.
- Numeración heredada: `Figura 4.12`, `Tabla 3.7`, `Ecuación (5.3)`. En el artículo se
  renumera desde 1 y se dejan las referencias cruzadas al sistema de LaTeX o de Word.
- Apéndices citados que ya no existen.

## Densidad

Un artículo tiene entre tres y cinco veces más contenido por palabra que una tesis. Lo que
más sube la densidad, por orden de rentabilidad:

1. **Una idea por párrafo, con la idea en la primera frase.** El revisor lee las primeras
   frases de cada párrafo cuando va con prisa; si ahí está el argumento, el artículo se
   entiende en esa pasada.
2. **Fuera las frases de transición vacías**: `una vez expuesto lo anterior, se procede a`,
   `es importante mencionar que`, `cabe destacar que`, `en este sentido`.
3. **Verbos en vez de perífrasis**: `se llevó a cabo la medición de` → `se midió`;
   `tiene la capacidad de` → `puede`; `hacer uso de` → `usar`.
4. **Números en vez de adjetivos**: `una mejora sustancial` → `una mejora del 18 %`.
5. **Nada de prosa que repita una tabla.** Se comenta lo que la tabla no dice: la tendencia,
   la excepción, lo que significa.

## Lo que delata texto generado

Importa doblemente aquí: los editores pasan detectores, y un revisor que sospecha lee con
mala fe. Los patrones más reconocibles:

- **Guiones largos** (—) usados como pausa retórica. En español académico se usan comas,
  paréntesis o dos puntos. Cero guiones largos.
- **Estructura de tres**: tres adjetivos, tres ejemplos, tres viñetas del mismo largo, una y
  otra vez.
- **`No solo... sino que también`**, `es importante destacar`, `en el mundo actual`, `de cara
  al futuro`, `juega un papel fundamental`, `abre nuevas posibilidades`, `constituye un
  desafío significativo`.
- **Párrafos de longitud sospechosamente uniforme** y secciones perfectamente simétricas.
- **Cierres que resumen lo ya dicho** al final de cada sección (`En resumen, en esta sección
  se ha presentado...`). En un artículo eso solo va al final del artículo, si acaso.
- **Adjetivos evaluativos sin dato**: `robusto`, `innovador`, `prometedor`, `exhaustivo`.
- Cursiva o negrita repartida para dar énfasis. En un artículo casi no aparecen.

El antídoto no es sustituir una muletilla por otra, sino escribir frases de longitud
variable, con la información concreta del trabajo dentro. Un párrafo con tres cifras y un
nombre de instrumento no parece generado, porque no lo puede parecer.

## Español, y traducción al inglés

Si la tesis está en español y el artículo va en inglés, **no traduzcas: reescribe desde el
plan.** Una traducción arrastra la sintaxis larga y subordinada del español académico y
produce ese inglés de frases de cuarenta palabras que los revisores comentan siempre. Tener
delante el capítulo original mientras se escribe la sección en inglés es la garantía de
traducirlo.

Diferencias que hay que ejecutar, no solo saber: frases más cortas; sujeto explícito; una
idea por frase; `The results show` en vez de `Se puede observar que los resultados muestran`;
voz activa donde el inglés la prefiere.

Falsos amigos frecuentes en textos técnicos: `actualmente` no es *actually* sino *currently*;
`realizar` casi nunca es *realize*; `eventualmente` no es *eventually*; `sensible` es
*sensitive*; `asistir* a un congreso es *attend*. Y `Doctor` o `Ing.` no se ponen delante del
nombre en el bloque de autores de una revista internacional.

Si el artículo queda en español, cuida la puntuación de las citas según el estilo, los
decimales con coma cuando la revista es hispanohablante (y con punto cuando es
internacional), y `%` separado del número según norma (`18 %`).

## Pares antes/después

**Introducción.**
*Antes:* "El presente trabajo de fin de máster tiene como objetivo general analizar el
comportamiento de los sistemas fotovoltaicos instalados en el departamento de Caaguazú,
teniendo en cuenta las particularidades del clima de la región, con el fin de aportar
información útil para el sector."
*Después:* "Las plantas fotovoltaicas de clima subtropical húmedo pierden producción por
ensuciamiento a un ritmo que los modelos calibrados en climas áridos subestiman. Medimos esa
pérdida durante 14 meses en cinco instalaciones de Caaguazú (Paraguay)."

**Método.**
*Antes:* "Para el análisis de los datos se decidió utilizar el software estadístico R, que es
una herramienta ampliamente utilizada en la comunidad científica por su versatilidad y su
amplia disponibilidad de paquetes."
*Después:* "Los datos se analizaron en R 4.3.1 con el paquete `lme4`."

**Resultados.**
*Antes:* "Se puede observar en la Figura 4.7 que existe una tendencia decreciente bastante
marcada en el rendimiento a medida que transcurren los días sin lluvia, lo cual resulta un
hallazgo interesante."
*Después:* "El rendimiento cae 0,42 % por día seco acumulado (IC 95 %: 0,31–0,53; fig. 3)."

**Discusión.**
*Antes:* "Los resultados obtenidos permiten concluir que se cumplieron satisfactoriamente
los objetivos planteados al inicio de esta investigación."
*Después:* "La tasa de pérdida duplica la que informan [8] y [11] para instalaciones
áridas, lo que sugiere que la deposición biológica, y no solo el polvo mineral, gobierna el
ensuciamiento en climas húmedos."
