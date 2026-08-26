# Formato, citas y referencias

## Sistema de citas: IEEE

Todo el trabajo se cita en IEEE. Solo se cambia si un documento ya redactado usa otro
sistema, en cuyo caso se respeta el existente y se avisa de la discrepancia.

**Regla que no admite excepción: nunca inventar una referencia, un DOI, un año, un volumen
ni un número de página.** Si el dato no está disponible, escribir `[PENDIENTE: referencia]`
y avisar al usuario al final.

### Cita en el texto

- Corchetes con el número de orden de **primera aparición**: `[1]`, `[2]`…
- Va antes del punto y pegada a la palabra: `… mejora la precisión [4].`
- Varias fuentes: `[2], [5], [9]`. Rango consecutivo: `[3]-[6]`. Nunca `[3, 5]` con guion.
- El número sustituye al nombre, pero puede acompañarlo cuando el autor es el sujeto de la
  frase: `Chi *et al.* [3] proponen…`. Con tres o más autores, `et al.` en cursiva.
- El mismo número se reutiliza en cada nueva mención de esa fuente.
- Cita literal: entre comillas y con página: `«texto literal» [7, p. 14]`.
- Referencia a una parte concreta: `[7, Fig. 3]`, `[7, Cap. 2]`, `[7, pp. 44-46]`.
- No se usa la cita como elemento gramatical: ❌ `en [5] se demuestra…` →
  ✅ `El estudio [5] demuestra…`.

### Lista de referencias

Numerada por orden de aparición, con el número entre corchetes alineado a la izquierda y
sangría francesa. Autores: inicial del nombre + apellido (`N. Apellido`); hasta seis
autores, a partir de ahí el primero seguido de `et al.`. Título del artículo entre comillas
y en redonda; nombre de revista, libro o actas en cursiva.

```
Artículo de revista
[1] N. Apellido y N. Apellido, "Título del artículo," Nombre de la Revista, vol. 4,
    no. 2, pp. 112-125, 2023, doi: 10.xxxx/xxxxx.

Libro
[2] N. Apellido, Título del Libro, 2.ª ed. Ciudad, País: Editorial, 2021.

Capítulo de libro
[3] N. Apellido, "Título del capítulo," en Título del Libro, N. Editor, Ed. Ciudad,
    País: Editorial, 2020, pp. 33-58.

Ponencia en congreso
[4] N. Apellido, "Título de la ponencia," en Proc. Conf. Robot Learning (CoRL),
    Atlanta, GA, EE. UU., 2023, pp. 2019-2032.

Preprint / arXiv
[5] N. Apellido, "Título del preprint," arXiv:2303.04137, 2023.

Tesis
[6] N. Apellido, "Título de la tesis," Tesis doctoral, Dept. de X, Univ. Y, Ciudad, 2022.

Recurso web
[7] Organización, "Título de la página," Nombre del sitio, 2024. [En línea]. Disponible
    en: https://… [Accedido: 12-ago-2026].

Software / repositorio
[8] N. Apellido, Nombre del software (versión 1.2). (2023). [Software]. Disponible
    en: https://github.com/…

Norma técnica
[9] Título de la norma, Norma ISO/IEC 25010, 2011.
```

### Errores frecuentes

| ❌ | ✅ |
|---|---|
| Bibliografía ordenada alfabéticamente | Ordenada por número de aparición |
| `(Chi et al., 2023)` | `[3]` |
| `[12].` con el punto antes del corchete | `… previo [12].` |
| Renumerar a mano tras insertar una cita | Numeración correlativa revisada al final |
| Una entrada en la lista que no se cita | Toda entrada aparece citada al menos una vez |

## Tablas y figuras

- **Tabla**: número y título **encima**; nota y fuente debajo. Sin líneas verticales;
  reglas horizontales solo en cabecera y cierre.
- **Figura**: número y pie **debajo**. Texto de los ejes legible al tamaño impreso.
- Numeración correlativa por capítulo (Tabla 3.1, Figura 3.2) o continua en todo el
  trabajo; una de las dos, nunca mezcladas.
- Toda tabla y figura se **anuncia en el texto antes de aparecer** y se comenta: qué debe
  mirar el lector y qué se concluye. Un elemento que no se comenta se elimina o se lleva a
  un anexo.
- Fuente obligatoria si el material es ajeno o adaptado: *Fuente: adaptado de [4].*
  Si es propio: *Fuente: elaboración propia.*

## Notas al pie

Van con llamada volada tras el signo de puntuación.¹ Se reservan para una precisión, una
aclaración terminológica o un dato accesorio. Si la nota contiene algo que el lector
necesita para seguir el argumento, su sitio es el cuerpo del texto. No sustituyen a la cita
bibliográfica.

## Presentación de la entrega

- Texto justificado, interlineado sencillo (o 1,5 si lo exige la normativa), coherente en
  todo el documento.
- Una tipografía para el cuerpo y, como mucho, otra para títulos; sin colores decorativos.
- Márgenes uniformes, numeración de páginas, encabezado con el título del capítulo.
- Índice general, índice de tablas e índice de figuras generados automáticamente.
- Estructura habitual: portada · resumen y palabras clave (en dos idiomas si se exige) ·
  índices · introducción · estado del arte · metodología · resultados · discusión ·
  conclusiones y trabajo futuro · bibliografía · anexos.
- Comprobación final: los índices reflejan la numeración real, no quedan referencias
  cruzadas rotas y no hay marcadores `[PENDIENTE: …]` sin resolver.
