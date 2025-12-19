class Configuracion:
    
    # Semilla maestra para reproducibilidad
    SEMILLA_MAESTRA = 42
    
    # Numero de procesadores identicos
    NUMERO_PROCESADORES = 8
    
    # Tamanos de instancias a probar
    TAMANOS_TAREAS = [50, 100, 200, 400]
    
    # Tipos de distribuciones
    DISTRIBUCIONES = ['uniforme', 'normal', 'exponencial']
    
    # Parametros para cada distribucion
    PARAMETROS_DISTRIBUCION = {
        'uniforme': {'minimo': 1, 'maximo': 100},
        'normal': {'media': 50, 'desviacion': 15},
        'exponencial': {'escala': 20}
    }
    
    # Instancias por cada configuracion
    INSTANCIAS_POR_CONFIGURACION = 10
    
    # Limite de tiempo para Gurobi en segundos
    TIEMPO_LIMITE_GUROBI = 30
    
    # Directorios de salida
    DIRECTORIO_DATOS = 'data'
    DIRECTORIO_RESULTADOS = 'results'
    
    # Nivel de confianza para intervalos
    NIVEL_CONFIANZA = 0.95
    
    # Configuracion de graficas
    TAMANO_FIGURA = (10, 6)
    DPI = 300
    
    def obtener_semilla(self, indice_distribucion, indice_tamano, indice_instancia):
        # Genera una semilla unica para cada configuracion
        return self.SEMILLA_MAESTRA + indice_distribucion * 1000 + indice_tamano * 100 + indice_instancia
