from src.config import Configuracion
from src.generador import GeneradorInstancias
from src.algoritmos import AlgoritmoVorazEnLinea, AlgoritmoVorazLPT
from src.solucionador import SolucionadorGurobi
from src.metricas import RecolectorMetricas
from src.visualizacion import VisualizadorResultados


def main():    
    print("Calendarizacion en Multiprocesadores Homogeneos")
    
    configuracion = Configuracion()
    
    generador = GeneradorInstancias(configuracion)
    algoritmo_voraz_uno = AlgoritmoVorazEnLinea()
    algoritmo_voraz_dos = AlgoritmoVorazLPT()
    solucionador_gurobi = SolucionadorGurobi(tiempo_limite=configuracion.TIEMPO_LIMITE_GUROBI)
    recolector_metricas = RecolectorMetricas()
    visualizador = VisualizadorResultados()
    
    print("\nPaso 1 de 4: Generando instancias del problema...")
    instancias = generador.generar_todas_instancias()
    print(f"Se generaron {len(instancias)} instancias")
    
    print("\nPaso 2 de 4: Ejecutando algoritmos...")
    
    total_instancias = len(instancias)
    for indice, instancia in enumerate(instancias, 1):
        print(f"Procesando instancia {indice} de {total_instancias}...", end="\r")
        
        resultado_voraz_uno = algoritmo_voraz_uno.resolver(instancia)
        resultado_voraz_dos = algoritmo_voraz_dos.resolver(instancia)
        resultado_gurobi = solucionador_gurobi.resolver(instancia)
        
        recolector_metricas.agregar_resultado(instancia, resultado_voraz_uno, resultado_voraz_dos, resultado_gurobi)
    
    print(f"\nSe completaron {total_instancias} experimentos")
    
    print("\nPaso 3 de 4: Calculando estadisticas...")
    estadisticas = recolector_metricas.calcular_estadisticas()
    recolector_metricas.guardar_resultados()
    print("Estadisticas calculadas y guardadas")
    
    print("\nPaso 4 de 4: Generando visualizaciones...")
    visualizador.generar_todas_graficas(estadisticas)
    print("Graficas guardadas en directorio results")
    
    print("\nExperimento completado exitosamente")


if __name__ == "__main__":
    main()
