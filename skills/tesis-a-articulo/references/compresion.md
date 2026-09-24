# Compresión: de capítulos a secciones

Índice: presupuestos por formato · mapa capítulo→sección · el marco teórico · figuras y
tablas · referencias · resumen, título y palabras clave · material suplementario.

## Presupuestos por formato

Cuenta palabras del cuerpo, sin resumen ni referencias. Son órdenes de magnitud, no dogma;
si la revista da su propio límite, manda el suyo.

| Formato de destino | Cuerpo | Figuras+tablas | Referencias |
|---|---|---|---|
| Congreso IEEE, 4 páginas | 2 500–3 000 | 3–4 | 15–25 |
| Congreso IEEE / LNCS, 6–8 páginas | 4 000–5 000 | 4–6 | 20–35 |
| LNCS 12–16 páginas | 5 500–7 000 | 5–8 | 30–45 |
| Artículo de revista normal | 6 000–8 000 | 5–8 | 35–60 |
| Revista con formato largo o *review* | 8 000–12 000 | 6–10 | 60–120 |
| Carta / *short paper* | 1 500–2 500 | 2–3 | 10–20 |

Reparto orientativo del cuerpo en un artículo de investigación empírica:

| Sección | Proporción | En 6 000 palabras |
|---|---|---|
| Introducción (con trabajo relacionado dentro) | 15–20 % | 900–1 200 |
| Trabajo relacionado, si va en sección propia | 10–15 % | 600–900 |
| Método / materiales | 20–25 % | 1 200–1 500 |
| Resultados | 25–30 % | 1 500–1 800 |
| Discusión | 15–20 % | 900–1 200 |
| Conclusión | 3–5 % | 200–300 |

Si al terminar la Introducción llevas gastado más del 25 % del presupuesto, el artículo ya
va mal: casi siempre significa que el marco teórico de la tesis está colándose entero.

## Mapa capítulo → sección

**Cap. 1, Introducción (3 000–6 000 palabras) → 900 palabras.**
Sobrevive: el problema, por qué importa, el hueco concreto en la literatura, la contribución
y una frase de estructura del artículo (opcional, y en muchas revistas ya sobra). Se cae:
los objetivos general y específicos con esa numeración escolar, las preguntas de
investigación formuladas como en el anteproyecto, la justificación institucional, el alcance
y las limitaciones (van a la Discusión), la descripción de la propia estructura de capítulos.

Un patrón que funciona, cuatro párrafos: contexto y relevancia → qué se sabe ya → qué falta
por saber (el hueco) → qué hace este artículo y qué encuentra. El último párrafo debe
adelantar el resultado principal con su número; no se guarda la sorpresa para el final.

**Cap. 2, Marco teórico (8 000–15 000 palabras) → 400–800 palabras.**
Aquí está el 80 % de la compresión y es donde más gente falla. Ver el apartado siguiente.

**Cap. 3, Metodología (5 000–10 000) → 1 200–1 500.**
Sobrevive: diseño, población y muestra con su tamaño, instrumentos, variables, procedimiento
y análisis estadístico, en el nivel de detalle que permite a un par juzgar la validez y
repetir el estudio. Se cae: el manual de la técnica ("la regresión logística es un modelo
que..."), la justificación del paradigma de investigación, los tutoriales de las
herramientas, las capturas de pantalla del software, los formularios completos.

Regla práctica: si un lector del área ya lo sabe, cítalo en vez de explicarlo. `Se aplicó
regresión logística multinivel [12]` sustituye a tres páginas.

**Cap. 4, Resultados (5 000–15 000) → 1 500–1 800.**
Sobrevive: lo que responde a la afirmación central, con las 4–6 figuras y tablas que la
sostienen. Se cae: los resultados intermedios, las tablas de estadísticos descriptivos que
no se comentan, cada análisis exploratorio que se hizo por el camino, las salidas crudas del
software.

En la tesis se cuenta todo lo que se hizo; en el artículo, lo que hace falta para creer la
conclusión. El resto es material suplementario. No interpretes aquí si la revista separa
Resultados de Discusión.

**Cap. 5, Discusión y conclusiones → 900–1 200 + 200–300.**
Sobrevive: qué significa el resultado principal, cómo dialoga con la literatura de la
Introducción (ahí se cierra el círculo), limitaciones honestas y concretas, y qué abre.
Se cae: el resumen capítulo por capítulo, el cumplimiento de objetivos punto por punto, las
recomendaciones institucionales, los agradecimientos disfrazados de reflexión.

La conclusión del artículo son tres o cuatro frases. Si escribes una página, es un resumen
repetido.

**Anexos → material suplementario o fuera.**

## El marco teórico

La operación más rentable de todo el proceso. Un capítulo de marco teórico está escrito para
demostrarle al tribunal que el autor leyó; el trabajo relacionado de un artículo está
escrito para situar la contribución y para justificar que el hueco existe.

Cómo se hace en la práctica:

1. Quita todo lo que sea definición de manual. Un lector de la revista sabe qué es una red
   neuronal convolucional; si no lo supiera, no leería ese artículo.
2. Agrupa por enfoques, no por autores. `Los trabajos que abordan X mediante métodos basados
   en grafos [3], [7], [11] comparten la limitación de suponer Y` vale más que tres párrafos
   describiendo tres artículos uno detrás de otro.
3. Cierra cada grupo con lo que le falta, porque ese es el hueco que llena tu artículo. El
   trabajo relacionado sin esa frase de cierre es catálogo, no argumento.
4. Conserva la teoría que se usa de verdad después. Si un constructo aparece en el Método o
   en la Discusión, tiene que estar presentado antes; si no reaparece nunca, sobra por
   completo.

**Antes** (tesis, 180 palabras): *"El aprendizaje profundo es una rama del aprendizaje
automático que utiliza redes neuronales con múltiples capas. Fue popularizado a partir de
2012 con AlexNet [5], que ganó la competición ImageNet... Posteriormente, VGG [6] propuso...
ResNet [7] introdujo las conexiones residuales..."*

**Después** (artículo, 30 palabras): *"Las arquitecturas convolucionales profundas dominan la
clasificación de imágenes desde [5], pero su aplicación a imágenes de teledetección con
pocas etiquetas sigue limitada por el coste de anotación [6], [7]."*

## Figuras y tablas

Cuatro a seis en total, y cada una tiene que ganarse el espacio: la que no se comenta en el
texto, sobra.

- **Funde paneles.** Cuatro figuras de la tesis que muestran la misma métrica en cuatro
  condiciones se convierten en una figura de cuatro paneles (a)–(d) con eje compartido.
- **Regenera, no recortes.** Una figura recortada del PDF de la tesis se ve borrosa impresa a
  dos columnas. Si existen los datos o el script, regenera a la anchura de columna de la
  plantilla (típicamente 8,5 cm a una columna, 17,5 cm a doble) con tipografía de 8–9 pt.
  Vectorial (PDF/EPS) para gráficos, 300 dpi para fotos, 600 dpi para líneas rasterizadas.
- **Tablas de la tesis, siempre demasiado grandes.** Deja las columnas que se discuten,
  redondea a cifras significativas razonables, usa `booktabs` y ninguna línea vertical, y
  mueve las columnas de control al suplementario.
- **Los pies de figura del artículo se leen solos**: qué muestra, en qué condiciones, qué
  significan las barras de error. En la tesis podían apoyarse en el texto de alrededor; aquí
  no, porque el revisor mira las figuras antes de leer.

## Referencias

De 100–150 en la tesis a 30–60 en el artículo. Se quedan: las que sostienen el hueco, las
que aportan el método, aquellas con las que se comparan los resultados y las obras
fundacionales imprescindibles. Se caen: los manuales y libros de texto genéricos, las
fuentes web sin revisión, las normas que ya no se aplican y las citas de cortesía.

Al recortar es fácil dejar citas huérfanas (`\cite` a una entrada que ya no existe) o
entradas nunca citadas; `scripts/check_articulo.py` las encuentra. Aprovecha para actualizar:
si la tesis se defendió hace dos años, faltan trabajos recientes y un revisor lo notará.

## Resumen, título y palabras clave

El **resumen** del artículo no es el de la tesis. 150–250 palabras (mira el límite de la
revista) y con resultados numéricos dentro: contexto en una o dos frases, hueco, qué se hizo,
qué se encontró **con cifras**, y qué implica. Sin citas, sin abreviaturas sin definir, sin
`en este trabajo se pretende`. Algunas revistas exigen resumen estructurado con
encabezados; si es el caso, respeta exactamente sus etiquetas.

El **título** de la tesis suele describir el tema; el del artículo debe transmitir el
hallazgo, en 10–15 palabras y sin `Un estudio sobre` ni `Análisis de`.

*Tesis:* "Análisis del rendimiento de sistemas fotovoltaicos en el departamento de
Caaguazú: un estudio de caso" → *Artículo:* "El ensuciamiento reduce un 18 % la producción
fotovoltaica en clima subtropical húmedo".

Las **palabras clave**: 4–6, las que un colega escribiría en el buscador, sin repetir las
del título si la revista lo prohíbe, y usando el tesauro de la revista cuando exista.

## Material suplementario

Adonde va lo que se cae pero sigue siendo útil: protocolos e instrumentos completos,
resultados de todas las condiciones, análisis de sensibilidad, código y datos, demostraciones
largas, capturas del sistema. Se cita en el texto (`ver material suplementario, tabla S3`) y
se entrega en un fichero aparte. Comprueba si la revista lo acepta y en qué formato; algunas
lo publican sin revisar y otras no lo aceptan.

Ojo: no es un desván. Si un resultado hace falta para creer la afirmación central, va en el
artículo, aunque ocupe.
