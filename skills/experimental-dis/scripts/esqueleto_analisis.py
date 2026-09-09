#!/usr/bin/env python3
"""Genera analisis para respuestas continuas gaussianas, no un analisis universal.

Uso: --diseno dca --lenguaje python --salida analisis.py [--datos datos.csv]
Por defecto busca plan_aleatorizacion.csv junto al script generado. --datos es
relativo a ese directorio (o absoluto); el script admite otra ruta al ejecutarse.
Complete respuesta en el CSV: no se simulan resultados ni se eliminan NA.
Factores factoriales/splitplot se deducen de las columnas del CSV, en su orden.
Python requiere pandas, numpy y statsmodels, NO incluidos en requirements.txt
del planificador. R basico basta salvo medidas repetidas (requiere nlme).

Alcance: planes completos balanceados. Bloques fijos en DBCA/factorial.
Splitplot: bloques aleatorios y parcela grande anidada; R usa estratos exactos
del ANOVA balanceado, Python solo estimacion REML sin pruebas de efectos fijos.
Repetidas: tratamiento entre sujetos, tiempo categorico, intercepto aleatorio
por sujeto (simetria compuesta); solo estimacion, sin inferencia implementada.
Cruzado: exclusivamente AB/BA, 2 periodos, sin arrastre, sujeto fijo; no se
estima secuencia (absorbida por sujeto). No generalizar a otros cruzados.
aleatorizar.py NO genera planes repetidos/cruzados: esos CSV son externos.
"""

import argparse
import json
from pathlib import Path
import textwrap

DISENOS = ("dca", "dbca", "cuadrado-latino", "factorial", "parcelas-divididas",
           "medidas-repetidas", "cruzado")
RESERVADAS = ("unidad", "tratamiento", "bloque", "posicion", "fila", "columna",
              "parcela_grande", "semilla", "respuesta", "sujeto", "tiempo",
              "periodo", "secuencia")

PYTHON = r'''
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--datos", type=Path, default=Path(__file__).resolve().parent / DATOS)
args = p.parse_args()
d = pd.read_csv(args.datos, dtype=str, keep_default_na=False)

def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)

def columnas(nombres):
    exigir(set(nombres) <= set(d.columns), "Faltan columnas: " + str(nombres))
    exigir(not d[nombres].apply(lambda x: x.str.strip().eq("")).any().any(),
           "Complete todas las celdas requeridas; no se eliminan faltantes.")

def balance(nombres, una=False):
    columnas(nombres)
    c = d.groupby(nombres, observed=True).size()
    exigir(len(c) == np.prod([d[x].nunique() for x in nombres]) and c.nunique() == 1,
           "Se requiere un plan completo balanceado: " + str(nombres))
    if una:
        exigir(c.iloc[0] == 1, "Se requiere una observacion por celda.")
    return c.iloc[0]

exigir(len(d) > 0, "CSV vacio.")
columnas(["respuesta", "tratamiento"])
d["respuesta"] = pd.to_numeric(d["respuesta"], errors="raise")
exigir(np.isfinite(d["respuesta"]).all(), "Respuesta no finita.")
exigir(d.tratamiento.nunique() >= 2, "Se requieren al menos dos tratamientos.")
factores = [c for c in d.columns if c not in RESERVADAS]
if DISENO in ("factorial", "parcelas-divididas"):
    exigir(len(factores) >= 2, "Faltan columnas de factores del CSV de aleatorizar.")
    if DISENO == "parcelas-divididas":
        exigir(len(factores) == 2, "Solo un factor principal y uno de subparcela.")
    columnas(factores)
    exigir(all(d[c].nunique() >= 2 for c in factores), "Factores con un solo nivel.")
    # Nombres internos seguros incluso si los nombres originales son palabras reservadas.
    mapa = {c: "X" + str(i + 1) for i, c in enumerate(factores)}
    print("Factores (orden principal/subparcela en splitplot):", mapa)
    d = d.rename(columns=mapa)
    factores = list(mapa.values())
    formula = "respuesta ~ " + " * ".join("C(" + c + ")" for c in factores)

if DISENO not in ("medidas-repetidas", "cruzado"):
    columnas(["unidad"])
    exigir(d.unidad.is_unique, "unidad debe identificar una sola unidad experimental.")

if DISENO == "dca":
    exigir(balance(["tratamiento"]) >= 2, "Se requieren replicas independientes.")
    formula = "respuesta ~ C(tratamiento)"
elif DISENO == "dbca":
    balance(["bloque", "tratamiento"], una=True)
    exigir(d.bloque.nunique() >= 2, "Se requieren al menos dos bloques.")
    formula = "respuesta ~ C(bloque) + C(tratamiento)"
elif DISENO == "cuadrado-latino":
    balance(["fila", "columna"], una=True)
    balance(["fila", "tratamiento"], una=True)
    balance(["columna", "tratamiento"], una=True)
    exigir(d.tratamiento.nunique() >= 3, "Orden 2 no deja error residual.")
    formula = "respuesta ~ C(fila) + C(columna) + C(tratamiento)"
elif DISENO == "factorial":
    if "bloque" in d:
        balance(["bloque"] + factores, una=True)
        exigir(d.bloque.nunique() >= 2, "Se requieren al menos dos bloques.")
        formula += " + C(bloque)"
    else:
        exigir(balance(factores) >= 2, "Factorial sin replicas no estima error.")
elif DISENO == "parcelas-divididas":
    balance(["bloque"] + factores, una=True)
    columnas(["parcela_grande"])
    exigir(d.bloque.nunique() >= 2, "Se requieren al menos dos bloques.")
    exigir(d.groupby("parcela_grande")[["bloque", "X1"]].nunique().eq(1).all().all(),
           "parcela_grande debe ser globalmente unica y anidada en bloque/principal.")
    exigir(d.groupby(["bloque", "X1"]).parcela_grande.nunique().eq(1).all(),
           "Una parcela grande por nivel principal dentro de bloque.")
    # Dos componentes: bloque y parcela grande dentro del bloque; residual subparcela.
    ajuste = smf.mixedlm(formula, d, groups=d["bloque"], re_formula="1",
                        vc_formula={"parcela": "0 + C(parcela_grande)"}).fit(reml=True)
elif DISENO == "medidas-repetidas":
    # CSV externo largo: sujeto,tratamiento,tiempo,respuesta; sujeto globalmente unico.
    balance(["sujeto", "tiempo"], una=True)
    exigir(d.tiempo.nunique() >= 2, "Se requieren al menos dos tiempos.")
    exigir(d.groupby("sujeto").tratamiento.nunique().eq(1).all(),
           "tratamiento debe ser constante dentro del sujeto.")
    sujetos = d.drop_duplicates("sujeto").groupby("tratamiento").size()
    exigir(sujetos.min() >= 2 and sujetos.nunique() == 1, "Sujetos balanceados, >=2 por tratamiento.")
    formula = "respuesta ~ C(tratamiento) * C(tiempo)"
    ajuste = smf.mixedlm(formula, d, groups=d["sujeto"], re_formula="1").fit(reml=True)
elif DISENO == "cruzado":
    # CSV externo largo: sujeto,secuencia,periodo,tratamiento,respuesta.
    balance(["sujeto", "periodo"], una=True)
    columnas(["secuencia"])
    exigir(set(d.periodo) == {"1", "2"} and set(d.tratamiento) == {"A", "B"},
           "Solo cruzado AB/BA de dos periodos (1,2), sin arrastre.")
    exigir(d.groupby("sujeto").secuencia.nunique().eq(1).all(), "Secuencia cambia dentro de sujeto.")
    orden = d.sort_values("periodo").groupby("sujeto").tratamiento.agg("".join)
    sec = d.drop_duplicates("sujeto").set_index("sujeto").secuencia
    exigir(orden.eq(sec.reindex(orden.index)).all() and set(orden) == {"AB", "BA"},
           "Secuencias deben concordar con tratamientos por periodo.")
    exigir(orden.value_counts().min() >= 2 and orden.value_counts().nunique() == 1,
           "Se requieren secuencias balanceadas con >=2 sujetos cada una.")
    formula = "respuesta ~ C(sujeto) + C(periodo) + C(tratamiento)"

if DISENO in ("parcelas-divididas", "medidas-repetidas"):
    exigir(ajuste.converged, "REML no convergio; no interpretar estimaciones.")
    print("SOLO ESTIMACION REML; inferencia de efectos fijos no implementada.")
    print(ajuste.fe_params)
    print("Covarianza de interceptos:", ajuste.cov_re)
    print("Componentes adicionales:", ajuste.vcomp, "Residual:", ajuste.scale)
else:
    ajuste = smf.ols(formula, d, missing="raise").fit()
    exigir(ajuste.df_resid > 0 and np.linalg.matrix_rank(ajuste.model.exog) == ajuste.model.exog.shape[1],
           "Modelo sin error residual o de rango deficiente.")
    # Tipo I: efectos ortogonales en los planes balanceados admitidos.
    # En cruzado, tratamiento se prueba al final, ajustado por sujeto y periodo.
    print(anova_lm(ajuste, typ=1))
    print("No interpretar pruebas de sujeto/secuencia como efectos de tratamiento.")
print("Revisar residuos, normalidad, homocedasticidad e independencia al nivel experimental.")
'''

R = r'''
args <- commandArgs(trailingOnly=TRUE)
archivo <- grep("^--file=", commandArgs(), value=TRUE)
base <- if (length(archivo)) dirname(normalizePath(sub("^--file=", "", archivo[1]))) else getwd()
ruta <- if (length(args)) args[1] else if (grepl("^(/|[A-Za-z]:|\\\\)", DATOS)) DATOS else file.path(base, DATOS)
d <- read.csv(ruta, colClasses="character", check.names=FALSE, na.strings="", strip.white=TRUE)
exigir <- function(ok, mensaje) { if (!isTRUE(ok)) stop(mensaje, call.=FALSE) }
columnas <- function(nombres) {
  exigir(all(nombres %in% names(d)), paste("Faltan columnas:", paste(nombres, collapse=", ")))
  exigir(!anyNA(d[nombres]) && all(vapply(d[nombres], function(x) all(nzchar(trimws(as.character(x)))), logical(1))),
         "Complete celdas requeridas; no se eliminan faltantes.")
}
balance <- function(nombres, una=FALSE) {
  columnas(nombres)
  c <- table(d[nombres])
  exigir(all(c > 0) && length(unique(as.vector(c))) == 1, "Se requiere un plan completo balanceado.")
  if (una) exigir(all(c == 1), "Se requiere una observacion por celda.")
  as.numeric(c[1])
}
exigir(nrow(d) > 0, "CSV vacio.")
columnas(c("respuesta", "tratamiento"))
d$respuesta <- as.numeric(d$respuesta)
exigir(all(is.finite(d$respuesta)), "Respuesta no numerica o no finita.")
exigir(length(unique(d$tratamiento)) >= 2, "Se requieren al menos dos tratamientos.")
factores <- setdiff(names(d), RESERVADAS)
if (DISENO %in% c("factorial", "parcelas-divididas")) {
  exigir(length(factores) >= 2, "Faltan columnas de factores.")
  if (DISENO == "parcelas-divididas") exigir(length(factores) == 2, "Solo principal y subparcela.")
  columnas(factores)
  exigir(all(vapply(d[factores], function(x) length(unique(x)) >= 2, logical(1))), "Factor con un nivel.")
  internos <- paste0("X", seq_along(factores))
  print(setNames(internos, factores))
  names(d)[match(factores, names(d))] <- internos
  factores <- internos
  formula <- paste("respuesta ~", paste(factores, collapse=" * "))
}
for (c in setdiff(names(d), "respuesta")) d[[c]] <- factor(d[[c]])
if (!DISENO %in% c("medidas-repetidas", "cruzado")) {
  columnas("unidad")
  exigir(!anyDuplicated(d$unidad), "unidad debe ser unica.")
}
if (DISENO == "dca") {
  exigir(balance("tratamiento") >= 2, "Se requieren replicas independientes.")
  formula <- "respuesta ~ tratamiento"
} else if (DISENO == "dbca") {
  balance(c("bloque", "tratamiento"), TRUE)
  exigir(nlevels(d$bloque) >= 2, "Se requieren al menos dos bloques.")
  formula <- "respuesta ~ bloque + tratamiento"
} else if (DISENO == "cuadrado-latino") {
  balance(c("fila", "columna"), TRUE)
  balance(c("fila", "tratamiento"), TRUE)
  balance(c("columna", "tratamiento"), TRUE)
  exigir(nlevels(d$tratamiento) >= 3, "Orden 2 no deja error residual.")
  formula <- "respuesta ~ fila + columna + tratamiento"
} else if (DISENO == "factorial") {
  if ("bloque" %in% names(d)) {
    balance(c("bloque", factores), TRUE)
    exigir(nlevels(d$bloque) >= 2, "Se requieren al menos dos bloques.")
    formula <- paste(formula, "+ bloque")
  } else exigir(balance(factores) >= 2, "Factorial sin replicas no estima error.")
} else if (DISENO == "parcelas-divididas") {
  balance(c("bloque", factores), TRUE)
  columnas("parcela_grande")
  exigir(nlevels(d$bloque) >= 2, "Se requieren al menos dos bloques.")
  exigir(all(tapply(as.character(d$bloque), d$parcela_grande, function(x) length(unique(x))) == 1) &&
         all(tapply(as.character(d$X1), d$parcela_grande, function(x) length(unique(x))) == 1),
         "parcela_grande debe ser unica y anidada en bloque/principal.")
  exigir(all(tapply(as.character(d$parcela_grande), interaction(d$bloque, d$X1), function(x) length(unique(x))) == 1),
         "Una parcela grande por bloque/principal.")
  # A contra error de parcela grande; B y A:B contra error de subparcela.
  ajuste <- aov(as.formula(paste(formula, "+ Error(bloque/parcela_grande)")), data=d)
  print(summary(ajuste))
} else if (DISENO == "medidas-repetidas") {
  # CSV externo largo: sujeto,tratamiento,tiempo,respuesta. Solo simetria compuesta.
  balance(c("sujeto", "tiempo"), TRUE)
  exigir(nlevels(d$tiempo) >= 2, "Se requieren al menos dos tiempos.")
  exigir(all(tapply(d$tratamiento, d$sujeto, function(x) length(unique(x))) == 1), "Tratamiento cambia dentro de sujeto.")
  sujetos <- table(d$tratamiento[!duplicated(d$sujeto)])
  exigir(all(sujetos >= 2) && length(unique(as.vector(sujetos))) == 1, "Sujetos balanceados, >=2 por tratamiento.")
  if (!requireNamespace("nlme", quietly=TRUE)) stop("Instale nlme para estimacion REML.")
  ajuste <- nlme::lme(respuesta ~ tratamiento * tiempo, random= ~1|sujeto, data=d, method="REML", na.action=na.fail)
  print("SOLO ESTIMACION REML; inferencia de efectos fijos no implementada.")
  print(nlme::fixef(ajuste))
  print(nlme::VarCorr(ajuste))
} else if (DISENO == "cruzado") {
  # AB/BA, sin arrastre; sujeto absorbe secuencia. No prueba de secuencia.
  balance(c("sujeto", "periodo"), TRUE)
  columnas("secuencia")
  exigir(setequal(levels(d$periodo), c("1", "2")) && setequal(levels(d$tratamiento), c("A", "B")), "Solo AB/BA, periodos 1 y 2.")
  exigir(all(tapply(d$secuencia, d$sujeto, function(x) length(unique(x))) == 1), "Secuencia cambia dentro de sujeto.")
  orden <- vapply(split(d, d$sujeto), function(x) paste(as.character(x$tratamiento[order(x$periodo)]), collapse=""), character(1))
  sec <- vapply(split(d, d$sujeto), function(x) as.character(x$secuencia[1]), character(1))
  exigir(all(orden == sec) && setequal(orden, c("AB", "BA")), "Secuencia no concuerda con tratamientos.")
  exigir(all(table(orden) >= 2) && length(unique(as.vector(table(orden)))) == 1, "Secuencias balanceadas, >=2 sujetos cada una.")
  formula <- "respuesta ~ sujeto + periodo + tratamiento"
}
if (!DISENO %in% c("parcelas-divididas", "medidas-repetidas")) {
  ajuste <- lm(as.formula(formula), data=d, na.action=na.fail)
  exigir(df.residual(ajuste) > 0 && ajuste$rank == ncol(model.matrix(ajuste)), "Modelo sin error residual o rango deficiente.")
  print(anova(ajuste))
  print("No interpretar pruebas de sujeto/secuencia como efectos de tratamiento.")
}
print("Revisar residuos, normalidad, homocedasticidad e independencia al nivel experimental.")
'''


def generar(diseno, lenguaje, datos="plan_aleatorizacion.csv"):
    if diseno not in DISENOS or lenguaje not in ("r", "python"):
        raise ValueError("Diseno o lenguaje no soportado.")
    alcance = __doc__
    if lenguaje == "python":
        return (repr(alcance) + "\nDISENO = " + repr(diseno) + "\nDATOS = " + repr(datos)
                + "\nRESERVADAS = " + repr(RESERVADAS) + "\n" + textwrap.dedent(PYTHON))
    return ("\n".join("# " + linea for linea in alcance.splitlines())
            + "\nDISENO <- " + json.dumps(diseno) + "\nDATOS <- " + json.dumps(datos)
            + "\nRESERVADAS <- c(" + ", ".join(json.dumps(c) for c in RESERVADAS) + ")\n"
            + textwrap.dedent(R))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--diseno", choices=DISENOS, required=True)
    p.add_argument("--lenguaje", type=str.lower, choices=("r", "python"), required=True)
    p.add_argument("--salida", type=Path, required=True)
    p.add_argument("--datos", default="plan_aleatorizacion.csv")
    args = p.parse_args()
    try:
        # No sobrescribir silenciosamente un analisis ya completado.
        with args.salida.open("x", encoding="utf-8") as fh:
            fh.write(generar(args.diseno, args.lenguaje, args.datos))
    except OSError as exc:
        p.error(str(exc))
    print(f"Esqueleto guardado en {args.salida}. Lea el alcance antes de ejecutarlo.")


if __name__ == "__main__":
    main()
