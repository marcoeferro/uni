import simpy
import random

def cliente(env, nombre, servidores, tasa_servicio):
    """Proceso para un cliente que entra en la cola."""
    llegada = env.now
    print(f"{nombre} llegó a las {llegada:.2f}")
    
    with servidores.request() as req:
        yield req  # Espera un servidor disponible
        espera = env.now - llegada
        print(f"{nombre} es atendido tras esperar {espera:.2f} unidades de tiempo")
        
        # Tiempo de servicio (distribución exponencial)
        tiempo_servicio = random.expovariate(tasa_servicio)
        yield env.timeout(tiempo_servicio)
        print(f"{nombre} sale de la cola a las {env.now:.2f}")

def generar_clientes(env, tasa_llegada, tasa_servicio, servidores):
    """Genera clientes con tiempos de llegada exponenciales."""
    i = 0
    while True:
        yield env.timeout(random.expovariate(tasa_llegada))
        i += 1
        env.process(cliente(env, f"Cliente-{i}", servidores, tasa_servicio))

# Parámetros de la simulación
tasa_llegada = 1.0  # Tasa de llegada (media de 1 llegada por unidad de tiempo)
tasa_servicio = 1.2  # Tasa de servicio (media de 1.2 clientes atendidos por unidad de tiempo)
n_servidores = 3     # Número de servidores en paralelo
tiempo_simulacion = 10  # Tiempo total de simulación

# Crear el entorno de simulación
env = simpy.Environment()
servidores = simpy.Resource(env, capacity=n_servidores)

# Iniciar el proceso de generación de clientes
env.process(generar_clientes(env, tasa_llegada, tasa_servicio, servidores))

# Ejecutar la simulación
env.run(until=tiempo_simulacion)
