#!/usr/bin/env python3
"""
Tamaño de muestra por potencia estadística para los casos frecuentes en tesis.

Depende sólo de scipy. Todos los cálculos se hacen con distribuciones no centrales,
no con aproximaciones normales, salvo en proporciones y correlación donde la
aproximación es la práctica estándar.

Ejemplos:
  python3 tamano_muestral.py --caso dos-medias --dme 5 --sd 8
  python3 tamano_muestral.py --caso anova --grupos 4 --dme 2.5 --sd 3.0
  python3 tamano_muestral.py --caso dos-proporciones --p1 0.30 --p2 0.55
  python3 tamano_muestral.py --caso medias-pareadas --dme 4 --sd 6 --correlacion 0.6
  python3 tamano_muestral.py --caso correlacion --r 0.40
"""

import argparse
import math
import sys

from scipy import stats

MAX_N = 100000


# ---------------------------------------------------------------- potencias

def potencia_dos_medias(n, d, alfa):
    """Dos medias independientes, n por grupo, d = tamaño de efecto de Cohen."""
    if n < 2:
        return 0.0
    gl = 2 * n - 2
    ncp = d * math.sqrt(n / 2)
    crit = stats.t.ppf(1 - alfa / 2, gl)
    # Simetria: evita NaN de algunas versiones de scipy en cdf(-crit, gl, ncp).
    return stats.nct.sf(crit, gl, ncp) + stats.nct.sf(crit, gl, -ncp)


def potencia_pareadas(n, dz, alfa):
    """Medias pareadas, n = número de pares, dz = efecto sobre las diferencias."""
    if n < 2:
        return 0.0
    gl = n - 1
    ncp = dz * math.sqrt(n)
    crit = stats.t.ppf(1 - alfa / 2, gl)
    return stats.nct.sf(crit, gl, ncp) + stats.nct.sf(crit, gl, -ncp)


def potencia_anova(n, k, f, alfa):
    """ANOVA de una vía, n por grupo, k grupos, f = tamaño de efecto de Cohen."""
    if n < 2:
        return 0.0
    gl1 = k - 1
    gl2 = k * (n - 1)
    lam = f ** 2 * k * n
    crit = stats.f.ppf(1 - alfa, gl1, gl2)
    return stats.ncf.sf(crit, gl1, gl2, lam)


def potencia_proporciones(n, p1, p2, alfa):
    """Dos proporciones independientes, n por grupo, vía transformación arcoseno."""
    if n < 2:
        return 0.0
    h = abs(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))
    if h == 0:
        return 0.0
    z_alfa = stats.norm.ppf(1 - alfa / 2)
    z = h * math.sqrt(n / 2) - z_alfa
    return stats.norm.cdf(z) + stats.norm.cdf(-h * math.sqrt(n / 2) - z_alfa)


def potencia_correlacion(n, r, alfa):
    """Correlación de Pearson contra cero, vía transformación z de Fisher."""
    if n < 4:
        return 0.0
    zr = abs(math.atanh(r))
    z_alfa = stats.norm.ppf(1 - alfa / 2)
    z = zr * math.sqrt(n - 3) - z_alfa
    return stats.norm.cdf(z) + stats.norm.cdf(-zr * math.sqrt(n - 3) - z_alfa)


def buscar_n(funcion_potencia, objetivo, n_min=2):
    """Menor n hasta MAX_N inclusive; requiere potencia monotona creciente."""
    if not math.isfinite(objetivo) or not 0 < objetivo < 1:
        raise ValueError("La potencia objetivo debe estar entre 0 y 1.")
    if not isinstance(n_min, int) or not 2 <= n_min <= MAX_N:
        raise ValueError("n_min debe ser entero entre 2 y MAX_N.")

    def evaluar(n):
        valor = float(funcion_potencia(n))
        if not math.isfinite(valor) or not -1e-12 <= valor <= 1 + 1e-12:
            raise ValueError("Potencia no finita o fuera de [0, 1].")
        return min(1.0, max(0.0, valor))

    lo, hi = n_min, MAX_N
    if evaluar(hi) < objetivo:
        return None, None
    while lo < hi:
        mid = (lo + hi) // 2
        if evaluar(mid) >= objetivo:
            hi = mid
        else:
            lo = mid + 1
    return lo, evaluar(lo)


# ---------------------------------------------------------------- redacción

def parrafo(caso, n_grupo, n_total, grupos, alfa, potencia_real, objetivo, args,
            n_grupo_base=None, n_total_base=None):
    """Párrafo de justificación listo para pegar en la tesis."""
    pot = f"{objetivo * 100:.0f} %"
    sig = f"{alfa:.2f}".replace(".", ",")
    # En el cuerpo del párrafo va el n que sale del cálculo de potencia; el n
    # inflado por pérdidas se menciona aparte para que el tribunal vea las dos cifras.
    n_grupo_base = n_grupo if n_grupo_base is None else n_grupo_base
    n_total_base = n_total if n_total_base is None else n_total_base
    n_grupo, n_total = n_grupo_base, n_total_base

    if caso == "anova":
        base = (
            f"El tamaño de muestra se determinó mediante análisis de potencia para un "
            f"análisis de varianza de una vía con {grupos} tratamientos. Se fijó como "
            f"diferencia mínima de interés {fmt(args.dme)} unidades entre los tratamientos "
            f"extremos, asumiendo un desvío estándar de {fmt(args.sd)} unidades, un nivel "
            f"de significancia de {sig} y una potencia de {pot}. Se supusieron las "
            f"medias restantes en el punto medio de los extremos y grupos iguales. El cálculo arroja "
            f"{n_grupo} repeticiones por tratamiento, esto es {n_total} unidades "
            f"experimentales en total."
        )
    elif caso == "dos-medias":
        base = (
            f"El tamaño de muestra se determinó mediante análisis de potencia para la "
            f"comparación de dos medias independientes. Se estableció como diferencia "
            f"mínima detectable {fmt(args.dme)} unidades, con un desvío estándar de "
            f"{fmt(args.sd)} unidades, un nivel de significancia de {sig} y una potencia "
            f"de {pot}, lo que requiere {n_grupo} unidades por grupo y {n_total} en total."
        )
    elif caso == "medias-pareadas":
        base = (
            f"Se calculó el tamaño de muestra para una comparación de medias pareadas, "
            f"fijando una diferencia mínima de interés de {fmt(args.dme)} unidades sobre "
            f"un desvío estándar de las diferencias de {fmt(args.sd_dif)} unidades, con "
            f"significancia de {sig} y potencia de {pot}. Se requieren {n_total} pares."
        )
    elif caso == "dos-proporciones":
        base = (
            f"El tamaño de muestra se calculó para detectar una diferencia entre "
            f"proporciones de {fmt(args.p1 * 100)} % y {fmt(args.p2 * 100)} %, con un "
            f"nivel de significancia de {sig} y una potencia de {pot}, lo que exige "
            f"{n_grupo} sujetos por grupo y {n_total} en total."
        )
    else:
        base = (
            f"El tamaño de muestra se calculó para detectar una correlación de "
            f"{fmt(args.r)} como significativa, con un nivel de significancia de {sig} "
            f"y una potencia de {pot}, lo que requiere {n_total} observaciones."
        )

    if args.perdidas > 0:
        base += (
            f" Previendo una pérdida de seguimiento del {fmt(args.perdidas)} %, la "
            f"cifra prevista se elevó a {args.n_total_final} "
            f"{'pares' if caso == 'medias-pareadas' else 'unidades'} en total."
        )
        if grupos > 1:
            base += f" Se reclutarán {args.n_grupo_final} unidades por grupo."
    if caso in ("dos-proporciones", "correlacion"):
        base += " El calculo usa una aproximacion normal, no una prueba exacta."
    if args.fuente:
        base += f" La estimación de variabilidad se basa en {args.fuente}."
    else:
        base += (
            " [PENDIENTE: indicar de dónde proviene la estimación de variabilidad, "
            "sea un estudio previo, un ensayo piloto o literatura del área.]"
        )
    return base


def fmt(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


# ---------------------------------------------------------------- principal

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--caso", required=True,
                   choices=["dos-medias", "medias-pareadas", "anova",
                            "dos-proporciones", "correlacion"])
    p.add_argument("--dme", type=float, help="Diferencia mínima de interés, en unidades de la variable")
    p.add_argument("--sd", type=float, help="Desvío estándar dentro de grupo")
    p.add_argument("--sd-dif", type=float, help="Desvío estándar de las diferencias (caso pareado)")
    p.add_argument("--correlacion", type=float, default=None,
                   help="Correlación entre medidas pareadas, para derivar sd-dif desde sd")
    p.add_argument("--grupos", type=int, default=2, help="Número de tratamientos (caso anova)")
    p.add_argument("--p1", type=float, help="Proporción en el grupo control")
    p.add_argument("--p2", type=float, help="Proporción esperada en el grupo tratado")
    p.add_argument("--r", type=float, help="Correlación a detectar")
    p.add_argument("--alfa", type=float, default=0.05)
    p.add_argument("--potencia", type=float, default=0.80)
    p.add_argument("--perdidas", type=float, default=0.0,
                   help="Porcentaje esperado de pérdidas o unidades descartadas")
    p.add_argument("--fuente", type=str, default="",
                   help="De dónde sale la estimación de variabilidad, para la redacción")
    args = p.parse_args()

    for nombre in ("dme", "sd", "sd_dif", "correlacion", "p1", "p2", "r",
                   "alfa", "potencia", "perdidas"):
        valor = getattr(args, nombre)
        if valor is not None and not math.isfinite(valor):
            p.error(f"--{nombre.replace('_', '-')} debe ser finito.")
    if not 0 < args.alfa < args.potencia < 1:
        p.error("Se requiere 0 < alfa < potencia < 1.")
    if not 0 <= args.perdidas < 100:
        p.error("--perdidas debe estar en [0, 100).")
    for nombre in ("dme", "sd", "sd_dif"):
        if getattr(args, nombre) is not None and getattr(args, nombre) <= 0:
            p.error(f"--{nombre.replace('_', '-')} debe ser positivo.")
    if args.grupos < 2:
        p.error("--grupos debe ser al menos 2.")
    if args.correlacion is not None and not -1 <= args.correlacion < 1:
        p.error("--correlacion debe estar en [-1, 1).")
    if args.r is not None and not 0 < abs(args.r) < 1:
        p.error("--r requiere 0 < abs(r) < 1.")
    for nombre in ("p1", "p2"):
        if getattr(args, nombre) is not None and not 0 <= getattr(args, nombre) <= 1:
            p.error(f"--{nombre} debe estar en [0, 1].")
    if args.caso == "dos-proporciones" and args.p1 == args.p2 and args.p1 is not None:
        p.error("--p1 y --p2 deben diferir.")

    caso = args.caso
    k = args.grupos

    if caso == "dos-medias":
        exigir(args, ["dme", "sd"])
        d = args.dme / args.sd
        n, pot = buscar_n(lambda n: potencia_dos_medias(n, d, args.alfa), args.potencia)
        k = 2
        efecto = f"d de Cohen = {d:.3f}"

    elif caso == "medias-pareadas":
        exigir(args, ["dme"])
        if args.sd_dif is None:
            if args.sd is None or args.correlacion is None:
                salir("Falta --sd-dif, o bien --sd junto con --correlacion.")
            rho = args.correlacion
            args.sd_dif = args.sd * math.sqrt(2 * (1 - rho))
        dz = args.dme / args.sd_dif
        n, pot = buscar_n(lambda n: potencia_pareadas(n, dz, args.alfa), args.potencia)
        k = 1
        efecto = f"dz = {dz:.3f} (sd de las diferencias = {args.sd_dif:.3f})"

    elif caso == "anova":
        exigir(args, ["dme", "sd"])
        if k < 2:
            salir("--grupos debe ser 2 o más.")
        # f de Cohen para el escenario de dos medias extremas separadas por dme,
        # con las restantes en el punto medio; no es un supuesto universal.
        f = args.dme / (args.sd * math.sqrt(2 * k))
        n, pot = buscar_n(lambda n: potencia_anova(n, k, f, args.alfa), args.potencia)
        efecto = f"f de Cohen = {f:.3f}"

    elif caso == "dos-proporciones":
        exigir(args, ["p1", "p2"])
        n, pot = buscar_n(lambda n: potencia_proporciones(n, args.p1, args.p2, args.alfa),
                          args.potencia)
        k = 2
        h = abs(2 * math.asin(math.sqrt(args.p1)) - 2 * math.asin(math.sqrt(args.p2)))
        efecto = f"h de Cohen = {h:.3f}"

    else:
        exigir(args, ["r"])
        n, pot = buscar_n(lambda n: potencia_correlacion(n, args.r, args.alfa),
                          args.potencia, n_min=4)
        k = 1
        efecto = f"r = {args.r}"

    if n is None:
        salir("No se alcanza la potencia pedida con un tamaño razonable. "
              "Revisá la diferencia mínima o la variabilidad supuesta.")

    n_grupo, n_total = n, k * n
    n_grupo_base, n_total_base = n_grupo, n_total
    if args.perdidas > 0:
        factor = 1 / (1 - args.perdidas / 100)
        n_grupo = math.ceil(n_grupo * factor)
        n_total = k * n_grupo

    print()
    print("=" * 62)
    print(f"  Caso: {caso}   alfa = {args.alfa}   potencia objetivo = {args.potencia}")
    print("=" * 62)
    print(f"  Tamaño de efecto:        {efecto}")
    if k > 1:
        print(f"  n por grupo:             {n_grupo}")
        print(f"  Grupos:                  {k}")
    print(f"  n total:                 {n_total}")
    print(f"  Potencia (n sin perdidas): {pot:.4f}")
    if args.perdidas > 0:
        print(f"  n antes de pérdidas:     {n_grupo_base} por grupo, {n_total_base} total")
        print(f"  Ajustado por {fmt(args.perdidas)} % de pérdidas previstas")
    print()
    print("-" * 62)
    print("  Párrafo para la tesis")
    print("-" * 62)
    print()
    args.n_grupo_final, args.n_total_final = n_grupo, n_total
    print(parrafo(caso, n_grupo, n_total, k, args.alfa, pot, args.potencia, args,
                  n_grupo_base, n_total_base))
    print()
    print("-" * 62)
    print("  Recordatorio: n se cuenta en unidades experimentales independientes.")
    print("  Las submuestras dentro de una unidad no cuentan como repeticiones.")
    print("-" * 62)
    print()


def exigir(args, campos):
    faltan = [c for c in campos if getattr(args, c.replace("-", "_")) is None]
    if faltan:
        salir("Faltan argumentos: " + ", ".join("--" + c for c in faltan))


def salir(msg):
    print("Error: " + msg, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OverflowError, ZeroDivisionError) as exc:
        salir(str(exc))
