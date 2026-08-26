# Redacción en LaTeX con citas IEEE

Aplica cuando el trabajo se escribe en `.tex`. El sistema es bibtex clásico con
`IEEEtran.bst`, no biblatex.

## Citar

| Situación | LaTeX | Sale como |
|---|---|---|
| Una fuente | `\cite{chi2025diffusion}` | [1] |
| Varias sueltas | `\cite{ho2020ddpm}, \cite{song2021sde}` | [2], [3] |
| Rango consecutivo | `\cite{a}--\cite{c}` | [4]-[6] |
| Con página | `\cite[p.~14]{ross2011dagger}` | [5, p. 14] |
| Con figura o capítulo | `\cite[Fig.~3]{clave}` | [7, Fig. 3] |
| Autor como sujeto | `Chi \textit{et al.} \cite{chi2025diffusion} proponen…` | Chi *et al.* [1] proponen… |

Reglas:

- La cita va **antes** del punto y pegada a la palabra: `… reduce el error \cite{clave}.`
- La numeración la asigna BibTeX por orden de primera aparición. **Nunca se escribe `[3]` a
  mano** ni se reordena la lista.
- La cita no es un elemento gramatical de la frase: `en \cite{5} se demuestra` está mal;
  `el estudio \cite{5} demuestra` está bien.
- Antes de citar, leer el `.bib` del proyecto y reutilizar sus claves. Si la obra falta, se
  añade la entrada con los datos reales de la portada del documento. Si un dato no consta,
  se deja `[PENDIENTE: referencia]` en el texto y se avisa al terminar. **Jamás se inventa
  una entrada para que el documento compile.**
- Un dato tomado de fuera del documento original (paginación de unas actas, volumen de una
  serie) se marca en el `.bib` con un comentario `% verificar`, **entre entradas**: BibTeX
  no admite `%` dentro de una entrada.

## Entradas .bib más frecuentes

```bibtex
@article{clave,        % revista
  author = {N. Apellido and N. Apellido}, title = {...},
  journal = {...}, volume = {44}, number = {10--11}, pages = {1684--1704},
  year = {2025}, note = {doi: 10.xxxx/xxxxx}}   % IEEEtran.bst no admite el campo doi

@inproceedings{clave,  % congreso
  author = {...}, title = {...},
  booktitle = {Proc. 5th Conf. Robot Learning (CoRL)},
  address = {London, U.K.}, year = {2021}, note = {arXiv:2108.03298}}

@misc{clave,           % preprint o recurso
  author = {...}, title = {...}, howpublished = {arXiv:2403.03954}, year = {2024}}
```

## Figuras, tablas y referencias cruzadas

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{img/fichero}
  \caption{Frase que explica qué se muestra.}
  \label{fig:etiqueta}
  \fuente{adaptado de \cite{clave}}      % macro del estilo del proyecto
\end{figure}
```

- Pie **debajo** en figuras, título **encima** en tablas: lo impone el estilo, no se ajusta
  a mano con `\vspace`.
- Toda figura o tabla se menciona antes de aparecer: `\cref{fig:etiqueta}` produce
  «Figura 3».
- Etiquetas con prefijo: `fig:`, `tab:`, `eq:`, `cap:`, `sec:`, `lst:`, `anx:`.
- Tablas con `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), sin líneas verticales.
- Números con `\num{0,8645}` (siunitx) para que el decimal salga con coma.

## Qué no se toca al redactar

- El fichero de estilo (`.sty`) y la clase: un problema de redacción no se arregla
  cambiando el formato.
- La numeración de capítulos, figuras, tablas y referencias: la lleva LaTeX.
- El `.bbl` generado: se edita el `.bib` y se recompila.

## Trampas que cuelgan la compilación

- Una celda de tabla que empieza por `[` justo después de `\midrule`, `\toprule` o `\\` se
  interpreta como el argumento opcional de anchura de ese comando: TeX entra en bucle y no
  da error. Se escribe `{[texto]}`. Vale para cualquier texto entre corchetes al principio
  de línea tras un comando con argumento opcional.
- Un `\makeatother` dentro de un `.sty` desactiva las macros `\@...` del resto del fichero;
  dentro de un paquete la arroba ya es letra y no hace falta `\makeatletter`.
- Cambiar opciones de `babel` deja el `.toc` anterior con macros inexistentes: limpiar los
  auxiliares antes de recompilar.
- `amssymb` después de una fuente matemática (`newtx`) da `\Bbbk already defined`.

## Comprobación antes de dar por cerrado un capítulo

- [ ] El documento compila y el número de avisos no ha crecido
- [ ] Ninguna cita sale como `[?]` (clave inexistente en el `.bib`)
- [ ] Ninguna referencia cruzada sale como `??`
- [ ] Todas las figuras y tablas nuevas están citadas en el texto
- [ ] No quedan marcadores `[PENDIENTE: …]` sin avisar al usuario

## Proyecto actual del usuario

`~/Documents/001_TFM/tfm_madi/memoria/`: `main.tex`, capítulos en `secciones/`, obras
citadas en `bib/referencias.bib`, consultadas en `bib/bibliografia.bib`, estilo en
`tecnun-tfm.sty`, compilación con `./compilar.sh`. Contexto y decisiones en
`memoria/MEMORY.md`; conviene leerlo antes de escribir.
