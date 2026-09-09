# Agronomía, ambiente y laboratorio

## 1. Preguntas de entrada

Identificá material, escala de aplicación, heterogeneidad espacial o temporal, recursos compartidos y variable principal. Preguntá por campañas, sitios, lotes, cámaras, bandejas, días y operadores antes de contar muestras.

En ambiente, verificá si se interviene o solo se seleccionan sitios expuestos. Comparar un sitio contaminado con uno de referencia no es un experimento aleatorizado, aunque se extraigan muchas muestras.

## 2. Unidad según la aplicación

| Intervención | Unidad candidata | Observaciones internas |
|---|---|---|
| Fertilizante aplicado a parcela | Parcela | Plantas, hojas o puntos de suelo |
| Riego por sector | Sector con asignación propia | Surcos y plantas |
| Solución por circuito hidropónico | Circuito | Plantas conectadas |
| Temperatura por cámara | Cámara o cámara-período con diseño válido | Bandejas y organismos |
| Reactivo aplicado a preparaciones independientes | Preparación o recipiente asignado | Lecturas instrumentales |
| Remediación de cuerpos de agua | Cuerpo de agua asignado | Estaciones, profundidades y fechas |

La unidad depende del protocolo real. Una maceta por planta puede ser unidad si recibe tratamiento propio; varias macetas que comparten un baño tratado pueden estar agrupadas para ese factor. Los duplicados analíticos estiman error de medición, no variación entre unidades tratadas.

## 3. Campo y heterogeneidad espacial

Mapeá pendiente, fertilidad, sombra, drenaje y antecedentes antes de asignar. En un DBCA se busca que cada bloque sea internamente comparable y contenga todos los tratamientos. La orientación se decide según la geometría del gradiente, no mediante una regla única sobre puntos cardinales.

Si los tratamientos son demasiados para bloques compactos, considerá bloques incompletos conectados, diseños fila-columna o ajuste espacial. Medir una covariable basal puede mejorar precisión, pero no elimina una asignación confundida con ubicación.

Predefiní tamaño de parcela, área útil, borduras, caminos y distancias para limitar deriva, sombreado o movimiento de agua. No fijes metros universales: fundamentá según cultivo, intervención y mecanismo de interferencia. Registrá coordenadas o posiciones de todas las unidades.

**Ejemplo de decisión.** Un factor riego aplicado por sector puede usar sectores organizados en bloques. Si además se aleatorizan variedades dentro de cada sector, se obtiene un arreglo de parcelas divididas. El n para riego es el de sectores asignados, no el de variedades o plantas.

## 4. Invernadero y cámaras

Temperatura, luz y ventilación pueden variar por estante y posición. Distribuí tratamientos entre esas condiciones o bloqueá antes de asignar. Rotar macetas puede reducir exposición desigual, pero exige un calendario predefinido y registro; no sustituye replicar tratamientos a la escala correcta.

Una cámara por temperatura confunde ambos efectos. Opciones: más cámaras asignadas, repetición en períodos con reasignación y reinicio adecuados, o limitar el objetivo a descripción. Reutilizar cámaras exige considerar persistencia, período y arrastre.

Si se aplican varios tratamientos dentro de una cámara, esta puede ser bloque para esos tratamientos, pero no réplica de un factor constante para toda la cámara. Dibujá los niveles antes de elegir el modelo mixto.

## 5. Laboratorio y control de calidad

Distribuí tratamientos entre días, lotes de reactivo, placas y operadores cuando sea posible. Evitá procesar todos los controles un día y todos los tratados otro. Aleatorizá el orden de preparación o lectura dentro de restricciones de seguridad y calibración.

Documentá blancos, controles positivos, materiales de referencia, curvas de calibración y criterios de aceptación según el ensayo. Un blanco analítico detecta contaminación o fondo; no sustituye un grupo comparador experimental.

Predefiní qué se hace si falla una placa o corrida: repetición completa, repetición selectiva por criterio técnico o resultado faltante. Repetir únicamente resultados inesperados hasta obtener lo deseado introduce selección.

Registrá límites de detección y cuantificación. Un valor por debajo del límite es censurado, no necesariamente cero. Elegí un tratamiento analítico acorde a la proporción censurada y al estimando; no reemplaces siempre por la mitad del límite.

## 6. Muestreo y respuestas

Una muestra compuesta mezcla material de varios puntos y puede estimar el promedio de una parcela, pero pierde información sobre variación interna. Si se desea esa variación, conservá muestras separadas con identificadores y modelá su agrupación.

Para cosechas sucesivas, definí si el objetivo es rendimiento acumulado o trayectoria. La primera opción puede resumirse por parcela; la segunda requiere dependencia temporal. Muestreo destructivo de plantas distintas no elimina el agrupamiento por parcela tratada.

| Respuesta | Información imprescindible | Análisis candidato |
|---|---|---|
| Rendimiento continuo | Área útil, humedad de referencia y unidad | Modelo lineal o mixto según diseño |
| Germinación | Semillas germinadas y total evaluado | Binomial, con agrupamiento o sobredispersión si procede |
| Insectos por trampa | Tiempo activa, esfuerzo y ubicación | Conteo con exposición y dependencia |
| Concentración | Unidad, recuperación y censura | Modelo continuo o censurado pertinente |
| Cobertura porcentual | Método de estimación y naturaleza de la proporción | Familia acorde, no binomial automática |

No transformes porcentajes por arcoseno ni conteos por raíz de forma rutinaria. La distribución, el denominador y la estructura experimental guían la elección.

## 7. Sitios y campañas

Varias parcelas de un sitio replican asignaciones dentro de ese sitio, pero no hacen representativa una sola campaña. Para generalizar a sitios o años, justificá su selección y representá variación tratamiento×ambiente cuando sea pertinente.

En evaluaciones ambientales antes-después con control, describí estructura BACI, sitios de impacto y referencia, períodos y autocorrelación. El contraste temporal diferencial puede fortalecer evidencia, pero pocos sitios y ausencia de aleatorización limitan causalidad. Ver `../cuasiexperimentales.md`.

## 8. Dimensionamiento y entrega

Dimensioná el contraste con varianza de parcelas, cámaras o lotes, no con la variación de lecturas técnicas. Para parcelas divididas necesitás componentes de ambos estratos; aumentar plantas por sector no sustituye más sectores.

Entregá plano y CSV concordantes, identificadores jerárquicos, calendario, protocolo de muestreo, criterios de calidad, permisos y manejo de residuos. Comprobá que el croquis conserve todas las parcelas grandes y subparcelas. Las guías generales de unidad y análisis están en `../unidad-experimental.md` y `../plan-de-analisis.md`.
