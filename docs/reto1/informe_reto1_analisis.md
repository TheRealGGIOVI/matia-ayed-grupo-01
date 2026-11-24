# Análisis Cuantitativo y Estadístico · Reto 1

> **Proyecto:** MatIA · Datos de instrumental quirúrgico con Python y Bash
> **Asignatura:** Algoritmos y Estructura de Datos · 2.º Grado en Computación e Inteligencia Artificial · UAX Mare Nostrum · ULAB MatIA
> **Grupo:** Grupo 01
> **Integrantes:** Pablo Picón, Francisco Jiménez y Giovanni Giove

## 1. Resumen ejecutivo

El presente documento recoge el análisis estadístico, algorítmico y de calidad de datos derivado de la ejecución del Reto 1 (`retos/reto1_contar.py`) sobre el conjunto de datos real del hospital (**208 registros** en la hoja `Materiales`, sin depuración previa).

### Indicadores clave (KPIs)

| Indicador                                                |  Valor obtenido  | Interpretación                                               |
| :------------------------------------------------------- | :---------------: | :------------------------------------------------------------ |
| **Volumen total analizado ($n$)**                | `208` registros | Población completa de la hoja `Materiales`                 |
| **Integridad de clave primaria (`id_material`)** |   `100,00 %`   | 0 vacíos y 0 duplicados                                      |
| **Completitud de `codigo_material`**             |    `99,04 %`    | 2 registros sin código (`0,96 %`)                          |
| **Completitud de `Descripcion_material_hqsmlg`** |    `87,50 %`    | 26 registros vacíos (`12,50 %`)                            |
| **Reducción global de operaciones**               |    `99,60 %`    | 624 pasos (`dict`) frente a 155.518 comparaciones (ingenuo) |
| **Aceleración temporal ($N = 10.400$)**         |   `315,60×`   | `0,0015 s` frente a `0,4734 s` (`99,68 %` menos tiempo) |
| **Concentración del Top 10 de categorías**       |    `45,67 %`    | 95 de los 208 registros se concentran en 10 entradas          |

---

## 2. Perfilado estadístico de las columnas

A continuación se desglosa la estructura de cardinalidad, completitud y unicidad de las tres columnas evaluadas sobre $n = 208$ registros:

| Columna                         | Registros no vacíos | Completitud (%) | Vacíos | Tasa de vacíos (%) | Valores distintos (no vacíos) | Tasa de unicidad* (%) |        Valores repetidos        |
| :------------------------------ | :------------------: | :-------------: | :-----: | :-----------------: | :----------------------------: | :-------------------: | :-----------------------------: |
| `id_material`                 |         208         |  `100,00 %`  |    0    |     `0,00 %`     |              208              |     `100,00 %`     |         0 (`0,00 %`)         |
| `codigo_material`             |         206         |   `99,04 %`   |    2    |     `0,96 %`     |              206              |     `100,00 %`     |         0 (`0,00 %`)         |
| `Descripcion_material_hqsmlg` |         182         |   `87,50 %`   |   26   |     `12,50 %`     |               79               |      `43,41 %`      | 29 (`36,71 %` de categorías) |

*\*Tasa de unicidad calculada como $\text{Valores distintos} / \text{Registros no vacíos}$.*

### Lectura analítica por columna

1. **`id_material` (clave primaria perfecta):** presenta un `100,00 %` de completitud y un `100,00 %` de unicidad. Actúa como identificador fiable para cruzar tablas en retos posteriores.
2. **`codigo_material` (casi completo, sin colisiones):** alcanza un `99,04 %` de completitud. Los 206 códigos presentes son todos únicos (`0` duplicados), pero existen **2 registros (`0,96 %`)** carentes de código, lo que impedirá su cruce directo con el inventario de imágenes en el Reto 5 si no se subsanan.
3. **`Descripcion_material_hqsmlg` (alta dispersión y vacíos relevantes):**
   - De las **79 categorías distintas** no vacías, **29 categorías (`36,71 %`)** aparecen más de una vez, mientras que **50 categorías (`63,29 %`)** son *singletons* (aparecen exactamente una vez).
   - La densidad media es de **$2{,}30$ registros por categoría no vacía** ($182 / 79$).
   - El **`12,50 %`** de la tabla (1 de cada 8 registros) carece de descripción de categoría.

---

## 3. Análisis de complejidad y eficiencia algorítmica

El reto compara el recuento ingenuo basado en listas (`contar_ingenuo`) con el recuento mediante tabla hash (`contar_diccionario`).

### 3.1. Comparativa de operaciones elementales ($n = 208$)

| Columna                         | Valores distintos ($k$)* | Comparaciones (ingenuo) | Pasos (diccionario) |  Factor de reducción  | Ahorro de operaciones (%) |
| :------------------------------ | :------------------------: | :---------------------: | :-----------------: | :--------------------: | :-----------------------: |
| `id_material`                 |            208            |         64.792         |         208         |      `311,50×`      |        `99,68 %`        |
| `codigo_material`             |            207            |         64.558         |         208         |      `310,38×`      |        `99,68 %`        |
| `Descripcion_material_hqsmlg` |             80             |         26.168         |         208         |      `125,81×`      |        `99,21 %`        |
| **Total acumulado**       |             —             |    **155.518**    |    **624**    | **`249,23×`** |   **`99,60 %`**   |

*\*Incluyendo la cadena vacía `""` cuando está presente en la columna.*

### 3.2. Verificación matemática del coste

En el peor caso (cuando todos los elementos son distintos, como en `id_material` con $n = k = 208$), `contar_ingenuo` ejecuta dos fases:

1. **Construcción de la lista de distintos:** $\sum_{i=0}^{n-1} i = \frac{n(n-1)}{2} = \frac{208 \times 207}{2} = 21.528\text{ comparaciones}$.
2. **Recuento por cada elemento distinto:** $k \times n = 208 \times 208 = 43.264\text{ comparaciones}$.

$$
\text{Total teórico} = 21.528 + 43.264 = 64.792\text{ comparaciones}
$$

El valor teórico coincide **al 100 %** con el medido empíricamente (`64.792`). Por el contrario, `contar_diccionario` mantiene un coste estrictamente lineal $O(n) = 208$ pasos, completamente invariante respecto a la cardinalidad $k$.

### 3.3. Benchmark temporal y tasa de procesamiento ($N = 10.400$)

Al escalar la columna `codigo_material` por un factor de 50 ($N = 208 \times 50 = 10.400$ elementos):

| Métrica                                       |      Algoritmo ingenuo      |   Algoritmo diccionario   |       Diferencia / Mejora       |
| :--------------------------------------------- | :-------------------------: | :-----------------------: | :------------------------------: |
| **Tiempo total de ejecución**           | `0,4734 s` (`473,4 ms`) | `0,0015 s` (`1,5 ms`) | **`-99,68 %` de tiempo** |
| **Factor de aceleración (*speedup*)** |      `1,00×` (base)      |  **`315,60×`**  |     315,6 veces más rápido     |
| **Tiempo medio por elemento**            |        `45,52 µs`        |       `0,14 µs`       |    `~316×` menor latencia    |
| **Rendimiento (*throughput*)**         |      `21.969 elem/s`      |   `6.933.333 elem/s`   |        `+6,91 M elem/s`        |

---

## 4. Distribución de frecuencias y análisis de concentración (Top 10)

El análisis de las 10 categorías más frecuentes de `Descripcion_material_hqsmlg` (tal como figuran en el Excel sin depurar) revela una fuerte concentración:

| Pos. | Categoría (sin depurar)         |  Frecuencia  | % sobre total ($n=208$) |  % sobre no vacíos ($n=182$)  |  % acumulado (total)  | Observación de calidad        |
| :--: | :------------------------------- | :-----------: | :-----------------------: | :-------------------------------: | :--------------------: | :----------------------------- |
|  1  | `(vacía)`                     |      26      |        `12,50 %`        |                —                |      `12,50 %`      | Dato ausente                   |
|  2  | `«PORTA»`                    |      13      |        `6,25 %`        |            `7,14 %`            |      `18,75 %`      | Categoría válida             |
|  3  | `«CLAN VASCULAR»`            |      10      |        `4,81 %`        |            `5,49 %`            |      `23,56 %`      | Probable errata (*CLAMP*)    |
|  4  | `«PINZA »`                   |       8       |        `3,85 %`        |            `4,40 %`            |      `27,40 %`      | Espacio final sobrante         |
|  5  | `«KOCHER CURVO S/D»`         |       8       |        `3,85 %`        |            `4,40 %`            |      `31,25 %`      | Categoría válida             |
|  6  | `«DISECTOR»`                 |       7       |        `3,37 %`        |            `3,85 %`            |      `34,62 %`      | Categoría válida             |
|  7  | `«CLAN INTESTINAL»`          |       7       |        `3,37 %`        |            `3,85 %`            |      `37,98 %`      | Probable errata (*CLAMP*)    |
|  8  | `«SONDA ACANALADA»`          |       6       |        `2,88 %`        |            `3,30 %`            |      `40,87 %`      | Categoría válida             |
|  9  | `«TIJERAS MEC»`              |       5       |        `2,40 %`        |            `2,75 %`            |      `43,27 %`      | Categoría válida             |
|  10  | `«KOCHER RECTO C/D»`         |       5       |        `2,40 %`        |            `2,75 %`            |      `45,67 %`      | Categoría válida             |
|  —  | **Subtotal Top 10**        | **95** |   **`45,67 %`**   | **`37,91 %`** *(Top 9)* | **`45,67 %`** | —                             |
|  —  | **Resto (70 categorías)** | **113** |   **`54,33 %`**   |       **`62,09 %`**       | **`100,00 %`** | Media: `1,61` reg/categoría |

### Interpretación de la distribución

- **Efecto cola larga (*long tail*):** excluyendo los vacíos, las 9 categorías principales (`11,39 %` de las 79 categorías distintas) concentran **69 registros (`37,91 %` de los datos etiquetados)**, mientras que las 70 categorías restantes (`88,61 %`) se reparten los otros 113 registros con una media de apenas `1,61` piezas por categoría.
- **Impacto directo en el entrenamiento de visión artificial (MatIA):** esta distribución altamente desbalanceada (con `63,29 %` de categorías apareciendo una sola vez) anticipa un reto de clases minoritarias si se entrena un modelo directamente sobre las descripciones sin agrupar o depurar.

---

## 5. Cuantificación preliminar de incidencias de calidad de datos

Incluso antes de ejecutar el Reto 2 (depuración y normalización), el recuento del Reto 1 permite cuantificar incidencias concretas visibles solo en el resumen y el Top 10:

| Tipo de incidencia detectada                                      | Registros afectados | % sobre total ($n=208$) | Impacto esperado                                          |
| :---------------------------------------------------------------- | :-----------------: | :-----------------------: | :-------------------------------------------------------- |
| Categorías vacías en `Descripcion_material_hqsmlg`            |         26         |        `12,50 %`        | Pérdida de etiqueta de clase                             |
| Posibles erratas tipográficas (`CLAN` por `CLAMP` en Top 10) |         17         |        `8,17 %`        | Fragmentación artificial de categorías                  |
| Espacios sobrantes al final (`«PINZA »`)                      |          8          |        `3,85 %`        | Duplicación de clases al comparar cadenas                |
| Códigos vacíos en `codigo_material`                           |          2          |        `0,96 %`        | Imposibilidad de cruce con imágenes                      |
| **Total mínimo observable en el Reto 1**                   |    **51***    |   **`24,52 %`**   | **Al menos 1 de cada 4 filas requiere depuración** |

*\*Cota inferior considerando únicamente los defectos visibles en el Top 10 de `Descripcion_material_hqsmlg` (`26 + 17 + 8 = 51`), sin sumar posibles solapamientos con los 2 códigos vacíos ni erratas en las 70 categorías restantes.*

---

## 6. Conclusiones y próximos pasos

1. **Eficiencia demostrada:** la sustitución de búsquedas lineales en listas por un diccionario reduce las operaciones en un **`99,60 %`** y multiplica la velocidad por **`315,6×`**, garantizando que la herramienta escale sin cuellos de botella.
2. **Fiabilidad estructural:** la ausencia total de duplicados en `id_material` y `codigo_material` confirma una base sólida para los índices del Reto 3.
3. **Prioridad inmediata para el Reto 2:** con al menos un **`24,52 %`** de registros presentando vacíos, espacios residuales o erratas visibles ya en el Top 10, la normalización de cadenas y la detección de similitud léxica del Reto 2 resultan imprescindibles antes de obtener estadísticas definitivas del inventario.
