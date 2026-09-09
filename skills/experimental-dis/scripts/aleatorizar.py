#!/usr/bin/env python3
"""
Plan de aleatorización reproducible y croquis de campo, bandeja o secuencia.

La semilla se guarda en la salida. Sin semilla registrada, una aleatorización
no es verificable y el tribunal puede objetarla con razón.

Ejemplos:
  python3 aleatorizar.py --diseno dca --tratamientos T1,T2,T3,T4 --repeticiones 5
  python3 aleatorizar.py --diseno dbca --tratamientos A,B,C --bloques 4 --semilla 2026
  python3 aleatorizar.py --diseno cuadrado-latino --tratamientos A,B,C,D
  python3 aleatorizar.py --diseno factorial --factor "Variedad:V1,V2,V3" \\
      --factor "Dosis:D0,D1" --bloques 3
  python3 aleatorizar.py --diseno parcelas-divididas --principal "Riego:R0,R1" \\
      --subparcela "Variedad:V1,V2,V3" --bloques 3
"""

import argparse
import csv
import itertools
from pathlib import Path
import random
import re
import sys

RESERVADAS = {"unidad", "tratamiento", "bloque", "posicion", "fila", "columna",
              "parcela_grande", "semilla", "respuesta", "sujeto", "tiempo",
              "periodo", "secuencia"}


# ---------------------------------------------------------------- utilidades

def parsear_factor(texto):
    """'Variedad:V1,V2,V3' -> ('Variedad', ['V1','V2','V3'])"""
    if ":" not in texto:
        salir(f"Formato de factor inválido: {texto}. Usá Nombre:nivel1,nivel2")
    nombre, niveles = texto.split(":", 1)
    nombre = nombre.strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", nombre) or nombre in RESERVADAS:
        salir("Nombre de factor invalido o reservado: " + nombre)
    niveles = validar_niveles(niveles)
    return nombre, niveles


def validar_niveles(texto):
    niveles = [n.strip() for n in texto.split(",")]
    if len(niveles) < 2 or any(not n for n in niveles) or len(set(niveles)) != len(niveles):
        salir("Se requieren al menos dos niveles no vacios y distintos.")
    return niveles


def validar_factores(factores):
    nombres = [nombre for nombre, _ in factores]
    if len(set(nombres)) != len(nombres):
        salir("Los nombres de factores deben ser distintos.")
    etiquetas = [" x ".join(c) for c in itertools.product(*(niveles for _, niveles in factores))]
    if len(set(etiquetas)) != len(etiquetas):
        salir("Las etiquetas combinadas son ambiguas; cambie los niveles que contienen ' x '.")


def salir(msg):
    print("Error: " + msg, file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- diseños

def dca(tratamientos, repeticiones, rng):
    unidades = [t for t in tratamientos for _ in range(repeticiones)]
    rng.shuffle(unidades)
    return [{"unidad": i + 1, "tratamiento": t} for i, t in enumerate(unidades)]


def dbca(tratamientos, bloques, rng):
    filas = []
    unidad = 1
    for b in range(1, bloques + 1):
        orden = tratamientos[:]
        rng.shuffle(orden)
        for pos, t in enumerate(orden, start=1):
            filas.append({"unidad": unidad, "bloque": b, "posicion": pos,
                          "tratamiento": t})
            unidad += 1
    return filas


def cuadrado_latino(tratamientos, rng):
    t = len(tratamientos)
    base = list(range(t))
    cuadrado = [[base[(i + j) % t] for j in range(t)] for i in range(t)]
    rng.shuffle(cuadrado)
    cols = list(range(t))
    rng.shuffle(cols)
    cuadrado = [[fila[c] for c in cols] for fila in cuadrado]
    etiquetas = tratamientos[:]
    rng.shuffle(etiquetas)
    filas = []
    unidad = 1
    for i, fila in enumerate(cuadrado, start=1):
        for j, idx in enumerate(fila, start=1):
            filas.append({"unidad": unidad, "fila": i, "columna": j,
                          "tratamiento": etiquetas[idx]})
            unidad += 1
    return filas


def factorial(factores, bloques, repeticiones, rng):
    validar_factores(factores)
    nombres = [f[0] for f in factores]
    combos = list(itertools.product(*[f[1] for f in factores]))
    etiquetas = ["".join(c) if len(c) == 1 else " x ".join(c) for c in combos]

    if bloques:
        filas = dbca(etiquetas, bloques, rng)
    else:
        filas = dca(etiquetas, repeticiones, rng)

    mapa = dict(zip(etiquetas, combos))
    for f in filas:
        for nombre, nivel in zip(nombres, mapa[f["tratamiento"]]):
            f[nombre] = nivel
    return filas


def parcelas_divididas(principal, subparcela, bloques, rng):
    validar_factores([principal, subparcela])
    nom_p, niv_p = principal
    nom_s, niv_s = subparcela
    filas = []
    unidad = 1
    parcela_grande = 1
    for b in range(1, bloques + 1):
        orden_p = niv_p[:]
        rng.shuffle(orden_p)
        for p in orden_p:
            orden_s = niv_s[:]
            rng.shuffle(orden_s)
            for pos, s in enumerate(orden_s, start=1):
                filas.append({
                    "unidad": unidad,
                    "bloque": b,
                    "parcela_grande": parcela_grande,
                    "posicion": pos,
                    nom_p: p,
                    nom_s: s,
                    "tratamiento": f"{p} x {s}",
                })
                unidad += 1
            parcela_grande += 1
    return filas


# ---------------------------------------------------------------- croquis

def dibujar(filas, diseno, ruta, semilla):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Aviso: matplotlib no está disponible, se omite el croquis.")
        return

    if diseno == "cuadrado-latino":
        n_filas = max(f["fila"] for f in filas)
        n_cols = max(f["columna"] for f in filas)
        celdas = {(f["fila"], f["columna"]): f["tratamiento"] for f in filas}
        etiq_fila = [f"Fila {i}" for i in range(1, n_filas + 1)]
        etiq_col = [f"Col {j}" for j in range(1, n_cols + 1)]
    elif diseno == "parcelas-divididas":
        parcelas = list(dict.fromkeys(f["parcela_grande"] for f in filas))
        indice = {parcela: i + 1 for i, parcela in enumerate(parcelas)}
        n_filas = len(parcelas)
        n_cols = max(f["posicion"] for f in filas)
        celdas = {(indice[f["parcela_grande"]], f["posicion"]): f["tratamiento"]
                  for f in filas}
        bloques = {f["parcela_grande"]: f["bloque"] for f in filas}
        etiq_fila = [f"Bloque {bloques[pg]} / PG {pg}" for pg in parcelas]
        etiq_col = [f"Sub {j}" for j in range(1, n_cols + 1)]
    elif "bloque" in filas[0]:
        n_filas = max(f["bloque"] for f in filas)
        n_cols = max(f["posicion"] for f in filas)
        celdas = {(f["bloque"], f["posicion"]): f["tratamiento"] for f in filas}
        etiq_fila = [f"Bloque {i}" for i in range(1, n_filas + 1)]
        etiq_col = [f"{j}" for j in range(1, n_cols + 1)]
    else:
        total = len(filas)
        n_cols = min(6, total)
        n_filas = (total + n_cols - 1) // n_cols
        celdas = {}
        for idx, f in enumerate(filas):
            celdas[(idx // n_cols + 1, idx % n_cols + 1)] = f["tratamiento"]
        etiq_fila = [f"" for _ in range(n_filas)]
        etiq_col = [f"{j}" for j in range(1, n_cols + 1)]

    tratamientos = sorted({f["tratamiento"] for f in filas})
    cmap = plt.get_cmap("Pastel1" if len(tratamientos) <= 9 else "tab20")
    color = {t: cmap(i % cmap.N) for i, t in enumerate(tratamientos)}

    fig, ax = plt.subplots(figsize=(max(6, n_cols * 1.5), max(3, n_filas * 1.1)))
    for (i, j), t in celdas.items():
        ax.add_patch(plt.Rectangle((j - 1, n_filas - i), 1, 1,
                                   facecolor=color[t], edgecolor="black", lw=0.8))
        ax.text(j - 0.5, n_filas - i + 0.5, t, ha="center", va="center", fontsize=9)

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_filas)
    ax.set_xticks([j + 0.5 for j in range(n_cols)])
    ax.set_xticklabels(etiq_col, fontsize=8)
    ax.set_yticks([n_filas - i - 0.5 for i in range(n_filas)])
    ax.set_yticklabels(etiq_fila, fontsize=8)
    ax.set_aspect("equal")
    for lado in ax.spines.values():
        lado.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(f"Croquis de aleatorización, diseño {diseno} (semilla {semilla})",
                 fontsize=10, pad=12)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    print(f"Croquis guardado en {ruta}")


# ---------------------------------------------------------------- principal

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--diseno", required=True,
                   choices=["dca", "dbca", "cuadrado-latino", "factorial",
                            "parcelas-divididas"])
    p.add_argument("--tratamientos", help="Lista separada por comas")
    p.add_argument("--factor", action="append", default=[],
                   help="Nombre:nivel1,nivel2 (repetible, para factorial)")
    p.add_argument("--principal", help="Nombre:nivel1,nivel2 de la parcela grande")
    p.add_argument("--subparcela", help="Nombre:nivel1,nivel2 de la subparcela")
    p.add_argument("--repeticiones", type=int, help="Por tratamiento en DCA/factorial sin bloques (defecto: 3)")
    p.add_argument("--bloques", type=int)
    p.add_argument("--semilla", type=int, default=None)
    p.add_argument("--salida", default="plan_aleatorizacion.csv")
    p.add_argument("--croquis", default=None)
    args = p.parse_args()
    permitidos = {
        "dca": {"tratamientos", "repeticiones"},
        "dbca": {"tratamientos", "bloques"},
        "cuadrado-latino": {"tratamientos"},
        "factorial": {"factor", "bloques", "repeticiones"},
        "parcelas-divididas": {"principal", "subparcela", "bloques"},
    }
    for nombre in ("tratamientos", "factor", "principal", "subparcela", "bloques", "repeticiones"):
        valor = getattr(args, nombre)
        if valor is not None and valor != [] and nombre not in permitidos[args.diseno]:
            p.error(f"--{nombre} no aplica a {args.diseno}.")
    if args.bloques is not None and args.repeticiones is not None:
        p.error("Con bloques hay una repeticion por combinacion y bloque; no use --repeticiones.")
    if args.repeticiones is not None and args.repeticiones < 1:
        p.error("--repeticiones debe ser positivo.")
    args.repeticiones = 3 if args.repeticiones is None else args.repeticiones
    if args.bloques is not None and args.bloques < 1:
        p.error("--bloques debe ser positivo.")
    if args.croquis and Path(args.salida).resolve() == Path(args.croquis).resolve():
        p.error("CSV y croquis deben tener rutas distintas.")

    semilla = args.semilla if args.semilla is not None else random.randrange(1, 10 ** 6)
    rng = random.Random(semilla)

    if args.diseno in ("dca", "dbca", "cuadrado-latino"):
        if not args.tratamientos:
            salir("Falta --tratamientos.")
        trat = validar_niveles(args.tratamientos)

    if args.diseno == "dca":
        filas = dca(trat, args.repeticiones, rng)
    elif args.diseno == "dbca":
        if not args.bloques:
            salir("Falta --bloques.")
        filas = dbca(trat, args.bloques, rng)
    elif args.diseno == "cuadrado-latino":
        filas = cuadrado_latino(trat, rng)
    elif args.diseno == "factorial":
        if len(args.factor) < 2:
            salir("Un factorial necesita al menos dos --factor.")
        factores = [parsear_factor(f) for f in args.factor]
        filas = factorial(factores, args.bloques, args.repeticiones, rng)
    else:
        if not (args.principal and args.subparcela):
            salir("Parcelas divididas necesita --principal y --subparcela.")
        if not args.bloques:
            salir("Falta --bloques.")
        filas = parcelas_divididas(parsear_factor(args.principal),
                                   parsear_factor(args.subparcela),
                                   args.bloques, rng)

    columnas = []
    for f in filas:
        f["semilla"] = semilla
        f["respuesta"] = ""
        for c in f:
            if c not in columnas:
                columnas.append(c)

    with open(args.salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas)
        w.writeheader()
        w.writerows(filas)

    print()
    print("=" * 62)
    print(f"  Diseño: {args.diseno}")
    print(f"  Semilla: {semilla}   (anotala, sin ella el plan no es reproducible)")
    print(f"  Unidades experimentales: {len(filas)}")
    print("=" * 62)
    print()
    for f in filas[:12]:
        print("  " + "  ".join(f"{c}={f[c]}" for c in columnas))
    if len(filas) > 12:
        print(f"  ... {len(filas) - 12} filas más en {args.salida}")
    print()
    print(f"Plan guardado en {args.salida}")

    if args.croquis:
        dibujar(filas, args.diseno, args.croquis, semilla)

    print()
    print("Frase para la tesis:")
    print(f"  La asignación de los tratamientos a las unidades experimentales se "
          f"realizó de forma aleatoria mediante un generador de números "
          f"pseudoaleatorios con semilla {semilla}, cuyo plan completo se presenta "
          f"en el anexo correspondiente.")
    print()


if __name__ == "__main__":
    try:
        main()
    except OSError as exc:
        salir(str(exc))
