import numpy as np
from scipy.stats import chi2
from collections import Counter

# Tabla de frecuencias esperadas (por cada 100 manos)
EXPECTED_FREQ = {
    "todos_diferentes": 30.24,
    "par": 50.40,
    "dos_pares": 10.80,
    "tercia": 7.20,
    "full": 0.90,
    "poker": 0.45,
    "quintilla": 0.10
}

def classify_hand(digits):
    """
    Clasifica una mano (5 dígitos) según las categorías de póker estadísticas.
    """
    counts = sorted(Counter(digits).values(), reverse=True)

    if counts == [5]:
        return "quintilla"
    elif counts == [4, 1]:
        return "poker"
    elif counts == [3, 2]:
        return "full"
    elif counts == [3, 1, 1]:
        return "tercia"
    elif counts == [2, 2, 1]:
        return "dos_pares"
    elif counts == [2, 1, 1, 1]:
        return "par"
    else:
        return "todos_diferentes"


def poker_test(sample, alpha=0.05, df=6):
    """
    Prueba de Póker para generadores pseudoaleatorios.
    
    Parámetros:
        sample: lista/array de números reales en [0,1] (cada uno da una mano)
        alpha : nivel de significancia
        df    : grados de libertad (por defecto 6)

    Retorna:
        chi_stat     : estadístico Chi-cuadrado
        chi_critical : valor crítico de Chi-cuadrado según tabla
        accept       : True si NO se rechaza H0
        observed     : frecuencias observadas por categoría
    """

    n = len(sample)

    # Inicializar contadores
    observed = {
        "todos_diferentes": 0,
        "par": 0,
        "dos_pares": 0,
        "tercia": 0,
        "full": 0,
        "poker": 0,
        "quintilla": 0
    }

    # Clasificar cada número como mano de póker
    for x in sample:
        digits = list(str(f"{x:.5f}").split(".")[1])  # extrae 5 dígitos
        category = classify_hand(digits)
        observed[category] += 1

    # Frecuencias esperadas ajustadas al tamaño de la muestra
    expected = {k: (v / 100.0) * n for k, v in EXPECTED_FREQ.items()}

    # Calcular Chi-cuadrado
    chi_stat = sum((observed[k] - expected[k]) ** 2 / expected[k] for k in observed)

    # Valor crítico de tabla
    chi_critical = chi2.ppf(1 - alpha, df)

    # Decisión
    accept = chi_stat <= chi_critical

    return chi_stat, chi_critical, accept, observed


# -----------------------------------------------------
# Ejemplo de uso
# -----------------------------------------------------
if __name__ == "__main__":
    # Genero 10,000 manos
    sample = np.random.random(10000)

    chi, crit, ok, obs = poker_test(sample, alpha=0.05, df=6)

    print("Chi-cuadrado =", chi)
    print("Valor crítico =", crit)
    print("¿Aceptar H0 (póker pasa la prueba)?", ok)
    print("Frecuencias observadas:", obs)
