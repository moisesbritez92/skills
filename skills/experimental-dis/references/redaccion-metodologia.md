# Redacción de la metodología

## 1. Escribir lo que permite reproducir

La metodología debe conectar pregunta, asignación, medición y análisis. No alcanza con nombrar un diseño ni enumerar marcas de equipos. Otra persona debe poder reconstruir qué se hará, sobre qué unidades, en qué orden y con qué decisiones previstas.

Usá futuro para un protocolo y pasado para procedimientos realizados. En una revisión retrospectiva no conviertas decisiones posteriores en planes previos. Mantené estilo impersonal y terminología consistente, sin confundir «aleatorio», «representativo» y «homogéneo».

Los ejemplos siguientes son plantillas. Los campos entre corchetes se completan con información comprobada o quedan como pendientes explícitos. No inventes ubicaciones, coordenadas, versiones, aprobaciones, fechas ni referencias para cerrar un párrafo.

## 2. Orden recomendado

| Sección | Información operativa |
|---|---|
| Ámbito y período | Lugar, condiciones relevantes y calendario |
| Población y material | Procedencia, criterios de inclusión, selección y preparación |
| Diseño | Asignación, factores, niveles, bloques y seguimiento |
| Unidades y tamaño | n por nivel, submuestras y justificación |
| Intervenciones | Dosis, duración, aplicación y comparador |
| Variables | Definición, unidad, instrumento, momento y derivación |
| Procedimiento | Secuencia, calibración, control de calidad y desviaciones |
| Análisis | Estimando, modelo, contraste, incertidumbre y sensibilidad |
| Ética y datos | Revisión aplicable, protección, acceso y conservación |

Adaptá este orden al formato institucional sin ocultar información esencial. Un cuadro de tratamientos o de variables puede ser más claro que un párrafo extenso. No impongas una norma académica que el usuario no haya indicado.

## 3. Diseño y asignación

«Se realizará un [tipo de estudio] para estimar [contraste y población]. Se evaluarán [factores y niveles] mediante [estructura de asignación]. Los bloques se definirán según [criterio previo], debido a [fundamento]. Dentro de cada bloque se asignarán [tratamientos] a [unidades] mediante [procedimiento].»

Para aleatorización computacional, agregá algoritmo o software, versión, semilla y orden de partida archivados. Para un sorteo físico, describí elementos, procedimiento y registro. En ambos casos, documentá quién genera y aplica la secuencia y cómo se resguardará hasta la asignación si corresponde.

**Antes.** «Se distribuyeron completamente al azar en cuatro bloques».

**Después.** «Los tratamientos se asignarán al azar dentro de cada uno de los cuatro bloques definidos por [criterio]. Cada bloque contendrá [composición]». Esto describe asignación bloqueada, no un DCA.

No escribas «doble ciego» sin identificar quién desconoce la asignación: participantes, aplicadores, evaluadores o analistas. Si el cegamiento es inviable, indicá medidas para reducir sesgo de evaluación.

## 4. Unidad, replicación y muestra

«La unidad experimental será [entidad que recibe la asignación]. Se dispondrá de [N] unidades, [n] por [tratamiento/combinación]. En cada unidad se registrarán [submuestras o momentos]. Estas mediciones se [agregarán/modelarán] para representar [estimando y dependencia].»

**Antes.** «Se analizarán 90 muestras, con tres repeticiones».

**Después.** «Se asignarán [tratamientos] a [número] parcelas. En cada parcela se tomarán [número] submuestras que formarán [muestra compuesta o mediciones separadas]. La replicación del tratamiento corresponderá al número de parcelas asignadas, no al número de análisis de laboratorio».

En parcelas divididas, declará por separado parcelas grandes por nivel de A y subparcelas por combinación A×B. En ensayos humanos distinguí reclutados, aleatorizados y número analizable previsto; en un informe final, aportá además el flujo observado.

## 5. Justificación del tamaño

«El tamaño se determinará para [contraste], con una diferencia relevante de [valor y unidad], [variabilidad y fuente], alfa [valor] y potencia [valor]. Se considerará [correlación, bloques o estratos]. Mediante [método y versión] se estimarán [unidades]. Se evaluarán escenarios de [incertidumbre] y se ajustará por [pérdidas justificadas]».

Si el presupuesto fija n, escribí esa restricción y la precisión o efecto detectable que se evaluó. No atribuyas un cálculo de potencia a una decisión basada en conveniencia. Si el estudio es piloto, justificá sus objetivos de factibilidad sin prometer confirmación de eficacia.

Para ANOVA global, explicitá el escenario de medias y aclará que el n no garantiza potencia de cada comparación. Ver `tamano-muestral.md`.

## 6. Variables y procedimiento

Cada variable necesita definición operacional, unidad, instrumento o fuente, momento y regla de cálculo. «Crecimiento» no basta: podría significar altura final, incremento absoluto o tasa relativa, con interpretaciones distintas.

«La respuesta principal será [variable], expresada en [unidad], registrada en [momento] mediante [método]. Se realizarán [lecturas técnicas] y se obtendrá [resumen predefinido]. Se verificará [calibración o control] con [frecuencia]. Las respuestas secundarias serán [variables y momentos]».

Describí manejo común, orden de medición, condiciones ambientales y acciones ante fallos. Una marca puede ser necesaria para reproducir un instrumento, pero no sustituye resolución, calibración ni protocolo. En software, registrá versión, configuración, datos y recursos computacionales relevantes.

## 7. Análisis e interpretación

**Antes.** «Se utilizará ANOVA y Tukey al 5 % si los datos son normales».

**Después.** «Se estimará [contraste] mediante [modelo], que incluirá [términos] y representará [dependencia]. Se informarán estimación e intervalo de confianza de [nivel]. La familia de [comparaciones] se analizará mediante [estrategia]. Se evaluarán [diagnósticos] y se prevén [alternativas fundamentadas]. Los faltantes y exclusiones se tratarán según [reglas y sensibilidad]».

No afirmes que una prueba de normalidad valida independencia ni que «se aceptará la hipótesis nula». Describí incertidumbre y compatibilidad con efectos relevantes. Separá análisis confirmatorio de exploración y cambios posteriores al plan.

## 8. Ética, integridad y revisión final

En humanos, consigná comité, resolución y fecha solo si constan; de lo contrario, «se solicitará aprobación antes de…». Consentimiento, dispensa, privacidad y registro se describen según el estudio y la normativa aplicable. En animales, documentá autorización y bienestar, no consentimiento del animal.

Explicá custodia, anonimización o seudonimización, acceso y conservación de datos. No prometas publicación abierta de datos personales o material con restricciones. Para intervenciones ambientales, verificá permisos y disposición de residuos.

Antes de entregar, cotejá todos los números con el diseño y el tamaño calculado. Eliminá campos pendientes solo cuando se hayan resuelto. Las referencias deben respaldar procedimientos concretos y tener metadatos comprobados; una cita decorativa no justifica una decisión estadística.
