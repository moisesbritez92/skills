---
name: redactor-tesis
description: "Redacta y revisa texto académico (TFM, TFG, tesis, papers, memorias) aplicando un estilo impersonal, claro y sobrio, y comprobando los aspectos formales: ortografía, estructura en capítulos y epígrafes, tablas y figuras, citas y referencias, notas al pie y presentación. Úsala al escribir un capítulo, reescribir un borrador, revisar redacción o preparar la entrega de un trabajo académico."
---

# Redactor de tesis

Escribir para que el lector entienda la investigación al primer intento. Toda decisión de
estilo se resuelve a favor de la claridad, nunca del lucimiento.

## Cuándo hacer qué

| Petición | Modo |
|---|---|
| "escribe / redacta el apartado X" | **Redactar**: aplicar las reglas desde la primera frase |
| "revisa / corrige / mejora este texto" | **Revisar**: pasar el checklist y devolver el texto corregido + lista de cambios |
| "prepara la entrega / repasa el formato" | **Formal**: solo los aspectos formales de más abajo |

En modo revisar, **no reescribir lo que ya funciona**. Se corrige lo que incumple una regla
concreta; cada cambio debe poder justificarse señalando la regla.

## Uso del lenguaje

1. **Solo las palabras que comunican la idea.** Eliminar rellenos: *cabe destacar que*,
   *es importante señalar que*, *en el marco de*, *a nivel de*, *de alguna manera*.
   Si al quitar un fragmento la frase sigue diciendo lo mismo, sobraba.
2. **Sin repeticiones ni frases rebuscadas.** No repetir el mismo sustantivo o verbo en
   frases contiguas; usar sinónimo o pronombre, salvo en términos técnicos, donde la
   repetición literal es preferible a la variación (un concepto, un término, siempre el
   mismo).
3. **Conectores entre ideas.** Cada párrafo enlaza con el anterior. Marcar la relación
   lógica de forma explícita: adición (*además*, *asimismo*), contraste (*sin embargo*,
   *en cambio*), causa (*puesto que*, *debido a*), consecuencia (*por tanto*, *de ahí que*),
   orden (*en primer lugar*, *a continuación*), cierre (*en conjunto*, *en definitiva*).
4. **Discurso despersonalizado.** Nada de *yo*, *nosotros*, *mi trabajo*, ni apelaciones al
   lector (*como se puede ver*, *fíjese en*, *veamos*). Recursos: pasiva refleja
   (*se analizan*, *se observa que*), tercera persona (*el estudio muestra*, *los datos
   indican*), nominalización moderada (*el análisis de los resultados revela*).
5. **Frases cortas y registro formal.** Objetivo: 15–25 palabras por frase, una idea
   principal por frase, máximo una subordinada encadenada. Sin coloquialismos
   (*un montón de*, *súper*, *al final del día*) ni interrogaciones retóricas.
6. **Sin raya ni guion largo.** No se usa la raya (`—`, *em dash*) como signo de
   puntuación, ni para incisos ni para pausas enfáticas. Sustitutos, por orden de
   preferencia: coma para el inciso breve, paréntesis para el inciso explicativo, dos
   puntos para lo que anuncia una consecuencia o una enumeración, y punto y seguido cuando
   la frase da para dos. El guion medio (`–`) queda solo para rangos numéricos (15–25) y el
   guion corto (`-`) para palabras compuestas.
7. **Vocabulario sobrio.** Sin léxico recargado, jerga hiperespecializada innecesaria,
   metáforas ni eufemismos. Todo término técnico se define la primera vez que aparece;
   toda sigla se desarrolla en su primera aparición: *modelo de lenguaje visual (VLM)*.

Ejemplos de reescritura en `references/ejemplos-reescritura.md`.

## Aspectos formales

- **Ortografía y puntuación.** Tildes (incluidas mayúsculas), concordancia, comas en
  incisos y tras conectores iniciales, uso correcto de punto y coma. En español: comilla
  latina «», decimales con coma, cursiva para extranjerismos no adaptados.
- **Estructura.** Capítulos y epígrafes numerados jerárquicamente (1, 1.1, 1.2.1), sin
  bajar del tercer nivel salvo necesidad. Ningún epígrafe con un solo subepígrafe. Cada
  capítulo abre con una frase que anuncia su contenido y cierra enlazando con el siguiente.
- **Síntesis visual.** La información densa (comparativas, series de resultados,
  configuraciones experimentales) va en tabla, gráfico o figura, no en prosa. Todo elemento
  lleva número, título (tabla: encima; figura: debajo), fuente si es ajena, y se **cita en
  el texto antes de aparecer** (*véase la Tabla 3*). Una figura que el texto no menciona no
  debe estar.
- **Citas y referencias: sistema IEEE.** Cita numérica entre corchetes en el orden de
  primera aparición (`[1]`, `[3], [7]`, `[4]-[6]`) y lista final ordenada por ese mismo
  número, nunca alfabéticamente. La referencia va **antes** del punto: `… reduce el error
  [12].` Toda afirmación no propia se cita; toda cita tiene entrada en la bibliografía y
  toda entrada aparece citada al menos una vez. **Nunca inventar referencias, DOI, años ni
  números de página**: si un dato falta, marcarlo como `[PENDIENTE: referencia]`.
  Si un documento ya redactado usa otro sistema, respetarlo y avisar de la discrepancia.
- **Notas al pie.** Solo para precisiones que romperían el hilo del texto. Nunca para
  contenido esencial ni como sustituto de la cita bibliográfica.
- **Presentación.** Texto justificado, interlineado sencillo, una sola familia tipográfica
  para el cuerpo, sangría o espaciado entre párrafos (no ambos), sin colores decorativos ni
  recursos gráficos ajenos al contenido.

Detalle de formatos de cita y plantillas en `references/formato-y-citas.md`.

## Resumen, abstract y palabras clave

Las instrucciones para autores de la revista o institución prevalecen sobre estas pautas:
verificá idioma, extensión, estructura, número de palabras clave y formato antes de redactar.

- **Resumen y abstract.** Redactar uno o dos párrafos, salvo que la normativa indique otra
  extensión. Deben permitir comprender el problema, objetivo, método, resultado principal y
  conclusión sin leer el documento completo. Exponer desde el inicio el hallazgo o aporte más
  relevante; no reservarlo para la última frase. Incorporar de forma natural los términos que
  describen el trabajo, con lenguaje claro para lectores de áreas próximas. Limitar la jerga y
  explicar los tecnicismos imprescindibles. El abstract debe reflejar con fidelidad el resumen,
  no ser una traducción libre que cambie alcance, cifras o conclusiones.
- **Palabras clave.** Seleccionar normalmente entre tres y cinco, salvo indicación distinta.
  Preferir métodos, variables, autores, poblaciones, técnicas o subdisciplinas específicas del
  trabajo. Evitar términos demasiado amplios, como «filosofía» o «filología», que aportan poca
  capacidad de descubrimiento. Revisar los tesauros, índices o listas de términos habituales de
  la disciplina cuando existan. Las palabras clave deben aparecer de forma natural en el título,
  resumen o abstract, sin repetirlas artificialmente.
- **Descubrimiento.** El título, resumen, abstract y palabras clave se indexan en buscadores y
  bases como Google Scholar, PubMed, Web of Science y EBSCO. Elegir términos precisos mejora que
  el trabajo pueda encontrarse, leerse y citarse, incluso por quienes no accedan a la revista.
  No incluir afirmaciones, resultados ni referencias que no aparezcan o no estén respaldados en
  el cuerpo del manuscrito.

## Si el trabajo se redacta en LaTeX

Comandos, entradas `.bib` y errores frecuentes en `references/latex-ieee.md`. Lo esencial:

- Citar con `\cite{clave}`; la numeración la asigna BibTeX por orden de aparición y **no se
  escribe a mano**. La cita va antes del punto: `… reduce el error \cite{clave}.`
- Antes de citar, leer el `.bib` del proyecto y usar sus claves. Si la obra no está, se
  añade la entrada; si falta un dato, `[PENDIENTE: referencia]` en el texto y aviso al
  final. Nunca se inventa una entrada para que compile.
- Figuras y tablas con `\caption` y `\label`, citadas en el texto con `\cref{}` antes de
  aparecer.
- No se toca el fichero de estilo para resolver un problema de redacción.

## Checklist antes de dar por cerrado un texto

- [ ] Ninguna marca de primera persona ni apelación al lector
- [ ] Ninguna frase por encima de ~30 palabras sin justificación
- [ ] Cada párrafo enlaza con el anterior mediante un conector
- [ ] Sin muletillas ni relleno; sin metáforas ni eufemismos
- [ ] Ninguna raya (`—`) en el texto; incisos con comas o paréntesis
- [ ] Siglas desarrolladas y términos definidos en su primera aparición
- [ ] Resumen y abstract incluyen objetivo, método, resultado principal y conclusión, y respetan
  las instrucciones de la revista o institución
- [ ] Tres a cinco palabras clave específicas, salvo que la normativa establezca otra cantidad
- [ ] Tablas y figuras numeradas, tituladas y citadas en el texto
- [ ] Citas IEEE `[n]` correlativas por orden de aparición y bibliografía en ese orden
- [ ] Todas las citas con entrada en bibliografía, y a la inversa
- [ ] Ortografía y puntuación revisadas
- [ ] Numeración de epígrafes coherente y sin niveles huérfanos

Al terminar una revisión, informar de lo corregido en una lista breve y señalar de forma
explícita lo que quedó sin resolver (referencias pendientes, datos que faltan, decisiones
del autor).
