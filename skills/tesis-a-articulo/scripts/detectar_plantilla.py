#!/usr/bin/env python3
"""Identifica la plantilla de destino e imprime lo que exige.

Uso:
    python3 detectar_plantilla.py <directorio-o-fichero>

Reconoce las familias habituales de LaTeX y analiza plantillas de Word. Con un .cls
desconocido, extrae de el lo necesario para trabajar: opciones, comandos propios y ejemplo.
Los detalles de cada familia estan en references/plantillas.md.
"""

import argparse
import os
import re
import sys
import zipfile

try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass



W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

FAMILIAS = {
    "IEEEtran": {
        "nombre": "IEEE (IEEEtran)",
        "citas": "numerico [1], estilo IEEEtran.bst",
        "exige": [
            "resumen en \\begin{abstract} DESPUES de \\maketitle",
            "palabras clave en \\begin{IEEEkeywords}",
            "autores con \\IEEEauthorblockN y \\IEEEauthorblockA",
            "figuras a doble columna con figure* (solo salen arriba de pagina)",
        ],
        "trampas": [
            "no escribas el numero de seccion: la clase los pone en romanos",
            "\\balance equilibra las columnas de la ultima pagina",
            "la opcion conference elimina las notas de filiacion al pie",
        ],
        "esqueleto": r"""\documentclass[conference]{IEEEtran}
\title{...}
\author{\IEEEauthorblockN{Nombre Apellido}
\IEEEauthorblockA{\textit{Departamento} \\ \textit{Universidad} \\ Ciudad, Pais \\ correo}}
\begin{document}\maketitle
\begin{abstract} ... \end{abstract}
\begin{IEEEkeywords} uno, dos, tres \end{IEEEkeywords}
\section{Introduccion}
\bibliographystyle{IEEEtran}\bibliography{refs}
\end{document}""",
    },
    "elsarticle": {
        "nombre": "Elsevier (elsarticle)",
        "citas": "elsarticle-num o elsarticle-harv, segun la revista",
        "exige": [
            "todo el bloque inicial dentro de \\begin{frontmatter}",
            "entorno keyword EN SINGULAR, terminos separados con \\sep",
            "\\affiliation con sintaxis clave=valor (organization=, city=, country=)",
        ],
        "trampas": [
            "casi todas sus revistas piden Highlights: 3-5 frases de <=85 caracteres",
            "declaracion de disponibilidad de datos en el formulario de envio",
            "con la opcion review conviene \\linenumbers",
        ],
        "esqueleto": r"""\documentclass[preprint,12pt]{elsarticle}
\begin{document}
\begin{frontmatter}
\title{...}
\author[a]{Nombre Apellido}
\affiliation[a]{organization={Facultad}, city={Ciudad}, country={Pais}}
\begin{abstract} ... \end{abstract}
\begin{keyword} uno \sep dos \sep tres \end{keyword}
\end{frontmatter}
\section{Introduction}
\bibliographystyle{elsarticle-num}\bibliography{refs}
\end{document}""",
    },
    "sn-jnl": {
        "nombre": "Springer Nature (sn-jnl)",
        "citas": "se elige en la opcion de clase: sn-mathphys-num, sn-nature, sn-apa...",
        "exige": [
            "\\author*[1] con asterisco para el autor de correspondencia",
            "\\abstract{} y \\keywords{} son COMANDOS con argumento, no entornos",
            "\\affil con \\orgdiv, \\orgname, \\city, \\country",
        ],
        "trampas": ["Springer pide declaraciones finales: financiacion, conflictos, "
                    "contribucion de autores"],
        "esqueleto": r"""\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}
\title[Titulo corto]{Titulo completo}
\author*[1]{\fnm{Nombre}\sur{Apellido}\email{correo}}
\affil[1]{\orgdiv{Departamento}, \orgname{Universidad}, \city{Ciudad}, \country{Pais}}
\abstract{...}
\keywords{uno, dos, tres}
\begin{document}\maketitle
\section{Introduction}
\bibliography{refs}
\end{document}""",
    },
    "llncs": {
        "nombre": "Springer LNCS (congresos)",
        "citas": "splncs04.bst",
        "exige": [
            "\\keywords{} DENTRO del entorno abstract, separadas con \\and",
            "\\titlerunning y \\authorrunning si titulo o autores son largos",
            "\\institute con \\email",
        ],
        "trampas": ["el limite de paginas de LNCS INCLUYE las referencias",
                    "no cargues hyperref a mano: la clase lo gestiona"],
        "esqueleto": r"""\documentclass{llncs}
\title{...}\titlerunning{Titulo corto}
\author{Nombre Apellido\inst{1}\orcidID{0000-0000-0000-0000}}
\authorrunning{N. Apellido}
\institute{Universidad, Ciudad, Pais \email{correo}}
\begin{document}\maketitle
\begin{abstract} ... \keywords{uno \and dos \and tres} \end{abstract}
\section{Introduction}
\bibliographystyle{splncs04}\bibliography{refs}
\end{document}""",
    },
    "acmart": {
        "nombre": "ACM (acmart)",
        "citas": "natbib con ACM-Reference-Format: usa \\citep y \\citet",
        "exige": [
            "\\acmConference, \\copyrightyear y \\setcopyright rellenados",
            "bloque de conceptos CCS generado en la web de ACM",
            "\\keywords{} antes de \\maketitle",
        ],
        "trampas": ["para preprint: \\settopmatter{printacmref=false}",
                    "para doble ciego: opciones review y anonymous"],
        "esqueleto": r"""\documentclass[sigconf]{acmart}
\copyrightyear{2026}\acmYear{2026}\setcopyright{acmlicensed}
\acmConference[XXX '26]{...}{...}{...}
\title{...}
\author{Nombre Apellido}\affiliation{\institution{Universidad}\country{Pais}}
\email{correo}
\keywords{uno, dos, tres}
\begin{document}
\begin{abstract} ... \end{abstract}
\maketitle
\section{Introduction}
\bibliographystyle{ACM-Reference-Format}\bibliography{refs}
\end{document}""",
    },
    "mdpi": {
        "nombre": "MDPI",
        "citas": "numerico con su propio .bst incluido en el paquete",
        "exige": ["la carpeta Definitions/ completa del paquete oficial",
                  "comandos propios: \\Title, \\Author, \\address, \\abstract{}, \\keyword{}"],
        "trampas": ["secciones fijas al final: contribuciones, financiacion, etica, "
                    "disponibilidad de datos, conflictos de interes",
                    "no recrees la clase a mano, descarga el paquete entero"],
        "esqueleto": r"""\documentclass[journal,article,submit,pdftex]{Definitions/mdpi}
\Title{...}
\Author{Nombre Apellido $^{1}$}
\address{$^{1}$ Universidad; correo}
\abstract{...}
\keyword{uno; dos; tres}
\begin{document}
\section{Introduction}
\end{document}""",
    },
    "revtex": {
        "nombre": "APS/AIP (RevTeX)",
        "citas": "numerico, apsrev4-2",
        "exige": ["\\affiliation justo despues de cada \\author",
                  "el resumen va dentro de \\begin{abstract} antes de \\maketitle"],
        "trampas": ["opciones reprint / preprint cambian por completo el aspecto",
                    "\\bibliographystyle{apsrev4-2} y bibliografia con natbib"],
        "esqueleto": r"""\documentclass[aps,prl,reprint]{revtex4-2}
\begin{document}
\title{...}
\author{Nombre Apellido}\affiliation{Universidad, Ciudad, Pais}
\begin{abstract} ... \end{abstract}
\maketitle
\section{Introduction}
\bibliography{refs}
\end{document}""",
    },
    "article": {
        "nombre": "clase article estandar (plantilla generica o preprint)",
        "citas": "la que elija el usuario; comprueba las normas de la revista",
        "exige": ["nada especifico: revisa las instrucciones para autores"],
        "trampas": ["si la revista tiene plantilla propia, usala en vez de article"],
        "esqueleto": r"""\documentclass[11pt,a4paper]{article}
\title{...}\author{Nombre Apellido}
\begin{document}\maketitle
\begin{abstract} ... \end{abstract}
\section{Introduccion}
\bibliographystyle{plain}\bibliography{refs}
\end{document}""",
    },
}

ALIAS = {
    "ieeetran": "IEEEtran", "ieeeconf": "IEEEtran", "elsarticle": "elsarticle",
    "sn-jnl": "sn-jnl", "svjour3": "sn-jnl", "llncs": "llncs", "acmart": "acmart",
    "mdpi": "mdpi", "revtex4-2": "revtex", "revtex4-1": "revtex", "revtex4": "revtex",
    "article": "article", "scrartcl": "article",
}

PISTAS_DOCX = [
    (r"elsevier", "plantilla de Elsevier en Word"),
    (r"springer", "plantilla de Springer en Word"),
    (r"mdpi", "plantilla de MDPI en Word"),
    (r"ieee", "plantilla de IEEE en Word"),
    (r"scielo|latindex|redalyc", "plantilla de revista iberoamericana"),
]


def mostrar_familia(clave, opciones=""):
    f = FAMILIAS[clave]
    print("=" * 72)
    print("PLANTILLA: " + f["nombre"] + ((" [opciones: %s]" % opciones) if opciones else ""))
    print("=" * 72)
    print("Citas: " + f["citas"])
    print("\nExige:")
    for x in f["exige"]:
        print("  - " + x)
    if f.get("trampas"):
        print("\nTrampas:")
        for x in f["trampas"]:
            print("  - " + x)
    print("\nEsqueleto minimo:\n")
    print(f["esqueleto"])
    print("\nDetalles y casos raros: references/plantillas.md")


def analizar_cls(ruta):
    with open(ruta, encoding="utf-8", errors="replace") as fh:
        texto = fh.read()
    print("=" * 72)
    print("PLANTILLA NO RECONOCIDA: " + os.path.basename(ruta))
    print("=" * 72)
    m = re.search(r"\\ProvidesClass\s*\{([^}]*)\}\s*(\[[^\]]*\])?", texto)
    if m:
        print("ProvidesClass: %s %s" % (m.group(1), m.group(2) or ""))
    opciones = re.findall(r"\\DeclareOption\s*\{([^}]*)\}", texto)
    if opciones:
        print("Opciones admitidas: " + ", ".join(sorted(set(opciones))[:25]))
    comandos = sorted(set(re.findall(r"\\(?:re)?newcommand\s*\*?\s*\{?\\([a-zA-Z@]+)", texto)))
    interes = [c for c in comandos if any(k in c.lower() for k in
               ("title", "author", "abstract", "keyword", "affil", "inst", "email",
                "address", "date", "running", "corres"))]
    if interes:
        print("Comandos propios relevantes: " + ", ".join("\\" + c for c in interes[:25]))
    entornos = sorted(set(re.findall(r"\\newenvironment\s*\{([^}]*)\}", texto)))
    if entornos:
        print("Entornos propios: " + ", ".join(entornos[:25]))
    paquetes = sorted(set(re.findall(r"\\RequirePackage\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}", texto)))
    if paquetes:
        print("Paquetes que ya carga (no los vuelvas a cargar): " + ", ".join(paquetes[:20]))
    print("""
Como seguir:
  1. Busca el .tex de ejemplo que acompana a la plantilla y compilalo SIN TOCARLO.
  2. Copia su estructura literalmente y sustituye el contenido por bloques.
  3. Si la plantilla no ofrece algo que necesitas, reorganiza el contenido en vez
     de parchear la clase.
  4. Las instrucciones para autores de la revista mandan sobre la plantilla.""")


def analizar_docx(ruta):
    print("=" * 72)
    print("PLANTILLA WORD: " + os.path.basename(ruta))
    print("=" * 72)
    try:
        with zipfile.ZipFile(ruta) as z:
            estilos = z.read("word/styles.xml").decode("utf-8", "replace")
            try:
                doc = z.read("word/document.xml").decode("utf-8", "replace")
            except KeyError:
                doc = ""
    except (OSError, zipfile.BadZipFile) as e:
        print("No puedo abrir el fichero: %s" % e)
        return
    ids = sorted(set(re.findall(r'w:styleId="([^"]*)"', estilos)))
    usados = sorted(set(re.findall(r'w:pStyle w:val="([^"]*)"', doc)))
    print("Estilos definidos (%d): %s" % (len(ids), ", ".join(ids[:40])))
    if usados:
        print("\nEstilos que usa el documento: " + ", ".join(usados[:30]))
    texto_bajo = (doc + estilos).lower()
    for patron, etiqueta in PISTAS_DOCX:
        if re.search(patron, texto_bajo):
            print("\nPista: parece " + etiqueta)
            break
    print("""
Como trabajar con ella:
  - Aplica los ESTILOS de arriba en vez de dar formato a mano: la editorial maqueta
    a partir de ellos.
  - Rellena sobre la propia plantilla, sustituyendo el texto de muestra; no crees un
    documento nuevo parecido.
  - No toques margenes, fuente ni interlineado.
  - Las ecuaciones deben ser objetos OMML de Word, no imagenes.
  - Genera el fichero con la skill docx y revisa el PDF pagina a pagina.""")


def main():
    ap = argparse.ArgumentParser(description="Identifica la plantilla de destino.")
    ap.add_argument("ruta", help="directorio de la plantilla, .cls, .tex, .docx o .dotx")
    args = ap.parse_args()

    ficheros = []
    if os.path.isdir(args.ruta):
        for raiz, _, fs in os.walk(args.ruta):
            for f in fs:
                if f.lower().endswith((".cls", ".tex", ".docx", ".dotx")):
                    ficheros.append(os.path.join(raiz, f))
    elif os.path.exists(args.ruta):
        ficheros = [args.ruta]
    else:
        sys.exit("No existe: %s" % args.ruta)
    if not ficheros:
        sys.exit("No encuentro .cls, .tex, .docx ni .dotx en %s" % args.ruta)

    # 1. documentclass en algun .tex
    for f in sorted(ficheros):
        if not f.lower().endswith(".tex"):
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            m = re.search(r"\\documentclass\s*(\[[^\]]*\])?\s*\{([^}]*)\}", fh.read())
        if m:
            clase = os.path.basename(m.group(2)).lower()
            clave = ALIAS.get(clase)
            print("Fichero principal: %s\n" % f)
            if clave:
                mostrar_familia(clave, (m.group(1) or "").strip("[]"))
                return
            print("documentclass{%s} no esta en la lista de familias conocidas.\n" % m.group(2))
            break

    # 2. .cls presentes
    for f in sorted(ficheros):
        if f.lower().endswith(".cls"):
            clave = ALIAS.get(os.path.basename(f)[:-4].lower())
            if clave:
                mostrar_familia(clave)
            else:
                analizar_cls(f)
            return

    # 3. plantilla Word
    for f in sorted(ficheros):
        if f.lower().endswith((".docx", ".dotx")):
            analizar_docx(f)
            return

    print("No he podido identificar la plantilla. Pide al usuario el paquete oficial "
          "de la revista (clase, ejemplo y estilo bibliografico).")


if __name__ == "__main__":
    main()
