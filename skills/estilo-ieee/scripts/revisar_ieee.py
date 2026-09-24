#!/usr/bin/env python3
"""
revisar_ieee.py — Primera pasada automática de estilo y citas IEEE.

Uso:
    python revisar_ieee.py documento.docx [--idioma es|en|auto] [--salida informe.md]
    python revisar_ieee.py articulo.tex refs.bib
    python revisar_ieee.py tesis.md
    python revisar_ieee.py documento.pdf        (requiere pdftotext)

Detecta problemas mecánicos y los clasifica en:
    ERROR       contradice una regla explícita de IEEE
    AVISO       probablemente incorrecto; confirmar leyendo el contexto
    SUGERENCIA  mejora de estilo o decisión que depende de la norma institucional

No modifica el documento. Es una ayuda: los hallazgos se verifican leyendo el texto,
y hay cosas (sentido técnico, calidad de la prosa, datos faltantes en referencias)
que solo se revisan leyendo.
"""
import argparse
import os
import re
import subprocess
import sys
from collections import Counter, OrderedDict, defaultdict

# ----------------------------------------------------------------------------
# Lectura de documentos
# ----------------------------------------------------------------------------

class Parrafo:
    __slots__ = ("idx", "texto", "estilo", "es_titulo")

    def __init__(self, idx, texto, estilo="", es_titulo=False):
        self.idx = idx
        self.texto = texto
        self.estilo = estilo or ""
        self.es_titulo = es_titulo


def leer_docx(ruta):
    try:
        import docx  # python-docx
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError:
        sys.exit("Falta python-docx: pip install python-docx --break-system-packages")
    d = docx.Document(ruta)
    parrafos = []
    idx = 0

    def agregar(p):
        nonlocal idx
        t = p.text.replace("\u00a0", " ").strip()
        if not t:
            return
        idx += 1
        est = p.style.name if p.style is not None else ""
        titulo = bool(re.match(r"(Heading|Título|Titulo|Title)", est, re.I))
        parrafos.append(Parrafo(idx, t, est, titulo))

    for hijo in d.element.body.iterchildren():
        tag = hijo.tag.split("}")[-1]
        if tag == "p":
            agregar(Paragraph(hijo, d))
        elif tag == "tbl":
            for fila in Table(hijo, d).rows:
                vistos = set()
                for celda in fila.cells:
                    if id(celda._tc) in vistos:
                        continue
                    vistos.add(id(celda._tc))
                    for p in celda.paragraphs:
                        agregar(p)
    return parrafos


def leer_texto_plano(texto):
    parrafos = []
    bloques = re.split(r"\n\s*\n", texto)
    idx = 0
    for b in bloques:
        lineas = [l.strip() for l in b.split("\n") if l.strip()]
        if not lineas:
            continue
        # Las listas de referencias suelen venir una entrada por línea
        if sum(1 for l in lineas if re.match(r"^\[\d+\]", l)) >= 2:
            actual = ""
            for l in lineas:
                if re.match(r"^\[\d+\]", l) and actual:
                    idx += 1
                    parrafos.append(Parrafo(idx, actual))
                    actual = l
                else:
                    actual = (actual + " " + l).strip()
            if actual:
                idx += 1
                parrafos.append(Parrafo(idx, actual))
            continue
        for l in (lineas if all(l.startswith("#") for l in lineas[:1]) and len(lineas) > 1 else [" ".join(lineas)]):
            t = l.strip()
            titulo = t.startswith("#")
            t = t.lstrip("#").strip()
            idx += 1
            parrafos.append(Parrafo(idx, t, "", titulo))
    return parrafos


def leer_pdf(ruta):
    try:
        out = subprocess.run(["pdftotext", "-layout", ruta, "-"], capture_output=True, text=True, check=True).stdout
    except Exception:
        sys.exit("No se pudo extraer texto del PDF (¿falta pdftotext?).")
    out = re.sub(r"-\n(\w)", r"\1", out)
    return leer_texto_plano(out)


def limpiar_latex(texto):
    """Convierte LaTeX en texto aproximado. Conserva \\cite como [cite:clave]."""
    t = re.sub(r"(?<!\\)%.*", "", texto)
    t = re.sub(r"\\begin\{(equation|align|eqnarray|gather|multline)\*?\}.*?\\end\{\1\*?\}", " (EQ) ", t, flags=re.S)
    t = re.sub(r"\\\[.*?\\\]", " (EQ) ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " (EQ) ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", "x", t)
    t = re.sub(r"\\(?:cite|citep|citet)\{([^}]*)\}", lambda m: "[cite:" + m.group(1) + "]", t)
    t = re.sub(r"\\(?:section|subsection|subsubsection|chapter)\*?\{([^}]*)\}", r"\n\n# \1\n\n", t)
    t = re.sub(r"\\(?:ref|eqref|autoref|label)\{[^}]*\}", "N", t)
    t = re.sub(r"\\(?:textbf|textit|emph|texttt|mbox|text)\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = t.replace("~", " ").replace("{", "").replace("}", "")
    t = t.replace("---", "—").replace("--", "–")
    return t


# ----------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------

class Informe:
    def __init__(self):
        self.items = defaultdict(list)  # categoría -> [(nivel, idx, mensaje, fragmento)]

    def add(self, cat, nivel, idx, msg, frag=""):
        self.items[cat].append((nivel, idx, msg, frag))

    def contar(self):
        c = Counter()
        for lst in self.items.values():
            for n, *_ in lst:
                c[n] += 1
        return c


def fragmento(texto, ini, fin, margen=40):
    a = max(0, ini - margen)
    b = min(len(texto), fin + margen)
    s = texto[a:b].replace("\n", " ")
    return ("…" if a > 0 else "") + s + ("…" if b < len(texto) else "")


def detectar_idioma(parrafos):
    txt = " ".join(p.texto for p in parrafos[:400]).lower()
    es = len(re.findall(r"\b(el|la|los|las|de|del|que|en|para|con|por|una|se|es)\b", txt))
    en = len(re.findall(r"\b(the|of|and|to|in|is|for|that|with|on|are|this)\b", txt))
    return "es" if es >= en else "en"


RE_TIT_REFS = re.compile(
    r"^(?:[IVXLC]+\.|\d+(?:\.\d+)*\.?|Cap[ií]tulo\s+\d+[.:]?)?\s*"
    r"(references|referencias(?: bibliogr[aá]ficas)?|bibliograf[ií]a|bibliography|literatura citada)\s*$",
    re.I,
)
RE_TIT_FIN_REFS = re.compile(
    r"^(?:[IVXLC]+\.|\d+\.?)?\s*(anexos?|ap[eé]ndices?|appendix|appendixes|appendices|biograph(?:y|ies)|"
    r"biograf[ií]as?|glosario)\b",
    re.I,
)


def partir_cuerpo_y_refs(parrafos):
    ini = None
    for i, p in enumerate(parrafos):
        if len(p.texto) < 60 and RE_TIT_REFS.match(p.texto.strip()):
            ini = i  # nos quedamos con el último título de referencias
    if ini is None:
        # Sin título: bloque final de entradas que empiezan con [n]
        j = len(parrafos)
        while j > 0 and re.match(r"^\[\d+\]", parrafos[j - 1].texto):
            j -= 1
        if len(parrafos) - j >= 2:
            return parrafos[:j], parrafos[j:], None
        return parrafos, [], None
    fin = len(parrafos)
    for k in range(ini + 1, len(parrafos)):
        t = parrafos[k].texto.strip()
        if len(t) < 60 and RE_TIT_FIN_REFS.match(t) and not re.match(r"^\[\d+\]", t):
            fin = k
            break
    return parrafos[:ini] + parrafos[fin:], parrafos[ini + 1:fin], parrafos[ini]


def es_titulo(p):
    if p.es_titulo:
        return True
    t = p.texto.strip()
    if len(t) > 90 or t.endswith((".", ":", ";", ",")):
        return False
    if re.match(r"^([IVXLC]+\.|[A-H]\.|\d+(\.\d+)*\.?)\s+\S", t) and len(t.split()) <= 10:
        return True
    letras = [c for c in t if c.isalpha()]
    return len(letras) > 3 and all(c.isupper() for c in letras) and len(t.split()) <= 8


def es_leyenda(t):
    return bool(re.match(r"^\s*(Fig\.?|Figura|Figure|Gr[aá]fico|TABLE|TABLA|Table|Tabla|Cuadro)\s*[\dIVXLC]+", t))


# ----------------------------------------------------------------------------
# Citas en el texto
# ----------------------------------------------------------------------------

RE_GRUPO = re.compile(r"\[([^\[\]\n]{1,80})\]")
LOCALIZADORES = r"(?:pp?\.|Fig\.|Figs\.|eq\.|eqs\.|ec\.|Sec\.|Secs\.|Ch\.|Cap\.|Th\.|Teo\.|Lemma|Lema|Appendix|Ap[eé]ndice|Algorithm|Algoritmo|Tab\.|Table|Tabla|Prop\.|Def\.|Cor\.|Rem\.|Ex\.|Art\.)"
RE_CITA_OK = re.compile(r"^\s*\d+\s*(,\s*" + LOCALIZADORES + r".*)?$")
RE_CITA_MULTI = re.compile(r"^\s*\d+(\s*[,;–—-]\s*\d+)+\s*$")


def expandir(contenido):
    nums = []
    for parte in re.split(r"\s*[,;]\s*", contenido.strip()):
        m = re.match(r"^(\d+)\s*[–—-]\s*(\d+)$", parte)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a < b and b - a < 200:
                nums.extend(range(a, b + 1))
        elif parte.isdigit():
            nums.append(int(parte))
    return nums


def sugerir_multi(contenido):
    partes = re.split(r"\s*[,;]\s*", contenido.strip())
    out = []
    for parte in partes:
        m = re.match(r"^(\d+)\s*[–—-]\s*(\d+)$", parte)
        if m:
            out.append(f"[{m.group(1)}]–[{m.group(2)}]")
        else:
            out.append(f"[{parte}]")
    return ", ".join(out)


def revisar_citas(cuerpo, n_refs, inf, idioma, es_latex=False):
    orden = []
    vistos = set()
    for p in cuerpo:
        t = p.texto
        if es_latex:
            continue
        rangos = {}
        for m in re.finditer(r"\[(\d+)\]\s*[–—-]\s*\[(\d+)\]", t):
            a, b = int(m.group(1)), int(m.group(2))
            if 0 < a < b and b - a < 200:
                rangos[m.start() + 1 + len(m.group(1)) + 1] = list(range(a + 1, b))
        for m in RE_GRUPO.finditer(t):
            c = m.group(1)
            if c.startswith("cite:"):
                continue
            if RE_CITA_OK.match(c):
                n = int(re.match(r"\s*(\d+)", c).group(1))
                if n == 0:
                    continue
                nums = [n]
            elif RE_CITA_MULTI.match(c):
                nums = expandir(c)
                if not nums or 0 in nums:
                    continue
                # [0,1] o [1, 2] podrían ser intervalos matemáticos; solo advertimos si hay más de dos números o rango
                inf.add("Citas en el texto", "ERROR", p.idx,
                        f"Cita agrupada `[{c}]`: cada número va en su corchete → `{sugerir_multi(c)}`.",
                        fragmento(t, m.start(), m.end()))
            else:
                continue
            nums = nums + rangos.get(m.end(), [])
            for n in nums:
                if n not in vistos:
                    vistos.add(n)
                    orden.append((n, p.idx))
            # superíndice o sin espacio antes del corchete
            if m.start() > 0 and t[m.start() - 1].isalnum():
                inf.add("Citas en el texto", "SUGERENCIA", p.idx,
                        "Falta espacio antes de la cita: `texto [1]`.", fragmento(t, m.start(), m.end()))
            # cita después del punto final
            if m.start() > 1 and t[m.start() - 1] == " " and t[m.start() - 2] == "." and not re.search(r"(al|et al|Fig|pp|p|Sec|eq|ec)\.$", t[:m.start() - 1]):
                resto = t[m.end():m.end() + 2]
                if resto.strip() in ("", ) or resto.startswith(" ") or resto == "":
                    inf.add("Citas en el texto", "AVISO", p.idx,
                            "La cita parece quedar fuera de la oración; va dentro de la puntuación: `…resultado [3].`",
                            fragmento(t, m.start() - 2, m.end()))

        for m in re.finditer(r"\]\s*[-—]\s*\[", t):
            inf.add("Citas en el texto", "ERROR", p.idx,
                    "Rango de citas con guion o raya larga: usar raya corta `[1]–[4]`.", fragmento(t, m.start(), m.end()))
        for m in re.finditer(r"\[\d+\]\s*\[\d+\]", t):
            inf.add("Citas en el texto", "ERROR", p.idx,
                    "Citas pegadas `[1][2]`: separar con coma `[1], [2]` o rango `[1]–[3]`.", fragmento(t, m.start(), m.end()))
        for m in re.finditer(r"\b(reference|references|ref\.|refs\.|referencia|referencias|Ref\.|Refs\.)\s*\[\d", t, re.I):
            inf.add("Citas en el texto", "ERROR", p.idx,
                    "No escribir «referencia [n]» ni «ref. [n]»: basta «en [n]».", fragmento(t, m.start(), m.end()))
        for m in re.finditer(
                r"\b(Fig\.|Figure|Figura|Table|Tabla|equation|ecuaci[oó]n|Eq\.|Section|Secci[oó]n|Chapter|Cap[ií]tulo|Theorem|Teorema|page|p[aá]gina)\s*\(?[\dIVX.]+\)?\s+"
                r"(?:of|in|from|de|en|del)\s+(?:the\s+|la\s+|el\s+)?(?:reference\s+|referencia\s+|ref\.\s+|work\s+|trabajo\s+)?\[(\d+)\]",
                t, re.I):
            inf.add("Citas en el texto", "ERROR", p.idx,
                    f"Parte de una fuente fuera del corchete: usar la forma `[{m.group(2)}, Fig. 2]`, `[{m.group(2)}, eq. (8)]`, `[{m.group(2)}, Sec. IV]`, `[{m.group(2)}, p. 5]`.",
                    fragmento(t, m.start(), m.end()))
        for m in re.finditer(r"\(([A-ZÁÉÍÓÚÑ][\w'´-]+(?:\s+et\s+al\.?|\s+(?:y|and|&)\s+[A-ZÁÉÍÓÚÑ][\w'-]+)?),?\s+(?:19|20)\d{2}[a-z]?(?:[;,][^)]{0,60})?\)", t):
            inf.add("Citas en el texto", "ERROR", p.idx,
                    "Cita autor-año (APA/Harvard): IEEE usa número entre corchetes por orden de aparición.",
                    fragmento(t, m.start(), m.end()))
        for m in re.finditer(r"\bet al(?!\.)\b", t):
            inf.add("Citas en el texto", "ERROR", p.idx, "«et al» sin punto: «et al.».", fragmento(t, m.start(), m.end()))
        for m in re.finditer(r"\b(ibid|ibíd|op\.\s*cit|loc\.\s*cit)\b", t, re.I):
            inf.add("Citas en el texto", "ERROR", p.idx,
                    "ibid./op. cit. no se usan en IEEE: repetir el número original, p. ej. `[3, p. 12]`.",
                    fragmento(t, m.start(), m.end()))

    # Orden de primera aparición
    esperado = 1
    reportado = False
    for n, idx in orden:
        if n == esperado:
            esperado += 1
        elif n > esperado and not reportado:
            inf.add("Citas en el texto", "ERROR", idx,
                    f"Orden de citas: aparece [{n}] antes de que se haya citado [{esperado}]. "
                    "La lista se numera por orden de primera cita; hay que renumerar lista y texto.")
            reportado = True
    citados = {n for n, _ in orden}
    if n_refs:
        faltan_en_lista = sorted(n for n in citados if n > n_refs)
        if faltan_en_lista:
            inf.add("Coherencia texto–lista", "ERROR", None,
                    f"Se citan números que no existen en la lista ({n_refs} entradas): {rango_legible(faltan_en_lista)}.")
        no_citadas = sorted(set(range(1, n_refs + 1)) - citados)
        if no_citadas:
            inf.add("Coherencia texto–lista", "AVISO", None,
                    f"Entradas de la lista que nunca se citan en el texto: {rango_legible(no_citadas)}. "
                    "Citalas o eliminálas (si se eliminan, renumerar).")
    return orden


def rango_legible(nums):
    nums = sorted(set(nums))
    out = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"[{nums[i]}]" if i == j else f"[{nums[i]}]–[{nums[j]}]")
        i = j + 1
    return ", ".join(out)


# ----------------------------------------------------------------------------
# Lista de referencias
# ----------------------------------------------------------------------------

MESES_EN = ["January", "February", "March", "April", "June", "July", "August", "September",
            "October", "November", "December"]
MESES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
            "setiembre", "octubre", "noviembre", "diciembre"]
NO_ABREV = [
    (r"\bTransactions on\b", "Trans."), (r"\bJournal of\b", "J."), (r"\bProceedings of the\b", "Proc."),
    (r"\bProceedings of\b", "Proc."), (r"\bInternational Conference\b", "Int. Conf."),
    (r"\bInternational Journal\b", "Int. J."), (r"\bInternational Symposium\b", "Int. Symp."),
    (r"\bLetters\b", "Lett."), (r"\bMagazine\b", "Mag."),
]


def revisar_referencias(refs, inf, idioma):
    entradas = []
    con_num = sum(1 for p in refs if re.match(r"^\[\d+\]", p.texto))
    if refs and con_num < len(refs) * 0.5:
        inf.add("Lista de referencias", "AVISO", refs[0].idx,
                "Las entradas no empiezan con `[n]` (posible numeración automática de Word o formato no IEEE). "
                "Se asume que el orden de los párrafos es la numeración. Las entradas deben verse como `[1]`, `[2]`, … "
                "alineadas a la izquierda.")
    for i, p in enumerate(refs, 1):
        m = re.match(r"^\[(\d+)\]\s*(.*)$", p.texto, re.S)
        if m:
            num, cuerpo = int(m.group(1)), m.group(2)
        else:
            m2 = re.match(r"^(\d+)[.)]\s+(.*)$", p.texto, re.S)
            if m2:
                num, cuerpo = int(m2.group(1)), m2.group(2)
                inf.add("Lista de referencias", "ERROR", p.idx, f"Numeración `{num}.`: en IEEE va entre corchetes `[{num}]`.")
            else:
                num, cuerpo = i, p.texto
        entradas.append((num, cuerpo, p.idx))

    # numeración consecutiva
    nums = [n for n, _, _ in entradas]
    if nums and nums != list(range(1, len(nums) + 1)):
        inf.add("Lista de referencias", "ERROR", None,
                f"La numeración de la lista no es consecutiva desde [1] (se leyó: {', '.join(map(str, nums[:15]))}{'…' if len(nums) > 15 else ''}).")

    titulos = defaultdict(list)
    etiq_en = etiq_es = 0
    for num, e, idx in entradas:
        r = lambda nivel, msg: inf.add("Lista de referencias", nivel, idx, f"[{num}] {msg}", e[:140] + ("…" if len(e) > 140 else ""))
        es_web = bool(re.search(r"https?://|www\.", e))

        # Formato autor-año / APA
        if re.match(r"^[A-ZÁÉÍÓÚÑ][\w'´-]+(?:\s[A-ZÁÉÍÓÚÑ][\w'-]+)?,\s*(?:[A-Z]\.\s*)+", e) and re.search(r"\((?:19|20)\d{2}[a-z]?\)", e):
            r("ERROR", "Formato autor-año (APA/Harvard). IEEE: `A. B. Apellido, “Título,” Revista abrev., vol. x, no. x, pp. x–y, mes año.`")
        elif re.match(r"^[A-ZÁÉÍÓÚÑ][\w'´-]+,\s*(?:[A-Z]\.\s*)+", e):
            r("ERROR", "Apellido antes de la inicial. IEEE pone la inicial primero: `J. Smith`, no `Smith, J.`")

        # Segmento de autores: hasta la primera comilla de apertura
        mq = re.search(r"[“\"]", e)
        autores = e[:mq.start()] if mq else ""
        if autores:
            if not re.search(r"\b[A-ZÁÉÍÓÚÑ]\.", autores) and re.search(r"[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}", autores) and not re.search(
                    r"\b(Inc|Corp|Ltd|Univ|University|Universidad|Ministerio|Instituto|Institute|Organization|Organizaci[oó]n|Agency|Agencia|Comisi[oó]n|Association|Asociaci[oó]n|IEEE|ISO|IEC|ITU|NASA|Group|Grupo|Consortium|Company|Compañ[ií]a|Dept|Department|Departamento)\b", autores):
                r("ERROR", "Nombres de pila completos: IEEE usa iniciales antes del apellido (`J. K. Smith`).")
            n_aut = len([a for a in re.split(r",\s*|\s+and\s+|\s+y\s+|\s*&\s*", autores.strip(" ,")) if re.search(r"[A-Za-zÀ-ÿ]", a) and "et al" not in a])
            if n_aut > 6 and "et al" not in autores:
                r("ERROR", f"{n_aut} autores: con más de seis se pone solo el primero seguido de «et al.».")
            if re.search(r"\b[A-Z]\.[A-Z]\.", autores):
                r("SUGERENCIA", "Iniciales sin espacio (`J.K.`): IEEE separa con espacio `J. K.`")
            if re.search(r"\s&\s", autores):
                r("ERROR", "«&» entre autores: usar «and» (o «y» en español).")
        if re.search(r"\bet al(?!\.)", e):
            r("ERROR", "«et al» sin punto.")

        # Título entre comillas: coma dentro
        if re.search(r"[”\"]\s*,", e):
            r("ERROR", "Coma fuera de las comillas del título: `“Título,”`.")
        # Páginas
        for m in re.finditer(r"\bpp?\.?\s*(\d+)\s*-{1,2}\s*(\d+)", e):
            r("ERROR", f"Rango de páginas con guion: `pp. {m.group(1)}–{m.group(2)}` (raya corta).")
        if re.search(r"\bpp\s+\d", e):
            r("ERROR", "«pp» sin punto: «pp.».")
        if re.search(r"\bp\.\s*\d+\s*[–-]\s*\d+", e):
            r("ERROR", "Rango con «p.»: para varias páginas es «pp.».")
        if re.search(r"\b(pages|págs?\.)\s*\d", e, re.I):
            r("ERROR", "Usar «pp.» para las páginas.")
        # Volumen / número
        if re.search(r"(?<!^)\bVol\.\s*\d", e):
            r("ERROR", "«Vol.» en mayúscula dentro de la referencia: «vol.».")
        if re.search(r"\b(issue|Issue|Iss\.)\s*\d", e):
            r("ERROR", "«issue» → «no.».")
        if re.search(r",\s*No\.\s*\d", e):
            r("ERROR", "«No.» → «no.» en minúscula.")
        if re.search(r"\b\d+\s*\(\d+\)\s*[:,]", e):
            r("ERROR", "Volumen(número) al estilo APA: IEEE escribe `vol. 5, no. 2,`.")
        # Meses
        for mes in MESES_EN:
            if re.search(r"\b" + mes + r"\b", e):
                r("ERROR", f"Mes completo «{mes}»: abreviar (Jan., Feb., Mar., Apr., May, Jun., Jul., Aug., Sep., Oct., Nov., Dec.).")
                break
        for mes in MESES_ES:
            if re.search(r"\b" + mes + r"\b", e, re.I) and not re.search(r"(Consultado|Accedido|accedido|consultado)", e):
                r("SUGERENCIA", f"Mes completo «{mes}»: en IEEE se abrevia (ene., feb., mar., abr., may., jun., jul., ago., sep., oct., nov., dic.).")
                break
        # En prensa
        if re.search(r"\bto appear\b|\baparecer[aá]\b", e, re.I):
            r("ERROR", "«to appear»: usar «to be published» (aceptado) o «submitted for publication» (enviado).")
        # DOI
        if re.search(r"https?://(dx\.)?doi\.org/", e):
            r("SUGERENCIA", "DOI como enlace: la forma IEEE es `doi: 10.xxxx/xxxx.` (salvo que la institución pida el enlace).")
        if re.search(r"\bDOI\s*:", e):
            r("ERROR", "«DOI:» → «doi:» en minúscula.")
        # Online / Available
        tiene_disp = re.search(r"\b(Available|Disponible)\b", e)
        tiene_online = re.search(r"\[(Online|En l[ií]nea)(?: Video)?\]", e)
        if tiene_disp and not tiene_online:
            r("ERROR", "«Available:/Disponible:» sin «[Online]./[En línea].» delante: `[Online]. Available: URL`.")
        if re.search(r"\bRetrieved from\b|\bRecuperado de\b", e, re.I):
            r("ERROR", "«Retrieved from / Recuperado de» es APA: usar `Accessed: fecha. [Online]. Available: URL`.")
        if re.search(r"\[(Online)\]|\bAvailable\b|\bAccessed\b", e):
            etiq_en += 1
        if re.search(r"\[En l[ií]nea\]|\bDisponible\b|\b(Consultado|Accedido)\b", e):
            etiq_es += 1
        # Cierre
        fin = e.rstrip()
        if re.search(r"(https?://\S+|www\.\S+)\.$", fin):
            r("ERROR", "Punto después de la URL final: se omite.")
        elif not re.search(r"(https?://\S+|www\.\S+)$", fin) and not fin.endswith("."):
            r("ERROR", "La referencia debe terminar en punto (salvo que termine en URL).")
        # Sin año
        if not re.search(r"\b(1[89]\d{2}|20\d{2})\b", e) and not re.search(r"to be published|submitted|unpublished|en prensa|in[eé]dito", e, re.I):
            r("AVISO", "No se encuentra el año.")
        # Nombres sin abreviar
        for pat, ab in NO_ABREV:
            if re.search(pat, e):
                r("SUGERENCIA", f"Nombre de revista/congreso sin abreviar («{re.search(pat, e).group(0)}» → «{ab}»).")
                break
        if re.search(r"\bIn:\s", e) or re.search(r"[.,]\s+In\s+[A-Z]", e):
            r("ERROR", "«In:» / «In» con mayúscula (estilo Springer/APA): IEEE escribe «in» en minúscula tras el título: `“Título,” in Proc. …`")
        # Varias obras en una entrada
        if len(re.findall(r"\b(19|20)\d{2}\b", e)) >= 3 and ";" in e:
            r("AVISO", "Parece contener varias obras: IEEE exige una fuente por número.")
        if re.search(r"^(For example|See also|Por ejemplo|Ver también|Véase)", e, re.I):
            r("ERROR", "Comentario dentro de la lista: pasarlo al texto o a una nota al pie.")
        if re.search(r"\b(ibid|ibíd|op\.\s*cit)\b", e, re.I):
            r("ERROR", "ibid./op. cit.: eliminar, citar el número original en el texto y renumerar.")
        # Duplicados
        mt = re.search(r"[“\"]([^”\"]{12,})[”\"]", e)
        if mt:
            clave = re.sub(r"\W+", " ", mt.group(1).lower()).strip()
            titulos[clave].append(num)
    for clave, ns in titulos.items():
        if len(ns) > 1:
            inf.add("Lista de referencias", "ERROR", None,
                    f"Posible referencia duplicada en {', '.join(f'[{n}]' for n in ns)}: una obra aparece una sola vez; "
                    "las páginas distintas se indican en el texto (`[5, p. 30]`).")
    if etiq_en and etiq_es:
        inf.add("Lista de referencias", "AVISO", None,
                f"Etiquetas mezcladas: {etiq_en} entradas con «[Online]/Available/Accessed» y {etiq_es} con «[En línea]/Disponible/Consultado». Unificar.")
    return len(entradas)


# ----------------------------------------------------------------------------
# Figuras, tablas, ecuaciones, secciones
# ----------------------------------------------------------------------------

ROMANOS = {v: i for i, v in enumerate(
    ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI",
     "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"])}


def num_valor(s):
    s = s.strip().rstrip(".")
    if s.isdigit():
        return int(s)
    return ROMANOS.get(s.upper())


def revisar_figuras_tablas(cuerpo, inf, idioma):
    orden_fig, orden_tab = [], []
    ley_fig, ley_tab = set(), set()
    formas_fig = Counter()
    for p in cuerpo:
        t = p.texto
        if es_leyenda(t):
            m = re.match(r"^\s*(Fig\.?|Figura|Figure|Gr[aá]fico)\s*(\d+)(.?)(\s*)(\S*)", t)
            if m:
                ley_fig.add(int(m.group(2)))
                if m.group(1) != "Fig.":
                    inf.add("Figuras y tablas", "SUGERENCIA" if idioma == "es" else "ERROR", p.idx,
                            f"Leyenda «{m.group(1)} {m.group(2)}»: en IEEE es «Fig. {m.group(2)}.» (si la norma de la tesis pide «Figura», respetarla).",
                            t[:90])
                if m.group(3) not in (".",):
                    inf.add("Figuras y tablas", "AVISO", p.idx,
                            f"Tras el número de figura va punto y espacio: «Fig. {m.group(2)}. Texto».", t[:90])
                if re.match(r"(A|An|The)\b", m.group(5) or ""):
                    inf.add("Figuras y tablas", "SUGERENCIA", p.idx,
                            "La leyenda no debe empezar con «A», «An» o «The».", t[:90])
                if re.search(r"\bLena\b|\bLenna\b", t, re.I):
                    inf.add("Figuras y tablas", "ERROR", p.idx,
                            "IEEE no acepta la imagen «Lena» desde el 1 de abril de 2024: reemplazarla.", t[:90])
            m = re.match(r"^\s*(TABLE|TABLA|Table|Tabla|Cuadro)\s*([\dIVXLC]+)\b(.*)", t)
            if m:
                v = num_valor(m.group(2))
                if v:
                    ley_tab.add(v)
                if m.group(2).isdigit():
                    inf.add("Figuras y tablas", "SUGERENCIA", p.idx,
                            f"Tabla con número arábigo: en IEEE es «{'TABLA' if idioma == 'es' else 'TABLE'} {roman(int(m.group(2)))}» centrado encima de la tabla (si la norma institucional usa arábigos, respetarla).",
                            t[:90])
                if m.group(3).strip().endswith("."):
                    inf.add("Figuras y tablas", "SUGERENCIA", p.idx,
                            "El título de tabla no lleva punto final.", t[:90])
            continue
        t = re.sub(r"\[\d+,[^\]]*\]", "[c]", t)
        for m in re.finditer(r"\b(Figs?\.?|Figures?|Figuras?|figures?|figuras?|fig\.)\s*(\d+)", t):
            n = int(m.group(2))
            orden_fig.append((n, p.idx))
            formas_fig[m.group(1)] += 1
            if m.group(1) not in ("Fig.", "Figs."):
                inf.add("Figuras y tablas", "SUGERENCIA" if idioma == "es" else "ERROR", p.idx,
                        f"«{m.group(1)} {n}» en el texto: IEEE usa «Fig. {n}» siempre, también al inicio de oración.",
                        fragmento(t, m.start(), m.end(), 30))
        for m in re.finditer(r"\b(TABLE|TABLA|Tables?|Tablas?|tables?|tablas?|Cuadro|cuadro)\s*([\dIVXLC]+)\b", t):
            v = num_valor(m.group(2))
            if v:
                orden_tab.append((v, p.idx))
    # orden de primera mención
    for nombre, orden in (("Fig.", orden_fig), ("Tabla/Table", orden_tab)):
        vistos, esperado = set(), 1
        for n, idx in orden:
            if n in vistos:
                continue
            vistos.add(n)
            if n != esperado and n > esperado:
                inf.add("Figuras y tablas", "ERROR", idx,
                        f"{nombre} {n} se menciona por primera vez antes que {nombre} {esperado}: la primera mención debe seguir el orden numérico.")
                break
            esperado = max(esperado, n + 1)
    mencionadas_f = {n for n, _ in orden_fig}
    for n in sorted(ley_fig - mencionadas_f):
        inf.add("Figuras y tablas", "AVISO", None, f"Fig. {n} tiene leyenda pero no se menciona en el texto.")
    mencionadas_t = {n for n, _ in orden_tab}
    for n in sorted(ley_tab - mencionadas_t):
        inf.add("Figuras y tablas", "AVISO", None, f"La tabla {roman(n)} tiene título pero no se menciona en el texto.")


def roman(n):
    inv = {v: k for k, v in ROMANOS.items()}
    return inv.get(n, str(n))


def revisar_ecuaciones_secciones(cuerpo, inf, idioma):
    for p in cuerpo:
        t = p.texto
        for m in re.finditer(r"\b(Eqs?\.|Equations?|equations?|eqs?\.)\s*\(?\d+\)?", t):
            inicio = m.start() == 0 or re.search(r"[.!?]\s*$", t[:m.start()])
            if m.group(1).lower().startswith("eq") or not inicio:
                inf.add("Ecuaciones y secciones", "ERROR" if idioma == "en" else "SUGERENCIA", p.idx,
                        "Citar ecuaciones solo con el número entre paréntesis: «in (1)». «Equation (1)» solo al inicio de oración.",
                        fragmento(t, m.start(), m.end(), 30))
        if idioma == "es":
            for m in re.finditer(r"(?<![.!?]\s)(?<!^)\b(ec\.|ecuaci[oó]n|ecuaciones)\s*\(\d+\)", t):
                inf.add("Ecuaciones y secciones", "SUGERENCIA", p.idx,
                        "En estilo IEEE basta el número: «en (3)». «La ecuación (3)» se reserva para el inicio de oración.",
                        fragmento(t, m.start(), m.end(), 30))
        for m in re.finditer(r"\b(Subsection|subsection|Subsecci[oó]n|subsecci[oó]n|Sub-section)\b", t):
            inf.add("Ecuaciones y secciones", "ERROR", p.idx,
                    "No usar «Subsection»: «Section II-A» (en español «Sección II-A»).", fragmento(t, m.start(), m.end(), 30))
        for m in re.finditer(r"\bsection\s+[IVX]+\b", t):
            inf.add("Ecuaciones y secciones", "ERROR", p.idx, "«Section» con mayúscula: «Section II».", fragmento(t, m.start(), m.end(), 30))
        for m in re.finditer(r"\b(Section|Sección|Secci[oó]n)\s+([IVX]+)\.([A-H])(\d?)\b", t):
            inf.add("Ecuaciones y secciones", "ERROR", p.idx,
                    f"Referencia a subsección: «{m.group(1)} {m.group(2)}-{m.group(3)}{m.group(4)}» (guion, sin punto).",
                    fragmento(t, m.start(), m.end(), 30))
        for m in re.finditer(r"\(([^()]*\(\d+[a-z]?\)[^()]*)\)", t):
            if re.search(r"\b(see|ver|véase|cf\.)\b", m.group(1), re.I):
                inf.add("Ecuaciones y secciones", "ERROR", p.idx,
                        "Paréntesis dobles en el texto: «(see (10))» → «[see (10)]».", fragmento(t, m.start(), m.end(), 20))
    # Encabezados
    for p in cuerpo:
        if not es_titulo(p):
            continue
        t = p.texto.strip()
        if re.search(r"acknowledgement", t, re.I):
            inf.add("Estructura", "ERROR", p.idx, "«Acknowledgement» → «Acknowledgment» (sin «e» entre g y m).", t)
        if re.search(r"^\W*(?:[IVXLC]+\.\s*)?acknowledgments?\s*$", t, re.I) and re.search(r"ments\s*$", t, re.I):
            inf.add("Estructura", "ERROR", p.idx, "El encabezado va en singular: «Acknowledgment».", t)
        if re.search(r"^(?:[IVXLC]+\.\s*)?(conclusions)\s*$", t, re.I):
            inf.add("Estructura", "SUGERENCIA", p.idx, "IEEE usa el encabezado en singular: «Conclusion».", t)
        if re.match(r"^[IVXLC]+\.\s*(references|acknowledg|referencias|agradecimiento)", t, re.I):
            inf.add("Estructura", "ERROR", p.idx, "References y Acknowledgment no se numeran.", t)


# ----------------------------------------------------------------------------
# Resumen y términos índice
# ----------------------------------------------------------------------------

def revisar_resumen(cuerpo, inf, idioma):
    for i, p in enumerate(cuerpo):
        t = p.texto.strip()
        m = re.match(r"^(Abstract|Resumen)\s*[—–:.-]\s*(.+)", t, re.I | re.S)
        texto = None
        if m:
            texto, idx = m.group(2), p.idx
        elif re.match(r"^(Abstract|Resumen)\s*$", t, re.I) and i + 1 < len(cuerpo):
            texto, idx = cuerpo[i + 1].texto, cuerpo[i + 1].idx
            if i + 2 < len(cuerpo):
                sig = cuerpo[i + 2]
                if not es_titulo(sig) and not re.match(r"^(Index Terms|Keywords|Palabras clave|T[eé]rminos)", sig.texto, re.I) and len(sig.texto.split()) > 25:
                    inf.add("Resumen", "AVISO", sig.idx, "El resumen parece tener más de un párrafo; IEEE exige uno solo.")
        if texto:
            n = len(texto.split())
            if n < 150 or n > 250:
                inf.add("Resumen", "AVISO", idx, f"El resumen tiene {n} palabras; IEEE pide entre 150 y 250 (en tesis manda la norma institucional).")
            if re.search(r"\[[1-9]\d*(?:\]|\s*,\s*" + LOCALIZADORES + r"|(?:\s*[,–-]\s*[1-9]\d*)+\])", texto):
                inf.add("Resumen", "ERROR", idx, "El resumen no debe contener citas numeradas.")
            if re.search(r"\(\d+\)", texto) and re.search(r"\b(eq|ec|equation|ecuaci)", texto, re.I):
                inf.add("Resumen", "ERROR", idx, "El resumen no debe contener ecuaciones numeradas.")
            break
    for p in cuerpo:
        m = re.match(r"^(Index Terms|Keywords|Key words|Palabras clave|T[eé]rminos [ií]ndice)\s*[—–:.-]\s*(.+)", p.texto.strip(), re.I)
        if m:
            terms = [x.strip().rstrip(".") for x in re.split(r"[,;]", m.group(2)) if x.strip()]
            norm = [re.sub(r"^\W+", "", x.lower()) for x in terms]
            if norm != sorted(norm):
                inf.add("Resumen", "SUGERENCIA", p.idx, "Los Index Terms van en orden alfabético.",
                        "Orden sugerido: " + ", ".join(sorted(terms, key=lambda s: s.lower())))
            if m.group(1).lower() == "keywords":
                inf.add("Resumen", "SUGERENCIA", p.idx, "En IEEE se titula «Index Terms».")
            break


# ----------------------------------------------------------------------------
# Siglas
# ----------------------------------------------------------------------------

SIGLAS_OK = set("""IEEE USA EE UU UK DOI URL ORCID ISBN ISSN PDF SI OK TV PC CO2 II III IV VI VII VIII IX XI XII XIII XIV XV XVI XVII
XVIII XIX XX TABLE TABLA FIG AI IA RAE ISO IEC ITU ANSI NASA UNESCO ONU OMS PhD MSc MS BS BSc HTML XML JSON CSV
FCyT UNCA INTN NP AM PM EQ UTC GMT""".split())


def revisar_siglas(cuerpo, inf, idioma):
    definidas = {}
    primer_uso = {}
    for p in cuerpo:
        if es_titulo(p) or es_leyenda(p.texto):
            continue
        t = p.texto
        letras = [c for c in t if c.isalpha()]
        if letras and sum(c.isupper() for c in letras) / len(letras) > 0.6:
            continue
        for m in re.finditer(r"\(([A-Z][A-Za-z0-9-]*[A-Z][A-Za-z0-9-]*)s?(?:,[^)]*)?\)", t):
            definidas.setdefault(m.group(1), p.idx)
        for m in re.finditer(r"\b([A-Z][A-Z0-9-]*[A-Z])(s?)\b", t):
            s = m.group(1)
            if s in SIGLAS_OK or re.fullmatch(r"[IVXLC]+(-[A-H]\d?)?", s) or len(s) < 2:
                continue
            primer_uso.setdefault(s, (p.idx, fragmento(t, m.start(), m.end(), 30)))
            if m.group(2) == "s" and idioma == "es":
                pass
    sin_def, antes = [], []
    for s, (idx, frag) in primer_uso.items():
        if s not in definidas:
            sin_def.append(s)
        elif definidas[s] > idx:
            antes.append((s, idx, frag))
    if sin_def:
        inf.add("Siglas", "AVISO", None,
                "Siglas que no parecen definidas con la forma «desarrollo (SIGLA)»: " + ", ".join(sorted(sin_def)[:60]) +
                (" …" if len(sin_def) > 60 else "") + ". Definir en el primer uso (resumen y cuerpo), salvo que estén en la Nomenclature.")
    for s, idx, frag in antes[:30]:
        inf.add("Siglas", "AVISO", idx, f"«{s}» se usa antes de definirse.", frag)
    if idioma == "es":
        pl = set()
        for p in cuerpo:
            for m in re.finditer(r"\b([A-Z]{2,})s\b", p.texto):
                if m.group(1) in primer_uso:
                    pl.add(m.group(0))
        if pl:
            inf.add("Siglas", "SUGERENCIA", None,
                    "En español las siglas no llevan plural gráfico (la RAE desaconseja «FETs»; mejor «los FET»): " + ", ".join(sorted(pl)[:30]))


# ----------------------------------------------------------------------------
# Números, unidades, rayas
# ----------------------------------------------------------------------------

UNIDADES = r"(?:km|cm|mm|µm|um|nm|kg|mg|kHz|MHz|GHz|THz|Hz|kV|mV|MV|kA|mA|µA|kW|MW|GW|mW|kWh|MWh|Wh|dBm|dBi|dB|ms|µs|ns|ps|Mb/s|Gb/s|kb/s|Mbps|Gbps|kbps|Ω|kΩ|MΩ|µF|nF|pF|mH|µH|°C|V|A|W|K|Pa|kPa|MPa|N|J)"


def revisar_numeros(cuerpo, inf, idioma):
    dec_punto = dec_coma = 0
    pct_junto = pct_sep = 0
    rayas_largas = 0
    for p in cuerpo:
        if es_titulo(p):
            continue
        t = p.texto
        for m in re.finditer(r"(?<![\w.,])(\d+(?:[.,]\d+)?)(" + UNIDADES + r")(?![\w/])", t):
            inf.add("Números y unidades", "ERROR", p.idx,
                    f"Falta espacio entre número y unidad: «{m.group(1)} {m.group(2)}».", fragmento(t, m.start(), m.end(), 25))
        for m in re.finditer(r"(?<![\w\-./:])(\d+(?:[.,]\d+)?)\s?-\s?(\d+(?:[.,]\d+)?)(\s?(?:%|" + UNIDADES + r"))(?![\w\-])", t):
            inf.add("Números y unidades", "ERROR", p.idx,
                    f"Rango con guion: «{m.group(1)}–{m.group(2)}{m.group(3)}» (raya corta; la unidad solo al final).",
                    fragmento(t, m.start(), m.end(), 25))
        for m in re.finditer(r"(?<![\w\-./:#])((?:19|20)\d{2})-((?:19|20)\d{2})(?![\w\-])", t):
            inf.add("Números y unidades", "AVISO", p.idx,
                    f"Intervalo de años con guion: «{m.group(1)}–{m.group(2)}» (raya corta).", fragmento(t, m.start(), m.end(), 25))
        for m in re.finditer(r"\b(from|between|de|desde|entre)\s+(\d+(?:[.,]\d+)?)\s?[–-]\s?(\d+(?:[.,]\d+)?)", t, re.I):
            conj = {"from": "to", "between": "and", "de": "a", "desde": "hasta", "entre": "y"}[m.group(1).lower()]
            inf.add("Números y unidades", "ERROR", p.idx,
                    f"«{m.group(1)} {m.group(2)}–{m.group(3)}»: con «{m.group(1)}» se escribe «{m.group(1)} {m.group(2)} {conj} {m.group(3)}».",
                    fragmento(t, m.start(), m.end(), 25))
        for m in re.finditer(r"\b(\d+)\s*(?:percent|por ciento|porciento)\b", t, re.I):
            inf.add("Números y unidades", "SUGERENCIA", p.idx, f"Usar el símbolo: «{m.group(1)}%».", fragmento(t, m.start(), m.end(), 25))
        pct_junto += len(re.findall(r"\d%", t))
        pct_sep += len(re.findall(r"\d\s%", t))
        dec_punto += len(re.findall(r"(?<![\d.,])0\.\d", t))
        dec_coma += len(re.findall(r"(?<![\d.,])0,\d", t))
        for m in re.finditer(r"(?<![\w\d.])(\.\d+)\b", t):
            if not re.search(r"\w$", t[:m.start()].rstrip()):
                inf.add("Números y unidades", "SUGERENCIA", p.idx, f"Decimal sin cero inicial: «0{m.group(1)}».",
                        fragmento(t, m.start(), m.end(), 20))
        if idioma == "en":
            for m in re.finditer(r"\b(\d+)(st|nd|rd|th)\b", t):
                inf.add("Números y unidades", "SUGERENCIA", p.idx,
                        f"Ordinal «{m.group(0)}» en el texto: escribir en letras (first, second, …; nth).",
                        fragmento(t, m.start(), m.end(), 20))
            for m in re.finditer(r"(?<![\d.])(\d{1,3}),(\d{3})(?![\d,])", t):
                inf.add("Números y unidades", "SUGERENCIA", p.idx,
                        "Separador de miles con coma: IEEE usa espacio fino desde cinco cifras (62 000) y nada en cuatro (4000).",
                        fragmento(t, m.start(), m.end(), 20))
            for m in re.finditer(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s*(\d{4})", t):
                inf.add("Números y unidades", "SUGERENCIA", p.idx,
                        f"Fecha en el texto: formato internacional «{m.group(2)} {m.group(1)} {m.group(3)}».",
                        fragmento(t, m.start(), m.end(), 20))
        for m in re.finditer(r"\b(micron|microns|micrón|micrones|cps|cycles per second|ciclos por segundo)\b", t, re.I):
            inf.add("Números y unidades", "ERROR", p.idx, f"«{m.group(0)}» → micrometer (µm) / hertz (Hz).", fragmento(t, m.start(), m.end(), 20))
        for m in re.finditer(r"[™®]", t):
            inf.add("Estilo", "ERROR", p.idx, "IEEE no usa ™ ni ®.", fragmento(t, m.start(), m.end(), 20))
        rayas_largas += re.sub(r"^(Abstract|Resumen|Index Terms|Palabras clave|Keywords|Note to Practitioners)\s*—", "", t, flags=re.I).count("—")
    if idioma == "en" and pct_sep:
        inf.add("Números y unidades", "SUGERENCIA", None, f"{pct_sep} porcentajes con espacio («20 %»): en IEEE van pegados («20%»).")
    if pct_junto and pct_sep:
        inf.add("Números y unidades", "AVISO", None,
                f"Porcentajes con y sin espacio mezclados ({pct_junto} pegados, {pct_sep} con espacio). Unificar según la norma (IEEE: pegado; RAE: con espacio).")
    if dec_punto and dec_coma:
        inf.add("Números y unidades", "AVISO", None,
                f"Separador decimal mezclado ({dec_punto} con punto, {dec_coma} con coma). Unificar.")
    if rayas_largas:
        inf.add("Estilo", "SUGERENCIA", None,
                f"Hay {rayas_largas} rayas largas (—) en el texto. IEEE las admite para incisos; si la norma institucional las prohíbe, reemplazarlas por comas, paréntesis o dos puntos.")


# ----------------------------------------------------------------------------
# Estilo propio del inglés y lenguaje inclusivo
# ----------------------------------------------------------------------------

BRITANICO = [
    (r"\b(behaviour|colour|favour|honour|labour|neighbour|rumour|vapour)(s|ed|ing|al)?\b", "-our → -or"),
    (r"\b(centre|metre|litre|fibre|theatre|calibre|spectre)(s|d)?\b", "-re → -er"),
    (r"\b(optim|minim|maxim|normal|organ|real|util|character|recogn|summar|visual|initial|general|parameter|synchron|"
     r"quant|stabil|regular|priorit|custom|categor|emphas|special|standard|local|central|neutral|polar|serial|random|"
     r"vector|token|digit|capital|author|modern|symbol|harmon)is(e|es|ed|ing|ation|ations|er|ers)\b", "-ise → -ize"),
    (r"\b(analys|paralys|catalys)(e|es|ed|ing)\b", "-yse → -yze"),
    (r"\b(modell|labell|travell|cancell|signall|channell|tunnell|levell|fuell)(ed|ing|er|ers)\b", "doble l → l"),
    (r"\b(programme|catalogue|analogue|dialogue|defence|licence|grey|aluminium|sulphur|towards|whilst|amongst)\b", "grafía británica"),
]
CONFUSOS = [
    (r"\bdata (is|was|has)\b", "«data» es plural: «data are/were/have»."),
    (r"\bcomprised of\b", "«comprised of» → «composed of» o «comprising»."),
    (r"\bless (\w+s)\b(?= (?:than|of|in|are|were))", "¿«fewer»? «less» es para no contables."),
    (r"\b(e\.g\.|i\.e\.)(?!,)", "«e.g.» e «i.e.» van seguidos de coma."),
    (r"\bentitled\b", "«entitled» → «titled» (al introducir un título)."),
]
INCLUSIVO_EN = [
    (r"\bmaster[/-]slave\b|\bslave (node|device|unit|process|clock)s?\b", "master/slave → primary/secondary, leader/follower, main/secondary"),
    (r"\bblack[- ]?list(s|ed|ing)?\b", "blacklist → blocklist"),
    (r"\bwhite[- ]?list(s|ed|ing)?\b", "whitelist → access list / allowlist"),
    (r"\bblack[- ]box(es)?\b", "black box → closed box"),
    (r"\bwhite[- ]box(es)?\b", "white box → glass box"),
    (r"\b(single|double)[- ]blind\b", "single/double-blind → single/double-anonymous"),
    (r"\bblind (channel|source|signal) (estimation|separation)\b|\bblind equaliz", "blind … → source … / mix … (IEEE Thesaurus)"),
    (r"\bunmanned\b|\bmanned\b", "unmanned/manned → uncrewed, autonomous, remote / crewed, piloted"),
    (r"\bmanpower\b|\bman[- ]?hours?\b|\bman[- ]?weeks?\b", "manpower, man-hours → workforce, work hours"),
    (r"\bchairman\b|\bchairwoman\b", "chairman → chairperson"),
    (r"\bwheelchair[- ]bound\b|\bhandicapped\b|\bnormal people\b|\bable[- ]bodied\b", "usar lenguaje centrado en la persona"),
    (r"\bcaucasian\b", "Caucasian → White / European American"),
]
INCLUSIVO_ES = [
    (r"\bmaestro[/-]esclavo\b|\besclavos?\b", "maestro/esclavo → principal/secundario, líder/seguidor"),
    (r"\blistas? negras?\b", "lista negra → lista de bloqueo"),
    (r"\blistas? blancas?\b", "lista blanca → lista de acceso / de permitidos"),
    (r"\bcajas? negras?\b", "caja negra → caja cerrada (sugerencia; el término técnico está muy arraigado)"),
    (r"\bcajas? blancas?\b", "caja blanca → caja de cristal (sugerencia)"),
    (r"\b(simple|doble) ciego\b", "doble ciego → doble anónimo"),
    (r"\bhoras[- ]hombre\b|\bmano de obra\b", "horas-hombre → horas de trabajo; mano de obra → fuerza laboral"),
    (r"\bdiscapacitad[oa]s?\b|\bminusv[aá]lid[oa]s?\b|\bpersonas normales\b|\bconfinad[oa] a (una )?silla de ruedas\b", "usar lenguaje centrado en la persona («persona con discapacidad»)"),
]


def revisar_estilo(cuerpo, inf, idioma):
    en_agradecimientos = False
    for p in cuerpo:
        t = p.texto
        if es_titulo(p):
            en_agradecimientos = bool(re.search(r"acknowledg|agradec", t, re.I))
        if idioma == "en":
            for m in re.finditer(r"\b(\w+n't|it's|let's|they're|we're|you're|we've|they've|we'll|it'll|that's|there's)\b", t, re.I):
                if re.match(r"don't care", t[m.start():m.start() + 10], re.I):
                    continue
                inf.add("Estilo", "ERROR", p.idx, f"Contracción «{m.group(0)}»: escribirla completa.", fragmento(t, m.start(), m.end(), 25))
            for pat, msg in BRITANICO:
                for m in re.finditer(pat, t, re.I):
                    inf.add("Estilo", "ERROR", p.idx, f"Ortografía británica «{m.group(0)}» ({msg}).", fragmento(t, m.start(), m.end(), 20))
            for pat, msg in CONFUSOS:
                for m in re.finditer(pat, t, re.I):
                    inf.add("Estilo", "SUGERENCIA", p.idx, msg, fragmento(t, m.start(), m.end(), 25))
        for pat, msg in (INCLUSIVO_EN if idioma == "en" else INCLUSIVO_ES + INCLUSIVO_EN[:6]):
            for m in re.finditer(pat, t, re.I):
                inf.add("Lenguaje inclusivo", "SUGERENCIA", p.idx, f"«{m.group(0)}»: {msg}.", fragmento(t, m.start(), m.end(), 25))
        if re.search(r"\b(ChatGPT|GPT-\d|Claude|Gemini|Copilot|Midjourney|DALL.E|Stable Diffusion)\b", t) and not en_agradecimientos:
            inf.add("Estilo", "AVISO", p.idx,
                    "Se menciona una herramienta de IA: IEEE exige declarar el contenido generado con IA en el Acknowledgment (sistema, secciones y nivel de uso).",
                    t[:100])


# ----------------------------------------------------------------------------
# LaTeX y BibTeX
# ----------------------------------------------------------------------------

def revisar_latex(texto, inf):
    if not re.search(r"\\documentclass(\[[^\]]*\])?\{IEEEtran\}", texto):
        inf.add("LaTeX", "SUGERENCIA", None, "La clase no es IEEEtran (normal en tesis; en artículos IEEE usar `\\documentclass[journal]{IEEEtran}`).")
    m = re.search(r"\\bibliographystyle\{([^}]*)\}", texto)
    if m and m.group(1) not in ("IEEEtran", "IEEEtranN", "ieeetr"):
        inf.add("LaTeX", "ERROR", None, f"`\\bibliographystyle{{{m.group(1)}}}`: usar `IEEEtran`.")
    if re.search(r"\\usepackage(\[[^\]]*\])?\{natbib\}", texto):
        inf.add("LaTeX", "AVISO", None, "natbib suele producir citas autor-año; para IEEE usar el paquete `cite`.")
    if "\\cite" in texto and not re.search(r"\\usepackage(\[[^\]]*\])?\{[^}]*\bcite\b[^}]*\}", texto) and "biblatex" not in texto:
        inf.add("LaTeX", "SUGERENCIA", None, "Agregar `\\usepackage{cite}` para que `\\cite{a,b,c}` se imprima ordenado y comprimido como `[1]–[3]`.")
    m = re.search(r"\\bibliography\{([^}]*)\}", texto)
    if m and "IEEEabrv" not in m.group(1):
        inf.add("LaTeX", "SUGERENCIA", None, "Incluir `IEEEabrv` en `\\bibliography{IEEEabrv,refs}` para abreviar nombres de revistas.")
    for m in re.finditer(r"\\cite\{[^}]*\}\s*,?\s*\\cite\{", texto):
        inf.add("LaTeX", "ERROR", None, "Citas consecutivas `\\cite{a}\\cite{b}`: unir en `\\cite{a,b}`.", fragmento(texto, m.start(), m.end(), 20))
    for m in re.finditer(r"\b(Figure|Figura|figure|fig\.)~?\\ref", texto):
        inf.add("LaTeX", "ERROR", None, "Usar `Fig.~\\ref{…}`.", fragmento(texto, m.start(), m.end(), 20))
    for m in re.finditer(r"\b(Eq\.|Equation|eq\.|Ec\.|ecuación)~?\\(eq)?ref", texto):
        inf.add("LaTeX", "SUGERENCIA", None, "Citar ecuaciones con `\\eqref{…}` sin «Eq.» (salvo al inicio de oración).", fragmento(texto, m.start(), m.end(), 20))
    for m in re.finditer(r"(?<!\\)\[\d+(?:[,\s–-]+\d+)*\]", re.sub(r"\\begin\{.*?\}|\\\[.*?\\\]|\$[^$]*\$|\\[a-zA-Z]+\[[^\]]*\]", "", texto)):
        inf.add("LaTeX", "AVISO", None, "Cita numérica escrita a mano: usar `\\cite{clave}` para que la numeración sea automática.", m.group(0))
        break
    if re.search(r"\\section\*?\{\s*Acknowledg?ements?\s*\}", texto, re.I):
        inf.add("LaTeX", "SUGERENCIA", None, "En IEEEtran: `\\section*{Acknowledgment}` (singular, sin «e»).")


def parsear_bib(texto):
    entradas = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", texto):
        tipo, clave = m.group(1).lower(), m.group(2)
        if tipo in ("string", "comment", "preamble"):
            continue
        i, prof = m.end(), 1
        while i < len(texto) and prof:
            if texto[i] == "{":
                prof += 1
            elif texto[i] == "}":
                prof -= 1
            i += 1
        cuerpo = texto[m.end():i - 1]
        campos = {}
        for f in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}|\"[^\"]*\"|[\w]+)", cuerpo):
            v = f.group(2)
            if v[:1] in "{\"":
                v = v[1:-1]
            campos[f.group(1).lower()] = v.strip()
        entradas.append((tipo, clave, campos))
    return entradas


REQUERIDOS = {
    "article": ["author", "title", "journal", "year", "volume"],
    "inproceedings": ["author", "title", "booktitle", "year", "pages"],
    "conference": ["author", "title", "booktitle", "year", "pages"],
    "book": ["title", "publisher", "year"],
    "incollection": ["author", "title", "booktitle", "publisher", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "misc": ["title"],
    "online": ["title", "url"],
    "standard": ["title"],
}


def revisar_bib(texto, claves_citadas, inf):
    entradas = parsear_bib(texto)
    for tipo, clave, c in entradas:
        faltan = [f for f in REQUERIDOS.get(tipo, []) if f not in c and not (f == "author" and "editor" in c)]
        if tipo == "article" and "pages" not in c and "eid" not in c and "articleno" not in c:
            faltan.append("pages (o número de artículo)")
        if faltan:
            inf.add("BibTeX", "AVISO", None, f"`{clave}` ({tipo}): faltan {', '.join(faltan)}.")
        if "pages" in c and re.search(r"\d\s*[-–]\s*\d", c["pages"]) and "--" not in c["pages"]:
            inf.add("BibTeX", "SUGERENCIA", None, f"`{clave}`: páginas con un guion; usar `--` (`{c['pages'].replace('-', '--')}`).")
        if "title" in c:
            for s in re.findall(r"(?<![{\w])([A-Z][A-Z0-9]+[a-z]?s?)(?![}\w])", c["title"]):
                if not re.search(r"\{[^{}]*" + re.escape(s) + r"[^{}]*\}", c["title"]):
                    inf.add("BibTeX", "SUGERENCIA", None, f"`{clave}`: proteger «{s}» con llaves en el título (`{{{s}}}`) para que no pase a minúscula.")
                    break
        if "month" in c and re.fullmatch(r"[A-Za-z]{4,}", c["month"]) and c["month"].lower() not in ("sept",):
            inf.add("BibTeX", "SUGERENCIA", None, f"`{clave}`: mes como texto «{c['month']}»; usar la macro (`month = oct`).")
        if "doi" in c and c["doi"].startswith("http"):
            inf.add("BibTeX", "SUGERENCIA", None, f"`{clave}`: el campo doi debe llevar solo el identificador (`10.1109/...`).")
        if "journal" in c and re.search(r"Transactions on|Journal of|Proceedings of", c["journal"]) and not c["journal"].startswith("IEEE_"):
            inf.add("BibTeX", "SUGERENCIA", None, f"`{clave}`: revista sin abreviar; usar la macro de IEEEabrv o la abreviatura («{c['journal'][:60]}»).")
        if "author" in c:
            n = len(re.split(r"\s+and\s+", c["author"]))
            if "others" in c["author"] and n <= 6:
                inf.add("BibTeX", "AVISO", None, f"`{clave}`: «and others» con {n} autores; IEEE lista hasta seis.")
    claves = [k for _, k, _ in entradas]
    for k, n in Counter(claves).items():
        if n > 1:
            inf.add("BibTeX", "ERROR", None, f"Clave duplicada `{k}`.")
    if claves_citadas is not None:
        faltan = sorted(set(claves_citadas) - set(claves))
        if faltan:
            inf.add("BibTeX", "ERROR", None, "Claves citadas en el .tex que no están en el .bib: " + ", ".join(faltan[:40]))
    return entradas


# ----------------------------------------------------------------------------
# Principal
# ----------------------------------------------------------------------------

def generar_informe(inf, meta):
    c = inf.contar()
    out = [f"# Revisión IEEE: {meta['archivo']}", ""]
    out.append(f"Idioma detectado: **{meta['idioma']}** · Párrafos analizados: {meta['parrafos']} · "
               f"Entradas en la lista de referencias: {meta['n_refs']} · Números citados en el texto: {meta['citados']}")
    out.append("")
    out.append(f"**{c['ERROR']} errores · {c['AVISO']} avisos · {c['SUGERENCIA']} sugerencias**")
    out.append("")
    out.append("Revisión automática: confirmá cada hallazgo en su contexto. "
               "«párr.» es el número de párrafo no vacío contado desde el inicio del documento.")
    orden = ["Coherencia texto–lista", "Citas en el texto", "Lista de referencias", "BibTeX", "LaTeX", "Figuras y tablas",
             "Ecuaciones y secciones", "Estructura", "Resumen", "Siglas", "Números y unidades", "Estilo", "Lenguaje inclusivo"]
    niveles = {"ERROR": 0, "AVISO": 1, "SUGERENCIA": 2}
    for cat in orden + [k for k in inf.items if k not in orden]:
        lst = inf.items.get(cat)
        if not lst:
            continue
        out.append("")
        out.append(f"## {cat} ({len(lst)})")
        vistos = Counter()
        for nivel, idx, msg, frag in sorted(lst, key=lambda x: (niveles[x[0]], x[1] or 0)):
            clave = (nivel, msg.split("«")[0][:50])
            vistos[clave] += 1
            if vistos[clave] > 12:
                if vistos[clave] == 13:
                    out.append(f"- … (más casos del mismo tipo omitidos)")
                continue
            loc = f"párr. {idx}: " if idx else ""
            linea = f"- **{nivel}** {loc}{msg}"
            if frag:
                linea += f"\n  > {frag}"
            out.append(linea)
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Revisión automática de estilo y citas IEEE.")
    ap.add_argument("archivos", nargs="+", help=".docx, .tex, .bib, .md, .txt o .pdf")
    ap.add_argument("--idioma", choices=["es", "en", "auto"], default="auto")
    ap.add_argument("--salida", help="Guardar el informe en este archivo (.md)")
    a = ap.parse_args()

    inf = Informe()
    parrafos = []
    texto_tex = None
    textos_bib = []
    principal = None
    for ruta in a.archivos:
        ext = os.path.splitext(ruta)[1].lower()
        if ext == ".bib":
            textos_bib.append(open(ruta, encoding="utf-8", errors="replace").read())
            continue
        principal = principal or ruta
        if ext == ".docx":
            parrafos = leer_docx(ruta)
        elif ext == ".tex":
            texto_tex = open(ruta, encoding="utf-8", errors="replace").read()
            parrafos = leer_texto_plano(limpiar_latex(texto_tex))
        elif ext == ".pdf":
            parrafos = leer_pdf(ruta)
        else:
            parrafos = leer_texto_plano(open(ruta, encoding="utf-8", errors="replace").read())
    principal = principal or a.archivos[0]

    idioma = a.idioma if a.idioma != "auto" else (detectar_idioma(parrafos) if parrafos else "en")
    n_refs = 0
    citados = 0
    if parrafos:
        cuerpo, refs, _ = partir_cuerpo_y_refs(parrafos)
        if texto_tex is None:
            if refs:
                n_refs = revisar_referencias(refs, inf, idioma)
            else:
                inf.add("Lista de referencias", "AVISO", None,
                        "No se encontró la lista de referencias (título «References», «Referencias» o «Bibliografía»).")
            orden = revisar_citas(cuerpo, n_refs, inf, idioma)
            citados = len(orden)
        revisar_figuras_tablas(cuerpo, inf, idioma)
        revisar_ecuaciones_secciones(cuerpo, inf, idioma)
        revisar_resumen(cuerpo, inf, idioma)
        revisar_siglas(cuerpo, inf, idioma)
        revisar_numeros(cuerpo, inf, idioma)
        revisar_estilo(cuerpo, inf, idioma)
    claves = None
    if texto_tex is not None:
        revisar_latex(texto_tex, inf)
        claves = []
        for m in re.finditer(r"\\cite\w*\{([^}]*)\}", texto_tex):
            claves.extend(k.strip() for k in m.group(1).split(","))
        citados = len(set(claves))
    for tb in textos_bib:
        ents = revisar_bib(tb, claves, inf)
        n_refs += len(ents)

    rep = generar_informe(inf, {"archivo": os.path.basename(principal), "idioma": idioma,
                                "parrafos": len(parrafos), "n_refs": n_refs, "citados": citados})
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as f:
            f.write(rep)
        c = inf.contar()
        print(f"Informe guardado en {a.salida}: {c['ERROR']} errores, {c['AVISO']} avisos, {c['SUGERENCIA']} sugerencias.")
    else:
        print(rep)


if __name__ == "__main__":
    main()
