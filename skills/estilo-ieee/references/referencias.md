# Citas y referencias IEEE

Fuentes: *IEEE Editorial Style Manual for Authors* (sección II.B, References) y la *IEEE Reference Guide* del Transactions/Journals Department, a la que el manual remite para el formato de cada tipo de fuente.

## Contenido
1. Citas en el texto
2. Reglas generales de la lista
3. Plantillas por tipo de fuente
4. Fuentes en línea: orden de URL, DOI y fecha de acceso
5. Abreviaturas frecuentes
6. Documentos en español
7. LaTeX y gestores de referencias
8. Errores típicos y su corrección

---

## 1. Citas en el texto

**Forma.** Número entre corchetes, en la línea (no superíndice), dentro de la puntuación, con espacio antes del corchete: `como se mostró en [3].`

**Varias fuentes.** Cada número en su propio corchete, separados por coma; los rangos con raya corta (en dash) entre corchetes completos:

| Incorrecto | Correcto |
|---|---|
| `[1,2]`, `[1, 2]` | `[1], [2]` |
| `[1-4]`, `[1–4]` | `[1]–[4]` |
| `[2,4-7,9]` | `[2], [4]–[7], [9]` |
| `[1][2][3]` | `[1]–[3]` |

**Como sustantivo.** La cita puede funcionar como sustantivo: `según [4] y [6]–[9]`, `en [1] se propone…`. No escribas "en la referencia [1]", "ref. [1]" ni "el trabajo [1]" cuando basta "en [1]".

**Autor en el texto.** No pongas el nombre del autor junto al número salvo que sea necesario para entender la oración: "In Smith [1]" pasa a "In [1]", pero "Smith [1] redujo el tiempo…" se mantiene. Con tres o más autores: `Wood et al. [7]`. Si se menciona un autor, su apellido debe coincidir con la lista.

**Sin año como identificador.** "(Smith, 2019)" o "[1] (2019)" no son IEEE; el año se borra salvo que sea relevante para el contenido.

**Partes de una fuente.** Nunca "en la Fig. 2 de [1]" ni "la ecuación (8) de la referencia [1]". Se escriben dentro del corchete:
`[1, Fig. 2]`, `[1, eq. (8)]`, `[3, Th. 1]`, `[3, Lemma 2]`, `[3, pp. 5–10]`, `[3, Sec. IV]`, `[3, Ch. 2, pp. 5–10]`, `[3, Appendix I]`, `[3, Algorithm 5]`.
En español: `[1, Fig. 2]`, `[1, ec. (8)]`, `[3, Teo. 1]`, `[3, pp. 5–10]`, `[3, Sec. IV]`, `[3, Cap. 2]`.

**Orden.** La lista se numera en el orden de la primera cita en el texto. Si se renumera la lista hay que renumerar todas las citas del texto (y avisar al autor).

**"Por ejemplo" y comentarios.** Frases como "For example", "see also" o comentarios no van dentro de la lista: pasan al texto o a una nota al pie: `Por ejemplo, véase [5].`

**ibid. / op. cit.** Se eliminan: en el texto se repite el número original y se agrega la localización si hace falta (`[3, p. 12]`). Luego se renumera.

**Resumen (Abstract).** No lleva citas numeradas, ecuaciones numeradas ni notas al pie.

## 2. Reglas generales de la lista

- Una fuente por número. Prohibido agrupar varias obras bajo un número; si el autor lo hizo, se separan en números consecutivos y se renumera todo lo posterior (ejemplo del manual: la entrada [37] que contenía cuatro libros se divide en [37]–[40] y las antiguas [38]–[40] pasan a [41]–[43]).
- Una obra aparece una sola vez. Si figura repetida para citar páginas distintas, se fusiona y las páginas van en el texto: `[5, p. 30]`.
- Números alineados a la izquierda formando columna propia (sangría francesa).
- Autores: inicial(es) del nombre antes del apellido: `J. K. Author`. Iniciales con punto y espacio: `J. K.`, no `J.K.` ni `JK`. Nombres compuestos con guion: `C.-Y. Chen`.
- Sufijos: en la firma del artículo van sin coma (`K. S. Snyder Jr.`). La Reference Guide dice que en referencias van entre comas, pero sus propios ejemplos las omiten (`W. P. Pratt Jr.`). Elegí una forma y aplicala igual en toda la lista; ante la duda, sin coma.
- Separadores: dos autores con "and" sin coma (`A. Smith and B. Jones`); tres o más con coma serial (`A. Smith, B. Jones, and C. Lee`).
- Hasta seis autores se listan todos. Con más de seis: primer autor + `et al.` (`M. Ito et al.,`). "et al." lleva punto.
- Títulos de artículos, capítulos, ponencias, tesis e informes: entre comillas, en *sentence case* (solo mayúscula inicial y nombres propios/siglas), con la coma **dentro** de las comillas: `“Title of paper,”`.
- Títulos de libros, revistas y actas de congreso: en cursiva y en *title case*; revistas y congresos con abreviaturas estándar.
- Meses abreviados: Jan., Feb., Mar., Apr., May, Jun., Jul., Aug., Sep., Oct., Nov., Dec. Dos meses de un mismo número: `Jul./Aug.`
- Rangos de páginas con raya corta: `pp. 10–15` (no guion). Página única: `p. 475`.
- Artículos con número de artículo en lugar de páginas: `Art. no. 061103`.
- En prensa: `to be published` (aceptado) o `submitted for publication` (enviado). Nunca "to appear in".
- Para IEEE Transactions, incluir número (no.) y mes; si faltan, buscarlos en IEEE Xplore.
- Toda referencia termina en punto, incluso con DOI, **excepto** si termina en URL.
- Lugar de edición: ciudad, estado (solo EE. UU., abreviatura postal), país: `New York, NY, USA:`; `London, U.K.:`; `Rijeka, Croatia:`. Si la universidad lleva el estado en el nombre se omite el estado.
- Editorial abreviada sin "Inc.", "Publishing Co.", etc.: `Wiley`, `Springer-Verlag`, `MIT Press`, `Cambridge Univ. Press`.
- Obras en otro idioma: `(in German)` después del título (en español: `(en alemán)`).
- Faltan datos: buscarlos; si no se consiguen, marcar al usuario qué falta en lugar de inventarlos.

## 3. Plantillas por tipo de fuente

Las plantillas usan las etiquetas en inglés de la guía. Para documentos en español mirá la sección 6.

### Artículo de revista
```
J. K. Author, “Name of paper,” Abbrev. Title of Periodical, vol. x, no. x, pp. xxx–xxx, Abbrev. Month, year, doi: xxx.
```
- M. M. Chiampi and L. L. Zilberti, “Induction of electric field in human bodies moving near MRI: An efficient BEM computational procedure,” *IEEE Trans. Biomed. Eng.*, vol. 58, no. 10, pp. 2787–2793, Oct. 2011, doi: 10.1109/TBME.2011.2158315.
- M. Ito et al., “Application of amorphous oxide TFT to electrophoretic display,” *J. Non-Cryst. Solids*, vol. 354, no. 19, pp. 2777–2782, Feb. 2008.

Con número de artículo:
```
J. K. Author, “Name of paper,” Abbrev. Title of Periodical, vol. x, no. x, Abbrev. Month, year, Art. no. xxx.
```
- J. Zhang and N. Tansu, “Optical gain and laser characteristics of InGaN quantum wells on ternary InGaN substrates,” *IEEE Photon. J.*, vol. 5, no. 2, Apr. 2013, Art. no. 2600111.

### Libro
```
J. K. Author, Title of Book, xth ed. City, State (solo EE. UU.), Country: Abbrev. of Publisher, year.
```
- B. Klaus and P. Horn, *Robot Vision*. Cambridge, MA, USA: MIT Press, 1986.

### Capítulo de libro / libro con editores
```
J. K. Author, “Title of chapter,” in Title of Book, X. Editor, Ed., xth ed. City, State, Country: Abbrev. of Publisher, year, ch. x, sec. x, pp. xxx–xxx.
```
- L. Stein, “Random patterns,” in *Computers and You*, J. S. Brake, Ed. New York, NY, USA: Wiley, 1994, pp. 55–70.
- W. R. Leonard and M. H. Crawford, Eds., *Human Biology of Pastoral Populations*. New York, NY, USA: Cambridge Univ. Press, 2002.

### Libro en línea
```
J. K. Author, Title of Book, xth ed. City, State, Country: Publisher, year. Accessed: Mon. DD, YYYY. [Online]. Available: URL
```

### Artículo en actas de congreso (publicado)
```
J. K. Author, “Title of paper,” in Abbrev. Name of Conf., (City, Country,) (Month day(s),) year, pp. xxx–xxx, doi: xxx.
```
- A. Amador-Perez and R. A. Rodriguez-Solis, “Analysis of a CPW-fed annular slot ring antenna using DOE,” in *Proc. IEEE Antennas Propag. Soc. Int. Symp.*, Jul. 2006, pp. 4301–4304.
- G. Veruggio, “The EURON roboethics roadmap,” in *Proc. Humanoids ’06: 6th IEEE-RAS Int. Conf. Humanoid Robots*, 2006, pp. 612–617, doi: 10.1109/ICHR.2006.321337.

Nombre del congreso: "Proceedings of the 1996 Robotics and Automation Conference" → `Proc. 1996 Robot. Automat. Conf.` Se omiten artículos y preposiciones ("of the", "on"); ordinales en cifra (`4th`, no "Fourth"); si el año está en el título puede omitirse al final. Todo artículo publicado en actas tiene páginas.

### Ponencia presentada (sin actas)
```
J. K. Author, “Title of paper,” presented at the Abbrev. Name of Conf., City, State, Country, Month day(s), year, Paper number.
```
- D. Caratelli, M. C. Viganó, G. Toso, and P. Angeletti, “Analytical placement technique for sparse arrays,” presented at the 32nd ESA Antenna Workshop, Noordwijk, The Netherlands, Oct. 5–8, 2010.

### Tesis y disertaciones
```
J. K. Author, “Title of thesis,” M.S. thesis, Abbrev. Dept., Abbrev. Univ., City, State, Country, year.
J. K. Author, “Title of dissertation,” Ph.D. dissertation, Abbrev. Dept., Abbrev. Univ., City, State, Country, year.
```
- J. O. Williams, “Narrow-band analyzer,” Ph.D. dissertation, Dept. Elect. Eng., Harvard Univ., Cambridge, MA, USA, 1993.
- Tesis de grado: `B.S. thesis` (en español: `Tesis de grado`, `Trabajo final de grado`, `Tesis de maestría`, `Tesis doctoral`). En línea: agregar `[Online]. Available: URL`.

### Informe técnico
```
J. K. Author, “Title of report,” Abbrev. Name of Co., City, State, Country, Rep. xxx, year.
```
- E. E. Reber, R. L. Michell, and C. J. Carter, “Oxygen absorption in the earth’s atmosphere,” Aerospace Corp., Los Angeles, CA, USA, Tech. Rep. TR-0200 (4230-46)-3, Nov. 1988.

### Norma
```
Title of Standard, Standard number, Corporate author, location, date.
Title of Standard, Standard number, date.
```
- *IEEE Criteria for Class IE Electric Systems*, IEEE Standard 308, 1969.
- *Parameter Values for Ultra-High Definition Television Systems…*, Rec. ITU-R BT.2020-2, International Telecommunications Union, Geneva, Switzerland, Oct. 2015.

### Patente
```
J. K. Author, “Title of patent,” Country Patent xxx, Abbrev. Month day, year.
```
- J. P. Wilkinson, “Nonlinear resonant circuit devices,” U.S. Patent 3 624 125, Jul. 16, 1990.

### Manual / hoja de datos
```
Name of Manual, x ed., Abbrev. Name of Co., City, State, Country, year, pp. xxx–xxx.
```
- *Transmission Systems for Communications*, 3rd ed., Western Electric Co., Winston-Salem, NC, USA, 1985, pp. 44–60.

### Software
```
Title of Software. (version or year), Publisher. Accessed: Date. [Online]. Available: URL
```
- *Ngspice*. (2011). [Online]. Available: http://ngspice.sourceforge.net

### Conjunto de datos (dataset)
```
Author, “Title.” (Date). Distributed by Publisher. URL        ← o termina en DOI con punto
Title, Source, Date, doi: xxx.
```

### Preprint (arXiv)
- S. Urazhdin, N. O. Birge, W. P. Pratt Jr., and J. Bass, “Current-driven magnetic excitations in permalloy-based multilayer nanopillars,” 2003, arXiv:0303149.
Si ya existe la versión publicada, citá esa.

### Sitio web
Forma de uso corriente en la guía vigente:
```
J. K. Author (u organización). “Page title.” Website Title. Accessed: Mon. DD, YYYY. [Online]. Available: URL
```
Sin autor, se empieza por el título de la página. Sitios informales sin título: frase descriptiva.

### Video en línea
```
Owner, Location. Title of Video. (Release date). Accessed: Mon. DD, YYYY. [Online Video]. Available: URL
```

### No publicado
- A. Harrison, private communication, May 1995.
- B. Smith, “An approach to graphs of linear forms,” unpublished.

## 4. Fuentes en línea: orden de URL, DOI y fecha de acceso

Fecha de acceso: `Accessed: Abbrev. Month Day, Year.` Opciones de cierre válidas:

| Caso | Cierre |
|---|---|
| Acceso + URL + DOI | `Accessed: date. [Online]. Available: URL, DOI.` (punto final) |
| Acceso + URL | `Accessed: date. [Online]. Available: URL` (sin punto) |
| Acceso + DOI | `Accessed: date, DOI.` |
| URL + DOI | `URL, DOI.` |
| Solo DOI | `…, doi: 10.xxxx/xxxxx.` |
| Solo URL | `URL` (sin punto) |

- DOI en formato `doi: 10.1109/…` (prefijo en minúscula, sin `https://doi.org/`), salvo que la institución pida el enlace resolvible.
- Cuando hay DOI, preferilo a una URL de editorial.
- Cortes de URL (si el maquetado obliga): después de `/` o `//`; antes de `~`, `-`, `_`, `?`, `%`; antes o después de `=`, `&`, `@`. Nunca agregar guiones ni espacios.

## 5. Abreviaturas frecuentes

**Congresos:** Annals Ann., Annual Annu., Colloquium Colloq., Conference Conf., Congress Congr., Convention Conv., Digest Dig., Exposition Expo., International Int., National Nat., Proceedings Proc., Record Rec., Symposium Symp., Technical Digest Tech. Dig., Workshop Workshop.

**Palabras en títulos de revistas (selección):** Advanced Adv., Analysis Anal., Applied/Applications Appl., Artificial Artif., Automation Automat., Automatic Autom., Communications Commun., Computer/Computing/Computational Comput., Conference Conf., Electrical Elect., Electronic Electron., Engineering Eng., Environment Environ., European Eur., Industrial Ind., Information Inf., Institute Inst., Instrumentation Instrum., Intelligence/Intelligent Intell., International Int., Journal J., Learning Learn., Letters Lett., Machine Mach., Magazine Mag., Management Manage., Mathematics/Mathematical Math., Measurement Meas., Mechanical Mech., Medical Med., Microwave Microw., Network(ing) Netw., Optical/Optics Opt., Photonics Photon., Physics Phys., Processing Process., Propagation Propag., Recognition Recognit., Research Res., Review Rev., Robotics Robot., Science Sci., Security Secur., Society Soc., Software Softw., Systems Syst., Technology Technol., Telecommunications Telecommun., Transactions Trans., University Univ., Vehicular Veh.

Ejemplos: *IEEE Trans. Power Syst.*, *IEEE Trans. Pattern Anal. Mach. Intell.*, *IEEE Commun. Mag.*, *IEEE Access* (no se abrevia), *Proc. IEEE*, *J. Mach. Learn. Res.*, *Renew. Sustain. Energy Rev.* Para abreviaturas de revistas no listadas, usá la norma ISO 4 (LTWA) y avisá al usuario que conviene verificarla.

**Genéricas:** edition ed., Editor(s) Ed./Eds., volume vol., number no., pages pp., page p., chapter ch., section sec., Department Dept., Technical Report Tech. Rep., translated Transl.

## 6. Documentos en español

El manual está pensado para artículos en inglés. En una tesis o un artículo en español, la institución o la revista puede pedir las etiquetas traducidas. Regla: **elegí un juego y aplicalo igual en toda la lista**. Si el documento ya usa uno de forma mayoritaria, respetalo; si no hay pauta, preguntá o usá el español, que es lo más frecuente en universidades hispanohablantes.

| Inglés (IEEE) | Español |
|---|---|
| and | y |
| et al. | et al. (no se traduce) |
| Ed. / Eds. | Ed. / Eds. |
| ed. (edición) | ed. (`2.ª ed.` o `2nd ed.` según pauta) |
| vol. | vol. |
| no. | no. (o `n.º`; mantener uno) |
| pp. / p. | pp. / p. |
| ch. | cap. |
| Art. no. | Art. no. |
| [Online]. Available: | [En línea]. Disponible en: |
| Accessed: | Consultado: / Accedido: |
| presented at the | presentado en |
| to be published | en prensa |
| submitted for publication | enviado para publicación |
| unpublished | inédito |
| private communication | comunicación privada |
| M.S. thesis / Ph.D. dissertation | Tesis de maestría / Tesis doctoral |
| Tech. Rep. | Inf. téc. (o Tech. Rep.) |
| (in German) | (en alemán) |

- Los títulos de fuentes en español van con mayúscula solo inicial y en nombres propios (es la norma del español y coincide con el *sentence case* de IEEE). Títulos de revistas y libros en español: sin forzar el *title case* inglés.
- Nombres de revistas en inglés se abrevian igual que en un artículo IEEE.
- Fechas de acceso: mantené el formato IEEE abreviado (`Consultado: 14 mar. 2026` o `Accessed: Mar. 14, 2026`) de forma consistente.
- Apellidos compuestos hispanos: se conservan ambos apellidos si la fuente los usa (`J. C. García Pérez`); no conviertas el segundo apellido en inicial.
- La coma del título va dentro de las comillas en IEEE (`“Título,”`). En español hay quien la saca; si la institución no dice nada, seguí IEEE.

## 7. LaTeX y gestores de referencias

- LaTeX: clase `IEEEtran`, estilo `\bibliographystyle{IEEEtran}` con `IEEEabrv.bib` para abreviar revistas (`\bibliography{IEEEabrv,refs}`). Paquete `cite` para que `\cite{a,b,c,d}` produzca `[1]–[4]` ordenado y comprimido. Con `biblatex`: `\usepackage[style=ieee]{biblatex}`.
- En `.bib`: páginas con `--` (`pages = {10--15}`), mes con macros (`month = oct`), DOI en su campo `doi`, protección de siglas en títulos con llaves (`{MIMO}`, `{IEEE}`) para que el estilo no las pase a minúscula.
- Word: la galería de estilos de Word incluye "IEEE"; Zotero y Mendeley tienen el estilo CSL "IEEE". Sirven como base, pero suelen fallar en abreviaturas de revistas, et al. y rayas de rango: revisá la salida.
- Si el documento tiene campos de cita vivos (Zotero, Mendeley, EndNote, citas de Word), no los reemplaces por texto plano sin avisar: se rompe el vínculo con el gestor. Corregí en el gestor o marcá el cambio para que el usuario lo haga ahí.

## 8. Errores típicos y su corrección

| Encontrado | Corrección |
|---|---|
| `Smith, J. (2019). Title. Journal, 5(2), 10-15.` (APA) | `J. Smith, “Title,” Abbrev. J., vol. 5, no. 2, pp. 10–15, 2019.` |
| `John Smith and Mary Jones` | `J. Smith and M. Jones` |
| `J. Smith, M. Jones, A. Lee, B. Kim, C. Park, D. Wu, E. Tan` (7) | `J. Smith et al.` |
| `J. Smith et al` | `J. Smith et al.` |
| `pp. 10-15` / `pp 10–15` | `pp. 10–15` |
| `vol. 5, issue 2` | `vol. 5, no. 2` |
| `October 2011` | `Oct. 2011` |
| `“Title”, IEEE…` | `“Title,” IEEE…` |
| `IEEE Transactions on Power Systems` | `IEEE Trans. Power Syst.` |
| `https://doi.org/10.1109/X.2020.1` al final | `doi: 10.1109/X.2020.1.` |
| `Available: http://x.org/a.pdf.` | `Available: http://x.org/a.pdf` |
| `to appear in IEEE Trans. …` | `IEEE Trans. …, to be published.` |
| `[1] ver también [2]` dentro de la lista | pasar el comentario al texto |
| `[5] Ibid., p. 30.` | eliminar, citar `[4, p. 30]` en el texto y renumerar |
