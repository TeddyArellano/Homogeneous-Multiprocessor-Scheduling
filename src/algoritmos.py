import numpy as np
import time


class ResultadoCalendarizacion:
    
    def __init__(self, asignaciones, cargas_procesadores, makespan, tiempo_ejecucion, nombre_algoritmo):
        # Almacena el resultado de un algoritmo de calendarizacion
        self.asignaciones = asignaciones
        self.cargas_procesadores = cargas_procesadores
        self.makespan = makespan
        self.tiempo_ejecucion = tiempo_ejecucion
        self.nombre_algoritmo = nombre_algoritmo


class AlgoritmoVorazEnLinea:
    
    def __init__(self):
        self.nombre = "Voraz en Linea"
    
    def resolver(self, instancia):
        # Asigna tareas en orden de llegada al procesador con menor carga
        tiempo_inicio = time.perf_counter()
        
        tareas = instancia.duraciones_tareas
        numero_procesadores = instancia.numero_procesadores
        
        cargas = np.zeros(numero_procesadores)
        asignaciones = []
        
        for id_tarea, duracion in enumerate(tareas):
            procesador_minimo = np.argmin(cargas)
            cargas[procesador_minimo] += duracion
            asignaciones.append((id_tarea, procesador_minimo))
        
        makespan = np.max(cargas)
        tiempo_ejecucion = time.perf_counter() - tiempo_inicio
        
        return ResultadoCalendarizacion(
            asignaciones=asignaciones,
            cargas_procesadores=cargas,
            makespan=makespan,
            tiempo_ejecucion=tiempo_ejecucion,
            nombre_algoritmo=self.nombre
        )


class AlgoritmoVorazLPT:
    
    def __init__(self):
        self.nombre = "Voraz LPT"
    
    def resolver(self, instancia):
        # Ordena tareas de mayor a menor duracion y asigna al procesador con menor carga
        tiempo_inicio = time.perf_counter()
        
        tareas = instancia.duraciones_tareas
        numero_procesadores = instancia.numero_procesadores
        
        indices_tareas = np.argsort(tareas)[::-1]
        tareas_ordenadas = tareas[indices_tareas]
        
        cargas = np.zeros(numero_procesadores)
        asignaciones = [None] * len(tareas)
        
        for id_original, duracion in zip(indices_tareas, tareas_ordenadas):
            procesador_minimo = np.argmin(cargas)
            cargas[procesador_minimo] += duracion
            asignaciones[id_original] = (id_original, procesador_minimo)
        
        makespan = np.max(cargas)
        tiempo_ejecucion = time.perf_counter() - tiempo_inicio
        
        return ResultadoCalendarizacion(
            asignaciones=asignaciones,
            cargas_procesadores=cargas,
            makespan=makespan,
            tiempo_ejecucion=tiempo_ejecucion,
            nombre_algoritmo=self.nombre
        )
