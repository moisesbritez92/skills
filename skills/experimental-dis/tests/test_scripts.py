import ast
import contextlib
import csv
import importlib.util
import io
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import aleatorizar as az
import esqueleto_analisis as ea
import tamano_muestral as tm


def cli(script, *args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"})


class TamanoTests(unittest.TestCase):
    def test_referencia_y_minimalidad(self):
        n, potencia = tm.buscar_n(lambda n: tm.potencia_dos_medias(n, .5, .05), .8)
        self.assertEqual(n, 64)
        self.assertGreaterEqual(potencia, .8)
        casos = [lambda n: tm.potencia_pareadas(n, .5, .05),
                 lambda n: tm.potencia_anova(n, 4, .25, .05),
                 lambda n: tm.potencia_proporciones(n, .3, .55, .05),
                 lambda n: tm.potencia_correlacion(n, .4, .05)]
        for f in casos:
            n, potencia = tm.buscar_n(f, .8, n_min=4)
            self.assertGreaterEqual(potencia, .8)
            self.assertLess(f(n - 1), .8)

    def test_limite_y_no_alcanzable(self):
        with patch.object(tm, "MAX_N", 10):
            self.assertEqual(tm.buscar_n(lambda n: .8 if n == 10 else .1, .8), (10, .8))
            self.assertEqual(tm.buscar_n(lambda n: .1, .8), (None, None))
        with self.assertRaises(ValueError):
            tm.buscar_n(lambda n: float("nan"), .8)
        self.assertEqual(tm.buscar_n(lambda n: 1 + 1e-15, .8), (2, 1))
        with self.assertRaises(ValueError):
            tm.buscar_n(lambda n: 1.1, .8)

    def test_none_antes_de_operar_todos_los_casos(self):
        casos = [("dos-medias", "--dme", "1", "--sd", "1"),
                 ("anova", "--dme", "1", "--sd", "1"),
                 ("medias-pareadas", "--dme", "1", "--sd-dif", "1"),
                 ("dos-proporciones", "--p1", ".1", "--p2", ".2"),
                 ("correlacion", "--r", ".2")]
        for caso in casos:
            with self.subTest(caso=caso), patch.object(tm, "buscar_n", return_value=(None, None)), \
                    patch.object(sys, "argv", ["tm", "--caso", *caso]), \
                    contextlib.redirect_stderr(io.StringIO()) as error:
                with self.assertRaises(SystemExit):
                    tm.main()
                self.assertIn("No se alcanza", error.getvalue())

    def test_perdidas_balanceadas_y_pareadas(self):
        for caso, extra, k in [("dos-medias", ["--dme", "1", "--sd", "1"], 2),
                               ("anova", ["--dme", "1", "--sd", "1", "--grupos", "3"], 3),
                               ("medias-pareadas", ["--dme", "1", "--sd-dif", "1"], 1)]:
            with patch.object(tm, "buscar_n", return_value=(7, .81)), \
                    patch.object(sys, "argv", ["tm", "--caso", caso, *extra, "--perdidas", "10"]), \
                    contextlib.redirect_stdout(io.StringIO()) as salida:
                tm.main()
            self.assertRegex(salida.getvalue(), rf"n total:\s+{8 * k}\b")
            if k == 1:
                self.assertIn("8 pares en total", salida.getvalue())

    def test_inputs_invalidos(self):
        base = ["--caso", "dos-medias", "--dme", "1", "--sd", "1"]
        for extra in [("--sd", "0"), ("--sd", "nan"), ("--dme", "inf"),
                      ("--dme", "-1"), ("--perdidas", "100"), ("--perdidas", "-1"),
                      ("--alfa", "1"), ("--potencia", ".01"), ("--grupos", "0"),
                      ("--correlacion", "1"), ("--r", "0"), ("--p1", "1.1")]:
            with self.subTest(extra=extra), patch.object(sys, "argv", ["tm", *base, *extra]), \
                    contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    tm.main()
        for args in [("medias-pareadas", "--dme", "1", "--sd", "2"),
                     ("dos-proporciones", "--p1", ".3", "--p2", ".3")]:
            resultado = cli("tamano_muestral.py", "--caso", *args)
            self.assertNotEqual(resultado.returncode, 0)
            self.assertNotIn("Traceback", resultado.stderr)


class AleatorizarTests(unittest.TestCase):
    def test_validacion_factores(self):
        for texto in ["A:a,a", "A:a,", ":a,b", "bloque:a,b", "A B:a,b", "A:a,,b", "sin-dos-puntos"]:
            with self.subTest(texto=texto), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    az.parsear_factor(texto)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            az.factorial([("A", ["1", "2"]), ("A", ["3", "4"])], 2, 3, random.Random(1))
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            az.factorial([("A", ["a", "a x b"]), ("B", ["b x c", "c"])], 2, 3, random.Random(1))

    def test_planes(self):
        tratamientos = ["A", "B", "C"]
        filas = az.dca(tratamientos, 3, random.Random(1))
        self.assertEqual(len(filas), 9)
        self.assertTrue(all(sum(f["tratamiento"] == t for f in filas) == 3 for t in tratamientos))
        filas = az.dbca(tratamientos, 4, random.Random(1))
        for b in range(1, 5):
            self.assertEqual({f["tratamiento"] for f in filas if f["bloque"] == b}, set(tratamientos))
        filas = az.cuadrado_latino(tratamientos, random.Random(1))
        for campo in ("fila", "columna"):
            for i in range(1, 4):
                self.assertEqual({f["tratamiento"] for f in filas if f[campo] == i}, set(tratamientos))

    def test_csv_semilla_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            opciones = ["--diseno", "factorial", "--factor", "Variedad:V1,V2",
                        "--factor", "Dosis:D0,D1", "--bloques", "3"]
            a = cli("aleatorizar.py", *opciones, cwd=tmp)
            self.assertEqual(a.returncode, 0, a.stderr)
            ruta = Path(tmp) / "plan_aleatorizacion.csv"
            with ruta.open(encoding="utf-8", newline="") as fh:
                filas = list(csv.DictReader(fh))
            semilla = filas[0]["semilla"]
            self.assertTrue(all(f["semilla"] == semilla and f["respuesta"] == "" for f in filas))
            b = cli("aleatorizar.py", *opciones, "--semilla", semilla, "--salida", "otro.csv", cwd=tmp)
            self.assertEqual(b.returncode, 0, b.stderr)
            self.assertEqual(ruta.read_bytes(), (Path(tmp) / "otro.csv").read_bytes())

    def test_cli_invalida(self):
        for extra in [("--repeticiones", "0"), ("--bloques", "-1"),
                      ("--tratamientos", "A,A"), ("--tratamientos", "A,,B")]:
            with tempfile.TemporaryDirectory() as tmp:
                result = cli("aleatorizar.py", "--diseno", "dca", "--tratamientos", "A,B", *extra, cwd=tmp)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse((Path(tmp) / "plan_aleatorizacion.csv").exists())

    def test_croquis_splitplot_no_pierde_celdas(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        filas = az.parcelas_divididas(("Riego", ["R0", "R1"]),
                                     ("Variedad", ["V1", "V2", "V3"]), 3, random.Random(2))
        self.assertEqual(len(filas), 18)
        fig, ax = plt.subplots()
        with patch.object(plt, "subplots", return_value=(fig, ax)), \
                patch.object(fig, "savefig"), contextlib.redirect_stdout(io.StringIO()):
            az.dibujar(filas, "parcelas-divididas", "no-escribir.png", 2)
        self.assertEqual(len(ax.patches), len(filas))
        self.assertEqual(len({tuple(p.get_xy()) for p in ax.patches}), len(filas))
        self.assertFalse(plt.fignum_exists(fig.number))


class EsqueletoTests(unittest.TestCase):
    def test_sintaxis_python_y_modelos_r(self):
        for diseno in ea.DISENOS:
            with self.subTest(diseno=diseno):
                texto = ea.generar(diseno, "python", "datos con espacio/'ensayo.csv")
                ast.parse(texto)
                compile(texto, "analisis.py", "exec")
                r = ea.generar(diseno, "r")
                self.assertIn('DATOS <- "plan_aleatorizacion.csv"', r)
                self.assertIn("Error(bloque/parcela_grande)", r)
                self.assertIn("random= ~1|sujeto", r)
                self.assertIn("respuesta ~ sujeto + periodo + tratamiento", r)
                self.assertIn("inferencia de efectos fijos no implementada", r)
        with self.assertRaises(ValueError):
            ea.generar("otro", "r")

    def test_cli_y_no_sobrescribir(self):
        with tempfile.TemporaryDirectory() as tmp:
            for lenguaje, extension in [("Python", "py"), ("R", "R")]:
                ruta = Path(tmp) / ("analisis." + extension)
                args = ["--diseno", "dca", "--lenguaje", lenguaje, "--salida", ruta]
                result = cli("esqueleto_analisis.py", *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                original = ruta.read_bytes()
                self.assertNotEqual(cli("esqueleto_analisis.py", *args).returncode, 0)
                self.assertEqual(original, ruta.read_bytes())

    @unittest.skipUnless(all(importlib.util.find_spec(m) for m in ("pandas", "numpy", "statsmodels")),
                         "Ejecucion opcional requiere pandas, numpy y statsmodels")
    def test_ejecutar_python_con_csv_aleatorizar(self):
        casos = [("dca", ["--tratamientos", "A,B,C"]),
                 ("dbca", ["--tratamientos", "A,B,C", "--bloques", "4"]),
                 ("cuadrado-latino", ["--tratamientos", "A,B,C,D"]),
                 ("factorial", ["--factor", "Variedad:V1,V2", "--factor", "Dosis:D0,D1"]),
                 ("factorial", ["--factor", "Variedad:V1,V2", "--factor", "Dosis:D0,D1", "--bloques", "4"]),
                 ("parcelas-divididas", ["--principal", "Riego:R0,R1", "--subparcela", "Variedad:V1,V2,V3", "--bloques", "12"])]
        for diseno, opciones in casos:
            with self.subTest(diseno=diseno, opciones=opciones), tempfile.TemporaryDirectory() as tmp:
                result = cli("aleatorizar.py", "--diseno", diseno, *opciones, "--semilla", "42", cwd=tmp)
                self.assertEqual(result.returncode, 0, result.stderr)
                ruta = Path(tmp) / "plan_aleatorizacion.csv"
                with ruta.open(encoding="utf-8", newline="") as fh:
                    filas = list(csv.DictReader(fh))
                rng = random.Random(42)
                bloque = {f.get("bloque"): rng.gauss(0, 3) for f in filas}
                pg = {f.get("parcela_grande"): rng.gauss(0, 2) for f in filas}
                for f in filas:
                    f["respuesta"] = str(10 + bloque[f.get("bloque")] + pg[f.get("parcela_grande")] + rng.gauss(0, 1))
                with ruta.open("w", encoding="utf-8", newline="") as fh:
                    w = csv.DictWriter(fh, filas[0].keys())
                    w.writeheader()
                    w.writerows(filas)
                script = Path(tmp) / "analisis.py"
                script.write_text(ea.generar(diseno, "python"), encoding="utf-8")
                result = subprocess.run([sys.executable, str(script)], cwd=SCRIPTS, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("SOLO ESTIMACION" if diseno == "parcelas-divididas" else "PR(>F)", result.stdout)
                filas[0]["respuesta"] = ""
                with ruta.open("w", encoding="utf-8", newline="") as fh:
                    w = csv.DictWriter(fh, filas[0].keys())
                    w.writeheader()
                    w.writerows(filas)
                result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Complete", result.stderr)

    @unittest.skipUnless(all(importlib.util.find_spec(m) for m in ("pandas", "numpy", "statsmodels")),
                         "Ejecucion opcional requiere pandas, numpy y statsmodels")
    def test_longitudinales_y_agrupacion_invalida(self):
        rng = random.Random(17)
        repetidas = []
        cruzado = []
        for sujeto in range(24):
            grupo = "A" if sujeto < 12 else "B"
            intercepto = rng.gauss(0, 3)
            for tiempo in range(3):
                repetidas.append(dict(sujeto=str(sujeto), tratamiento=grupo, tiempo=str(tiempo),
                                      respuesta=str(10 + intercepto + tiempo + rng.gauss(0, 1))))
            secuencia = "AB" if sujeto < 12 else "BA"
            for periodo, tratamiento in enumerate(secuencia, 1):
                cruzado.append(dict(sujeto=str(sujeto), secuencia=secuencia, periodo=str(periodo),
                                    tratamiento=tratamiento,
                                    respuesta=str(10 + intercepto + periodo + rng.gauss(0, 1))))
        split = az.parcelas_divididas(("Riego", ["R0", "R1"]),
                                     ("Variedad", ["V0", "V1"]), 4, rng)
        for f in split:
            f["respuesta"] = str(rng.gauss(10, 1))

        for diseno, filas in [("medidas-repetidas", repetidas), ("cruzado", cruzado),
                              ("parcelas-divididas", split)]:
            with self.subTest(diseno=diseno), tempfile.TemporaryDirectory() as tmp:
                ruta = Path(tmp) / "plan_aleatorizacion.csv"
                script = Path(tmp) / "analisis.py"
                script.write_text(ea.generar(diseno, "python"), encoding="utf-8")

                def ejecutar():
                    with ruta.open("w", encoding="utf-8", newline="") as fh:
                        w = csv.DictWriter(fh, filas[0].keys())
                        w.writeheader()
                        w.writerows(filas)
                    return subprocess.run([sys.executable, str(script)], capture_output=True, text=True)

                if diseno != "parcelas-divididas":
                    result = ejecutar()
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("SOLO ESTIMACION" if diseno == "medidas-repetidas" else "PR(>F)", result.stdout)
                if diseno == "medidas-repetidas":
                    filas[0]["tratamiento"] = "B"
                    mensaje = "constante dentro del sujeto"
                elif diseno == "cruzado":
                    filas[0]["tratamiento"] = "B"
                    mensaje = "Secuencias deben concordar"
                else:
                    filas[-1]["parcela_grande"] = filas[0]["parcela_grande"]
                    mensaje = "globalmente unica"
                result = ejecutar()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(mensaje, result.stderr)


if __name__ == "__main__":
    unittest.main()
