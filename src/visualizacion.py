import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


class VisualizadorResultados:
    
    def __init__(self, directorio_salida='results'):
        self.directorio_salida = Path(directorio_salida)
        self.directorio_salida.mkdir(parents=True, exist_ok=True)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colores = {
            'voraz1': '#e74c3c',
            'voraz2': '#3498db',
            'gurobi': '#2ecc71'
        }
        self.etiquetas = {
            'voraz1': 'Voraz en Linea',
            'voraz2': 'Voraz LPT',
            'gurobi': 'Gurobi Exacto'
        }
    
    def graficar_calidad(self, estadisticas, distribucion, nombre_archivo):
        # Grafica el factor de aproximacion vs tamano del problema
        figura, eje = plt.subplots(figsize=(10, 6))
        
        tamanos = sorted(estadisticas[distribucion].keys())
        
        for algoritmo in ['voraz1', 'voraz2', 'gurobi']:
            medias = []
            ic_bajos = []
            ic_altos = []
            
            for tamano in tamanos:
                diccionario_stats = estadisticas[distribucion][tamano][algoritmo]
                medias.append(diccionario_stats['media_factor'])
                ic_bajos.append(diccionario_stats['factor_ic_bajo'])
                ic_altos.append(diccionario_stats['factor_ic_alto'])
            
            medias = np.array(medias)
            ic_bajos = np.array(ic_bajos)
            ic_altos = np.array(ic_altos)
            
            eje.plot(tamanos, medias, 
                   marker='o', 
                   linewidth=2, 
                   markersize=8,
                   color=self.colores[algoritmo],
                   label=self.etiquetas[algoritmo])
            
            eje.fill_between(tamanos, ic_bajos, ic_altos, 
                           alpha=0.2, 
                           color=self.colores[algoritmo])
        
        eje.set_xlabel('Tamano del Problema (N)', fontsize=12, fontweight='bold')
        eje.set_ylabel('Factor de Aproximacion', fontsize=12, fontweight='bold')
        eje.set_title(f'Calidad de Solucion - Distribucion {distribucion.capitalize()}', 
                    fontsize=14, fontweight='bold')
        eje.legend(loc='best', fontsize=10)
        eje.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.directorio_salida / nombre_archivo, dpi=300, bbox_inches='tight')
        plt.close()
    
    def graficar_velocidad(self, estadisticas, distribucion, nombre_archivo):
        # Grafica el tiempo de ejecucion vs tamano del problema
        figura, eje = plt.subplots(figsize=(10, 6))
        
        tamanos = sorted(estadisticas[distribucion].keys())
        
        for algoritmo in ['voraz1', 'voraz2', 'gurobi']:
            medias = []
            ic_bajos = []
            ic_altos = []
            
            for tamano in tamanos:
                diccionario_stats = estadisticas[distribucion][tamano][algoritmo]
                medias.append(diccionario_stats['media_tiempo'])
                ic_bajos.append(diccionario_stats['tiempo_ic_bajo'])
                ic_altos.append(diccionario_stats['tiempo_ic_alto'])
            
            medias = np.array(medias)
            ic_bajos = np.array(ic_bajos)
            ic_altos = np.array(ic_altos)
            
            eje.plot(tamanos, medias, 
                   marker='s', 
                   linewidth=2, 
                   markersize=8,
                   color=self.colores[algoritmo],
                   label=self.etiquetas[algoritmo])
            
            eje.fill_between(tamanos, ic_bajos, ic_altos, 
                           alpha=0.2, 
                           color=self.colores[algoritmo])
        
        eje.set_xlabel('Tamano del Problema (N)', fontsize=12, fontweight='bold')
        eje.set_ylabel('Tiempo de Ejecucion (segundos)', fontsize=12, fontweight='bold')
        eje.set_title(f'Velocidad de Algoritmo - Distribucion {distribucion.capitalize()}', 
                    fontsize=14, fontweight='bold')
        eje.legend(loc='best', fontsize=10)
        eje.grid(True, alpha=0.3)
        eje.set_yscale('log')
        
        plt.tight_layout()
        plt.savefig(self.directorio_salida / nombre_archivo, dpi=300, bbox_inches='tight')
        plt.close()
    
    def generar_todas_graficas(self, estadisticas):
        # Genera todas las graficas requeridas
        numero_grafica = 1
        
        for distribucion in estadisticas.keys():
            nombre_calidad = f'grafica_{numero_grafica}_{distribucion}_calidad.png'
            self.graficar_calidad(estadisticas, distribucion, nombre_calidad)
            print(f"Generada {nombre_calidad}")
            numero_grafica += 1
            
            nombre_velocidad = f'grafica_{numero_grafica}_{distribucion}_velocidad.png'
            self.graficar_velocidad(estadisticas, distribucion, nombre_velocidad)
            print(f"Generada {nombre_velocidad}")
            numero_grafica += 1
