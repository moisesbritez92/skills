# Envío: publicación previa, autoría y comprobaciones

## Publicar lo que ya está en el repositorio de la universidad

Casi todas las revistas aceptan artículos derivados de una tesis depositada, porque una tesis
no cuenta como publicación previa revisada por pares. Pero hay tres cosas que sí dan
problemas y que conviene resolver antes, no después del rechazo:

1. **Declararlo.** Muchas revistas piden decir en la carta de presentación que el trabajo
   procede de una tesis, con el enlace al repositorio. Es una frase y evita una acusación de
   publicación duplicada.
2. **Solapamiento de texto.** Los detectores de similitud comparan contra los repositorios
   institucionales y encontrarán la tesis del propio autor. Con un artículo *reescrito* (que
   es lo que produce esta skill) el solapamiento es bajo; con un artículo hecho a base de
   borrar frases, alto. Es otra razón para reescribir de verdad.
3. **Embargo y licencia.** Si la tesis está bajo embargo, o con una licencia que la revista
   considera incompatible, hay que comprobarlo con la biblioteca antes de enviar.

Consulta la política concreta de la revista; algunas editoriales la publican como *prior
publication policy* o dentro de sus normas éticas.

## Autoría

En la mayoría de las áreas, el director o tutor de la tesis es coautor del artículo derivado,
y en muchas es el autor de correspondencia. **No decidas esto tú**: pregunta al usuario quién
firma, en qué orden y quién es el corresponsal, y déjalo por escrito en el plan. Un artículo
enviado sin el tutor, o con alguien que no participó, es un problema serio y frecuente.

Si la revista pide la declaración CRediT (contribución de cada autor), pide al usuario que la
complete; no la inventes.

## Carta de presentación

Media página, y no repite el resumen. Cuatro párrafos:

1. Título, tipo de artículo y a qué revista se envía.
2. Qué se encontró y por qué encaja en el alcance de esa revista concreta (una o dos frases
   que demuestren que el autor la ha leído).
3. Declaraciones: que el trabajo es original, que no está en revisión en otro sitio, que
   procede de la tesis de X depositada en Y, y los conflictos de interés si los hay.
4. Datos del autor de correspondencia. Si la revista pide revisores sugeridos, van aquí.

## Lista de comprobación antes de enviar

Formato:

- [ ] Compila o abre sin errores y el PDF se ha mirado página a página.
- [ ] Dentro del límite de páginas o palabras, **contando referencias si la revista las cuenta**.
- [ ] Plantilla sin modificar: márgenes, fuente, tamaño, interlineado, columnas.
- [ ] Estilo de citas el de la revista, y todas las referencias completas (DOI incluido).
- [ ] Figuras a la resolución exigida y legibles en el PDF final; en ficheros aparte si lo piden.
- [ ] Numeración de figuras, tablas y ecuaciones desde 1, y todas citadas en el texto.

Contenido:

- [ ] El resumen dice lo que se encontró, con cifras, y cabe en el límite.
- [ ] La afirmación central se sostiene en el resumen, la introducción y la conclusión, y es la misma.
- [ ] Ni un resto de voz de tesis (`scripts/check_articulo.py` lo comprueba).
- [ ] Cada figura y tabla se comenta en el texto y aporta algo que no está ya en otra.
- [ ] Limitaciones explícitas y honestas.
- [ ] Ningún `[[FALTA: ...]]` sin resolver.

Trámite:

- [ ] Palabras clave, ORCID y filiaciones completas.
- [ ] Declaraciones que exija la revista: financiación, ética, disponibilidad de datos,
      conflictos de interés, contribución de autores.
- [ ] Carta de presentación.
- [ ] Material suplementario en el formato admitido.
- [ ] Coautores avisados y de acuerdo con la versión que se envía.
