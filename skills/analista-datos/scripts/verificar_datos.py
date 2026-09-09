#!/usr/bin/env python3
"""
Auditoría de la planilla de datos contra el protocolo del diseño.

Se corre siempre antes de ajustar cualquier modelo. Su trabajo principal es
determinar el n verdadero, en unidades experimentales, y avisar cuando la
planilla trae submuestras que el software contaría como repeticiones.

Ejemplos:
  python3 verificar_datos.py datos.csv --protocolo diseno.json
  python3 verificar_datos.py datos.csv --protocolo diseno.json --respuesta rendimiento
  python3 verificar_datos.py datos.csv --unidad parcela --tratamiento variedad --bloque bloque
"""

import argparse
import json
import sys

import pandas as pd


VERDE, AMARILLO, ROJO = "OK   ", "AVISO", "GRAVE"


class Auditoria:
    def __init__(self):
        self.hallazgos = []

    def add(self, nivel, titulo, detalle=""):
        self.hallazgos.append((nivel, titulo, detalle))

    @property
    def graves(self):
        return [h for h in self.hallazgos if h[0] == ROJO]

    def imprimir(self):
        print()
        print("=" * 70)
        print("  AUDITORÍA DE DATOS")
        print("=" * 70)
        for nivel, titulo, detalle in self.hallazgos:
            print(f"  [{nivel}] {titulo}")
            for linea in str(detalle).splitlines():
                if linea.strip():
                    print(f"          {linea}")
        print("=" * 70)
        if self.graves:
            print(f"  {len(self.graves)} hallazgo(s) grave(s). No ajustes ningún modelo")
            print("  hasta resolverlos o hasta decidir explícitamente cómo tratarlos.")
        else:
            print("  Sin hallazgos graves. Se puede pasar al análisis.")
        print("=" * 70)
        print()


def cargar_protocolo(ruta):
    if not ruta:
        return {}
    try:
        with open(ruta, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        print(f"Error: no se encontró el protocolo {ruta}.", file=sys.stderr)
        print("Reconstruilo con el usuario antes de seguir, o pasá las columnas "
              "a mano con --unidad, --tratamiento y --bloque.", file=sys.stderr)
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("datos")
    p.add_argument("--protocolo", default=None)
    p.add_argument("--plan", default=None, help="plan_aleatorizacion.csv, para cotejar unidades faltantes")
    p.add_argument("--unidad", default=None)
    p.add_argument("--tratamiento", default=None)
    p.add_argument("--bloque", default=None)
    p.add_argument("--respuesta", action="append", default=[])
    args = p.parse_args()

    prot = cargar_protocolo(args.protocolo)
    aud = Auditoria()

    try:
        df = pd.read_csv(args.datos)
    except Exception as e:
        print(f"Error al leer {args.datos}: {e}", file=sys.stderr)
        sys.exit(1)

    col_unidad = args.unidad or ("unidad" if "unidad" in df.columns else None)
    col_trat = args.tratamiento or ("tratamiento" if "tratamiento" in df.columns else None)
    col_bloque = args.bloque or ("bloque" if "bloque" in df.columns else None)
    respuestas = args.respuesta or [r["nombre"] for r in prot.get("respuestas", [])]

    print(f"\nArchivo: {args.datos}   filas: {len(df)}   columnas: {len(df.columns)}")
    if prot:
        print(f"Protocolo: diseño {prot.get('diseno')}, "
              f"{prot.get('n_unidades')} unidades previstas, "
              f"{prot.get('submuestras_por_unidad', 1)} submuestra(s) por unidad")

    # --- columnas esperadas
    esperadas = prot.get("columnas_estructura", [])
    faltan = [c for c in esperadas if c not in df.columns]
    if faltan:
        aud.add(ROJO, "Faltan columnas que declara el protocolo",
                ", ".join(faltan))

    if col_trat is None:
        aud.add(ROJO, "No se identificó la columna de tratamiento",
                "Pasala con --tratamiento.")
        aud.imprimir()
        sys.exit(1)

    # --- n verdadero y submuestreo
    submuestras_decl = int(prot.get("submuestras_por_unidad", 1) or 1)
    if col_unidad and col_unidad in df.columns:
        n_unidades = df[col_unidad].nunique()
        filas_por_unidad = df.groupby(col_unidad).size()
        maximo = int(filas_por_unidad.max())
        detalle = (f"Filas en la planilla: {len(df)}\n"
                   f"Unidades experimentales distintas: {n_unidades}\n"
                   f"n VERDADERO para el análisis: {n_unidades}")
        if maximo > 1:
            aud.add(AMARILLO, "La planilla contiene submuestras", detalle +
                    f"\nHasta {maximo} filas por unidad. Promediá por unidad, o modelá "
                    f"la submuestra como término anidado, pero no dejes que el software "
                    f"cuente {len(df)} observaciones independientes.")
        else:
            aud.add(VERDE, "Una fila por unidad experimental", detalle)

        if filas_por_unidad.nunique() > 1:
            habitual = int(filas_por_unidad.mode().iloc[0])
            incompletas = filas_por_unidad[filas_por_unidad < habitual]
            excedidas = filas_por_unidad[filas_por_unidad > habitual]
            partes = []
            if len(incompletas):
                partes.append(f"{len(incompletas)} unidad(es) con menos de {habitual} "
                              f"filas: {list(incompletas.index)[:10]}")
            if len(excedidas):
                partes.append(f"{len(excedidas)} unidad(es) con más de {habitual} "
                              f"filas: {list(excedidas.index)[:10]}. Suele ser carga repetida.")
            aud.add(AMARILLO, f"Número desigual de mediciones por unidad "
                              f"(lo habitual son {habitual})", "\n".join(partes))

        habitual_gen = int(filas_por_unidad.mode().iloc[0])
        if submuestras_decl > 1 and habitual_gen != submuestras_decl:
            aud.add(AMARILLO, "Las submuestras no coinciden con lo declarado",
                    f"El protocolo declara {submuestras_decl} por unidad, la planilla "
                    f"tiene {habitual_gen} como valor habitual y hasta {maximo}.")

        n_prev = prot.get("n_unidades")
        if n_prev and n_unidades != n_prev:
            nivel = ROJO if n_unidades < n_prev * 0.9 else AMARILLO
            aud.add(nivel, "El número de unidades no coincide con el plan",
                    f"Previstas {n_prev}, presentes {n_unidades}. "
                    f"Registrá las pérdidas como desviación del protocolo.")
    else:
        aud.add(AMARILLO, "No hay columna de unidad experimental",
                "Sin ella no se puede verificar el n real ni detectar submuestreo. "
                "Confirmá con el usuario que cada fila es una unidad independiente.")

    # --- balance por tratamiento
    conteo = df.groupby(col_trat).size()
    if col_unidad and col_unidad in df.columns:
        conteo = df.groupby(col_trat)[col_unidad].nunique()
    detalle = "\n".join(f"{t}: {n}" for t, n in conteo.items())
    if conteo.nunique() == 1:
        aud.add(VERDE, f"Diseño balanceado, {int(conteo.iloc[0])} repeticiones por tratamiento",
                detalle)
    else:
        aud.add(AMARILLO, "Diseño desbalanceado", detalle +
                "\nUsá suma de cuadrados de tipo II o III y decilo en la tesis.")
    if conteo.min() < 2:
        aud.add(ROJO, "Hay tratamientos con una sola repetición",
                "Sin repetición no se puede estimar el error experimental.")

    # --- estructura de bloques
    if col_bloque and col_bloque in df.columns:
        tabla = df.pivot_table(index=col_bloque, columns=col_trat,
                               values=respuestas[0] if respuestas and respuestas[0] in df.columns
                               else df.columns[0], aggfunc="count", fill_value=0)
        vacias = (tabla == 0).sum().sum()
        if vacias:
            aud.add(ROJO, "Bloques incompletos",
                    f"{vacias} combinación(es) de bloque y tratamiento sin datos. "
                    f"El ANOVA de bloques completos no aplica.")
        else:
            aud.add(VERDE, f"Bloques completos, {df[col_bloque].nunique()} bloques", "")

    # --- cruce factorial
    factores = [f for f in prot.get("factores", []) if f in df.columns]
    if len(factores) >= 2:
        cruce = df.groupby(factores).size()
        niveles = 1
        for f in factores:
            niveles *= df[f].nunique()
        if len(cruce) < niveles:
            aud.add(ROJO, "Cruce factorial incompleto",
                    f"Se esperaban {niveles} combinaciones y hay {len(cruce)}. "
                    f"Sin todas las celdas no se puede estimar la interacción.")
        else:
            aud.add(VERDE, f"Cruce factorial completo, {niveles} combinaciones", "")

    # --- respuestas
    for r in respuestas:
        if r not in df.columns:
            aud.add(ROJO, f"No está la columna de respuesta '{r}'", "")
            continue
        serie = pd.to_numeric(df[r], errors="coerce")
        no_numericos = serie.isna() & df[r].notna()
        faltantes = df[r].isna().sum()
        if no_numericos.any():
            ejemplos = df.loc[no_numericos, r].unique()[:5]
            aud.add(ROJO, f"Valores no numéricos en '{r}'",
                    f"{int(no_numericos.sum())} celda(s). Ejemplos: {list(ejemplos)}. "
                    f"Suele ser coma decimal, texto o unidades escritas en la celda.")
        if faltantes:
            pct = 100 * faltantes / len(df)
            nivel = ROJO if pct > 10 else AMARILLO
            aud.add(nivel, f"Datos faltantes en '{r}'",
                    f"{faltantes} de {len(df)} ({pct:.1f} %). Decidí y declará "
                    f"cómo se tratan antes de analizar.")
        if serie.notna().sum() > 2:
            aud.add(VERDE, f"Respuesta '{r}'",
                    f"n = {int(serie.notna().sum())} valores, "
                    f"media {serie.mean():.3f}, sd {serie.std():.3f}, "
                    f"rango {serie.min():.3f} a {serie.max():.3f}")
            if (serie < 0).any() and prot:
                tipo = next((x["tipo"] for x in prot.get("respuestas", [])
                             if x["nombre"] == r), "")
                if tipo in ("conteo", "proporcion", "binaria", "tiempo"):
                    aud.add(ROJO, f"Valores negativos en una variable de tipo {tipo}", "")

    # --- duplicados
    claves = [c for c in [col_unidad, "submuestra"] if c and c in df.columns]
    if claves:
        dup = df.duplicated(subset=claves).sum()
        if dup:
            aud.add(ROJO, "Filas duplicadas",
                    f"{dup} fila(s) repiten la combinación {claves}.")

    # --- cotejo con el plan
    if args.plan and col_unidad:
        try:
            plan = pd.read_csv(args.plan)
            faltantes = set(plan[col_unidad]) - set(df[col_unidad])
            if faltantes:
                aud.add(AMARILLO, "Unidades del plan que no aparecen en los datos",
                        f"{len(faltantes)}: {sorted(faltantes)[:15]}")
        except Exception as e:
            aud.add(AMARILLO, "No se pudo cotejar con el plan", str(e))

    aud.imprimir()
    sys.exit(2 if aud.graves else 0)


if __name__ == "__main__":
    main()
