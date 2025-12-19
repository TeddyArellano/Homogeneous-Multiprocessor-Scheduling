import numpy as np
import time
try:
    import gurobipy as gp
    from gurobipy import GRB
    GUROBI_DISPONIBLE = True
except ImportError:
    GUROBI_DISPONIBLE = False
    print("Advertencia: Gurobi no esta disponible")

from .algoritmos import ResultadoCalendarizacion


class SolucionadorGurobi:
    
    def __init__(self, tiempo_limite=30):
        # Solucionador exacto usando programacion entera mixta
        self.nombre = "Gurobi Exacto"
        self.tiempo_limite = tiempo_limite
        
        if not GUROBI_DISPONIBLE:
            raise ImportError("Gurobi no esta instalado")
    
    def resolver(self, instancia):
        # Encuentra la calendarizacion optima usando formulacion MIP
        tiempo_inicio = time.perf_counter()
        
        tareas = instancia.duraciones_tareas
        numero_tareas = len(tareas)
        numero_procesadores = instancia.numero_procesadores
        
        modelo = gp.Model("Calendarizacion_Multiprocesadores")
        modelo.setParam('OutputFlag', 0)
        modelo.setParam('TimeLimit', self.tiempo_limite)
        
        variable_asignacion = modelo.addVars(numero_tareas, numero_procesadores, vtype=GRB.BINARY, name="x")
        variable_makespan = modelo.addVar(vtype=GRB.CONTINUOUS, name="C_max")
        
        modelo.setObjective(variable_makespan, GRB.MINIMIZE)
        
        for i in range(numero_tareas):
            modelo.addConstr(gp.quicksum(variable_asignacion[i, j] for j in range(numero_procesadores)) == 1, 
                          name=f"asignar_tarea_{i}")
        
        for j in range(numero_procesadores):
            modelo.addConstr(
                gp.quicksum(tareas[i] * variable_asignacion[i, j] for i in range(numero_tareas)) <= variable_makespan,
                name=f"carga_procesador_{j}"
            )
        
        modelo.optimize()
        
        tiempo_ejecucion = time.perf_counter() - tiempo_inicio
        
        if modelo.Status == GRB.OPTIMAL or modelo.Status == GRB.TIME_LIMIT:
            makespan = variable_makespan.X
            
            asignaciones = []
            cargas = np.zeros(numero_procesadores)
            
            for i in range(numero_tareas):
                for j in range(numero_procesadores):
                    if variable_asignacion[i, j].X > 0.5:
                        asignaciones.append((i, j))
                        cargas[j] += tareas[i]
                        break
            
            return ResultadoCalendarizacion(
                asignaciones=asignaciones,
                cargas_procesadores=cargas,
                makespan=makespan,
                tiempo_ejecucion=tiempo_ejecucion,
                nombre_algoritmo=self.nombre
            )
        else:
            raise RuntimeError(f"Gurobi fallo al encontrar solucion. Estado: {modelo.Status}")
