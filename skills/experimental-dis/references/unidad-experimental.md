# Unidad experimental y replicación

## 1. Separar las unidades

Antes de contar observaciones, dibujá la secuencia: población objetivo, unidades disponibles, asignación, aplicación, muestreo y medición. El tamaño de una hoja de cálculo no define el tamaño experimental.

| Concepto | Pregunta que lo identifica | Ejemplo |
|---|---|---|
| Unidad experimental | ¿A qué entidad se asigna el tratamiento? | Maceta que recibe una dosis |
| Unidad de observación | ¿Sobre qué entidad se registra la respuesta? | Planta dentro de la maceta |
| Unidad de muestreo | ¿Qué entidad se selecciona de una población? | Parcela elegida para tomar suelo |
| Réplica técnica | ¿Se vuelve a medir el mismo material? | Lecturas del mismo extracto |
| Bloque | ¿Dentro de qué conjunto se restringe la asignación? | Bandeja que contiene todas las dosis |

En diseños restringidos las asignaciones no son probabilísticamente independientes entre sí: por ejemplo, completar un bloque fija su última asignación. Lo esencial es identificar unidades y mecanismo de asignación, y no tratar subobservaciones como nuevas réplicas del tratamiento.

## 2. Prueba práctica de identificación

Preguntá qué podría haber recibido un tratamiento distinto manteniendo el resto del protocolo. Si una válvula aplica riego a todo un sector, una planta de ese sector no podría recibir otro riego de forma independiente. El sector es la unidad para riego.

Después comprobá aplicación compartida, contacto y contaminación. Macetas nominalmente separadas pueden compartir solución nutritiva; usuarios pueden compartir una cuenta; animales pueden recibir alimento por jaula. El nombre de la entidad no basta para decidir independencia.

**Registro mínimo.** Escribí: tratamiento o factor, unidad de asignación, número total y por condición, subunidades medidas, momentos y población a la que se pretende generalizar.

**Ejemplo ilustrativo.** Cuatro dosis se asignan a 6 macetas por dosis, con 3 plantas en cada una. Son 24 unidades experimentales y 72 plantas observadas. Para comparar dosis, n = 6 macetas por dosis, no 18 plantas. Estas cantidades ilustran la estructura; no justifican potencia.

## 3. Promediar o modelar

Promediar por unidad es razonable si la respuesta de interés es el promedio de esa unidad y las submuestras tienen un protocolo comparable. Conservá número de submuestras, dispersión interna y datos originales para auditoría. En conteos o proporciones, conservá también exposición o denominador.

Un modelo jerárquico permite aprovechar observaciones internas y tamaños desiguales:

`y_ijk = μ + τ_i + u_ij + ε_ijk`

Aquí j identifica unidades tratadas dentro del tratamiento i y k las submuestras; `u_ij` representa variación entre unidades. La inferencia de tratamiento debe reconocer ese nivel. El modelo no convierte cien hojas de una única planta tratada en cien plantas tratadas.

Elegí ponderaciones según el estimando. Dar igual peso a cada maceta estima una media entre macetas; ponderar por número de plantas puede dirigirse a otra población y favorecer unidades grandes. No ponderes automáticamente por cantidad de lecturas técnicas.

## 4. Casos que cambian el n

| Situación | Replicación relevante | Qué no debe contarse como réplica adicional |
|---|---|---|
| Dieta suministrada por jaula | Jaulas asignadas a cada dieta | Animales que comen del mismo suministro |
| Tratamiento aplicado a cultivo celular | Cultivos o preparaciones asignadas según protocolo | Pozos derivados de una única preparación sin independencia biológica |
| Programa asignado a escuelas | Escuelas por condición | Alumnos como si hubieran sido aleatorizados individualmente |
| Algoritmos sobre los mismos conjuntos de datos | Comparaciones pareadas entre conjuntos, según población objetivo | Semillas como sustituto de conjuntos distintos |
| Temperatura por cámara y variedad dentro de cámara | Cámaras para temperatura; subunidades para variedad | Plantas como réplicas de temperatura |
| Ensayo mecánico sobre piezas de lotes tratados | Lotes para tratamiento industrial | Probetas extraídas del mismo lote |

En laboratorio, «biológica» y «técnica» deben definirse por el proceso, no solo por la etiqueta del archivo. Pozos pueden ser unidades de asignación de un reactivo, pero un solo donante no representa variabilidad entre donantes.

## 5. Tiempo, destrucción y reutilización

Mediciones repetidas de una persona no aumentan el número de personas asignadas. Pueden aumentar información sobre trayectorias si el modelo recoge la correlación.

En muestreo destructivo, cada momento puede usar organismos distintos. Aun así, si proceden de la misma parcela tratada, siguen compartiendo la asignación de parcela. Si cada organismo recibió tratamiento individual y se asignó además al momento de sacrificio, la estructura es diferente y debe registrarse.

Reutilizar una cámara en varios períodos puede generar nuevas asignaciones cámara-período si hay reinicio, lavado y secuencias adecuadas. No supongas independencia: considerá efecto persistente de cámara, período y arrastre. Repetir una lectura sin reiniciar el sistema es medición técnica.

## 6. Qué hacer ante pseudorreplicación

1. Reconstruí qué se asignó realmente y recuperá identificadores de unidades superiores.
2. Contá unidades por tratamiento, bloque, período y estrato; buscá confusión perfecta.
3. Si hay replicación real, agregá o ajustá un modelo jerárquico coherente con el estimando.
4. Si falta replicación del tratamiento, limitá la inferencia y proponé nuevas asignaciones cuando sea viable.
5. Documentá el cambio respecto del plan, sin presentar el rediseño analítico como corrección total del experimento.

Una cámara por temperatura permite describir esas cámaras bajo esas condiciones, pero no separar temperatura de diferencias propias de cámara sin supuestos adicionales fuertes. Ni un efecto aleatorio ni un bootstrap de plantas resuelven esa confusión.

## 7. Salida que debe quedar escrita

«La unidad experimental para [factor] será [entidad]. Se asignarán [n] unidades a cada [condición], mediante [procedimiento]. En cada unidad se medirán [submuestras] en [momentos]. Estas observaciones se [resumirán/modelarán] considerando [dependencia]. La inferencia se referirá a [población y condiciones].»

Comprobá que estos números coincidan con la asignación y con `tamano-muestral.md`. Para dos niveles de asignación, completá la declaración una vez por factor.
