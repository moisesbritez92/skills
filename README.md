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
