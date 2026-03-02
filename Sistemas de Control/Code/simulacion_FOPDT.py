import numpy as np
import matplotlib.pyplot as plt
from control import TransferFunction, feedback, forced_response

# Parámetros del sistema
Kp = 1.0      # Ganancia del proceso
taup = 1.0    # Constante de tiempo (días)
thetap = 4.0  # Tiempo muerto (días)
Kc = 0.5875   # Ganancia proporcional del PID
Ki = 5.053763 # Ganancia integral del PID
Kd = 0.8510638 # Ganancia derivativa del PID
safety_stock = 100.0  # Nivel deseado de inventario

# Aproximación de Padé para el tiempo muerto
num_pade = [-thetap/2, 1]
den_pade = [thetap/2, 1]
pade_approx = TransferFunction(num_pade, den_pade)

# Modelo del proceso (FOPDT)
G_p = TransferFunction(Kp, [taup, 1]) * pade_approx

# Controlador PID
num_pid = [Kd, Kc, Ki]
den_pid = [1, 0]
C = TransferFunction(num_pid, den_pid)

# Sistema en lazo cerrado para referencia
sys_closed = feedback(C * G_p, 1)

# Función de sensibilidad para perturbaciones
S = feedback(1, C * G_p)
integrador = TransferFunction([1], [1, 0])  # 1/s
sys_perturbacion = -integrador * S  # TF perturbación

# Tiempo de simulación
t = np.linspace(0, 20, 200)

# Señales
r = safety_stock * np.ones_like(t)        # Referencia
demanda = 10 * np.sin(0.5 * t)           # Perturbación

# Simular respuestas
_, y_control = forced_response(sys_closed, T=t, U=r)
_, y_perturbacion = forced_response(sys_perturbacion, T=t, U=demanda)

# Inventario total = respuesta a referencia + perturbación
inventario = y_control + y_perturbacion

# Gráficos
plt.figure(figsize=(10, 6))
plt.plot(t, inventario, label='Inventario Real')
plt.plot(t, demanda, 'm--', alpha=0.5, label='Demanda (Tasa)')
plt.axhline(safety_stock, color='r', linestyle='--', label='Safety Stock')
plt.xlabel('Tiempo (días)')
plt.ylabel('Nivel de Inventario')
plt.title('Control PID de Inventario con Perturbaciones')
plt.legend()
plt.grid(True)
plt.show()