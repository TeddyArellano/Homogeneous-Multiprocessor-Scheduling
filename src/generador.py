import numpy as np
import json
from pathlib import Path


class Instancia:
    
    def __init__(self, duraciones_tareas, numero_procesadores, distribucion, tamano, id_instancia, semilla):
        # Representa una instancia del problema de calendarizacion
        self.duraciones_tareas = duraciones_tareas
        self.numero_procesadores = numero_procesadores
        self.distribucion = distribucion
        self.tamano = tamano
        self.id_instancia = id_instancia
        self.semilla = semilla
    
    def convertir_a_diccionario(self):
        # Convierte la instancia a diccionario para guardar en JSON
        return {
            'duraciones_tareas': self.duraciones_tareas.tolist() if isinstance(self.duraciones_tareas, np.ndarray) else self.duraciones_tareas,
            'numero_procesadores': self.numero_procesadores,
            'distribucion': self.distribucion,
            'tamano': self.tamano,
            'id_instancia': self.id_instancia,
            'semilla': self.semilla
        }
    
    @classmethod
    def crear_desde_diccionario(cls, datos):
        # Crea una instancia desde un diccionario
        return cls(
            duraciones_tareas=np.array(datos['duraciones_tareas']),
            numero_procesadores=datos['numero_procesadores'],
            distribucion=datos['distribucion'],
            tamano=datos['tamano'],
            id_instancia=datos['id_instancia'],
            semilla=datos['semilla']
        )


class GeneradorInstancias:
    
    def __init__(self, configuracion):
        # Inicializa el generador con la configuracion del proyecto
        self.configuracion = configuracion
        self.instancias = []
    
    def generar_tareas(self, distribucion, tamano, semilla):
        # Genera duraciones de tareas segun la distribucion especificada
        generador_aleatorio = np.random.RandomState(semilla)
        parametros = self.configuracion.PARAMETROS_DISTRIBUCION[distribucion]
        
        if distribucion == 'uniforme':
            tareas = generador_aleatorio.uniform(parametros['minimo'], parametros['maximo'], tamano)
        elif distribucion == 'normal':
            tareas = generador_aleatorio.normal(parametros['media'], parametros['desviacion'], tamano)
            tareas = np.abs(tareas)
            tareas = np.maximum(tareas, 1.0)
        elif distribucion == 'exponencial':
            tareas = generador_aleatorio.exponential(parametros['escala'], tamano)
            tareas = np.maximum(tareas, 1.0)
        else:
            raise ValueError(f"Distribucion desconocida: {distribucion}")
        
        return tareas
    
    def generar_todas_instancias(self):
        # Genera todas las instancias segun la configuracion
        instancias = []
        contador_instancia = 0
        
        for indice_dist, distribucion in enumerate(self.configuracion.DISTRIBUCIONES):
            for indice_tamano, tamano in enumerate(self.configuracion.TAMANOS_TAREAS):
                for indice_instancia in range(self.configuracion.INSTANCIAS_POR_CONFIGURACION):
                    
                    semilla = self.configuracion.obtener_semilla(indice_dist, indice_tamano, indice_instancia)
                    tareas = self.generar_tareas(distribucion, tamano, semilla)
                    
                    instancia = Instancia(
                        duraciones_tareas=tareas,
                        numero_procesadores=self.configuracion.NUMERO_PROCESADORES,
                        distribucion=distribucion,
                        tamano=tamano,
                        id_instancia=contador_instancia,
                        semilla=semilla
                    )
                    
                    instancias.append(instancia)
                    contador_instancia += 1
        
        self.instancias = instancias
        self.guardar_instancias()
        return instancias
    
    def guardar_instancias(self, nombre_archivo=None):
        # Guarda las instancias generadas en archivo JSON
        if nombre_archivo is None:
            nombre_archivo = f"{self.configuracion.DIRECTORIO_DATOS}/instancias.json"
        
        Path(self.configuracion.DIRECTORIO_DATOS).mkdir(parents=True, exist_ok=True)
        
        datos = {
            'configuracion': {
                'semilla_maestra': self.configuracion.SEMILLA_MAESTRA,
                'numero_procesadores': self.configuracion.NUMERO_PROCESADORES,
                'tamanos_tareas': self.configuracion.TAMANOS_TAREAS,
                'distribuciones': self.configuracion.DISTRIBUCIONES,
                'instancias_por_configuracion': self.configuracion.INSTANCIAS_POR_CONFIGURACION
            },
            'instancias': [inst.convertir_a_diccionario() for inst in self.instancias]
        }
        
        with open(nombre_archivo, 'w') as archivo:
            json.dump(datos, archivo, indent=2)
    
    @staticmethod
    def cargar_instancias(nombre_archivo, configuracion):
        # Carga instancias desde archivo JSON
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
        
        instancias = [Instancia.crear_desde_diccionario(dato) for dato in datos['instancias']]
        return instancias
