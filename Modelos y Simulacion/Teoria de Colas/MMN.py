import simpy
import random
import csv
from datetime import timedelta
from pathlib import Path

def formato_hora(segundos):
    """Convierte segundos a formato HH:MM:SS."""
    return str(timedelta(seconds=round(segundos)))


def cliente(env, nombre, servidores, tasa_servicio, datos_cliente):
    """Proceso que representa un cliente."""
    llegada = env.now
    tiempo_entre_llegada = llegada - datos_cliente['ultima_llegada'] if datos_cliente['ultima_llegada'] is not None else 0
    datos_cliente['ultima_llegada'] = llegada

    # Calcular longitud del sistema (clientes siendo atendidos + en cola)
    longitud_sistema = len(servidores.queue) + (servidores.count if servidores.count > 0 else 0)
    longitud_cola = len(servidores.queue)

    print(f"{nombre} llegó a las {formato_hora(llegada)}")
    
    with servidores.request() as req:
        yield req
        tiempo_en_cola = env.now - llegada
        inicio_servicio = env.now
        
        # Tiempo de servicio
        tiempo_servicio = random.expovariate(tasa_servicio)
        yield env.timeout(tiempo_servicio)
        
        fin_servicio = env.now
        
        # Registrar datos individuales del cliente
        datos_cliente['clientes'].append({
            'ID de simulación': datos_cliente['id_simulacion'],
            'Numero de cliente': nombre,
            'Hora de llegada': formato_hora(llegada),
            'Tiempo entre llegada': tiempo_entre_llegada,
            'Tiempo de llegada': llegada,
            'Tiempo en Cola': tiempo_en_cola,
            'Hora de inicio de servicio': formato_hora(inicio_servicio),
            'Tiempo de servicio': tiempo_servicio,
            'Hora de fin de servicio': formato_hora(fin_servicio),
            'Tiempo en el sistema': tiempo_en_cola + tiempo_servicio,
            'Longitud del sistema': longitud_sistema,
            'Longitud de la Cola': longitud_cola
        })


def generar_clientes(env, tasa_llegada, tasa_servicio, servidores, datos_cliente):
    """Genera clientes con tiempos de llegada exponenciales."""
    i = 0
    while True:
        yield env.timeout(random.expovariate(tasa_llegada))
        i += 1
        env.process(cliente(env, f"Cliente-{i}", servidores, tasa_servicio, datos_cliente))


def simulacion(tasa_llegada, tasa_servicio, n_servidores, tiempo_simulacion, id_simulacion):
    """Ejecuta la simulación y retorna los datos recolectados."""
    # Preparar entorno
    env = simpy.Environment()
    servidores = simpy.Resource(env, capacity=n_servidores)
    datos_cliente = {'ultima_llegada': None, 'clientes': [], 'id_simulacion': id_simulacion}

    # Iniciar generación de clientes
    env.process(generar_clientes(env, tasa_llegada, tasa_servicio, servidores, datos_cliente))

    # Ejecutar simulación
    env.run(until=tiempo_simulacion)

    return datos_cliente['clientes']


def guardar_resultados_csv(datos_clientes, archivo_csv="resultados_simulacion.csv"):
    """Guarda los resultados de la simulación en un archivo CSV en la misma carpeta del script."""
    columnas = [
        'ID de simulación', 'Numero de cliente', 'Hora de llegada', 'Tiempo entre llegada', 'Tiempo de llegada',
        'Tiempo en Cola', 'Hora de inicio de servicio', 'Tiempo de servicio',
        'Hora de fin de servicio', 'Tiempo en el sistema', 'Longitud del sistema', 'Longitud de la Cola'
    ]

    # Obtener el directorio del script y definir la ruta completa del archivo CSV
    ruta_script = Path(__file__).parent
    ruta_csv = ruta_script / archivo_csv

    # Escribir encabezado solo si el archivo no existe
    escribir_encabezado = not ruta_csv.exists()

    # Abrir el archivo para agregar filas
    with ruta_csv.open(mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        if escribir_encabezado:
            escritor.writeheader()
        escritor.writerows(datos_clientes)



def convertir_parametros(hora_inicio, hora_fin, clientes_por_hora, capacidad_servicio_por_hora, n_servidores):
    """
    Convierte los parámetros de la simulación al formato requerido en segundos.
    """
    def convertir_hora_a_segundos(hora):
        """Convierte una hora en formato HH:MM:SS a segundos desde la medianoche."""
        h, m, s = map(int, hora.split(':'))
        return h * 3600 + m * 60 + s

    # Convertir horas a segundos
    hora_inicio_segundos = convertir_hora_a_segundos(hora_inicio)
    hora_fin_segundos = convertir_hora_a_segundos(hora_fin)
    
    # Calcular el tiempo de simulación en segundos
    tiempo_simulacion = hora_fin_segundos - hora_inicio_segundos
    
    # Convertir tasas
    tasa_llegada = clientes_por_hora / 3600  # Clientes por segundo
    tasa_servicio = capacidad_servicio_por_hora / 3600  # Servicio por segundo
    
    return {
        'hora_inicio_segundos': hora_inicio_segundos,
        'hora_fin_segundos': hora_fin_segundos,
        'tiempo_simulacion': tiempo_simulacion,
        'tasa_llegada': tasa_llegada,
        'tasa_servicio': tasa_servicio,
        'n_servidores': n_servidores
    }


def obtener_ultimo_id_simulacion(archivo_csv="resultados_simulacion.csv"):
    """Obtiene el último ID de simulación del archivo CSV, si existe."""
    ruta_csv = Path(__file__).parent / archivo_csv
    
    if not ruta_csv.exists():
        return 0  # Si no existe el archivo, comenzar desde el ID 1
    
    with ruta_csv.open(mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        ids_simulacion = [int(fila['ID de simulación']) for fila in lector if 'ID de simulación' in fila]
        return max(ids_simulacion, default=0)  # Si no hay filas, regresar 0

def ejecutar_simulaciones(cantidad_simulaciones, parametros, archivo_csv="resultados_simulacion.csv"):
    """
    Ejecuta múltiples simulaciones y las guarda en un archivo CSV.
    
    Args:
        cantidad_simulaciones (int): Número de simulaciones a ejecutar.
        parametros (dict): Parámetros de la simulación.
        archivo_csv (str): Nombre del archivo CSV donde guardar los resultados.
    """
    # Obtener el último ID del CSV y calcular el primer ID de esta ejecución
    ultimo_id = obtener_ultimo_id_simulacion(archivo_csv)
    primer_id = ultimo_id + 1

    # Ejecutar simulaciones
    for id_simulacion in range(primer_id, primer_id + cantidad_simulaciones):
        clientes = simulacion(
            parametros["tasa_llegada"],
            parametros["tasa_servicio"],
            parametros["n_servidores"],
            parametros["tiempo_simulacion"],
            id_simulacion
        )
        # Guardar resultados en CSV
        guardar_resultados_csv(clientes, archivo_csv)


# Parámetros legibles convertidos a formato requerido
parametros_simulacion = convertir_parametros(
    hora_inicio="08:00:00",
    hora_fin="16:00:00",
    clientes_por_hora=10,
    capacidad_servicio_por_hora=12,
    n_servidores=2
)

# Ejecutar simulaciones
ejecutar_simulaciones(3, parametros_simulacion)
# Si se vuelve a ejecutar, los nuevos IDs se asignarán de manera continua.
# ejecutar_simulaciones(3, parametros_simulacion)


print("Simulaciones completadas y resultados guardados en 'resultados_simulacion.csv'.")


"""
Este script simula una cola de atención con múltiples servidores usando SimPy, 
genera clientes con tiempos exponenciales de llegada y servicio, registra métricas 
por cliente y guarda resultados en CSV con IDs persistentes.

1) Imports y utilidades:
   - simpy: motor de simulación de eventos discretos (tiempo virtual).
   - random: genera variables aleatorias (exponenciales para llegadas/servicios).
   - csv: escritura de resultados tabulares.
   - datetime.timedelta: formatea tiempos en HH:MM:SS.
   - pathlib.Path: rutas portables del archivo CSV.
   - formato_hora(segundos): convierte segundos a "HH:MM:SS" redondeando.

2) Proceso de cliente: cliente(env, nombre, servidores, tasa_servicio, datos_cliente)
   - Registra la hora de llegada (env.now).
   - Calcula tiempo entre llegadas usando datos_cliente['ultima_llegada'] y actualiza ese valor.
   - Calcula longitud del sistema: tamaño de la cola + servidores ocupados (servidores.count).
   - Solicita un recurso (servidores.request()):
     * Al hacer 'yield req', el cliente espera si no hay servidor libre.
   - Mide tiempo en cola: env.now - llegada al obtener el servidor.
   - Genera tiempo de servicio ~ Exponencial(tasa_servicio) y avanza el reloj: yield env.timeout(tiempo_servicio).
   - Registra métricas del cliente en datos_cliente['clientes']:
     * ID de simulación, número de cliente, hora de llegada/inicio/fin (formateadas),
       tiempos (entre llegada, en cola, servicio, en el sistema),
       y estados del sistema (longitud de la cola/sistema) en su llegada.

3) Generación de clientes: generar_clientes(env, tasa_llegada, tasa_servicio, servidores, datos_cliente)
   - Bucle infinito:
     * Espera un tiempo interarribo ~ Exponencial(tasa_llegada): yield env.timeout(...)
     * Incrementa contador i y lanza un nuevo proceso cliente con env.process(...).

4) Simulación principal: simulacion(tasa_llegada, tasa_servicio, n_servidores, tiempo_simulacion, id_simulacion)
   - Crea el entorno: env = simpy.Environment().
   - Define el recurso servidores con capacidad n_servidores (servidores paralelos).
   - Prepara contenedor de datos: {'ultima_llegada': None, 'clientes': [], 'id_simulacion': id_simulacion}.
   - Inicia el generador de clientes como proceso de SimPy.
   - Ejecuta la simulación hasta tiempo_simulacion: env.run(until=...).
   - Retorna la lista de registros de clientes.

5) Persistencia en CSV: guardar_resultados_csv(datos_clientes, archivo_csv)
   - Define columnas esperadas en el CSV.
   - Usa la carpeta del script (Path(__file__).parent) para construir la ruta del CSV.
   - Si el archivo no existe, escribe encabezado; luego agrega filas con DictWriter.
   - Permite acumulación de resultados en ejecuciones sucesivas.

6) Conversión de parámetros legibles: convertir_parametros(...)
   - Convierte horas 'HH:MM:SS' a segundos desde medianoche.
   - Calcula tiempo_simulacion = hora_fin_segundos - hora_inicio_segundos.
   - Convierte tasas por hora a tasas por segundo:
     * tasa_llegada = clientes_por_hora / 3600
     * tasa_servicio = capacidad_servicio_por_hora / 3600
   - Devuelve dict con parámetros en segundos/tasas y n_servidores.

7) Gestión de IDs de simulación: obtener_ultimo_id_simulacion(archivo_csv)
   - Si el CSV no existe, retorna 0 (empezará en 1).
   - Si existe, lee la columna 'ID de simulación' y retorna el máximo, o 0 si no hay filas.
   - Permite continuidad de IDs entre ejecuciones para trazabilidad.

8) Ejecución múltiple y guardado: ejecutar_simulaciones(cantidad_simulaciones, parametros, archivo_csv)
   - Determina primer_id = obtener_ultimo_id_simulacion(...) + 1.
   - Para cada id_simulacion en el rango, ejecuta simulacion(...) con los parámetros
     y guarda los resultados inmediatamente en CSV (append).
   - Desacopla simulación y persistencia, facilitando reanudación y auditoría.

9) Parámetros y ejecución:
   - Convierte una jornada (08:00–16:00), con 10 clientes/hora y capacidad de 12 servicios/hora, 2 servidores.
   - Ejecuta 3 simulaciones consecutivas, acumulando resultados y manteniendo IDs continuos.
   - Mensaje final indica que se guardó en 'resultados_simulacion.csv'.

Notas clave de modelado:
- Interarribo y servicio con distribución exponencial (proceso de Poisson/M/M/c).
- 'servidores' es un recurso con capacidad c: colas FIFO, servicio paralelo.
- Todas las métricas se registran por cliente para análisis de desempeño (cola, servicio, sistema).
- CSV en la carpeta del script con encabezado único y anexado de filas para rastreo histórico.
"""
