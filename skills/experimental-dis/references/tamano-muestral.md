# Tamaño muestral y precisión

## 1. Elegir qué se dimensiona

El tamaño depende del objetivo, no del nombre general del diseño. Definí población, respuesta principal, momento, estimando, contraste y unidad independiente antes de calcular.

| Objetivo | Criterio de dimensionamiento |
|---|---|
| Superioridad | Potencia para una diferencia científicamente relevante |
| Estimación | Ancho o semiancho esperado del intervalo de confianza |
| Equivalencia o no inferioridad | Margen justificado y prueba específica |
| Piloto de factibilidad | Precisión de reclutamiento, adherencia, variabilidad o viabilidad |
| Presupuesto fijo | Precisión y efecto detectable bajo escenarios explícitos |

Alfa = 0,05 y potencia = 0,80 son elecciones habituales, no leyes. Justificá unilateralidad antes de observar resultados. Una comparación no significativa no demuestra equivalencia. No calcules «potencia observada» usando el efecto estimado como sustituto del intervalo de confianza.

## 2. Insumos y procedencia

Registrá diferencia de interés en unidades originales, desvío estándar en el nivel correcto, correlación si hay pares o grupos, proporciones basales si corresponde, asignación entre grupos, pérdidas y multiplicidad. Para cada valor anotá fuente, población, método de medición y compatibilidad con el ensayo previsto.

Un piloto pequeño produce una estimación incierta del desvío. Usá escenarios, no solo su estimación puntual. No confundas error estándar con desvío estándar. Si solo hay CV, `sd = |media|·CV/100` requiere una escala y media pertinentes; cerca de cero el CV puede ser inadecuado.

La diferencia mínima relevante proviene de la decisión científica o práctica. No la elijas retrospectivamente para que el n entre en el presupuesto ni uses automáticamente el efecto grande de un estudio publicado pequeño.

## 3. Casos simples y comandos

Desde el directorio de la skill, verificá primero `python scripts/tamano_muestral.py --help`. El script requiere `scipy`; no representa todos los diseños. Los siguientes valores son ejemplos de uso, no supuestos recomendados.

```bash
python scripts/tamano_muestral.py --caso dos-medias --dme 5 --sd 8 --potencia 0.80
python scripts/tamano_muestral.py --caso medias-pareadas --dme 4 --sd-dif 6
python scripts/tamano_muestral.py --caso anova --grupos 4 --dme 2.5 --sd 3
python scripts/tamano_muestral.py --caso dos-proporciones --p1 0.30 --p2 0.55
python scripts/tamano_muestral.py --caso correlacion --r 0.40
```

**Dos medias.** Para grupos independientes balanceados, varianza común y prueba bilateral, una aproximación orientativa es `n ≈ 2(z_(1-alfa/2)+z_potencia)^2·sd^2/delta^2` por grupo. El cálculo con t no central incorpora los grados de libertad. Desigualdad de varianzas, asignación desigual o ajustes requieren otro planteamiento.

**Medias pareadas.** n cuenta pares completos. Usá el desvío de las diferencias, no el de una medición aislada. En general, `sd_dif^2 = sd_1^2 + sd_2^2 - 2·rho·sd_1·sd_2`. La expresión `sd·sqrt(2(1-rho))` supone desvíos marginales iguales. No omitas rho esperando que el programa adivine la correlación.

**Proporciones y correlación.** La implementación auditada usa aproximaciones mediante arcoseno y z de Fisher, respectivamente. Con eventos raros o n pequeño, comprobá precisión con un método específico o simulación. La correlación de Pearson contra cero presupone observaciones independientes y condiciones acordes al modelo; no cubre correlaciones repetidas ni comparación de correlaciones.

## 4. Qué significa la potencia ANOVA

Para k grupos balanceados de una vía con varianza residual común:

`f^2 = sum((mu_i - mu_global)^2)/(k·sd^2)`

La prueba global contrasta igualdad de todas las medias. Su potencia depende del vector completo de medias, no solo de la distancia entre dos de ellas.

En la implementación auditada, dos medias están separadas por `delta = --dme` y las otras k-2 se sitúan en su punto medio. De allí sale `f = delta/(sd·sqrt(2k))`, con no centralidad `lambda = k·n·f^2`. Explicitá ese escenario al usar la salida; no lo atribuyas a una convención universal de otro programa.

Detectar alguna diferencia global no garantiza potencia para una comparación tratamiento-control ni para todas las comparaciones por pares. Si ese contraste es el objetivo, dimensioná su prueba y su ajuste de multiplicidad. La corrección por comparaciones puede cambiar el n.

## 5. Diseños que requieren más información

| Estructura | Parámetros adicionales | Procedimiento razonable |
|---|---|---|
| DBCA o ANCOVA | Varianza residual tras ajuste, bloques, covariables y grados de libertad | Potencia del contraste bajo el modelo previsto |
| Factorial | Medias por combinación o coeficientes, interacción objetivo | Potencia del contraste factorial específico |
| Parcelas divididas | Parcelas grandes por nivel, subparcelas y varianzas de ambos estratos | Modelo mixto o simulación con doble asignación |
| Conglomerados | Número y tamaño de grupos, ICC, desigualdad de tamaños | Método para ensayos por conglomerados |
| Medidas repetidas | Tiempos, correlaciones, trayectoria, pérdidas | Modelo longitudinal o simulación |
| Cruzado | Diferencias intraunidad, períodos, secuencias y arrastre | Método específico para el diseño cruzado |

No existe un porcentaje fijo de ahorro por bloquear. Usar una sd residual plausible puede orientar, pero el cálculo debe respetar los grados de libertad y el estimando. No presentes un ANOVA independiente como potencia exacta de DBCA.

Para conglomerados de igual tamaño m, `DE ≈ 1+(m-1)·ICC` es una aproximación de efecto de diseño bajo condiciones simples. No basta con multiplicar n individual si quedan muy pocos conglomerados, hay tamaños desiguales, ajuste basal o un contraste diferente. Más individuos dentro del mismo grupo no reemplazan ilimitadamente nuevos grupos.

## 6. Simulación reproducible

1. Fijá parámetros generadores: efecto relevante, componentes de varianza, correlación, distribución y faltantes.
2. Generá unidades según el diseño, incluidos bloques y los niveles de asignación.
3. Aplicá exactamente el modelo y contraste previstos, con multiplicidad cuando corresponda.
4. Repetí para cada tamaño y escenario; registrá semilla, versiones, convergencia y fallos.
5. Estimá potencia como fracción de rechazos y acompañala de incertidumbre Monte Carlo.

Con B simulaciones y potencia estimada p, el error estándar Monte Carlo es aproximadamente `sqrt(p(1-p)/B)`. Elegí B según la precisión deseada. No elimines silenciosamente ajustes fallidos: informá su frecuencia y una regla de tratamiento. Comprobá también error tipo I bajo efecto nulo y cobertura si el objetivo es estimación.

## 7. Pérdidas, redondeo y viabilidad

Si q es la fracción prevista de pérdidas, `n_reclutar = ceil(n_analizable/(1-q))`. Aplicá el ajuste en el nivel donde ocurre la pérdida y redondeá por grupo o por bloque completo, respetando el esquema de asignación. El total debe coincidir con la suma de los grupos; verificá las cifras del programa.

Pérdida de un conglomerado no equivale a pérdida de un individuo. En pares, estimá la probabilidad de disponer del resultado necesario en ambos momentos. Inflar n no corrige sesgo por abandono informativo.

Si no hay estimación fiable, presentá una tabla con varios efectos y desvíos plausibles, claramente marcados como supuestos. Con presupuesto fijo, describí lo que puede estimarse y qué incertidumbre persistirá. No inventes datos previos ni bibliografía.

## 8. Párrafo y trazabilidad

«Se dimensionó [contraste] para detectar [delta y unidad], con [variabilidad y fuente], alfa [valor], potencia [valor] y asignación [razón]. Se asumió [dependencia y distribución]. Mediante [método, software y versión] se estimaron [unidades analizables por nivel]. Se previó [pérdida y fundamento], por lo que se incorporarán [unidades finales]. Se evaluó sensibilidad a [escenarios].»

Documentación de las distribuciones usadas: [t no central de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nct.html) y [F no central de SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ncf.html). Estas páginas documentan funciones numéricas; no validan por sí mismas el diseño aplicado.
