import numpy as np
from scipy.stats import chi2

def frequency_test_chi_square(bits, alpha=0.05, df=1):
    """
    Prueba de Frecuencia (Monobit) usando Chi-cuadrado.
    
    Parámetros:
        bits: lista/array de 0s y 1s
        alpha: nivel de significancia
        df: grados de libertad (usualmente 1)
    
    Retorna:
        chi_stat     : estadístico chi-cuadrado
        chi_critical : valor crítico según tabla
        accept       : True si NO se rechaza H0
    """
    bits = np.array(bits)
    n = len(bits)

    # Observados
    O0 = np.sum(bits == 0)
    O1 = np.sum(bits == 1)

    # Esperados (uniforme)
    E = n / 2

    # Calcular Chi-cuadrado
    chi_stat = ((O0 - E)**2 / E) + ((O1 - E)**2 / E)

    # Valor crítico por tabla
    chi_critical = chi2.ppf(1 - alpha, df)

    # Decisión
    accept = chi_stat <= chi_critical

    return chi_stat, chi_critical, accept


# -----------------------------------------------------
# Ejemplo de uso
# -----------------------------------------------------
if __name__ == "__main__":
    bits = np.random.randint(0, 2, 10000)

    chi, crit, ok = frequency_test_chi_square(bits, alpha=0.05, df=1)

    print("Chi-cuadrado:", chi)
    print("Valor crítico:", crit)
    print("¿Aceptar H0 (frecuencia uniforme)?", ok)
