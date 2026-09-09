# skills

Colección de [Agent Skills](https://agentskills.io/) instalables con la CLI [`npx skills`](https://skills.sh/).

## Instalación global

```bash
# Instala todas las skills del repo, disponibles en cualquier proyecto
npx skills add moisesbritez92/skills -g -y

# Instala solo una skill concreta (p. ej. redactor-tesis)
npx skills add moisesbritez92/skills -g --skill redactor-tesis -y
```

El flag `-g` instala en el directorio global del agente (por ejemplo `~/.claude/skills/`,
`~/.codex/skills/` o `~/.copilot/skills/` según el agente detectado), quedando disponible en
cualquier proyecto sin necesidad de repetir la instalación.

## Skills disponibles

- [`skills/redactor-tesis`](skills/redactor-tesis/SKILL.md): redacción y revisión de texto
  académico (TFM, TFG, tesis, papers, memorias).
- [`skills/redactor-anteproyecto`](skills/redactor-anteproyecto/SKILL.md): redacción y revisión de
  anteproyectos, protocolos de investigación y proyectos finales de grado según la NP 62 001 18
  y el formato de la FCyT UNCA.
- [`skills/experimental-dis`](skills/experimental-dis/SKILL.md): diseño experimental, potencia
  estadística, aleatorización y plan de análisis para investigaciones y tesis.
- [`skills/analista-datos`](skills/analista-datos/SKILL.md): auditoría y análisis de datos
  experimentales, con resultados, tablas y figuras para tesis e investigaciones.

## Diseño experimental

`experimental-dis` incluye referencias metodológicas, cálculo de potencia, planes de
aleatorización reproducibles y generación de esqueletos de análisis en R o Python.
El alcance y las limitaciones estadísticas se detallan en su `SKILL.md`.

Para instalar la versión del clon local en Claude Code y OpenCode, desde la raíz del repo:

```bash
npx skills add ./skills/experimental-dis -g --agent claude-code opencode --skill experimental-dis -y --copy
```

Repetí el comando después de actualizar la skill y reiniciá los agentes para cargarla.
La instalación de la skill no instala las dependencias Python. Para ejecutar el
planificador, desde `skills/experimental-dis`, en un entorno virtual:

```bash
python -m pip install -r requirements.txt
python scripts/aleatorizar.py --help
python scripts/tamano_muestral.py --help
python scripts/esqueleto_analisis.py --help
python -m unittest discover -s tests -v
```

Ejecutar los análisis Python generados requiere además `pandas`, `numpy` y `statsmodels`.
Las pruebas omiten las comprobaciones que requieren dependencias no disponibles.
Las plantillas R indican sus requisitos; su ejecución requiere una instalación de R.
