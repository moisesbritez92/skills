---
name: estilo-ieee
description: Revisa, corrige o redacta desde cero artículos, tesis, TFG, TFM e informes técnicos según el IEEE Editorial Style Manual y la IEEE Reference Guide, con foco en citas numéricas y lista de referencias IEEE (citas agrupadas o desordenadas, APA mezclado, referencias incompletas o sin abreviar, figuras, tablas, siglas, unidades, ecuaciones y estructura). Trabaja con .docx, .tex/.bib, .md y PDF, en español o inglés. Usala siempre que se hable de estilo, formato, citas, referencias o normas IEEE, bibliografía numérica, IEEEtran, pasar de APA a IEEE, revisar o corregir la bibliografía o las citas de un trabajo técnico o de ingeniería, preparar un artículo para una revista o congreso IEEE, o escribir un documento nuevo con citas IEEE, aunque no se nombre el manual. Si también aplica una norma institucional (p. ej. anteproyecto FCyT UNCA) o se convierte una tesis en artículo, usala junto con esa skill.
---

# Estilo y citas IEEE

Esta skill aplica las reglas del *IEEE Editorial Style Manual for Authors* y de la *IEEE Reference Guide* a documentos existentes o nuevos. Tiene tres modos:

1. **Revisar**: informe de problemas, sin tocar el archivo.
2. **Corregir**: devolver el archivo corregido más un resumen de cambios.
3. **Redactar desde cero** siguiendo IEEE (citas, referencias, figuras, tablas, redacción).

Si el pedido no deja claro si quiere informe o corrección, corregí y entregá también el informe: es lo que casi siempre se busca. Si el documento es largo y los cambios son de fondo (renumerar 80 referencias, rehacer la estructura), avisá el alcance en una línea antes de empezar.

## Archivos de apoyo

Leelos según lo que haga falta; no hace falta cargar todos siempre.

| Archivo | Cuándo |
|---|---|
| `references/referencias.md` | Siempre que haya citas o lista de referencias. Plantillas por tipo de fuente, abreviaturas, etiquetas en español, LaTeX/BibTeX. |
| `references/estructura.md` | Artículos para revista o congreso; figuras, tablas, ecuaciones, encabezados, agradecimientos. Sección 11: qué aplica a una tesis. |
| `references/redaccion.md` | Revisión de estilo: siglas, números, unidades, rayas, matemática, gramática, lenguaje inclusivo, adaptación al español. |
| `scripts/revisar_ieee.py` | Primera pasada automática sobre el documento. |

## Paso 1: situar el documento

Antes de tocar nada, determiná tres cosas (casi siempre se deducen del archivo y del pedido; preguntá solo si falta algo que cambia el resultado, y en un único mensaje):

- **Tipo**: artículo para revista o congreso IEEE, o trabajo académico (tesis, TFG, TFM, anteproyecto, informe). En un artículo se aplica el manual completo. En un trabajo académico se aplican las citas, las referencias y el estilo, pero la estructura la manda la norma de la institución (ver `estructura.md`, sección 11).
- **Idioma**: las reglas propias del inglés (contracciones, ortografía estadounidense, coma serial) no se aplican a un documento en español; ahí rige la RAE y la adaptación descrita en `redaccion.md`, sección 11.
- **Norma institucional**: si el usuario la menciona o el documento la sigue claramente (por ejemplo "Figura 1" y "Tabla 1" en todo el texto), respetala en lo que regula y aplicá IEEE en lo demás. Si hay otra skill instalada para esa norma (como `anteproyecto-fcyt-unca`), leela también: ella manda en estructura y esta en los detalles IEEE.

## Paso 2: primera pasada automática

```bash
python /ruta/a/estilo-ieee/scripts/revisar_ieee.py documento.docx --salida /home/claude/revision.md
python /ruta/a/estilo-ieee/scripts/revisar_ieee.py articulo.tex refs.bib --salida /home/claude/revision.md
```

Acepta `.docx`, `.tex` (con uno o más `.bib`), `.md`, `.txt` y `.pdf`. Detecta idioma solo; se puede forzar con `--idioma es|en`. Clasifica en ERROR (contradice una regla explícita), AVISO (probable problema, confirmar en contexto) y SUGERENCIA (estilo o decisión que depende de la norma).

El script es una ayuda, no el veredicto. Tiene falsos positivos (un intervalo matemático `[1, 2]` puede parecer una cita agrupada; una sigla puede estar definida de otra forma) y no ve lo que exige leer. Por eso el paso 3 es obligatorio.

## Paso 3: lectura completa

Leé el documento entero (para `.docx`, `pandoc -t markdown` da una vista cómoda). Confirmá o descartá cada hallazgo del script y revisá lo que el script no puede ver:

- **Referencias incompletas**: faltan volumen, número, páginas, mes, editorial, ciudad o DOI. Si hay búsqueda web, verificá cada dato en la fuente (IEEE Xplore, sitio de la revista, Crossref, repositorio de la universidad) antes de completarlo. **Nunca inventes un dato bibliográfico**: si no se puede verificar, dejá `[FALTA: páginas]` o similar y listalo en el resumen.
- **Tipo de fuente mal formateado**: un capítulo con formato de libro, un artículo de congreso sin "in", una tesis sin universidad, una página web sin fecha de acceso. Compará cada entrada con su plantilla en `referencias.md`.
- **Abreviaturas de revistas y congresos**: aplicá las de `referencias.md`, sección 5; para revistas no listadas usá ISO 4 y avisá.
- **Autor mencionado en el texto** que no coincide con la lista, o nombre de autor innecesario junto al número.
- **Siglas**: definidas en el primer uso del resumen y otra vez en el cuerpo; usadas de forma coherente después.
- **Figuras y tablas**: toda figura y tabla se menciona en el texto antes o cerca de su aparición, en orden; leyendas y títulos con el formato de `estructura.md`.
- **Ecuaciones**: numeración consecutiva sin saltos; puntuación de la oración que las contiene.
- **Estructura** (solo artículos): orden de las partes, resumen de 150–250 palabras en un párrafo, Index Terms en orden alfabético, encabezados, agradecimientos en tercera persona, financiamiento en la primera nota al pie, declaración de uso de IA.
- **Redacción**: consistencia de guiones y grafías, números, unidades, rayas, listas, concordancia.

**No toques el contenido técnico ni el estilo personal del autor.** IEEE corrige forma, no fondo. Si una corrección puede cambiar el significado (reordenar una frase con fórmulas, cambiar un término técnico, "caja negra" en un contexto de control), no la apliques: señalala como consulta.

## Paso 4a: entregar la revisión

Informe en la respuesta (o en archivo si es muy largo), ordenado por impacto:

1. Resumen en dos o tres oraciones: estado general y lo más urgente.
2. Citas y referencias: problemas de coherencia (citas sin entrada, entradas sin cita, orden), luego entrada por entrada con la versión corregida propuesta.
3. Figuras, tablas, ecuaciones y estructura.
4. Estilo y redacción, agrupando repeticiones ("12 rangos con guion en lugar de raya corta, p. ej. párr. 14 y 31").
5. Consultas al autor: datos faltantes y cambios que podrían alterar el sentido.

Mostrá siempre el "antes → después" en las referencias; es lo que el usuario más necesita copiar.

## Paso 4b: corregir el archivo

### Word (.docx)
Leé primero la skill `docx` (`/mnt/skills/public/docx/SKILL.md`) y seguí su flujo de edición (descomprimir, `merge_runs.py`, editar `document.xml`, validar). Por defecto entregá **con control de cambios** (autor "Revisión IEEE") para que el autor vea y acepte cada corrección; si pidió una versión limpia, entregá también la copia con los cambios aceptados. Consultas al autor como comentarios de Word en el lugar exacto.

Cuidados propios de Word:
- **Numeración automática**: si la lista usa numeración de Word o campos `SEQ`/`REF`, no la conviertas en texto sin avisar. Si la numeración automática no muestra corchetes, cambiá el formato del número de la lista a `[%1]` en `numbering.xml`.
- **Gestores de referencias** (Zotero, Mendeley, EndNote, citas nativas de Word): los campos se reconocen por `ADDIN ZOTERO_ITEM`, `ADDIN EN.CITE`, `CITATION` en `w:instrText`. Si están, lo correcto es cambiar el estilo en el gestor (estilo "IEEE") y no editar el texto del campo, porque el gestor lo sobrescribe. Explicáselo al usuario y corregí solo lo que el gestor no controla.
- **Raya corta**: carácter U+2013 (–). Espacio fino en miles: U+2009. No uses el guion común en rangos.

### LaTeX (.tex + .bib)
Editá los archivos directamente. Clase `IEEEtran` si es un artículo IEEE; `\bibliographystyle{IEEEtran}`, `\bibliography{IEEEabrv,refs}`, `\usepackage{cite}`. Corregí el `.bib` (campos faltantes, `--` en páginas, macros de mes, siglas protegidas con llaves, DOI sin prefijo) y dejá que el estilo haga el resto; no escribas números de cita a mano. Compilá si hay TeX disponible (`pdflatex`, `bibtex`, `pdflatex` ×2) para verificar que no quedan `[?]`.

### Markdown o texto
Editá directamente y entregá el archivo.

### PDF
No se puede corregir un PDF con fidelidad. Entregá el informe y la lista de referencias corregida completa, lista para pegar, y ofrecé reconstruir el documento en Word si el usuario lo necesita.

### Renumerar referencias
Cuando el orden de primera cita no coincide con la lista, o hay que separar, fusionar o eliminar entradas:

1. Recorré el texto en orden y armá el mapa `número viejo → número nuevo` según la primera aparición. Las entradas que nadie cita se señalan (no se borran sin preguntar); si el usuario quiere conservarlas, van al final.
2. Aplicá el mapa **en una sola pasada** con marcadores temporales (`[1]` → `⟦R7⟧` → `[7]`) para no pisar números ya cambiados.
3. Rehacé los rangos con los números nuevos: `[3]–[5]` puede dejar de ser consecutivo y pasar a `[4], [8], [9]`; ordená los números dentro de cada grupo.
4. Reordená la lista según el mapa.
5. Verificá con el script que no quedan citas sin entrada ni entradas sin cita.
6. Informá al usuario que se renumeró (el manual pide consultar siempre al autor al renumerar).

### Resumen de cambios
Al terminar, un resumen breve: qué se cambió por categoría con cantidades, qué quedó como consulta y qué datos faltan. Sin repetir el documento.

## Modo redactar desde cero

Cuando el usuario pide escribir algo nuevo "con citas IEEE" o "en formato IEEE":

- **Fuentes reales**: si hay búsqueda web, buscá y verificá cada fuente (autores, título, revista, volumen, número, páginas, año, DOI) antes de citarla. Sin búsqueda o sin fuente verificable, dejá `[CITA PENDIENTE: tema]` en lugar de inventar.
- **Numerá mientras escribís**: llevá un registro fuente → número en orden de primera aparición; una fuente conserva su número en todas las citas posteriores.
- **Citas**: `[1]`, `[1], [3]`, `[2]–[5]`, `[4, Fig. 2]`, `[4, p. 12]`, dentro de la puntuación y como parte de la oración cuando convenga ("en [3] se propone…"). Nada de autor-año.
- **Lista**: al final, en el orden del registro, cada entrada con la plantilla de su tipo (`referencias.md`), etiquetas en el idioma del documento y de forma uniforme.
- **Figuras y tablas**: "Fig. 1." bajo la figura, "TABLE I" / "TABLA I" encima de la tabla (o la forma de la institución), mencionadas en orden en el texto.
- **Ecuaciones**: numeradas consecutivamente, citadas como "(3)".
- **Redacción**: siglas definidas en el primer uso, unidades con espacio, rangos con raya corta, sin contracciones en inglés.
- **Formato del entregable**: para Word seguí la skill `docx` (lista de referencias con sangría francesa, números `[n]` en columna); para LaTeX usá `IEEEtran` con `.bib`. Esqueleto mínimo de artículo:

```latex
\documentclass[journal]{IEEEtran}
\usepackage{cite}
\usepackage{amsmath,graphicx}
\begin{document}
\title{Título en Title Case}
\author{Nombre~Apellido,~\IEEEmembership{Member,~IEEE}
\thanks{Received …; This work was supported by … (Corresponding author: …)}}
\maketitle
\begin{abstract} Un párrafo de 150 a 250 palabras, sin citas. \end{abstract}
\begin{IEEEkeywords} Términos en orden alfabético. \end{IEEEkeywords}
\section{Introduction}
\IEEEPARstart{T}{his} article … \cite{clave1,clave2}.
\section{Conclusion}
\section*{Acknowledgment}
\bibliographystyle{IEEEtran}
\bibliography{IEEEabrv,refs}
\end{document}
```

## Conversión desde APA u otro estilo

Pedido frecuente. Pasos: (1) listar las citas autor-año en orden de aparición y asignar números; (2) reemplazar cada "(Autor, año)" por `[n]` y cada "Autor (año)" por "Autor [n]" o "en [n]" según la frase; varias fuentes en un paréntesis pasan a `[n], [m]`; (3) reordenar la lista por número y reescribir cada entrada con la plantilla IEEE (iniciales antes del apellido, título entre comillas en *sentence case*, revista abreviada en cursiva, `vol.`, `no.`, `pp.`, mes abreviado, año, DOI); (4) verificar con el script. Ojo con "Pérez (2019a)" y "Pérez (2019b)": son dos números distintos.

## Criterios cuando hay duda

- Consistencia primero: una forma aplicada en todo el documento vale más que dos formas "correctas" mezcladas.
- La norma de la institución o de la revista destino prevalece sobre el manual general en lo que regula.
- Ante una regla ambigua del manual, elegí la opción que menos cambie el texto y mencionala.
- Si el usuario prohíbe algo que IEEE admite (por ejemplo la raya larga en la prosa), obedecé al usuario.
