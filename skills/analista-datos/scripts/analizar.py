#!/usr/bin/env python3
"""
Análisis de un experimento según el diseño con que se tomaron los datos.

Lee el protocolo generado por la skill de diseño, promedia submuestras, ajusta
el modelo que corresponde, verifica supuestos sobre residuos, corre Tukey o
Dunnett y produce tablas y figura.

Nunca decide el modelo mirando los datos: lo toma del protocolo.

Ejemplos:
  python3 analizar.py datos.csv --protocolo diseno.json --respuesta rendimiento
  python3 analizar.py datos.csv --protocolo diseno.json --respuesta rendimiento --post-hoc dunnett --control T0
  python3 analizar.py datos.csv --diseno dbca --respuesta y --tratamiento trat --bloque bloque
"""

import argparse
import json
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from statsmodels.stats.anova import anova_lm
except ImportError:
    print("Falta statsmodels. Instalar con:\n"
          "  pip install statsmodels --break-system-packages", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------------ ayudas

def linea(texto=""):
    print(texto)


def titulo(texto):
    print()
    print("=" * 72)
    print(f"  {texto}")
    print("=" * 72)


def fmt_p(p):
    """Nunca se escribe p = 0,000."""
    if p < 0.001:
        return "< 0,001"
    return f"{p:.4f}".replace(".", ",")


def p_txt(p):
    """'p < 0,001' o 'p = 0,0234', para no escribir 'p = < 0,001'."""
    return "p < 0,001" if p < 0.001 else f"p = {p:.4f}".replace(".", ",")


def fmt(x, dec=3):
    return f"{x:.{dec}f}".replace(".", ",")


# ------------------------------------------------------------------ datos

def cargar(args):
    with open(args.protocolo, encoding="utf-8") as fh:
        prot = json.load(fh)
    df = pd.read_csv(args.datos)
    return prot, df


def promediar_submuestras(df, col_unidad, respuesta, estructura):
    """Colapsa las submuestras a una fila por unidad experimental."""
    if col_unidad not in df.columns:
        return df, False
    if df.groupby(col_unidad).size().max() <= 1:
        return df, False
    claves = [c for c in estructura if c in df.columns and c != "submuestra"]
    agrupado = (df.groupby(claves, as_index=False)[respuesta]
                  .mean(numeric_only=True))
    return agrupado, True


# ------------------------------------------------------------------ modelo

def construir_formula(prot, respuesta, df):
    """Fórmula del modelo a partir del diseño declarado, no de los datos."""
    diseno = prot.get("diseno", "dca")
    factores = [f for f in prot.get("factores", []) if f in df.columns]

    if diseno == "dca":
        return f"Q('{respuesta}') ~ C(tratamiento)"
    if diseno == "dbca":
        return f"Q('{respuesta}') ~ C(tratamiento) + C(bloque)"
    if diseno == "cuadrado-latino":
        return f"Q('{respuesta}') ~ C(tratamiento) + C(fila) + C(columna)"
    if diseno == "factorial":
        if len(factores) >= 2:
            cruce = " * ".join(f"C({f})" for f in factores)
        else:
            cruce = "C(tratamiento)"
        if "bloque" in df.columns:
            return f"Q('{respuesta}') ~ {cruce} + C(bloque)"
        return f"Q('{respuesta}') ~ {cruce}"
    if diseno in ("parcelas-divididas", "medidas-repetidas"):
        return None  # va por modelo mixto
    return f"Q('{respuesta}') ~ C(tratamiento)"


def tabla_anova(modelo, respuesta):
    aov = anova_lm(modelo, typ=2)
    ss_error = aov.loc["Residual", "sum_sq"]
    gl_error = aov.loc["Residual", "df"]
    mse = ss_error / gl_error
    ss_total = aov["sum_sq"].sum()

    filas = []
    for termino, fila in aov.iterrows():
        if termino == "Residual":
            filas.append({"Fuente": "Error experimental", "gl": int(fila["df"]),
                          "SC": fila["sum_sq"], "CM": mse, "F": np.nan, "p": np.nan,
                          "eta2_parcial": np.nan, "omega2": np.nan})
            continue
        ss = fila["sum_sq"]
        gl = int(fila["df"])
        eta2p = ss / (ss + ss_error)
        omega2 = max(0.0, (ss - gl * mse) / (ss_total + mse))
        filas.append({"Fuente": limpiar(termino), "gl": gl, "SC": ss,
                      "CM": ss / gl, "F": fila["F"], "p": fila["PR(>F)"],
                      "eta2_parcial": eta2p, "omega2": omega2})
    return pd.DataFrame(filas), mse, gl_error


def limpiar(termino):
    return (termino.replace("C(", "").replace(")", "")
            .replace(":", " x ").replace("Q('", "").replace("'", ""))


def imprimir_anova(tab, mse, media_general, alfa):
    titulo("TABLA DE ANÁLISIS DE VARIANZA")
    linea(f"  {'Fuente':<24}{'gl':>4}{'SC':>14}{'CM':>13}{'F':>9}{'p':>11}")
    linea("  " + "-" * 70)
    for _, f in tab.iterrows():
        F = "" if pd.isna(f["F"]) else fmt(f["F"], 2)
        p = "" if pd.isna(f["p"]) else fmt_p(f["p"])
        marca = ""
        if not pd.isna(f["p"]):
            marca = " *" if f["p"] < alfa else " ns"
        linea(f"  {f['Fuente'][:23]:<24}{f['gl']:>4}{f['SC']:>14.2f}"
              f"{f['CM']:>13.2f}{F:>9}{p:>11}{marca}")
    cv = 100 * np.sqrt(mse) / media_general
    linea("  " + "-" * 70)
    linea(f"  Media general: {fmt(media_general, 2)}     "
          f"Coeficiente de variación: {fmt(cv, 1)} %")
    linea(f"  Nivel de significancia: {str(alfa).replace('.', ',')}")
    if cv > 30:
        linea(f"  AVISO: un CV de {fmt(cv,1)} % es alto. Revisá el control del ensayo")
        linea("         antes de interpretar diferencias.")
    return cv


# ------------------------------------------------------------------ supuestos

def verificar_supuestos(modelo, df, respuesta, alfa, ruta_grafico=None):
    titulo("VERIFICACIÓN DE SUPUESTOS (sobre los residuos del modelo)")
    res = modelo.resid
    ajustados = modelo.fittedvalues

    W, p_sw = stats.shapiro(res)
    linea(f"  Normalidad de residuos, Shapiro Wilk: W = {fmt(W)}, p = {fmt_p(p_sw)}")
    linea(f"    {'Sin evidencia contra la normalidad.' if p_sw >= alfa else 'Hay evidencia de desvío de la normalidad.'}")

    grupos = [g[respuesta].values for _, g in df.groupby("tratamiento")]
    if all(len(g) > 1 for g in grupos) and len(grupos) > 1:
        L, p_lev = stats.levene(*grupos, center="median")
        linea(f"  Homogeneidad de varianzas, Levene: F = {fmt(L)}, p = {fmt_p(p_lev)}")
        linea(f"    {'Varianzas compatibles con la homogeneidad.' if p_lev >= alfa else 'Hay evidencia de varianzas desiguales.'}")
    else:
        p_lev = None

    n = len(res)
    linea()
    if n < 20:
        linea(f"  Con n = {n}, Shapiro Wilk tiene poca potencia y difícilmente detecte")
        linea("  un desvío real. El gráfico cuantil cuantil pesa más que la prueba.")
    elif n > 200:
        linea(f"  Con n = {n}, las pruebas detectan desvíos irrelevantes para el ANOVA.")
        linea("  Mirá la magnitud del desvío en el gráfico, no sólo el valor p.")

    if ruta_grafico:
        graficar_supuestos(res, ajustados, ruta_grafico)
    return p_sw, p_lev


def graficar_supuestos(res, ajustados, ruta):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
    sm.qqplot(res, line="s", ax=ax[0], markerfacecolor="#4C72B0",
              markeredgecolor="#31506f", alpha=0.8)
    ax[0].set_title("Cuantil cuantil de residuos", fontsize=10)
    ax[0].set_xlabel("Cuantiles teóricos"); ax[0].set_ylabel("Residuos")

    ax[1].scatter(ajustados, res, color="#4C72B0", alpha=0.8, edgecolor="#31506f")
    ax[1].axhline(0, color="grey", lw=1, ls="--")
    ax[1].set_title("Residuos contra valores ajustados", fontsize=10)
    ax[1].set_xlabel("Ajustados"); ax[1].set_ylabel("Residuos")

    ax[2].hist(res, bins=max(6, int(np.sqrt(len(res)))), color="#4C72B0",
               edgecolor="white")
    ax[2].set_title("Distribución de residuos", fontsize=10)
    ax[2].set_xlabel("Residuo"); ax[2].set_ylabel("Frecuencia")

    for a in ax:
        for lado in ("top", "right"):
            a.spines[lado].set_visible(False)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    linea(f"  Gráfico de supuestos guardado en {ruta}")


# ------------------------------------------------------------------ post hoc

def elegir_comparaciones(prot, tab, df, alfa):
    """Sobre qué medias corresponde comparar, según lo que dio el ANOVA.

    En un factorial, comparar las combinaciones cuando la interacción no es
    significativa es un error frecuente: infla el número de comparaciones y
    baja la potencia sin motivo. Si no hay interacción, lo que corresponde es
    comparar las medias marginales de cada factor con efecto significativo.
    """
    factores = [f for f in prot.get("factores", []) if f in df.columns]
    if prot.get("diseno") != "factorial" or len(factores) < 2:
        return [("tratamiento", "tratamiento")]

    inter = tab[tab["Fuente"].str.contains(" x ") & tab["p"].notna()]
    if len(inter) and (inter["p"] < alfa).any():
        return [("tratamiento", "combinación de tratamientos")]

    salida = []
    for f in factores:
        fila = tab[tab["Fuente"] == f]
        if len(fila) and fila.iloc[0]["p"] < alfa and df[f].nunique() > 2:
            salida.append((f, f"medias marginales de {f}"))
        elif len(fila) and fila.iloc[0]["p"] < alfa:
            salida.append((f, f"medias marginales de {f}"))
    return salida or [("tratamiento", "tratamiento")]


def tukey(df, respuesta, mse, gl_error, alfa, columna="tratamiento"):
    """Tukey con el CM del error del modelo, correcto para diseños balanceados."""
    medias = df.groupby(columna)[respuesta].agg(["mean", "count", "std"])
    k = len(medias)
    q = stats.studentized_range.ppf(1 - alfa, k, gl_error)

    pares = []
    nombres = list(medias.index)
    for i in range(k):
        for j in range(i + 1, k):
            a, b = nombres[i], nombres[j]
            na, nb = medias.loc[a, "count"], medias.loc[b, "count"]
            se = np.sqrt(mse / 2 * (1 / na + 1 / nb))
            dif = medias.loc[a, "mean"] - medias.loc[b, "mean"]
            q_obs = abs(dif) / se
            p = stats.studentized_range.sf(q_obs, k, gl_error)
            hsd = q * se
            pares.append({"a": a, "b": b, "diferencia": dif, "p": p,
                          "ic_inf": dif - hsd, "ic_sup": dif + hsd,
                          "significativa": p < alfa})
    return medias, pd.DataFrame(pares)


def letras(medias, pares, alfa):
    """Letras de significancia por el método de insertar y absorber.

    Se parte de un único grupo con todos los tratamientos y se lo va partiendo
    cada vez que un par resulta significativo, de modo que al final dos
    tratamientos comparten letra si y sólo si no difieren.
    """
    tratamientos = medias.sort_values("mean", ascending=False).index.tolist()
    grupos = [set(tratamientos)]

    significativos = [(r["a"], r["b"]) for _, r in pares.iterrows() if r["significativa"]]
    for a, b in significativos:
        nuevos = []
        for g in grupos:
            if a in g and b in g:
                nuevos.append(g - {a})
                nuevos.append(g - {b})
            else:
                nuevos.append(g)
        # absorber los grupos contenidos en otro
        grupos = []
        for g in nuevos:
            if not g:
                continue
            if any(g < otro for otro in nuevos):
                continue
            if g not in grupos:
                grupos.append(g)

    # ordenar los grupos por la media más alta que contienen
    grupos.sort(key=lambda g: -max(medias.loc[t, "mean"] for t in g))

    abc = "abcdefghijklmnopqrstuvwxyz"
    asignadas = {t: "" for t in tratamientos}
    for idx, g in enumerate(grupos):
        for t in g:
            asignadas[t] += abc[idx]
    return {t: "".join(sorted(v)) for t, v in asignadas.items()}


def dunnett(df, respuesta, control, alfa):
    grupos, nombres = [], []
    for t, g in df.groupby("tratamiento"):
        if t == control:
            continue
        grupos.append(g[respuesta].values)
        nombres.append(t)
    ctrl = df.loc[df["tratamiento"] == control, respuesta].values
    if len(ctrl) == 0:
        print(f"  Error: no existe el tratamiento control '{control}'.", file=sys.stderr)
        sys.exit(1)
    r = stats.dunnett(*grupos, control=ctrl, alternative="two-sided")
    ic = r.confidence_interval(confidence_level=1 - alfa)
    return pd.DataFrame({
        "tratamiento": nombres,
        "diferencia_vs_control": [g.mean() - ctrl.mean() for g in grupos],
        "p": r.pvalue,
        "ic_inf": ic.low, "ic_sup": ic.high,
        "significativa": r.pvalue < alfa,
    })


# ------------------------------------------------------------------ salidas

def tabla_medias(medias, letras_map, respuesta, unidad, alfa, prueba, etiqueta="tratamiento", columna="Tratamiento"):
    titulo(f"MEDIAS, {etiqueta.upper()}, {respuesta}" + (f" ({unidad})" if unidad else ""))
    linea(f"  {columna[:19].capitalize():<20}{'n':>4}{'Media':>12}{'DE':>11}{'EE':>11}   Letras")
    linea("  " + "-" * 68)
    for t, f in medias.sort_values("mean", ascending=False).iterrows():
        ee = f["std"] / np.sqrt(f["count"]) if f["count"] > 1 else np.nan
        linea(f"  {str(t)[:19]:<20}{int(f['count']):>4}{f['mean']:>12.2f}"
              f"{f['std']:>11.2f}{ee:>11.2f}   {letras_map.get(t, '')}")
    linea("  " + "-" * 68)
    linea(f"  Medias con letra común no difieren según la prueba de {prueba} "
          f"(alfa = {str(alfa).replace('.', ',')}).")
    linea("  DE es el desvío estándar y EE el error estándar de la media.")


def graficar_medias(df, medias, letras_map, respuesta, unidad, ruta, prueba, alfa, columna="tratamiento"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    orden = medias.sort_values("mean", ascending=False).index.tolist()
    x = np.arange(len(orden))
    m = [medias.loc[t, "mean"] for t in orden]
    ee = [medias.loc[t, "std"] / np.sqrt(medias.loc[t, "count"]) for t in orden]

    fig, ax = plt.subplots(figsize=(max(6, len(orden) * 1.3), 4.6))
    ax.bar(x, m, yerr=ee, capsize=5, color="#B7C9E2", edgecolor="#31506f",
           linewidth=1, zorder=2)
    for i, t in enumerate(orden):
        crudos = df.loc[df[columna] == t, respuesta].values
        jitter = np.random.default_rng(1).normal(0, 0.05, len(crudos))
        ax.scatter(np.full(len(crudos), i) + jitter, crudos, s=18,
                   color="#31506f", alpha=0.55, zorder=3)
        ax.text(i, m[i] + ee[i] + (max(m) - min(m)) * 0.05,
                letras_map.get(t, ""), ha="center", fontsize=11, zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(orden, fontsize=9)
    ax.set_ylabel(f"{respuesta}" + (f" ({unidad})" if unidad else ""), fontsize=10)
    ax.set_title(f"Medias por tratamiento con error estándar\n"
                 f"Letras distintas indican diferencia según {prueba} "
                 f"(alfa = {str(alfa).replace('.', ',')})", fontsize=10)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.grid(axis="y", alpha=0.25, zorder=0)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    linea(f"\n  Figura de medias guardada en {ruta}")


def interpretar(tab, alfa, respuesta):
    titulo("LECTURA DEL RESULTADO")
    efectos = tab[tab["p"].notna()]
    interacciones = efectos[efectos["Fuente"].str.contains(" x ")]
    hay_inter = (interacciones["p"] < alfa).any() if len(interacciones) else False

    if hay_inter:
        nombres = interacciones.loc[interacciones["p"] < alfa, "Fuente"].tolist()
        linea(f"  La interacción {', '.join(nombres)} resultó significativa.")
        linea("  NO interpretes los efectos principales por separado. El efecto de un")
        linea("  factor depende del nivel del otro, así que corresponde analizar")
        linea("  efectos simples, esto es, cada factor dentro de cada nivel del otro.")
    else:
        for _, f in efectos.iterrows():
            if "bloque" in f["Fuente"].lower() or "fila" in f["Fuente"].lower() \
               or "columna" in f["Fuente"].lower():
                continue
            if f["p"] < alfa:
                linea(f"  {f['Fuente']}: efecto significativo "
                      f"(F({f['gl']}, {int(tab.iloc[-1]['gl'])}) = {fmt(f['F'],2)}, "
                      f"{p_txt(f["p"])}, eta cuadrado parcial = {fmt(f['eta2_parcial'])}).")
            else:
                linea(f"  {f['Fuente']}: no se detectaron diferencias significativas "
                      f"(F({f['gl']}, {int(tab.iloc[-1]['gl'])}) = {fmt(f['F'],2)}, "
                      f"{p_txt(f['p'])}).")
                linea("    Ojo: esto no prueba que los tratamientos sean iguales.")
    if any("bloque" in s.lower() for s in tab["Fuente"]):
        linea()
        linea("  El efecto de bloque es control del ensayo, no un hallazgo. No lo")
        linea("  reportes como resultado ni lo discutas.")


# ------------------------------------------------------------------ principal

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("datos")
    p.add_argument("--protocolo", required=True)
    p.add_argument("--respuesta", default=None)
    p.add_argument("--post-hoc", default=None, choices=["tukey", "dunnett", "ninguna"])
    p.add_argument("--control", default=None, help="Tratamiento testigo, para Dunnett")
    p.add_argument("--alfa", type=float, default=None)
    p.add_argument("--salida", default="resultados", help="Prefijo de los archivos de salida")
    args = p.parse_args()

    prot, df = cargar(args)
    alfa = args.alfa if args.alfa is not None else prot.get("alfa", 0.05)
    respuestas = prot.get("respuestas", [])
    nombre_resp = args.respuesta or (respuestas[0]["nombre"] if respuestas else None)
    if nombre_resp is None or nombre_resp not in df.columns:
        print(f"Error: indicá una respuesta válida con --respuesta. "
              f"Columnas disponibles: {list(df.columns)}", file=sys.stderr)
        sys.exit(1)
    unidad = next((r.get("unidad", "") for r in respuestas
                   if r["nombre"] == nombre_resp), "")
    tipo = next((r.get("tipo", "continua") for r in respuestas
                 if r["nombre"] == nombre_resp), "continua")

    titulo(f"ANÁLISIS DE {nombre_resp.upper()}")
    linea(f"  Diseño declarado en el protocolo: {prot.get('diseno')}")
    linea(f"  Unidad experimental: {prot.get('unidad_experimental') or 'no declarada'}")
    linea(f"  Modelo previsto: {prot.get('modelo')}")

    if tipo in ("conteo", "proporcion", "binaria"):
        linea()
        linea(f"  AVISO: la respuesta es de tipo {tipo}. El ANOVA supone errores")
        linea("  normales y varianza constante, cosa que estas variables rara vez")
        linea("  cumplen. Corresponde un modelo lineal generalizado. Lo que sigue")
        linea("  es orientativo, no el análisis definitivo.")

    df, colapsado = promediar_submuestras(
        df, "unidad", nombre_resp, prot.get("columnas_estructura", []))
    if colapsado:
        linea()
        linea(f"  Submuestras promediadas por unidad experimental. n = {len(df)}.")

    formula = construir_formula(prot, nombre_resp, df)
    if formula is None:
        linea()
        linea("  Este diseño requiere modelo mixto con dos términos de error.")
        linea("  Todavía no implementado en este script. Ver references/modelo-por-diseno.md")
        sys.exit(3)

    modelo = smf.ols(formula, data=df).fit()
    tab, mse, gl_error = tabla_anova(modelo, nombre_resp)
    cv = imprimir_anova(tab, mse, df[nombre_resp].mean(), alfa)

    verificar_supuestos(modelo, df, nombre_resp, alfa,
                        ruta_grafico=f"{args.salida}_supuestos.png")

    interpretar(tab, alfa, nombre_resp)

    prueba = args.post_hoc or prot.get("post_hoc", "tukey")
    if prueba == "dunnett":
        control = args.control or prot.get("control")
        if not control:
            print("\n  Para Dunnett hace falta --control con el nombre del testigo.")
            sys.exit(1)
        titulo(f"COMPARACIONES CONTRA EL TESTIGO ({control}), PRUEBA DE DUNNETT")
        res = dunnett(df, nombre_resp, control, alfa)
        linea(f"  {'Tratamiento':<20}{'Diferencia':>13}{'IC inferior':>14}"
              f"{'IC superior':>14}{'p':>11}")
        linea("  " + "-" * 72)
        for _, f in res.iterrows():
            linea(f"  {str(f['tratamiento'])[:19]:<20}{f['diferencia_vs_control']:>13.2f}"
                  f"{f['ic_inf']:>14.2f}{f['ic_sup']:>14.2f}{fmt_p(f['p']):>11}"
                  f"{'  *' if f['significativa'] else '  ns'}")
        linea("  " + "-" * 72)
        if "bloque" in df.columns:
            linea("  Nota: esta prueba se corre sobre las medias por unidad y no aprovecha")
            linea("  la reducción de error que aporta el bloque, así que es conservadora.")
        res.to_csv(f"{args.salida}_dunnett.csv", index=False)
    elif prueba == "tukey":
        for columna, etiqueta in elegir_comparaciones(prot, tab, df, alfa):
            medias, pares = tukey(df, nombre_resp, mse, gl_error, alfa, columna)
            letras_map = letras(medias, pares, alfa)
            tabla_medias(medias, letras_map, nombre_resp, unidad, alfa, "Tukey", etiqueta, columna)
            titulo(f"COMPARACIONES POR PARES, PRUEBA DE TUKEY, {etiqueta.upper()}")
            linea(f"  {'Comparación':<26}{'Diferencia':>13}{'IC inferior':>14}"
                  f"{'IC superior':>14}{'p':>11}")
            linea("  " + "-" * 78)
            for _, f in pares.iterrows():
                comp = f"{f['a']} vs {f['b']}"
                linea(f"  {comp[:25]:<26}{f['diferencia']:>13.2f}{f['ic_inf']:>14.2f}"
                      f"{f['ic_sup']:>14.2f}{fmt_p(f['p']):>11}"
                      f"{'  *' if f['significativa'] else '  ns'}")
            linea("  " + "-" * 78)
            linea("  El intervalo de confianza es el de la diferencia entre medias.")
            linea("  Una diferencia puede ser significativa y aun así carecer de")
            linea("  relevancia práctica. Juzgá la magnitud, no sólo el valor p.")
            sufijo = "" if columna == "tratamiento" else f"_{columna}"
            graficar_medias(df, medias, letras_map, nombre_resp, unidad,
                            f"{args.salida}_medias{sufijo}.png", "Tukey", alfa, columna)
            medias.to_csv(f"{args.salida}_medias{sufijo}.csv")
            pares.to_csv(f"{args.salida}_tukey{sufijo}.csv", index=False)

    tab.to_csv(f"{args.salida}_anova.csv", index=False)
    print()
    print(f"  Tablas guardadas con el prefijo '{args.salida}_'.")
    import scipy
    print(f"  Software: Python {sys.version.split()[0]}, statsmodels {sm.__version__}, "
          f"scipy {scipy.__version__}, pandas {pd.__version__}.")
    print("  Anotá estas versiones en la sección de análisis estadístico.")
    print()


if __name__ == "__main__":
    main()
