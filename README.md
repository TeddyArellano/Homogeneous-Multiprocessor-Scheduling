# Calendarizacion en Multiprocesadores Homogeneos

Proyecto Final - Diseño y Analisis de Algoritmos
Instituto Politecnico Nacional

## Descripcion del Proyecto

Este proyecto implementa y compara diferentes algoritmos para resolver el problema de Calendarizacion en Multiprocesadores Homogeneos, un problema NP-Dificil de la teoria de complejidad computacional.

### Definicion del Problema

El problema consiste en asignar N tareas con diferentes duraciones a K procesadores identicos, de manera que se minimice el makespan (tiempo en que termina el procesador que mas tarda).

- Entrada: N tareas con duraciones variables, K procesadores identicos
- Objetivo: Minimizar el makespan para equilibrar la carga de trabajo
- Complejidad: NP-Dificil

### Fundamento Teorico

El problema de calendarizacion en multiprocesadores homogeneos es un problema clasico de optimizacion combinatoria:

**Formulacion Matematica:**
- Variables: x[i,j] = 1 si la tarea i se asigna al procesador j, 0 en otro caso
- Objetivo: Minimizar C_max (makespan)
- Restricciones:
  - Cada tarea se asigna exactamente a un procesador
  - La carga de cada procesador debe ser menor o igual al makespan

**Razones de Aproximacion:**
- Algoritmo Voraz Online: Factor de 2
- Algoritmo LPT: Factor de 4/3 - 1/(3K)
- Gurobi: Solucion optima (factor de 1.0)

## Estructura del Proyecto

```
Final Project - Homogeneous Multiprocessor Scheduling/
│
├── src/                          Codigo fuente
│   ├── config.py                Parametros de configuracion
│   ├── generador.py             Generador de instancias aleatorias
│   ├── algoritmos.py            Algoritmos voraces
│   ├── solucionador.py          Solver exacto con Gurobi
│   ├── metricas.py              Recoleccion de metricas
│   ├── visualizacion.py         Generacion de graficas
│   └── __init__.py              Inicializacion del paquete
│
├── data/                         Instancias generadas (JSON)
├── results/                      Graficas y resultados (PNG, CSV)
│
├── main.py                       Script principal de ejecucion
├── requirements.txt              Dependencias de Python
├── .gitignore                   Archivos ignorados por Git
└── README.md                     Este archivo
```

## Algoritmos Implementados

### Algoritmo 1: Voraz en Linea (Online Scheduling)

Estrategia: Asigna cada tarea en orden de llegada al procesador que tenga la menor carga acumulada en ese momento.

Pseudocodigo:
```
Para cada tarea i:
    Encontrar procesador j con minima carga
    Asignar tarea i al procesador j
    Actualizar carga del procesador j
```

Caracteristicas:
- Complejidad temporal: O(N × K)
- Factor de aproximacion: 2
- Ventaja: Muy rapido, no requiere conocer todas las tareas de antemano
- Desventaja: Puede dar soluciones suboptimas

### Algoritmo 2: Voraz LPT (Longest Processing Time)

Estrategia: Primero ordena las tareas de mayor a menor duracion, luego aplica la misma logica del algoritmo 1.

Pseudocodigo:
```
Ordenar tareas de mayor a menor duracion
Para cada tarea i (en orden descendente):
    Encontrar procesador j con minima carga
    Asignar tarea i al procesador j
    Actualizar carga del procesador j
```

Caracteristicas:
- Complejidad temporal: O(N log N + N × K)
- Factor de aproximacion: 4/3 - 1/(3K)
- Ventaja: Mejor garantia teorica que el algoritmo 1
- Desventaja: Requiere conocer todas las tareas antes de empezar

### Algoritmo 3: Solucion Exacta con Gurobi

Estrategia: Formula el problema como un programa entero mixto y utiliza Gurobi para encontrar la solucion optima.

Formulacion MIP:
```
Variables:
  x[i,j] binaria: 1 si tarea i asignada a procesador j
  C_max continua: makespan

Minimizar: C_max

Sujeto a:
  suma_j x[i,j] = 1                    para toda tarea i
  suma_i duracion[i] × x[i,j] <= C_max para todo procesador j
```

Caracteristicas:
- Complejidad: Exponencial en el peor caso
- Factor de aproximacion: 1.0 (solucion optima)
- Limite de tiempo: 30 segundos
- Ventaja: Encuentra la solucion optima o la mejor posible en el tiempo limite
- Desventaja: No escala bien para instancias muy grandes

## Generacion de Instancias

El proyecto implementa un generador de instancias aleatorias reproducible que permite crear escenarios de prueba controlados.

### Parametros de Generacion

1. Distribuciones de Probabilidad (D):
   - Uniforme: Tareas con duraciones uniformemente distribuidas entre 1 y 100
   - Normal: Tareas con duraciones normalmente distribuidas (media=50, desviacion=15)
   - Exponencial: Tareas con duraciones exponencialmente distribuidas (escala=20)

2. Tamanos de Problema (N):
   - 50 tareas
   - 100 tareas
   - 200 tareas
   - 400 tareas

3. Reproducibilidad:
   - Semilla maestra: 42
   - Semillas derivadas: Se calculan unicamente para cada configuracion
   - Instancias por configuracion: 10

Total de instancias generadas: 3 distribuciones × 4 tamanos × 10 repeticiones = 120 instancias

### Sistema de Semillas

El generador utiliza una estrategia de semillas jerarquica:

```
semilla = semilla_maestra + indice_distribucion × 1000 + indice_tamano × 100 + indice_instancia
```

Esto garantiza que:
- Los experimentos son completamente reproducibles
- Cada instancia tiene una semilla unica
- Los resultados son identicos en cada ejecucion

## Metricas de Desempeno

El proyecto captura y analiza dos metricas principales:

### 1. Tiempo de Ejecucion

Mide el tiempo de CPU que tarda cada algoritmo en encontrar una solucion.

- Unidad: Segundos
- Precision: time.perf_counter() para alta precision
- Proposito: Evaluar la eficiencia computacional

### 2. Factor de Aproximacion

Mide la calidad de la solucion comparada con el optimo de Gurobi.

Formula:
```
Factor = Makespan_Algoritmo / Makespan_Gurobi
```

Interpretacion:
- Factor = 1.0: Solucion optima (identica a Gurobi)
- Factor = 1.2: Solucion 20% peor que el optimo
- Factor > 1.0: Solucion suboptima

### Analisis Estadistico

Para cada par (Distribucion, Tamano):
- Se calculan promedios sobre 10 instancias
- Se generan intervalos de confianza al 95% usando distribucion t de Student
- Se comparan los tres algoritmos

## Visualizacion de Resultados

El proyecto genera graficas comparativas automaticamente:

### Graficas de Calidad
- Eje X: Tamano del problema (N)
- Eje Y: Factor de aproximacion promedio
- Contenido: Curvas para Voraz 1, Voraz 2 y Gurobi
- Intervalos: Bandas de confianza al 95%

### Graficas de Velocidad
- Eje X: Tamano del problema (N)
- Eje Y: Tiempo de ejecucion promedio (segundos)
- Escala: Logaritmica para mejor visualizacion
- Contenido: Comparacion de tiempos de los tres algoritmos

Total de graficas: 6 (2 por cada distribucion)

## Instalacion

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Gurobi Optimizer con licencia academica

### Pasos de Instalacion

1. Clonar el repositorio:
```bash
git clone https://github.com/TeddyArellano/Homogeneous-Multiprocessor-Scheduling.git
cd "Final Project - Homogeneous Multiprocessor Scheduling"
```

2. Instalar dependencias de Python:
```bash
pip install -r requirements.txt
```

Dependencias incluidas:
- numpy: Operaciones numericas
- matplotlib: Generacion de graficas
- scipy: Analisis estadistico
- pandas: Manejo de datos
- gurobipy: Solver de optimizacion

3. Configurar licencia de Gurobi:

Opcion A - Licencia Academica Named-User (recomendada):
- Visitar: https://www.gurobi.com/academia/academic-program-and-licenses/
- Generar licencia Named-User Academic
- Seguir instrucciones de activacion

Opcion B - Licencia WLS Academic (alternativa):
- Valida por 90 dias
- No requiere conexion constante
- Ideal para pruebas

## Uso del Proyecto

### Ejecucion Completa

Para ejecutar todos los experimentos:

```bash
python main.py
```

### Flujo de Ejecucion

El programa ejecuta cuatro fases:

Fase 1: Generacion de Instancias
- Crea 120 instancias aleatorias
- Guarda instancias en data/instancias.json
- Tiempo estimado: 1-2 segundos

Fase 2: Ejecucion de Algoritmos
- Ejecuta Voraz 1, Voraz 2 y Gurobi en cada instancia
- Muestra progreso en tiempo real
- Tiempo estimado: 5-30 minutos (dependiendo del hardware)

Fase 3: Calculo de Estadisticas
- Agrupa resultados por distribucion y tamano
- Calcula promedios e intervalos de confianza
- Guarda resultados en results/resultados_crudos.csv
- Tiempo estimado: 1-2 segundos

Fase 4: Generacion de Visualizaciones
- Crea 6 graficas comparativas
- Guarda graficas en formato PNG (300 DPI)
- Tiempo estimado: 2-3 segundos

### Archivos de Salida

Despues de la ejecucion, se generan los siguientes archivos:

En directorio data/:
- instancias.json: Todas las instancias generadas con sus parametros

En directorio results/:
- resultados_crudos.csv: Datos completos de todos los experimentos
- grafica_1_uniforme_calidad.png: Factor de aproximacion (distribucion uniforme)
- grafica_2_uniforme_velocidad.png: Tiempo de ejecucion (distribucion uniforme)
- grafica_3_normal_calidad.png: Factor de aproximacion (distribucion normal)
- grafica_4_normal_velocidad.png: Tiempo de ejecucion (distribucion normal)
- grafica_5_exponencial_calidad.png: Factor de aproximacion (distribucion exponencial)
- grafica_6_exponencial_velocidad.png: Tiempo de ejecucion (distribucion exponencial)

## Configuracion Personalizada

Para modificar parametros del experimento, editar src/config.py:

```python
class Configuracion:
    SEMILLA_MAESTRA = 42                      # Cambiar para diferentes experimentos
    NUMERO_PROCESADORES = 2                   # Cantidad de procesadores (K)
    TAMANOS_TAREAS = [50, 100, 200, 400]     # Tamanos a probar
    DISTRIBUCIONES = ['uniforme', 'normal', 'exponencial']
    INSTANCIAS_POR_CONFIGURACION = 10         # Repeticiones por configuracion
    TIEMPO_LIMITE_GUROBI = 30                 # Limite de tiempo para Gurobi (segundos)
```

## Resultados Esperados

### Calidad de Soluciones

Esperado teoricamente:
- Voraz en Linea: Factor aproximado de 2.0
- Voraz LPT: Factor aproximado de 1.33 (4/3)
- Gurobi: Factor de 1.0 (optimo)

### Tiempo de Ejecucion

Esperado:
- Voraz en Linea: Milisegundos
- Voraz LPT: Milisegundos (ligeramente mas lento por el ordenamiento)
- Gurobi: Segundos (puede llegar al limite de 30 segundos en instancias grandes)

### Comportamiento por Distribucion

- Uniforme: Resultados mas predecibles
- Normal: Mayor variabilidad en los resultados
- Exponencial: Puede tener casos extremos con tareas muy largas

## Estructura del Codigo

### Modulo: config.py
Define todos los parametros configurables del experimento.

### Modulo: generador.py
Contiene:
- Clase Instancia: Representa una instancia del problema
- Clase GeneradorInstancias: Genera instancias aleatorias reproducibles

### Modulo: algoritmos.py
Contiene:
- Clase ResultadoCalendarizacion: Almacena el resultado de un algoritmo
- Clase AlgoritmoVorazEnLinea: Implementa el algoritmo voraz 1
- Clase AlgoritmoVorazLPT: Implementa el algoritmo voraz 2

### Modulo: solucionador.py
Contiene:
- Clase SolucionadorGurobi: Implementa la solucion exacta con MIP

### Modulo: metricas.py
Contiene:
- Clase RecolectorMetricas: Recolecta y analiza metricas de desempeno

### Modulo: visualizacion.py
Contiene:
- Clase VisualizadorResultados: Genera graficas comparativas

## Autor

Jose Juan Arellano Juarez
Diseño y Analisis de Algoritmos
Instituto Politecnico Nacional

## Licencia

Este proyecto es de uso academico.## Licencia

Este proyecto es de uso academico.
