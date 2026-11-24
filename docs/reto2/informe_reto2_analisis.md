# Análisis Cuantitativo y Estadístico · Reto 2

> **Proyecto:** MatIA · Datos de instrumental quirúrgico con Python y Bash  
> **Asignatura:** Algoritmos y Estructura de Datos · 2.º Grado en Computación e Inteligencia Artificial · UAX Mare Nostrum · ULAB MatIA  
> **Grupo:** Grupo 01  
> **Integrantes:** Pablo Picón, Francisco Jiménez y Giovanni Giove  
> **Documento complementario:** [informe_reto2.md](./informe_reto2.md)

---

## 1. Resumen ejecutivo

Este informe presenta el análisis numérico, estadístico y algorítmico de la fase de depuración (`retos/reto2_depurar.py` y `herramienta/normalizar.py`) aplicada a los **208 registros** reales de la hoja `Materiales`.

### Indicadores clave (KPIs)

| Indicador | Valor obtenido | Porcentaje / Referencia |
| :--- | :---: | :---: |
| **Códigos normalizados con cambio efectivo** | `1` de `206` | `0,49 %` de los códigos no vacíos |
| **Códigos conformes al patrón de fabricante** | `191` de `206` | `92,72 %` de los códigos no vacíos |
| **Códigos con formato atípico** | `15` de `206` | `7,28 %` de los códigos no vacíos |
| **Fusiones automáticas de categorías por normalización** | `0` de `79` | `0,00 %` de reducción de cardinalidad |
| **Comparaciones por pares (`SequenceMatcher`)** | `3.081` | Exactamente $\frac{79 \times 78}{2}$ |
| **Parejas por encima del umbral ($\ge 0{,}85$)** | `16` de `3.081` | `0,52 %` de tasa de detección |
| **Falsos positivos (instrumentos distintos)** | `9` de `16` | `56,25 %` de las alertas generadas |
| **Descripciones exactas repetidas** | `1` grupo (`2` IDs) | `0,96 %` de los registros (`2 / 208`) |

---

## 2. Impacto cuantitativo de la normalización

| Dimensión evaluada | Antes | Después | Variación absoluta | Variación relativa (%) |
| :--- | :---: | :---: | :---: | :---: |
| Códigos distintos (sin vacíos) | 206 | 206 | `0` | `0,00 %` |
| Códigos vacíos | 2 | 2 | `0` | `0,00 %` |
| Códigos repetidos | 0 | 0 | `0` | `0,00 %` |
| Categorías distintas | 79 | 79 | `0` | `0,00 %` |
| Materiales sin categoría | 26 | 26 | `0` | `0,00 %` |

### Interpretación estadística

- Aunque la cardinalidad neta no disminuye (`0,00 %` de variación), la normalización **sí corrige suciedad latente**: el registro `matcg000108` (`'BN012R '` $\rightarrow$ `BN012R`) habría fallado cualquier búsqueda exacta por clave en el Reto 3 o Reto 5.
- Del mismo modo, en categorías como `«PINZA »` (detectada en el Reto 1), la ausencia de fusiones (`0` grupos con múltiples variantes) indica que la cadena con espacio sobrante no coexistía con una versión limpia `«PINZA»`, por lo que al limpiarla mantiene el mismo conteo pero queda homogénea.

---

## 3. Análisis de conformidad de `codigo_material`

Sobre los **206 códigos no vacíos** (`99,04 %` de la tabla), la función `es_codigo_fabricante` clasifica los formatos de la siguiente manera:

| Tipo de formato | Cantidad | % sobre códigos no vacíos (`206`) | % sobre total (`208`) | Ejemplos |
| :--- | :---: | :---: | :---: | :--- |
| **Patrón estándar** (`LLNNN L[N]`) | 191 | `92,72 %` | `91,83 %` | `BN012R` |
| **Numéricos puros (7–8 dígitos)** | 7 | `3,40 %` | `3,37 %` | `83930072`, `8393184`, `8394933` |
| **Serie numérica larga con guion** | 4 | `1,94 %` | `1,92 %` | `40653405059-319` … `-456` |
| **Alfanuméricos / compuestos con guion o espacio** | 2 | `0,97 %` | `0,96 %` | `1-1010 202210171`, `RU4580-40` |
| **Alfabéticos / cortos no estándar** | 2 | `0,97 %` | `0,96 %` | `CONMED`, `SRNH1` |
| **Vacíos** | 2 | — | `0,96 %` | `""` |

### Lectura analítica

- Un **`7,28 %`** de los códigos no vacíos (`15` referencias) se aparta del patrón habitual de fabricante.
- El subgrupo más numeroso dentro de las anomalías son los **códigos puramente numéricos (`7` casos, `46,67 %` de los atípicos)** y la **serie `40653405059-XXX` (`4` casos, `26,67 %` de los atípicos)**, que en conjunto explican el **`73,33 %`** de todos los formatos no estándar.
- Especial atención merece `CONMED` (nombre comercial de fabricante en lugar de referencia de pieza) y `1-1010 202210171` (posible concatenación de código y fecha `20221017`), que requieren revisión antes de cruzar con los nombres de archivo de las imágenes.

---

## 4. Análisis algorítmico y estadístico de `parecidas()`

### 4.1. Complejidad combinatoria verificada

Con $k = 79$ categorías distintas no vacías, el bucle triangular (`for i ... for j in range(i + 1, k)`) evita comparar elementos consigo mismos y evita duplicar pares $(a, b)$ y $(b, a)$:

$$\text{Comparaciones} = \binom{k}{2} = \frac{k(k-1)}{2} = \frac{79 \times 78}{2} = 3.081$$

El coste es cuadrático respecto a la cardinalidad $O(k^2)$, lo que en este conjunto supone **3.081 evaluaciones** de `SequenceMatcher`.

### 4.2. Distribución de las 16 parejas detectadas ($\text{umbral} \ge 0{,}85$)

| Clasificación analítica | Parejas | % sobre alertas (`16`) | Rango de similitud | Media de similitud |
| :--- | :---: | :---: | :---: | :---: |
| **Instrumentos distintos (falsos positivos)** | 9 | `56,25 %` | `0,86 – 0,97` | `0,916` |
| **Ambiguos (requieren validación clínica)** | 4 | `25,00 %` | `0,86 – 0,90` | `0,880` |
| **Variantes / erratas probables (verdaderos positivos)** | 3 | `18,75 %` | `0,88 – 0,95` | `0,927` |
| **Total de alertas** | **16** | **`100,00 %`** | **`0,86 – 0,97`** | **`0,909`** |

### 4.3. Desglose por tramo de similitud

| Tramo de `ratio()` | Cantidad de parejas | % sobre `16` | Observación |
| :--- | :---: | :---: | :--- |
| `[0,95 – 1,00]` | 4 | `25,00 %` | Mezcla de 2 falsos positivos (`MANGO BISTURI 4/4L` `0,97`, `PINZA DISECCION C/D–S/D` `0,95`) y 2 variantes (`TIJERA(S) MAR/MEC` `0,95`) |
| `[0,90 – 0,94]` | 6 | `37,50 %` | 4 falsos positivos y 2 ambiguos (`TIJERA MAC` vs `MAR`/`MEC`) |
| `[0,85 – 0,89]` | 6 | `37,50 %` | 3 falsos positivos, 2 ambiguos y 1 variante (`PINZA BAKEY` / `DE BAKEY`) |

> **Hallazgo clave de precisión:** elevar el umbral de `0,85` a `0,95` **no eliminaría los falsos positivos**, ya que la pareja con mayor similitud de toda la tabla (`MANGO BISTURI 4` vs `MANGO BISTURI 4L`, con `0,97`) corresponde a dos instrumentos distintos. Esto demuestra cuantitativamente que la similitud léxica por sí sola tiene una **precisión estimada de entre el `18,75 %` y el `43,75 %`** (según cómo se resuelvan los 4 casos ambiguos) y debe utilizarse únicamente como filtro de apoyo a la decisión humana.

---

## 5. Conclusiones y recomendaciones para los siguientes retos

1. **Tasa de falsos positivos alta (`56,25 %`):** cualquier unificación automática basada únicamente en `SequenceMatcher` corrompería el catálogo al fusionar piezas con/sin dientes (`C/D` vs `S/D`) o calibres distintos (`3`, `4`, `4L`).
2. **Anomalías ocultas a la similitud por pares:** en la propia salida aparecen `KOTCHER RECTO MED` y `KOTCHER RECTO PEQ`, evidenciando la errata `KOTCHER` (por `KOCHER`) que el algoritmo solo empareja entre sí por tamaño, no contra `KOCHER RECTO C/D` (al diferir en más caracteres).
3. **Preparación para el Reto 3 y Reto 5:** la normalización de códigos y la identificación previa de los **15 códigos atípicos** (`7,28 %`) y de la descripción duplicada (`matcg000010` y `matcg000013`) permiten anticipar posibles incidencias de cruce en las hojas de cajas y en el inventario de imágenes.
