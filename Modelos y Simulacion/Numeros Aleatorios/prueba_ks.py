import Congruencial

def calculate_ks_statistic(cumulative_distribution, sample):
    """Calculates the Kolmogorov-Smirnov statistic.

    Args:
        cumulative_distribution: A list of cumulative probabilities.
        sample: A sorted list of sample data.

    Returns:
        The maximum absolute difference between the cumulative distribution
        and the empirical distribution function.
    """
    return max([abs(f_xi - x_i) for f_xi, x_i in zip(cumulative_distribution, sample)])

"""
Este script implementa la prueba de Kolmogorov-Smirnov para evaluar si una muestra de datos
se ajusta a una distribución uniforme.

1. Genera una muestra de números aleatorios utilizando el método congruencial lineal.
2. Calcula la distribución acumulada empírica de la muestra.
3. Calcula el estadístico de Kolmogorov-Smirnov.
4. Imprime los resultados.

El estadístico de Kolmogorov-Smirnov se utiliza para medir la máxima diferencia entre 
la distribución acumulada teórica y la empírica. Un valor bajo del estadístico sugiere 
que la muestra se ajusta bien a la distribución uniforme.

**Nota:** Para realizar una prueba de hipótesis formal, se necesitaría comparar el valor 
del estadístico KS con un valor crítico obtenido de una tabla o utilizando un software estadístico.
"""



sample_size = 10
lcg = Congruencial.Congruencial(seed=12345)

random_numbers = lcg.randoms(cantidad_numeros=sample_size)
random_numbers.sort()
print(f"Generated sample: {random_numbers}")

cumulative_probabilities = [(i + 1) / sample_size for i in range(sample_size)]
print(f"Cumulative probabilities: {cumulative_probabilities}")

ks_statistic = calculate_ks_statistic(cumulative_probabilities, random_numbers)
print(f"KS statistic: {round(ks_statistic, 3)}")