import time
import csv
from pathlib import Path

# Función para medir el tiempo de ejecución
def measure_execution_time(func, *args):
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    return result, end_time - start_time

# Función para guardar en CSV
def save_to_csv(file_name, tipo, mensaje, hash_result, tiempo_ejecucion):
    # Crear ruta en la carpeta local donde está el script
    script_dir = Path(__file__).parent  # Carpeta donde está alojado el script
    file_path = script_dir / file_name  # Ruta completa del archivo

    file_exists = file_path.exists()
    with file_path.open('a', newline='') as file:  # Utilizando la API de Path
        writer = csv.writer(file)
        if not file_exists:
            # Escribir encabezados si el archivo no existe
            writer.writerow(["tipo", "mensaje", "hash", "tiempo_ejecucion (s)"])
        # Escribir una nueva fila con los datos
        writer.writerow([tipo, mensaje, hash_result, tiempo_ejecucion])

# Función para ejecutar múltiples veces y guardar resultados
def run_sha256_multiple_times(messages, csv_file,tipo,func):
    for message in messages:
        hash, exec_time = measure_execution_time(func, message)
        save_to_csv(file_name = csv_file, 
                    tipo = tipo,
                    mensaje = message,
                    hash_result = hash, 
                    tiempo_ejecucion = exec_time)