import numpy as np
from scipy.stats import norm

def mean_test_z(sample, alpha=0.05):
    """
    Prueba de Promedio basada en Z (para U(0,1)).

    Parámetros:
        sample : lista/array de números en [0,1]
        alpha  : nivel de significancia (default 0.05)

    Retorna:
        z_stat      : estadístico Z
        z_critical  : valor crítico según tabla
        accept      : True si NO se rechaza H0
    """
    sample = np.array(sample)
    n = len(sample)

    # Media y parámetros teóricos de U(0,1)
    mean_sample = np.mean(sample)
    mu = 0.5
    var = 1/12

    # Estadístico Z
    z_stat = (mean_sample - mu) / np.sqrt(var / n)

    # Valor crítico Z(alpha/2) por tabla
    z_critical = norm.ppf(1 - alpha/2)

    # Decisión
    accept = abs(z_stat) <= z_critical

    return z_stat, z_critical, accept


# -----------------------------------------------------
# Ejemplo de uso
# -----------------------------------------------------
if __name__ == "__main__":
    sample = np.random.random(10000)

    z, zc, ok = mean_test_z(sample, alpha=0.05)
    print("Z =", z)
    print("Z crítico =", zc)
    print("¿Aceptar H0 (promedio ≈ 0.5)?", ok)
