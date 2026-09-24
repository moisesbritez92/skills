#!/usr/bin/env python3
"""Revision de un borrador de articulo antes de enviarlo.

Uso:
    python3 check_articulo.py main.tex --limite-paginas 8
    python3 check_articulo.py articulo.docx --limite-palabras 6000
    python3 check_articulo.py main.tex --pdf main.pdf --limite-paginas 6

Detecta restos de voz de tesis, muletillas, figuras y citas descolgadas, retoques de
plantilla y bloques sin rellenar. Lo mecanico lo ve el script; el fondo hay que leerlo.
Devuelve 1 si encuentra algo bloqueante.
"""

import argparse
import os
import re
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

RESIDUOS = [
    (r"\b(en (el|la) (presente|este|esta) (cap[ií]tulo|apartado|secci[oó]n de la tesis))", "autorreferencia de tesis"),
    (r"\b(este|el presente) (cap[ií]tulo|trabajo de fin de (grado|m[aá]ster)|trabajo final de grado)", "autorreferencia de tesis"),
    (r"\b(cap[ií]tulo|chapter)\s+[0-9IVX]+\b", "referencia a un capitulo"),
    (r"\b(como se (vio|expuso|mencion[oó]) en el (cap[ií]tulo|apartado))", "autorreferencia de tesis"),
    (r"\ba lo largo de (esta|la presente) (tesis|memoria|investigaci[oó]n)\b", "voz de tesis"),
    (r"\bobjetivos? (general|espec[ií]ficos?)\b", "aparato de anteproyecto"),
    (r"\b(justificaci[oó]n del (estudio|trabajo)|alcance y limitaciones)\b", "aparato de anteproyecto"),
    (r"\\section\*?\{\s*(Marco te[oó]rico|Objetivos|Justificaci[oó]n|Anexos?)\s*\}", "seccion de tesis"),
    (r"\b(Anexo|Ap[eé]ndice)\s+[A-Z0-9]\b", "referencia a un anexo"),
    (r"\b(Figura|Tabla|Cuadro|Ecuaci[oó]n)\s+\d+\.\d+", "numeracion heredada de la tesis"),
    (r"\b(el|los) (tribunal|jurado|miembros del tribunal)\b", "dirigido al tribunal"),
    (r"\bse espera que (este|el presente) (trabajo|estudio) (contribuya|sirva)", "voz de tesis"),
    (r"\b(se cumpli[oó]|se cumplieron) (satisfactoriamente )?(el|los) objetivos?\b", "cierre de tesis"),
    (r"\bin this (chapter|thesis|dissertation)\b", "autorreferencia de tesis (ingles)"),
    (r"\bthe (aim|objective) of this (thesis|dissertation)\b", "voz de tesis (ingles)"),
]

MULETILLAS = [
    r"\bcabe (destacar|mencionar|se[nñ]alar|resaltar)\b",
    r"\bes importante (destacar|mencionar|se[nñ]alar|recordar)\b",
    r"\ben el mundo (actual|de hoy)\b",
    r"\bhoy en d[ií]a\b",
    r"\bde cara al futuro\b",
    r"\bjuega un papel (fundamental|clave|crucial)\b",
    r"\bno solo\b[^.]{0,80}\bsino (que )?tambi[eé]n\b",
    r"\babre (nuevas )?posibilidades\b",
    r"\bun desaf[ií]o (significativo|importante)\b",
    r"\ben este sentido\b",
    r"\bse puede (observar|apreciar) que\b",
    r"\bresulta (interesante|fundamental|crucial)\b",
    r"\bes (ampliamente|comunmente|com[uú]nmente) (utilizado|conocido)\b",
    r"\bit is (important|worth) (to note|noting)\b",
    r"\bplays a (crucial|key|vital) role\b",
    r"\bin today'?s (world|society)\b",
    r"\bdelve into\b",
]

RETOQUES = [
    (r"\\usepackage(\[[^\]]*\])?\{geometry\}", "geometry: cambia los margenes de la plantilla"),
    (r"\\geometry\{", "geometry: cambia los margenes de la plantilla"),
    (r"\\addtolength\{\\(textheight|textwidth|topmargin|oddsidemargin)", "retoque de caja de texto"),
    (r"\\fontsize\{", "cambio manual de tamano de letra"),
    (r"\\(small|footnotesize|scriptsize|tiny)\b\s*\n?\s*\\begin\{(tabular|table)", "tabla encogida"),
    (r"\\vspace\{\s*-", "espacio negativo para ganar sitio"),
    (r"\\setlength\{\\(textfloatsep|floatsep|intextsep|abovecaptionskip|baselineskip)", "retoque de espaciado"),
    (r"\\linespread\{0?\.", "interlineado reducido"),
]

PENDIENTES = [
    r"\[\[FALTA[^\]]*\]\]", r"\bTODO\b", r"\bFIXME\b", r"\bXXX\b", r"\?\?\?",
    r"\blorem ipsum\b", r"\blipsum\b",
    r"Author Name", r"Nombre Apellido", r"First Author", r"Given Name Surname",
    r"Conference acronym", r"XXX'\d", r"978-1-XXXX", r"your@email", r"correo@dominio",
    r"Universidad, Ciudad, Pa[ií]s", r"name of organization",
]


class Informe(object):
    def __init__(self):
        self.items = []

    def add(self, nivel, titulo, detalles=None):
        self.items.append((nivel, titulo, detalles or []))

    def imprimir(self):
        orden = {"X": 0, "!": 1, "ok": 2}
        marca = {"X": "[X]", "!": "[!]", "ok": "[ok]"}
        for nivel, titulo, detalles in sorted(self.items, key=lambda i: orden[i[0]]):
            print("%-4s %s" % (marca[nivel], titulo))
            for d in detalles[:6]:
                print("       - %s" % d)
            if len(detalles) > 6:
                print("       ... y %d mas" % (len(detalles) - 6))
        graves = sum(1 for n, _, _ in self.items if n == "X")
        avisos = sum(1 for n, _, _ in self.items if n == "!")
        print("\n%d bloqueantes, %d para revisar." % (graves, avisos))
        return 1 if graves else 0


# --------------------------------------------------------------------- utilidades

def cargar_tex(ruta, vistos=None):
    vistos = vistos if vistos is not None else set()
    ruta = os.path.abspath(ruta)
    if ruta in vistos or not os.path.exists(ruta):
        return ""
    vistos.add(ruta)
    with open(ruta, encoding="utf-8", errors="replace") as fh:
        texto = re.sub(r"(?<!\\)%.*", "", fh.read())
    base = os.path.dirname(ruta)

    def sub(m):
        d = m.group(1).strip()
        if not d.endswith(".tex"):
            d += ".tex"
        return "\n" + cargar_tex(os.path.join(base, d), vistos) + "\n"

    return re.sub(r"\\(?:input|include)\s*\{([^}]*)\}", sub, texto)


def texto_docx(ruta):
    with zipfile.ZipFile(ruta) as z:
        raiz = ET.fromstring(z.read("word/document.xml"))
    return "\n".join("".join(t.text or "" for t in p.iter(W + "t"))
                     for p in raiz.iter(W + "p"))


def palabras_de(texto, es_tex):
    t = texto
    if es_tex:
        for env in ("equation", "align", "gather", "figure", "table", "tabular",
                    "lstlisting", "verbatim", "tikzpicture", "thebibliography"):
            t = re.sub(r"\\begin\{%s\*?\}.*?\\end\{%s\*?\}" % (env, env), " ", t, flags=re.S)
        t = re.sub(r"\$[^$]*\$", " ", t)
        t = re.sub(r"\\[a-zA-Z@]+\*?", " ", t)
        t = re.sub(r"[{}\[\]~^&_\\]", " ", t)
    return len([p for p in re.split(r"\s+", t)
                if re.search(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", p)])


def paginas_pdf(ruta):
    for cmd in (["pdfinfo", ruta], ["qpdf", "--show-npages", ruta]):
        try:
            s = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            continue
        m = re.search(r"Pages:\s*(\d+)", s) or re.match(r"\s*(\d+)", s)
        if m:
            return int(m.group(1))
    return None


def ocurrencias(texto, patron):
    return [m.group(0).strip()[:70] for m in re.finditer(patron, texto, re.I)]


# ------------------------------------------------------------------------ chequeos

def revisar_texto(texto, inf):
    encontrados = []
    for patron, etiqueta in RESIDUOS:
        for x in ocurrencias(texto, patron):
            encontrados.append("%s  (%s)" % (x, etiqueta))
    if encontrados:
        inf.add("X", "Restos de voz de tesis (%d)" % len(encontrados), encontrados)
    else:
        inf.add("ok", "Sin restos evidentes de voz de tesis")

    mule = []
    for patron in MULETILLAS:
        mule.extend(ocurrencias(texto, patron))
    if mule:
        inf.add("!", "Muletillas de relleno (%d)" % len(mule), mule)

    guiones = len(re.findall("\u2014", texto)) + len(re.findall(r"(?<!-)---(?!-)", texto))
    if guiones:
        inf.add("!", "Guiones largos: %d. En espanol academico usa comas, parentesis "
                     "o dos puntos." % guiones)

    pend = []
    for patron in PENDIENTES:
        pend.extend(ocurrencias(texto, patron))
    if pend:
        inf.add("X", "Marcadores o texto de plantilla sin rellenar (%d)" % len(pend), pend)


def revisar_tex(ruta, texto, args, inf):
    # abstract y keywords
    if not re.search(r"\\begin\{abstract\}|\\abstract\{", texto):
        inf.add("X", "No encuentro el resumen (abstract)")
    if not re.search(r"keywords|IEEEkeywords|\\keyword|palabras[ -]clave", texto, re.I):
        inf.add("!", "No encuentro palabras clave")

    # figuras y tablas: caption, label, citado
    for entorno, prefijo in (("figure", "figura"), ("table", "tabla")):
        bloques = re.findall(r"\\begin\{%s\*?\}(.*?)\\end\{%s\*?\}" % (entorno, entorno),
                             texto, re.S)
        sin_caption = sum(1 for b in bloques if "\\caption" not in b)
        if sin_caption:
            inf.add("X", "%d %s(s) sin \\caption" % (sin_caption, prefijo))
        etiquetas = re.findall(r"\\label\{([^}]*)\}", "".join(bloques))
        citadas = set(re.findall(r"\\(?:ref|autoref|cref|Cref|eqref)\{([^}]*)\}", texto))
        huerfanas = [e for e in etiquetas if e not in citadas]
        if huerfanas:
            inf.add("X", "%s(s) que no se citan en el texto" % prefijo.capitalize(), huerfanas)
        if bloques:
            inf.add("ok", "%d %s(s) con caption" % (len(bloques) - sin_caption, prefijo))

    total_flotantes = (len(re.findall(r"\\begin\{figure\*?\}", texto)) +
                       len(re.findall(r"\\begin\{table\*?\}", texto)))
    if total_flotantes > 8:
        inf.add("!", "%d figuras y tablas: en un articulo suelen ser 4-6" % total_flotantes)

    # referencias
    claves = set()
    for m in re.finditer(r"\\(?:cite|citep|citet|citeauthor|parencite|textcite)\s*"
                         r"(?:\[[^\]]*\])*\s*\{([^}]*)\}", texto):
        claves.update(k.strip() for k in m.group(1).split(",") if k.strip())
    entradas = {}
    directorio = os.path.dirname(os.path.abspath(ruta))
    for raiz, _, fs in os.walk(directorio):
        for f in fs:
            if f.endswith(".bib"):
                with open(os.path.join(raiz, f), encoding="utf-8", errors="replace") as fh:
                    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)", fh.read()):
                        entradas[m.group(1)] = f
    if entradas:
        rotas = sorted(claves - set(entradas))
        sin_citar = sorted(set(entradas) - claves)
        if rotas:
            inf.add("X", "Citas a entradas que no existen en el .bib (%d)" % len(rotas), rotas)
        if sin_citar:
            inf.add("!", "Entradas del .bib que ya no se citan (%d): quitalas"
                    % len(sin_citar), sin_citar)
        if not rotas and not sin_citar:
            inf.add("ok", "Bibliografia consistente (%d referencias)" % len(claves))
    if claves and len(claves) < 15:
        inf.add("!", "Solo %d referencias citadas; la mayoria de revistas esperan 20-60"
                % len(claves))

    # tablas con lineas verticales
    verticales = [s for s in re.findall(r"\\begin\{tabular\}\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}", texto)
                  if "|" in s]
    if verticales:
        inf.add("!", "%d tabla(s) con lineas verticales; usa booktabs sin verticales"
                % len(verticales))

    # retoques de plantilla
    retoques = []
    for patron, etiqueta in RETOQUES:
        if re.search(patron, texto, re.S):
            retoques.append(etiqueta)
    if retoques:
        inf.add("X", "Retoques de la plantilla para ganar espacio", sorted(set(retoques)))


def main():
    ap = argparse.ArgumentParser(description="Revision de un borrador de articulo.")
    ap.add_argument("fichero", help="main.tex o articulo.docx")
    ap.add_argument("--limite-paginas", type=int, default=None)
    ap.add_argument("--limite-palabras", type=int, default=None)
    ap.add_argument("--pdf", default=None, help="PDF compilado (si no, se busca junto al .tex)")
    args = ap.parse_args()

    if not os.path.exists(args.fichero):
        sys.exit("No existe: %s" % args.fichero)
    es_tex = args.fichero.lower().endswith(".tex")
    texto = cargar_tex(args.fichero) if es_tex else texto_docx(args.fichero)

    inf = Informe()
    print("=" * 72)
    print("REVISION: " + args.fichero)
    print("=" * 72)

    n = palabras_de(texto, es_tex)
    if args.limite_palabras:
        if n > args.limite_palabras:
            inf.add("X", "%d palabras: %d por encima del limite de %d"
                    % (n, n - args.limite_palabras, args.limite_palabras))
        else:
            inf.add("ok", "%d palabras (limite %d)" % (n, args.limite_palabras))
    else:
        inf.add("ok", "%d palabras en el cuerpo" % n)

    pdf = args.pdf or (args.fichero[:-4] + ".pdf" if es_tex else None)
    if pdf and os.path.exists(pdf):
        p = paginas_pdf(pdf)
        if p and args.limite_paginas:
            if p > args.limite_paginas:
                inf.add("X", "%d paginas: %d por encima del limite de %d. Quita contenido, "
                             "no reduzcas la letra" % (p, p - args.limite_paginas, args.limite_paginas))
            else:
                inf.add("ok", "%d paginas (limite %d)" % (p, args.limite_paginas))
        elif p:
            inf.add("ok", "%d paginas" % p)
    elif args.limite_paginas:
        inf.add("!", "No encuentro el PDF compilado; no puedo contar paginas")

    revisar_texto(texto, inf)
    if es_tex:
        revisar_tex(args.fichero, texto, args, inf)

    codigo = inf.imprimir()
    print("\nEsto es la revision mecanica. Falta mirar el PDF pagina a pagina y comprobar")
    print("la lista de references/envio.md antes de enviar.")
    sys.exit(codigo)


if __name__ == "__main__":
    main()
