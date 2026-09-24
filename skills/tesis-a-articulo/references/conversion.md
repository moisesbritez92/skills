# Conversión: recetas técnicas

Índice: leer la fuente · Word → LaTeX · LaTeX → Word · bibliografía · figuras · ecuaciones ·
tablas · lo que pandoc siempre rompe.

Comprueba primero qué hay instalado; las recetas suponen `pandoc` y una distribución LaTeX:

```bash
for c in pandoc pdflatex latexmk bibtex pdftoppm pdftotext detex convert; do
  printf "%-10s %s\n" "$c" "$(command -v $c || echo NO)"; done
```

Si falta algo que hace falta de verdad (por ejemplo `pdflatex` para compilar), dilo en vez de
entregar un `.tex` que no has visto compilar.

**Si falta la clase de la revista** (`kpsewhich IEEEtran.cls` devuelve vacío), no la
sustituyas por `article` y entregues eso como si nada. Por orden: pide al usuario el paquete
oficial, que se descarga de la web de la revista o de la galería de plantillas de Overleaf y
que casi siempre ya tiene; si hay red y `tlmgr`, instálalo; y si no hay manera, redacta el
contenido en `article` **avisando por escrito** de que falta el paso de maquetar en la
plantilla real y de que los límites de página aún no se han comprobado. Un `.tex` que no has
compilado nunca es un entregable a medias, y hay que decirlo.

## Leer la fuente

**Proyecto LaTeX repartido en varios ficheros.** Sigue los `\input`/`\include` desde
`main.tex`. Si existe `latexpand`, `latexpand main.tex > plano.tex` deja todo en uno; si no,
`scripts/inventario.py` ya resuelve las inclusiones para contar.

**Word.** `pandoc tesis.docx -t markdown -o tesis.md --extract-media=media/` da el texto
legible y saca las imágenes incrustadas a `media/`. Para inspeccionar estilos y estructura
sin convertir: `unzip -o tesis.docx -d _t && grep -o 'w:val="[^"]*"' _t/word/document.xml | sort | uniq -c | sort -rn | head`.

**PDF.** `pdftotext -layout tesis.pdf -` mantiene columnas y tablas mucho mejor que sin
`-layout`. Las figuras salen con `pdfimages -png tesis.pdf fig`, pero a la resolución con la
que se incrustaron: si están rasterizadas a 96 dpi no valen para publicar y hay que pedir los
originales.

## Word → LaTeX

```bash
pandoc tesis.docx -o cuerpo.tex --extract-media=figuras/ --wrap=preserve
```

Luego se trasplanta ese cuerpo a la plantilla de la revista; **nunca al revés**. Es decir:
partes del ejemplo de la plantilla que ya compila, y vas pegando secciones dentro.

Qué revisar siempre después de convertir:

- Las citas de Word (campos de Zotero o Mendeley) salen como texto plano, no como `\cite`.
  Pide el `.bib` exportado del gestor y vuelve a citar; buscar y reemplazar a mano sobre
  cincuenta citas produce errores silenciosos.
- Los títulos con formato directo (negrita 14 pt en vez de estilo `Título 1`) no se
  convierten en `\section`. Se detectan como párrafos sueltos en negrita.
- Los pies de figura quedan como párrafos normales: hay que reconstruir los entornos
  `figure`/`table` con `\caption` y `\label`.
- Las referencias cruzadas ("ver Figura 12") quedan como texto fijo; conviértelas a `\ref`.

## LaTeX → Word

```bash
pandoc main.tex -o articulo.docx \
  --reference-doc=plantilla_revista.docx \
  --citeproc --bibliography=refs.bib --csl=ieee.csl \
  --resource-path=.:figuras
```

`--reference-doc` es la pieza clave: pandoc toma de ahí los estilos (fuentes, títulos,
márgenes), así que pásale la plantilla de la revista, no un documento cualquiera. Los
nombres de estilo deben existir en esa plantilla; si la revista usa nombres propios
(`JournalTitle1`), habrá que renombrar después con la skill `docx`.

Antes de convertir, prepara el `.tex`:

- Sustituye o define de forma simple tus macros. Pandoc entiende `\newcommand` sencillos que
  estén en el propio fichero, pero no macros con `\@` ni definidas en un `.sty` aparte.
- Convierte las figuras PDF/EPS a PNG a 300–600 dpi: Word no incrusta PDF.
- Las figuras TikZ hay que compilarlas antes a PDF y luego a PNG; pandoc no las ejecuta.

Después de convertir, abre el `.docx`, conviértelo a PDF y **mira las páginas**. Es el único
modo de ver ecuaciones rotas y tablas desbordadas.

## Bibliografía

**Para LaTeX:** conserva el `.bib` de la tesis, recorta las entradas que ya no se citan y
usa el `.bst` de la revista (`IEEEtran`, `elsarticle-num`, `splncs04`, `ACM-Reference-Format`).
Compila con `pdflatex → bibtex → pdflatex → pdflatex`, o directamente `latexmk -pdf`.
Algunas revistas piden el `.bbl` pegado dentro del `.tex` en el envío final.

Limpieza que casi siempre hace falta en un `.bib` de tesis: proteger las mayúsculas de siglas
con llaves (`{DNA}`), completar `doi` y páginas, quitar los `url` de artículos con DOI si el
estilo no los quiere, y unificar los nombres de revista (abreviados o completos, pero no
mezclados).

**Para Word:** `--citeproc` con el `.csl` del estilo (IEEE, APA 7, Vancouver, Chicago). Los
`.csl` se descargan del repositorio de estilos de Zotero; si no hay red, pandoc trae varios
de serie (`pandoc --list-highlight-styles` no es esto: los CSL se pasan por ruta, así que
consíguelos antes). Comprueba a mano tres o cuatro referencias contra el ejemplo de la
revista, porque un CSL desactualizado produce diferencias sutiles.

Las citas quedan como **texto plano**, no como campos de Word. Si el usuario va a seguir
editando con Zotero, avísale: tendrá que reinsertarlas desde el gestor.

## Figuras

- Anchura objetivo: una columna ≈ 8,5 cm, doble columna ≈ 17,5 cm. Genera la figura a ese
  tamaño físico en vez de escalarla con `width=0.6\textwidth`, que encoge la letra.
- Texto dentro de la figura a 8–9 pt una vez colocada. Si al ver el PDF no se lee, se
  rehace; no se amplía el hueco.
- Vectorial siempre que sea posible (PDF o EPS para LaTeX, EMF o PNG a 600 dpi para Word).
  Fotos a 300 dpi. `convert -density 600 fig.pdf fig.png` para rasterizar.
- Nada de capturas del PDF de la tesis. Se nota, y en producción las rechazan.
- Comprueba que las figuras se entienden en escala de grises si la revista cobra por color, y
  que no dependen solo del color para distinguir series.

## Ecuaciones

- **Word → LaTeX:** pandoc convierte OMML a LaTeX bastante bien. Las ecuaciones que estén
  como *imagen* no se recuperan y hay que reescribirlas.
- **LaTeX → Word:** pandoc genera OMML nativo, que es lo que quieren las editoriales. Los
  entornos multilínea (`align`, `cases`) salen como un bloque, a veces con la alineación
  perdida; revísalos uno a uno.
- Numera solo las ecuaciones que se citan en el texto (`\begin{equation}` para esas,
  `\[ ... \]` para el resto).
- Unifica la notación con la de la tesis, pero renumera desde 1.

## Tablas

- `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) y **ninguna línea vertical**: es la
  convención en casi todas las revistas científicas.
- Las tablas anchas van en `table*` (doble columna) o giradas con `sidewaystable` del paquete
  `rotating`, si la clase lo admite.
- Pandoc genera `longtable`, que **se rompe en clases a dos columnas**. Sustituye
  `\begin{longtable}...` por `\begin{table}\centering\begin{tabular}...`.
- Alinea los números por la coma o el punto decimal (`siunitx` con `S`), con el mismo número
  de decimales en toda la columna.
- El título va **encima** de la tabla y debajo de la figura, salvo que la revista diga otra
  cosa.

## Lo que pandoc siempre rompe

Repásalo con la lista delante después de cada conversión:

| Rompe | Arreglo |
|---|---|
| Macros propias y paquetes cargados aparte | Expandirlas antes de convertir |
| `subfigure` / `subcaption` | Recomponer la figura como una sola imagen o a mano |
| Entornos `algorithm`, `lstlisting`, `minted` | Reescribir en el destino |
| `cleveref`, `glossaries`, `acronym` | Sustituir por texto o `\ref` normal |
| Referencias cruzadas hacia Word | Quedan como texto fijo; renumerar o rehacer |
| Colores y estilos de `tikz` | Compilar aparte a imagen |
| Notas al pie dentro de tablas | Rehacer con `\tablefootnote` o nota bajo la tabla |

Ninguna conversión automática sale lista para enviar. La conversión ahorra el trabajo
mecánico; el repaso es siempre a mano y siempre mirando el PDF final.
