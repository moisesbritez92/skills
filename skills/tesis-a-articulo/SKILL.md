---
name: tesis-a-articulo
description: Convierte una tesis, TFG, TFM, disertación o memoria (en LaTeX, Word o PDF) en un artículo científico listo para enviar, en LaTeX o en Word, ajustado a la plantilla de la revista o congreso de destino (IEEE, Elsevier, Springer/LNCS, ACM, MDPI, plantillas .cls o .dotx propias). Comprime 10:1 con criterio, reescribe la voz de tesis en voz de paper, reordena la argumentación en torno a una sola afirmación y cumple los límites de formato. Usa esta skill siempre que se hable de convertir, adaptar, extraer o "sacar un paper" de una tesis, TFG, TFM, PFG, tesina, disertación, monografía o capítulo, de pasar un trabajo de Word a LaTeX o de LaTeX a Word para publicar, de ajustarse a la plantilla o al formato de una revista o congreso, de límites de páginas o palabras, de IEEEtran, elsarticle, llncs, acmart o cualquier .cls de revista, y también para reformatear un artículo ya escrito a otra plantilla o para revisar un borrador antes de enviarlo. Vale en español y en inglés, aunque no se mencione la palabra plantilla.
---

# De tesis a artículo científico

## Lo que realmente hay que hacer

Esto no es una conversión de formato: es una reescritura con una compresión de entre 5:1 y
10:1. Una tesis de 30 000 palabras se convierte en un artículo de 6 000. Y la tesis y el
artículo no persiguen lo mismo, así que ni siquiera se comprime de forma uniforme:

- La tesis **demuestra competencia** ante un tribunal: explica lo que aprendió el autor,
  incluye el marco teórico completo y documenta todo lo que se hizo.
- El artículo **defiende una sola afirmación** ante pares que ya conocen el campo: cuenta
  solo lo necesario para que esa afirmación resulte creíble y reproducible.

De ahí salen los tres fracasos típicos, y conviene tenerlos presentes durante todo el trabajo:

1. **El artículo sigue siendo un resumen de la tesis.** Tiene cinco secciones que son cinco
   capítulos encogidos, treinta páginas de marco teórico reducidas a seis, y ninguna
   afirmación central. Un editor lo devuelve sin mandarlo a revisión.
2. **Incumple la plantilla.** Se pasa del límite de páginas, usa un estilo de cita distinto
   del que exige la revista o rompe el bloque de autores. Es rechazo de mesa antes de leer
   el contenido.
3. **Arrastra la voz de tesis.** "En el presente capítulo", "como se vio en el apartado
   anterior", "el objetivo general de este trabajo". Delata copiar y pegar, y el revisor
   deja de leer con buena fe.

**Regla innegociable: no inventar nada.** Cada cifra, cada *p*, cada tamaño de muestra y
cada cita salen de la tesis. Al comprimir aparecerán huecos (un dato que estaba en un anexo,
una referencia que ya no encaja); márcalos como `[[FALTA: ...]]` y pregunta al final. Un
número inventado en un artículo enviado es mala conducta científica, no un descuido.

## Flujo de trabajo

### 1. Leer e inventariar la fuente antes de proponer nada

Localiza el original: proyecto LaTeX (`main.tex` y sus `\input`, el `.bib`, las figuras),
`.docx`, o PDF si no hay otra cosa. Léelo de verdad, no solo el índice.

```bash
python3 scripts/inventario.py <ruta-tesis> --objetivo 6000
```

Devuelve palabras por capítulo, figuras, tablas, ecuaciones, citas únicas y el factor de
compresión que hace falta. Sirve para negociar con el usuario sobre datos y no sobre
intuiciones: es muy distinto recortar 3:1 que 12:1.

Anota mientras lees: la afirmación que sostiene el trabajo, los resultados con sus números,
las figuras que de verdad prueban algo, las macros del preámbulo y el estilo de citación.

### 2. Decidir cuál es el artículo, y a dónde va

Dos decisiones que condicionan todo lo demás, así que se toman antes de escribir una línea:

**Una sola afirmación.** Pide al usuario que complete: "Este artículo demuestra que ___".
Si no cabe en una frase, o hay dos artículos o todavía no está claro cuál es la
contribución. Una tesis buena suele dar uno o dos artículos, no cinco.

**El destino.** Revista o congreso concreto, porque de ahí salen el límite de páginas o
palabras, la plantilla, el estilo de citas, el idioma y hasta la estructura de secciones.
Sin destino no se puede planificar; si el usuario no lo tiene, ayúdale a elegir a partir de
dónde publican las referencias que más cita la tesis, y mientras tanto trabaja con un
supuesto explícito.

Pregunta también, en una sola tanda: idioma del artículo, coautores y su orden, filiación,
si la tesis ya está publicada en un repositorio, y si hay figuras con datos fuente
disponibles para regenerarlas.

### 3. Conseguir la plantilla y obedecerla

La plantilla manda sobre cualquier preferencia estética, incluidas las de esta skill.

```bash
python3 scripts/detectar_plantilla.py <directorio-o-fichero>
```

Identifica la familia (IEEEtran, elsarticle, sn-jnl, llncs, acmart, MDPI, plantilla Word o
`.cls` desconocido) e imprime sus exigencias y el esqueleto de preámbulo correcto. Los
detalles de cada familia y qué hacer con una plantilla que no conoces están en
`references/plantillas.md`; léela antes de montar nada.

Con una plantilla nueva, el orden que evita perder una tarde: compila primero el ejemplo tal
cual viene, comprueba que sale el PDF, y solo entonces sustituye el contenido. Nunca al
revés. Si la clase no está instalada, pídesela al usuario en vez de maquetar con `article` y
entregarlo como si fuera lo mismo.

### 4. Escribir el plan antes que el artículo

Copia `assets/plan.md` y rellénalo: afirmación, destino, presupuesto de palabras por
sección, mapa de qué capítulo alimenta qué sección, las 4–6 figuras que sobreviven, qué se
va a material suplementario y qué se cae del todo.

Enséñaselo al usuario y ajústalo **antes** de redactar. Discutir un plan cuesta cinco
minutos; reescribir un artículo entero porque el marco teórico se comió la mitad del espacio
cuesta un día. `references/compresion.md` tiene los presupuestos por formato y el mapa
capítulo→sección con lo que se salva y lo que no.

### 5. Reescribir, no recortar

Una sección de artículo no es el capítulo de la tesis con frases borradas: se escribe otra
vez desde el plan, mirando la tesis como fuente de datos. Borrar frases deja transiciones
rotas y párrafos que arrancan a media idea; se nota enseguida.

Dos referencias mandan aquí:

- `references/compresion.md` — qué sobrevive de cada capítulo, cómo se convierten treinta
  páginas de marco teórico en dos párrafos de trabajo relacionado, cómo se funden figuras,
  cuántas referencias quedan, resumen estructurado y título.
- `references/estilo.md` — el cambio de voz de tesis a paper, tiempos verbales, primera
  persona, qué léxico delata texto generado (empezando por los guiones largos) y pares
  antes/después. Si el artículo va en inglés y la tesis está en español, esta referencia
  explica por qué no se traduce, se reescribe.

### 6. Montar el artefacto

`references/conversion.md` tiene las recetas técnicas: `pandoc` en las dos direcciones,
bibliografía (`.bib` → estilo de la revista, o CSL para Word), figuras a resolución de
imprenta, ecuaciones OMML↔LaTeX, tablas con `booktabs`, y la lista de cosas que `pandoc`
siempre rompe con su arreglo.

Para salida en Word usa además la skill `docx`, y respeta los **estilos** de la plantilla
(`Heading 1`, `Abstract`, `Caption`) en vez de dar formato a mano: es lo que después usa la
editorial para maquetar.

### 7. Compilar, medir y mirar las páginas

```bash
latexmk -pdf -interaction=nonstopmode main.tex
python3 scripts/check_articulo.py main.tex --limite-paginas 8
```

`check_articulo.py` detecta restos de voz de tesis, figuras y tablas sin citar en el texto,
referencias huérfanas o sin citar, guiones largos, muletillas de relleno, líneas verticales
en tablas, exceso de páginas o palabras y bloques de plantilla sin rellenar. Lo mecánico lo
ve el script; el fondo lo tienes que leer tú.

Después rasteriza y **mira el PDF**, que es donde se ven los desbordes de columna, las
figuras ilegibles y las tablas que se salen del margen:

```bash
pdftoppm -png -r 80 main.pdf pg   # y abre las imágenes
```

Si algo no cabe, se quita contenido. Nunca se reduce el tamaño de letra ni se toquetean los
márgenes de la plantilla: los editores lo comprueban.

### 8. Entregar

Entrega el artículo compilado y sus fuentes, y con ello:

- La lista de lo que quedó fuera y a dónde fue (suplementario o descartado), para que el
  usuario pueda discrepar.
- Los `[[FALTA: ...]]` pendientes.
- Una nota sobre publicación previa: casi todas las revistas aceptan artículos derivados de
  una tesis depositada en un repositorio, pero muchas piden declararlo en la carta de
  presentación, y el solapamiento aparece en los detectores de similitud. `references/envio.md`
  cubre esto, la carta de presentación y la lista de comprobación previa al envío.

## Casos que se salen del flujo

- **Solo reformatear** un artículo ya escrito a otra plantilla: salta a los pasos 3, 6 y 7.
  No reescribas el contenido sin avisar.
- **Tesis por compendio**: el trabajo va al revés (los artículos ya existen y se integran).
  Aquí solo sirve la parte de plantillas y conversión.
- **Varios artículos de una tesis**: haz el plan de todos a la vez para repartir figuras y
  resultados sin solaparlos, y luego escribe uno. El solapamiento entre artículos propios sí
  es un problema real.
- **Revisar un borrador ajeno**: pasa `check_articulo.py`, lee, y da un diagnóstico
  priorizado (primero lo que impide publicar, luego lo mejorable) en vez de reescribirlo
  entero por tu cuenta.
- **Solo hay PDF de la tesis**: extrae el texto, avisa de que las figuras saldrán
  rasterizadas y pide los originales o los datos fuente antes de dar por buena una figura.

## Contenido de la skill

```
references/plantillas.md   familias de plantillas, exigencias y esqueletos; plantillas desconocidas
references/compresion.md   mapa capítulo→sección, presupuestos, figuras, resumen, título
references/estilo.md       voz de tesis → voz de artículo; qué delata texto generado
references/conversion.md   pandoc, bibliografía, figuras, ecuaciones, tablas, docx↔latex
references/envio.md        publicación previa, autoría, carta de presentación, checklist
scripts/inventario.py      mide la fuente y calcula el factor de compresión
scripts/detectar_plantilla.py  identifica la plantilla e imprime sus requisitos
scripts/check_articulo.py  revisión del borrador antes de enviar
assets/plan.md             plantilla del plan del artículo (paso 4)
```
