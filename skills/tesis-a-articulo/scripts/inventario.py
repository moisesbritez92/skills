#!/usr/bin/env python3
"""Inventario de una tesis: palabras por capitulo, figuras, tablas, ecuaciones y citas.

Uso:
    python3 inventario.py <ruta>            # .tex, directorio de proyecto, .docx o .pdf
    python3 inventario.py tesis/ --objetivo 6000

Sirve para decidir el presupuesto del articulo con datos y no con intuiciones.
Solo usa la biblioteca estandar (para .pdf necesita pdftotext en el sistema).
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
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


# --------------------------------------------------------------------------- LaTeX

def quitar_comentarios(texto):
    return re.sub(r"(?<!\\)%.*", "", texto)


def cargar_tex(ruta, vistos=None):
    """Lee un .tex resolviendo \\input y \\include de forma recursiva."""
    vistos = vistos if vistos is not None else set()
    ruta = os.path.abspath(ruta)
    if ruta in vistos or not os.path.exists(ruta):
        return ""
    vistos.add(ruta)
    with open(ruta, encoding="utf-8", errors="replace") as fh:
        texto = quitar_comentarios(fh.read())
    base = os.path.dirname(ruta)

    def sustituir(m):
        destino = m.group(1).strip()
        if not destino.endswith(".tex"):
            destino += ".tex"
        return "\n" + cargar_tex(os.path.join(base, destino), vistos) + "\n"

    return re.sub(r"\\(?:input|include)\s*\{([^}]*)\}", sustituir, texto)


def buscar_main(directorio):
    candidatos = []
    for raiz, _, ficheros in os.walk(directorio):
        if any(p in raiz for p in (".git", "build", "_minted")):
            continue
        for f in ficheros:
            if f.endswith(".tex"):
                ruta = os.path.join(raiz, f)
                try:
                    with open(ruta, encoding="utf-8", errors="replace") as fh:
                        cabeza = fh.read(4000)
                except OSError:
                    continue
                if "\\documentclass" in cabeza:
                    candidatos.append((0 if f in ("main.tex", "tesis.tex") else 1, ruta))
    candidatos.sort()
    return candidatos[0][1] if candidatos else None


ENTORNOS_FUERA = ("equation", "align", "gather", "eqnarray", "multline", "figure",
                  "table", "tabular", "lstlisting", "verbatim", "minted", "tikzpicture",
                  "algorithm", "algorithmic", "thebibliography")


def palabras_tex(fragmento):
    t = fragmento
    for env in ENTORNOS_FUERA:
        t = re.sub(r"\\begin\{%s\*?\}.*?\\end\{%s\*?\}" % (env, env), " ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " ", t)
    t = re.sub(r"\\\[.*?\\\]", " ", t, flags=re.S)
    t = re.sub(r"\\(?:cite|ref|label|eqref|autoref|citep|citet)\s*\{[^}]*\}", " ", t)
    t = re.sub(r"\\[a-zA-Z@]+\*?", " ", t)
    t = re.sub(r"[{}\[\]~^&_\\]", " ", t)
    return len([p for p in re.split(r"\s+", t) if re.search(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", p)])


def secciones_tex(texto):
    """Devuelve [(nivel, titulo, cuerpo)] partiendo por chapter/section."""
    patron = re.compile(r"\\(chapter|section)\*?\s*(?:\[[^\]]*\])?\s*\{", re.S)
    cortes = []
    for m in patron.finditer(texto):
        titulo, i, prof = "", m.end(), 1
        while i < len(texto) and prof:
            c = texto[i]
            prof += (c == "{") - (c == "}")
            if prof:
                titulo += c
            i += 1
        cortes.append((m.group(1), re.sub(r"\\[a-zA-Z]+|[{}]", "", titulo).strip(), m.start(), i))
    if not cortes:
        return [("documento", "(sin secciones)", texto)]
    hay_cap = any(c[0] == "chapter" for c in cortes)
    cortes = [c for c in cortes if c[0] == "chapter"] if hay_cap else cortes
    salida = []
    for n, (nivel, titulo, ini, fin) in enumerate(cortes):
        sig = cortes[n + 1][2] if n + 1 < len(cortes) else len(texto)
        salida.append((nivel, titulo, texto[fin:sig]))
    return salida


def contar_tex(texto, directorio):
    citas = set()
    for m in re.finditer(r"\\(?:cite|citep|citet|citeauthor|parencite|textcite)\s*"
                         r"(?:\[[^\]]*\])*\s*\{([^}]*)\}", texto):
        citas.update(k.strip() for k in m.group(1).split(",") if k.strip())
    entradas_bib = 0
    if directorio:
        for raiz, _, ficheros in os.walk(directorio):
            for f in ficheros:
                if f.endswith(".bib"):
                    with open(os.path.join(raiz, f), encoding="utf-8", errors="replace") as fh:
                        entradas_bib += len(re.findall(r"^\s*@\w+\s*\{", fh.read(), re.M))
    ecuaciones = sum(len(re.findall(r"\\begin\{%s\*?\}" % e, texto))
                     for e in ("equation", "align", "gather", "eqnarray", "multline"))
    ecuaciones += len(re.findall(r"\\\[", texto))
    return {
        "figuras": len(re.findall(r"\\begin\{figure\*?\}", texto)),
        "graficos": len(re.findall(r"\\includegraphics", texto)),
        "tablas": len(re.findall(r"\\begin\{table\*?\}", texto)),
        "ecuaciones": ecuaciones,
        "citas": len(citas),
        "bib": entradas_bib,
    }


# --------------------------------------------------------------------------- Word

def texto_docx(ruta):
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("word/document.xml")
    raiz = ET.fromstring(xml)
    parrafos = []
    for p in raiz.iter(W + "p"):
        estilo = ""
        pr = p.find(W + "pPr")
        if pr is not None:
            e = pr.find(W + "pStyle")
            if e is not None:
                estilo = e.get(W + "val", "")
        texto = "".join(t.text or "" for t in p.iter(W + "t"))
        parrafos.append((estilo, texto))
    conteos = {
        "figuras": len(list(raiz.iter(W + "drawing"))),
        "tablas": len(list(raiz.iter(W + "tbl"))),
        "ecuaciones": len(list(raiz.iter(M + "oMath"))) + len(list(raiz.iter(M + "oMathPara"))),
        "citas": len(re.findall(r"CITATION", xml.decode("utf-8", "replace"))),
        "bib": 0,
    }
    return parrafos, conteos


def es_titulo(estilo, texto):
    e = estilo.lower()
    if any(k in e for k in ("heading", "ttulo", "titulo", "encabezado")) and not e.endswith("char"):
        return True
    return bool(re.match(r"^\s*(cap[ií]tulo|chapter)\s+[0-9IVX]+", texto, re.I))


def secciones_docx(parrafos):
    secciones, actual, cuerpo = [], "(preliminares)", []
    for estilo, texto in parrafos:
        if es_titulo(estilo, texto) and texto.strip():
            secciones.append((actual, " ".join(cuerpo)))
            actual, cuerpo = texto.strip(), []
        else:
            cuerpo.append(texto)
    secciones.append((actual, " ".join(cuerpo)))
    return [(t, c) for t, c in secciones if c.strip() or t != "(preliminares)"]


def palabras(texto):
    return len([p for p in re.split(r"\s+", texto)
                if re.search(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", p)])


# --------------------------------------------------------------------------- salida

def barra(fraccion, ancho=24):
    n = int(round(fraccion * ancho))
    return "#" * n + "." * (ancho - n)


def informe(titulo, secciones, conteos, objetivo):
    total = sum(n for _, n in secciones) or 1
    print("\n" + "=" * 72)
    print("INVENTARIO: " + titulo)
    print("=" * 72)
    ancho = max([len(t) for t, _ in secciones] + [20])
    ancho = min(ancho, 46)
    for nombre, n in secciones:
        print("%-*s %7d  %5.1f%%  %s" % (ancho, nombre[:ancho], n, 100 * n / total,
                                         barra(n / total)))
    print("-" * 72)
    print("%-*s %7d" % (ancho, "TOTAL palabras", total))
    print("\nFiguras: %(figuras)d   Tablas: %(tablas)d   Ecuaciones: %(ecuaciones)d   "
          "Citas unicas: %(citas)d" % conteos)
    if conteos.get("bib"):
        print("Entradas en el .bib: %d" % conteos["bib"])
    if conteos.get("graficos"):
        print("Llamadas a includegraphics: %d" % conteos["graficos"])

    print("\n" + "-" * 72)
    print("PRESUPUESTO PARA UN ARTICULO DE %d PALABRAS" % objetivo)
    print("-" * 72)
    print("Factor de compresion necesario: %.1f : 1" % (total / objetivo))
    if total / objetivo > 8:
        print("  Compresion alta: casi seguro hay que elegir UNA parte de la tesis,")
        print("  no resumirla entera. Decide la afirmacion central antes de escribir.")
    elif total / objetivo < 2:
        print("  Compresion baja: quiza la fuente ya tiene tamano de articulo, o falta")
        print("  material por incluir. Comprueba que has cargado el documento completo.")
    reparto = [("Introduccion", .17), ("Trabajo relacionado", .12), ("Metodo", .22),
               ("Resultados", .27), ("Discusion", .17), ("Conclusion", .05)]
    for nombre, frac in reparto:
        print("  %-22s %5d palabras" % (nombre, round(objetivo * frac)))
    print("\nFiguras y tablas en el articulo: 4-6 de las %d actuales."
          % (conteos["figuras"] + conteos["tablas"]))
    if conteos["citas"]:
        print("Referencias: unas %d-%d de las %d citadas."
              % (min(30, conteos["citas"]), min(60, conteos["citas"]), conteos["citas"]))
    print()


def main():
    ap = argparse.ArgumentParser(description="Inventario de una tesis para planificar el articulo.")
    ap.add_argument("ruta", help=".tex, directorio del proyecto, .docx o .pdf")
    ap.add_argument("--objetivo", type=int, default=6000,
                    help="palabras objetivo del articulo (por defecto 6000)")
    args = ap.parse_args()

    ruta = args.ruta
    if os.path.isdir(ruta):
        principal = buscar_main(ruta)
        if not principal:
            docs = [os.path.join(ruta, f) for f in sorted(os.listdir(ruta))
                    if f.lower().endswith((".docx", ".pdf"))]
            if not docs:
                sys.exit("No encuentro ni un .tex con documentclass ni un .docx/.pdf en %s" % ruta)
            ruta = docs[0]
        else:
            ruta = principal

    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".tex":
        texto = cargar_tex(ruta)
        directorio = os.path.dirname(os.path.abspath(ruta))
        secciones = [(t, palabras_tex(c)) for _, t, c in secciones_tex(texto)]
        informe(ruta, secciones, contar_tex(texto, directorio), args.objetivo)
    elif ext == ".docx":
        parrafos, conteos = texto_docx(ruta)
        secciones = [(t, palabras(c)) for t, c in secciones_docx(parrafos)]
        if conteos["citas"]:
            print("Aviso: %d campos de cita de Word detectados; exporta el .bib del gestor "
                  "antes de convertir." % conteos["citas"])
        informe(ruta, secciones, conteos, args.objetivo)
    elif ext == ".pdf":
        try:
            texto = subprocess.run(["pdftotext", "-layout", ruta, "-"],
                                   capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            sys.exit("Necesito pdftotext para leer un PDF.")
        bloques, actual, cuerpo = [], "(inicio)", []
        for linea in texto.splitlines():
            if re.match(r"^\s*(cap[ií]tulo|chapter)\s+[0-9IVX]+", linea, re.I) or \
               re.match(r"^\s*\d+\.?\s+[A-ZÁÉÍÓÚÑ][^.]{3,60}$", linea):
                bloques.append((actual, " ".join(cuerpo)))
                actual, cuerpo = linea.strip()[:60], []
            else:
                cuerpo.append(linea)
        bloques.append((actual, " ".join(cuerpo)))
        conteos = {"figuras": len(re.findall(r"^\s*(Figura|Figure|Fig\.)\s*\d", texto, re.M)),
                   "tablas": len(re.findall(r"^\s*(Tabla|Table)\s*\d", texto, re.M)),
                   "ecuaciones": len(re.findall(r"\(\d+\.\d+\)\s*$", texto, re.M)),
                   "citas": len(set(re.findall(r"\[(\d{1,3})\]", texto))), "bib": 0}
        print("Aviso: leyendo desde PDF; los conteos son aproximados y las figuras "
              "saldran rasterizadas. Pide las fuentes originales.")
        informe(ruta, [(t, palabras(c)) for t, c in bloques], conteos, args.objetivo)
    else:
        sys.exit("Formato no soportado: %s (usa .tex, .docx, .pdf o un directorio)" % ext)


if __name__ == "__main__":
    main()
