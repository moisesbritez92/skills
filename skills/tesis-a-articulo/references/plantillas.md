# Plantillas de revistas y congresos

Índice: principio general · IEEEtran · elsarticle · Springer Nature · LNCS · ACM · MDPI ·
plantilla LaTeX desconocida · plantillas Word · lo que la plantilla no dice.

## Principio general

La plantilla es ley y no se negocia. Márgenes, tipografía, tamaño, interlineado, estilo de
citas y bloque de autores vienen dados; tocarlos para ganar espacio es la forma más rápida
de que devuelvan el artículo sin revisarlo. Cuando el gusto propio y la plantilla choquen,
gana la plantilla.

El orden que funciona con cualquier plantilla nueva:

1. Descarga el paquete oficial completo (`.cls`, `.bst`, ejemplo, figuras de muestra).
2. Compila el ejemplo **sin tocarlo** y comprueba que sale el PDF. Si falla aquí, es problema
   del entorno, no tuyo.
3. Sustituye el contenido por bloques, compilando cada dos o tres. Un error de LaTeX es
   trivial de localizar si acabas de cambiar una sección, e infernal si has cambiado todo.
4. No copies el preámbulo de otro artículo tuyo encima. Los paquetes que la clase ya carga
   (`hyperref`, `caption`, `geometry`, `graphicx`) provocan conflictos difíciles de leer.

## IEEEtran

`\documentclass[conference]{IEEEtran}` — congresos, 2 columnas · `[journal]` — revistas ·
`[10pt,twocolumn]` según el caso.

```latex
\documentclass[conference]{IEEEtran}
\title{Título que transmite el hallazgo}
\author{\IEEEauthorblockN{Nombre Apellido}
\IEEEauthorblockA{\textit{Departamento} \\ \textit{Universidad} \\ Ciudad, País \\ correo@dominio}}
\begin{document}\maketitle
\begin{abstract} ... \end{abstract}
\begin{IEEEkeywords} palabra, palabra, palabra \end{IEEEkeywords}
...
\bibliographystyle{IEEEtran}\bibliography{referencias}
\end{document}
```

Trampas: las figuras a doble columna necesitan `figure*` y solo salen arriba de página; el
resumen va **después** de `\maketitle`; las secciones se numeran solas en romanos, así que no
escribas el número en el título; para equilibrar las columnas de la última página está
`\balance` (paquete `balance`); no metas números de página si el congreso pide la versión de
cámara lista. Estilo de cita numérico `[1]`, en orden de aparición.

## elsarticle (Elsevier)

```latex
\documentclass[preprint,12pt]{elsarticle}   % review, 1p, 3p, 5p, final
\begin{document}
\begin{frontmatter}
\title{...}
\author[uni]{Nombre Apellido}
\affiliation[uni]{organization={Facultad}, city={Ciudad}, country={País}}
\begin{abstract} ... \end{abstract}
\begin{keyword} uno \sep dos \sep tres \end{keyword}
\end{frontmatter}
```

Trampas: el entorno es `keyword` en singular y los términos se separan con `\sep`; todo el
bloque inicial va dentro de `frontmatter`; con la opción `review` conviene `\linenumbers`
porque los revisores de Elsevier los piden; casi todas sus revistas exigen además
**Highlights** (3–5 frases de 85 caracteres como máximo) y una *declaración de disponibilidad
de datos*, que no están en el `.tex` sino en el formulario de envío. Estilos:
`elsarticle-num` (numérico) o `elsarticle-harv` (autor-año); mira cuál usa la revista.

## Springer Nature (sn-jnl)

```latex
\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}
\title[Título corto]{Título completo}
\author*[1]{\fnm{Nombre}\sur{Apellido}\email{correo@dominio}}
\affil[1]{\orgdiv{Departamento}, \orgname{Universidad}, \city{Ciudad}, \country{País}}
\abstract{...}
\keywords{uno, dos, tres}
```

Trampas: el asterisco de `\author*` marca al autor de correspondencia y es obligatorio; el
resumen y las palabras clave son **comandos con argumento**, no entornos; la opción de estilo
bibliográfico se elige en la clase (`sn-mathphys-num`, `sn-nature`, `sn-apa`...) y arrastra
el `.bst` correspondiente; Springer pide secciones de declaraciones al final (financiación,
conflictos de interés, contribución de autores).

## LNCS (Springer, congresos)

```latex
\documentclass{llncs}
\title{...}\titlerunning{Título corto}
\author{Nombre Apellido\inst{1}\orcidID{0000-0000-0000-0000}}
\authorrunning{N. Apellido}
\institute{Universidad, Ciudad, País \email{correo@dominio}}
\maketitle
\begin{abstract} ... \keywords{uno \and dos \and tres} \end{abstract}
```

Trampas: las palabras clave van **dentro** del entorno `abstract` y se separan con `\and`;
`\titlerunning` y `\authorrunning` son obligatorios si los originales son largos; el límite
de páginas de LNCS incluye las referencias, lo que sorprende a mucha gente al final;
bibliografía con `splncs04.bst`; nada de `hyperref` cargado a mano, la clase lo gestiona.

## ACM (acmart)

`\documentclass[sigconf]{acmart}` para congresos, `[acmsmall]` para revistas,
`[manuscript,review,anonymous]` para el envío a doble ciego.

Trampas: hay que rellenar `\acmConference`, `\copyrightyear`, `\setcopyright` y el bloque de
conceptos CCS (se genera en la web de ACM y se pega tal cual); `\keywords{}` va antes de
`\maketitle`; para un preprint, `\settopmatter{printacmref=false}` quita el bloque de
referencia ACM; la bibliografía usa `natbib` con `ACM-Reference-Format`, así que las citas
son `\citep`/`\citet` y no `\cite` a secas.

## MDPI

`\documentclass[journal,article,submit,pdftex]{Definitions/mdpi}` con la carpeta
`Definitions/` completa que viene en el paquete. Comandos propios: `\Title`, `\Author`,
`\address`, `\abstract{}`, `\keyword{}`. No intentes recrear la clase a mano; descarga el
paquete entero. MDPI exige además secciones fijas al final (contribuciones de autores,
financiación, comité de ética, disponibilidad de datos, conflictos de interés) y su plantilla
Word es igual de válida que la de LaTeX.

## Plantilla LaTeX desconocida

Cuando el `.cls` no es de ninguna familia conocida (revistas locales, plantillas de
universidad):

```bash
python3 scripts/detectar_plantilla.py <directorio>
grep -nE "\\\\(newcommand|renewcommand|DeclareOption|ProvidesClass|newenvironment)" *.cls | head -60
```

Busca en ese orden: el `\ProvidesClass` con fecha y versión; los `\DeclareOption` (te dicen
qué modos admite); los `\newcommand` de `\title`, `\author`, `\keywords`, `\abstract` (te
dicen qué sintaxis espera); y sobre todo el fichero de ejemplo. **El ejemplo vale más que la
documentación**: copia su estructura literalmente y sustituye el contenido.

Si la plantilla no define algo que necesitas (por ejemplo, no admite subsecciones), no la
parchees: reorganiza el contenido para que quepa en lo que la plantilla ofrece. Que un
artículo tenga estructura rara porque el autor forzó la clase se nota en el PDF.

## Plantillas de Word (.dotx / .docx)

Muchas revistas iberoamericanas y varias grandes editoriales solo dan plantilla Word.

- **Trabaja con los estilos, no con formato directo.** Aplica `Título 1`, `Resumen`,
  `Texto normal`, `Epígrafe`, los que la plantilla defina. La editorial maqueta a partir de
  esos estilos: un texto en negrita 14 pt "que parece un título" no le sirve.
- Para ver qué estilos hay antes de escribir:
  ```bash
  unzip -o plantilla.docx -d _pl >/dev/null && grep -o 'w:styleId="[^"]*"' _pl/word/styles.xml | sort -u
  ```
- No cambies márgenes, fuente ni interlineado, y conserva el orden de bloques de la
  plantilla (título, autores, filiación, resumen, palabras clave, cuerpo, referencias).
- Rellena sobre el ejemplo: abre la plantilla y sustituye el texto de muestra, en lugar de
  crear un documento nuevo con aspecto parecido.
- Las ecuaciones tienen que ser objetos de ecuación de Word (OMML), no imágenes, salvo que
  la revista diga lo contrario. `references/conversion.md` explica cómo pasarlas.
- Si la revista pide las figuras en ficheros aparte además de incrustadas, entrega ambas
  cosas con la nomenclatura que pidan (`Figura1.tif`, etc.).

Para generar el `.docx` usa la skill `docx`; para verificarlo, conviértelo a PDF y mira las
páginas.

## Lo que la plantilla no dice

Las *instrucciones para autores* de la revista mandan sobre la plantilla, y suelen exigir
cosas que el `.cls` no incluye: límite real de palabras o páginas, resumen estructurado con
etiquetas concretas, declaración de disponibilidad de datos, contribución de cada autor
(CRediT), ORCID, aprobación del comité de ética, financiación, conflictos de interés,
número de figuras en color y su coste, y a veces un límite de referencias. Léelas antes de
maquetar y comprueba una por una antes de enviar; `references/envio.md` tiene la lista.
