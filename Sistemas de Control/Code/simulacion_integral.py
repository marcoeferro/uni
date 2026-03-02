import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import control as ctrl

# Parámetros fijos
T = 100  # Total de pasos de tiempo
dt = 1.0  # Paso de tiempo (días)
mu_d = 10.0  # Media de la demanda
sigma_d = 2.0  # Desviación estándar de la demanda
Z_score = 1.645  # Z-score para el stock de seguridad

# Valores iniciales de los parámetros del PID y retraso
Kc_0 = 0.5
Ki_0 = 0.1
Kd_0 = 0.2
theta_0 = 4

# Función para crear el sistema con aproximación de Padé
def create_system(theta):
    # Aproximación de Padé de primer orden para e^{-theta s}
    num_pade = [1, -theta/2]
    den_pade = [1, theta/2]
    # Sistema integrador: 1/s
    integrator = ctrl.tf([1], [1, 0])
    # Sistema completo: Padé * integrador
    system = ctrl.series(ctrl.tf(num_pade, den_pade), integrator)
    return system

# Función para simular el sistema en lazo cerrado
def run_simulation(Kc, Ki, Kd, theta):
    # Crear el sistema
    system = create_system(theta)
    # Controlador PID: K_d s + K_c + K_i/s
    pid = ctrl.tf([Kd, Kc, Ki], [1, 0])
    # Sistema en lazo cerrado
    closed_loop = ctrl.feedback(pid * system, 1)
    # Tiempo de simulación
    t = np.arange(0, T+1, dt)
    # Setpoint: stock de seguridad basado en el retraso
    leadtime = theta
    S = Z_score * sigma_d * np.sqrt(leadtime)
    # Simular respuesta al setpoint
    t_out, I_list = ctrl.step_response(closed_loop * S, T=t)
    # Simular demanda aleatoria
    np.random.seed(42)  # Para reproducibilidad
    D_list = np.maximum(np.random.normal(mu_d, sigma_d, len(t)-1), 0)
    # Ajustar inventario con la demanda acumulada
    I_list_adjusted = I_list - np.cumsum(np.concatenate(([0], D_list)))[:len(t)] * dt
    return t, I_list_adjusted, D_list, S

# Crear figura y eje
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35)

# Simulación inicial
t, I_list, D_list, S = run_simulation(Kc_0, Ki_0, Kd_0, theta_0)

# Inicializar gráfico
ax.plot(t, I_list, label=f'Inventario (Kc={Kc_0:.2f}, Ki={Ki_0:.2f}, Kd={Kd_0:.2f})', linewidth=2)
ax.plot(t, [S] * len(t), 'r--', label='Stock de Seguridad', linewidth=1.5)
ax.plot(t[:-1], D_list, 'g--', alpha=0.5, label='Demanda (d(t))')
ax.set_xlabel('Tiempo (días)')
ax.set_ylabel('Unidades')
ax.set_title('Control PID de Inventario con Demanda Impredecible')
ax.legend()
ax.grid(True)
ax.set_ylim(-50, 200)

# Crear ejes para los sliders y botón
ax_Kc = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_Ki = plt.axes([0.2, 0.20, 0.65, 0.03])
ax_Kd = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_theta = plt.axes([0.2, 0.10, 0.65, 0.03])
reset_ax = plt.axes([0.8, 0.05, 0.1, 0.04])

# Crear sliders y botón
slider_Kc = Slider(ax_Kc, 'Kc', 0.01, 2.0, valinit=Kc_0, valstep=0.01)
slider_Ki = Slider(ax_Ki, 'Ki', 0.001, 1.0, valinit=Ki_0, valstep=0.001)
slider_Kd = Slider(ax_Kd, 'Kd', 0.0, 1.0, valinit=Kd_0, valstep=0.01)
slider_theta = Slider(ax_theta, 'Theta', 1, 10, valinit=theta_0, valstep=1)
button_reset = Button(reset_ax, 'Reset', color='lightgoldenrodyellow')

# Función para actualizar el gráfico
def update(val):
    Kc = slider_Kc.val
    Ki = slider_Ki.val
    Kd = slider_Kd.val
    theta = int(slider_theta.val)
    t, I_list, D_list, S = run_simulation(Kc, Ki, Kd, theta)
    ax.clear()
    ax.plot(t, I_list, label=f'Inventario (Kc={Kc:.2f}, Ki={Ki:.2f}, Kd={Kd:.2f})', linewidth=2)
    ax.plot(t, [S] * len(t), 'r--', label='Stock de Seguridad', linewidth=1.5)
    ax.plot(t[:-1], D_list, 'g--', alpha=0.5, label='Demanda (d(t))')
    ax.set_xlabel('Tiempo (días)')
    ax.set_ylabel('Unidades')
    ax.set_title('Control PID de Inventario con Demanda Impredecible')
    ax.legend()
    ax.grid(True)
    ax.set_ylim(-50, 200)
    fig.canvas.draw_idle()

# Función para el botón de reset
def reset(event):
    slider_Kc.set_val(Kc_0)
    slider_Ki.set_val(Ki_0)
    slider_Kd.set_val(Kd_0)
    slider_theta.set_val(theta_0)
    update(None)

# Conectar sliders y botón
slider_Kc.on_changed(update)
slider_Ki.on_changed(update)
slider_Kd.on_changed(update)
slider_theta.on_changed(update)
button_reset.on_clicked(reset)

# Mostrar la figura
plt.show()