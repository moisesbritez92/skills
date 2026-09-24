# skills

Colección de skills para trabajo académico, científico y técnico, pensadas para usarse con la CLI de [Agent Skills](https://agentskills.io/) y el comando [`npx skills`](https://skills.sh/).

Este repositorio reúne habilidades enfocadas en redacción académica, diseño de experimentos, análisis estadístico, conversión a artículo y revisión de estilo IEEE.

## Estructura del repositorio

```text
skills/
├── analista-datos/
├── estilo-ieee/
├── experimental-dis/
├── redactor-anteproyecto/
├── redactor-tesis/
├── tesis-a-articulo/
├── README.md
└── ...
```

Cada carpeta contiene:

- `SKILL.md`: instrucciones y criterio de uso de la habilidad.
- `references/`: material de apoyo y plantillas.
- `scripts/`: utilidades automatizadas cuando aplica.
- `tests/`: validaciones del comportamiento del módulo, si existe.

## Instalación global

Instalar todas las skills del repositorio para que queden disponibles en cualquier proyecto:

```bash
npx skills add moisesbritez92/skills -g -y
```

Instalar solo una skill concreta:

```bash
npx skills add moisesbritez92/skills -g --skill redactor-tesis -y
```

El flag `-g` las instala en el directorio global del agente, por ejemplo:

- `~/.claude/skills/`
- `~/.codex/skills/`
- `~/.copilot/skills/`

De ese modo no hace falta volver a instalarlas en cada proyecto.

## Skills disponibles

### Redacción académica

- [skills/redactor-tesis](skills/redactor-tesis/SKILL.md): escritura y revisión de tesis, TFG, TFM, papers y memorias con estilo sobrio, impersonal y formal.
- [skills/redactor-anteproyecto](skills/redactor-anteproyecto/SKILL.md): redacción de anteproyectos, protocolos de investigación y proyectos finales de grado, con foco en formato institucional y buenas prácticas académicas.
- [skills/estilo-ieee](skills/estilo-ieee/SKILL.md): revisión, corrección y redacción de documentos según estilo IEEE, citas numéricas y bibliografía compatible con IEEE.

### Investigación y diseño experimental

- [skills/experimental-dis](skills/experimental-dis/SKILL.md): diseño experimental, determinación de tamaño muestral, aleatorización, plan de análisis y estructura metodológica para tesis e investigaciones.
- [skills/analista-datos](skills/analista-datos/SKILL.md): auditoría, análisis y presentación de datos experimentales con tablas, figuras, supuestos y resultados en formato académico.

### Conversión y publicación

- [skills/tesis-a-articulo](skills/tesis-a-articulo/SKILL.md): transformación de tesis, TFG o TFM en un artículo científico con estructura, compresión y ajuste a una plantilla editorial.

## Instalación desde el clon local

Para probar la versión local del repositorio en Claude Code y OpenCode:

```bash
npx skills add ./skills/experimental-dis -g --agent claude-code opencode --skill experimental-dis -y --copy
```

Esto copia la skill local al directorio global del agente. Si se actualiza la skill, conviene repetir el comando y reiniciar los agentes para cargar la nueva versión.

## Uso recomendado por caso

### Si necesitás redactar un texto académico

- Redacción de notas, capítulos, resultados y discusión: `redactor-tesis`
- Anteproyecto o protocolo formal: `redactor-anteproyecto`
- Revisión de formato, citas y referencias IEEE: `estilo-ieee`

### Si necesitás planificar o evaluar un estudio

- Diseño de experimento, unidad experimental y potencia: `experimental-dis`
- Análisis estadístico de datos ya recolectados: `analista-datos`

### Si necesitás publicar el trabajo

- Convertir tesis en artículo: `tesis-a-articulo`

## Requisitos específicos

Algunas skills tienen dependencias adicionales o scripts de apoyo.

### `experimental-dis`

Desde la carpeta [skills/experimental-dis](skills/experimental-dis):

```bash
python -m pip install -r requirements.txt
python scripts/aleatorizar.py --help
python scripts/tamano_muestral.py --help
python scripts/esqueleto_analisis.py --help
python -m unittest discover -s tests -v
```

La ejecución de algunos análisis generados puede requerir `pandas`, `numpy` y `statsmodels`, además de R para plantillas o scripts específicos.

## Principio del repositorio

Las skills están diseñadas para ser:

- útiles en trabajos académicos reales;
- consistentes con rigor científico;
- reutilizables en distintos proyectos;
- fáciles de instalar y mantener desde un único repositorio central.

Si necesitás una habilidad específica para una tarea concreta, revisá la carpeta correspondiente y usá el `SKILL.md` como referencia principal antes de iniciar.
