import Congruencial

def distribute_numbers(num_intervals, numbers):
    """Distributes numbers into intervals and returns the observed frequencies.

    Args:
        num_intervals: The number of intervals to divide the data into.
        numbers: A list of random numbers.

    Returns:
        A list of observed frequencies for each interval.
    """
    interval_size = 1 / num_intervals
    ceiling = interval_size
    floor = 0
    distribution = [0] * num_intervals

    for i in range(num_intervals):
        for num in numbers:
            if floor < num <= ceiling:
                distribution[i] += 1
        floor = ceiling
        ceiling += interval_size

    return distribution

def calculate_chi_squared(observed_frequencies, expected_frequency):
    """Calculates the chi-squared statistic.

    Args:
        observed_frequencies: A list of observed frequencies.
        expected_frequency: The expected frequency for each interval.

    Returns:
        The calculated chi-squared statistic.
    """
    return sum([(x - expected_frequency)**2 / expected_frequency for x in observed_frequencies])

"""
Este script realiza una prueba de chi-cuadrado para evaluar si una muestra de números aleatorios
se distribuye uniformemente en un intervalo.

1. Genera una muestra de números aleatorios utilizando el método congruencial lineal.
2. Distribuye los números aleatorios en intervalos y cuenta la frecuencia de ocurrencia en cada intervalo.
3. Calcula el estadístico de chi-cuadrado comparando las frecuencias observadas con las frecuencias esperadas bajo la hipótesis de una distribución uniforme.
4. Imprime los resultados.

El estadístico de chi-cuadrado mide la discrepancia entre las frecuencias observadas y las esperadas. 
Un valor alto del estadístico sugiere que la distribución de los datos difiere significativamente 
de una distribución uniforme.

**Nota:** Para tomar una decisión estadística, se debe comparar el valor del estadístico chi-cuadrado
con un valor crítico obtenido de una tabla o utilizando un software estadístico.
"""



num_intervals = 5
sample_size = 1000
expected_frequency = sample_size / num_intervals

lcg = Congruencial.Congruencial(seed=12345)

random_numbers = lcg.randoms(cantidad_numeros=sample_size)
observed_frequencies = distribute_numbers(num_intervals, random_numbers)
chi_squared = calculate_chi_squared(observed_frequencies, expected_frequency)

print(f"Random numbers: {random_numbers}")
print(f"Observed frequencies: {observed_frequencies}")
print(f"Chi-squared statistic: {chi_squared}")