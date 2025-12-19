import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats


class RecolectorMetricas:
    
    def __init__(self):
        self.resultados = []
    
    def agregar_resultado(self, instancia, resultado_voraz_uno, resultado_voraz_dos, resultado_gurobi):
        # Registra los resultados de una instancia
        factor_voraz_uno = resultado_voraz_uno.makespan / resultado_gurobi.makespan
        factor_voraz_dos = resultado_voraz_dos.makespan / resultado_gurobi.makespan
        
        registro = {
            'id_instancia': instancia.id_instancia,
            'distribucion': instancia.distribucion,
            'tamano': instancia.tamano,
            'semilla': instancia.semilla,
            
            'voraz1_makespan': resultado_voraz_uno.makespan,
            'voraz1_tiempo': resultado_voraz_uno.tiempo_ejecucion,
            'voraz1_factor': factor_voraz_uno,
            
            'voraz2_makespan': resultado_voraz_dos.makespan,
            'voraz2_tiempo': resultado_voraz_dos.tiempo_ejecucion,
            'voraz2_factor': factor_voraz_dos,
            
            'gurobi_makespan': resultado_gurobi.makespan,
            'gurobi_tiempo': resultado_gurobi.tiempo_ejecucion,
            'gurobi_factor': 1.0
        }
        
        self.resultados.append(registro)
    
    def calcular_estadisticas(self):
        # Calcula estadisticas agregadas con intervalos de confianza
        tabla_datos = pd.DataFrame(self.resultados)
        estadisticas = {}
        
        for distribucion in tabla_datos['distribucion'].unique():
            estadisticas[distribucion] = {}
            
            for tamano in sorted(tabla_datos['tamano'].unique()):
                mascara = (tabla_datos['distribucion'] == distribucion) & (tabla_datos['tamano'] == tamano)
                subconjunto = tabla_datos[mascara]
                
                diccionario_stats = {}
                
                for algoritmo in ['voraz1', 'voraz2', 'gurobi']:
                    columna_factor = f'{algoritmo}_factor'
                    columna_tiempo = f'{algoritmo}_tiempo'
                    
                    factores = subconjunto[columna_factor].values
                    media_factor = np.mean(factores)
                    intervalo_factor = stats.t.interval(
                        0.95, 
                        len(factores) - 1,
                        loc=media_factor,
                        scale=stats.sem(factores)
                    )
                    
                    tiempos = subconjunto[columna_tiempo].values
                    media_tiempo = np.mean(tiempos)
                    intervalo_tiempo = stats.t.interval(
                        0.95,
                        len(tiempos) - 1,
                        loc=media_tiempo,
                        scale=stats.sem(tiempos)
                    )
                    
                    diccionario_stats[algoritmo] = {
                        'media_factor': media_factor,
                        'factor_ic_bajo': intervalo_factor[0],
                        'factor_ic_alto': intervalo_factor[1],
                        'media_tiempo': media_tiempo,
                        'tiempo_ic_bajo': intervalo_tiempo[0],
                        'tiempo_ic_alto': intervalo_tiempo[1],
                        'numero_muestras': len(factores)
                    }
                
                estadisticas[distribucion][tamano] = diccionario_stats
        
        return estadisticas
    
    def guardar_resultados(self, nombre_archivo='results/resultados_crudos.csv'):
        # Guarda resultados crudos en archivo CSV
        Path('results').mkdir(parents=True, exist_ok=True)
        tabla_datos = pd.DataFrame(self.resultados)
        tabla_datos.to_csv(nombre_archivo, index=False)
        print(f"Resultados guardados en {nombre_archivo}")
