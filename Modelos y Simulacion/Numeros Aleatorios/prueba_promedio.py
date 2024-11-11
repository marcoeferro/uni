import Congruencial
import scipy.stats as stats
import math

def calculate_z_score(alpha):
    """Calcula el valor crítico Z correspondiente al nivel de confianza dado."""
    return stats.norm.ppf(1 - alpha / 2)

def uniformity_test(sample, confidence):
    """Realiza la prueba de uniformidad utilizando el promedio de la muestra y un estadístico Z."""
    n = len(sample)
    mean_sample = sum(sample) / n
    z_statistic = ((mean_sample - 0.5) * math.sqrt(n)) / math.sqrt(1 / 12)
    print(f"Estadístico Z: {abs(z_statistic):.4f}")
    print(f"Media muestral: {mean_sample:.4f}")

    alpha = 1 - confidence
    critical_z = calculate_z_score(alpha)
    print(f"Valor crítico Z (α/2): {critical_z:.4f}")

    if abs(z_statistic) < critical_z:
        print("La muestra sigue una distribución uniforme.")
    else:
        print("La muestra no sigue una distribución uniforme.")

# Ejemplo de uso
sample_size = 100
lcg = Congruencial.Congruencial(seed=12345)

random_sample = lcg.randoms(cantidad_numeros=sample_size)
uniformity_test(random_sample, confidence=0.90)
