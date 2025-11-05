# Sistema de Análisis Estadístico COVID-19 y Censo Nacional 2022 – Argentina

Este proyecto implementa un sistema de análisis estadístico desarrollado en **Python**, orientado al procesamiento y estudio de datos de **COVID-19** en Argentina, complementados con información demográfica del **Censo Nacional 2022**.  
El objetivo es evaluar patrones epidemiológicos, distribución etaria, diferencias por sexo y proporciones relativas a la población provincial.

---

## 1. Descripción General

El sistema automatiza las siguientes tareas:

- Creación y administración de una base de datos **SQLite**.
- Carga de datos desde archivos CSV sanitarios y censales.
- Ejecución de consultas estadísticas sobre mortalidad y contagios.
- Análisis de distribución etaria y diferencias por sexo.
- Presentación de resultados por consola a través de un menú interactivo.

---

## 2. Requerimientos

### Software
- Python **3.x**
- Consola **CMD / PowerShell (Windows)**  
  *(usa `os.system("cls")` para limpiar la pantalla)*
- SQLite3 (incluido en Python)

### Archivos requeridos

| Archivo | Descripción |
|----------|-------------|
| `TpEst.py` | Script principal del sistema |
| `Covid19_limpio.csv` | Datos depurados de casos COVID-19 |
| `c2022_tp_c_resumen.csv` | Datos del Censo Nacional 2022 |
| `C19Casos.db` | Base de datos SQLite generada automáticamente |

---

## 3. Estructura de la Base de Datos

### Tabla `C19` – Casos COVID-19
| Campo | Tipo | Descripción |
|--------|------|-------------|
| `Sexo` | TEXT | Sexo del paciente (F / M) |
| `Edad` | INTEGER | Edad del paciente |
| `Provincia_Res` | TEXT | Provincia de residencia |
| `Fallecido` | TEXT | Indica si el paciente falleció (SI / NO) |
| `Confirmados` | TEXT | Estado del caso confirmado |

### Tabla `C22` – Censo 2022
| Campo | Tipo | Descripción |
|--------|------|-------------|
| `Jurisdiccion` | TEXT | Nombre de la provincia |
| `TT_Pob` | INTEGER | Población total |
| `PVP`, `PVC`, `PSC`, ... | INTEGER | Variables auxiliares por sexo y población |

---

## 4. Funcionalidades Principales

| Función | Descripción |
|----------|-------------|
| `crear_tabla()` | Crea las tablas `C19` y `C22` si no existen |
| `cargar_tabla()` | Carga los casos COVID-19 desde `Covid19_limpio.csv` |
| `cargar_tabla_c22()` | Carga los datos del Censo 2022 |
| `PromEdFall()` | Calcula el promedio de edad de fallecidos por provincia |
| `Intervalos()` | Genera intervalos etarios (Regla de Sturges) y analiza confirmados/fallecidos |
| `Fallecidos()` | Determina los intervalos con más fallecimientos por sexo |
| `CCPP()` | Muestra provincias con más casos confirmados por sexo |
| `MenorR()` | Identifica la provincia con menor proporción de casos confirmados |
| `MayorFallecidos()` | Calcula el porcentaje y proporción de fallecidos por provincia |
| `IndicePorSexo()` | Muestra el índice comparativo de contagios entre mujeres y varones |

---

## 5. Metodología Estadística

- Clasificación de intervalos mediante la **Regla de Sturges**  
  `k = 1 + 3.322 * log10(N)`
- Análisis de **proporciones normalizadas por población provincial**
- Segmentación por **sexo y grupos etarios**
- Cálculo de **promedios**, **porcentajes** y **frecuencias relativas**

---

## 6. Ejecución del Programa

Ejecutar desde consola:


python EEdD.py


[1] Menú de Tablas
[2] Promedio de fallecidos por provincia
[3] Intervalos de confirmados y fallecidos
[4] Intervalos de hombres y mujeres fallecidas
[5] Casos confirmados por provincia
[6] Menor proporción de casos confirmados
[7] Mayor porcentaje de fallecidos
[8] Mayor índice de casos confirmados por sexo
[0] Salir


## 7. Flujo Recomendado de Ejecución
Crear las tablas: [1] → [1]
Cargar datos COVID-19: [1] → [2]
Cargar datos Censo 2022: [1] → [3]
Ejecutar las consultas estadísticas deseadas (opciones [2] a [8])

## 8. Diseño Técnico
Lenguaje: Python 3
Base de datos: SQLite
Paradigma: Programación estructurada
Entrada: Archivos CSV delimitados por ;
Salida: Datos impresos en consola

Proyecto académico desarrollado por:
GOLART, DOLFI

```bash
