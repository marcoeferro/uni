import Congruencial
from scipy import stats as stats
from collections import Counter

def format_samples(samples):
    """Convierte una lista de números flotantes a cadenas de 5 dígitos sin el prefijo "0." """
    return [str("{:.5f}".format(num)).replace("0.", "") for num in samples]

def categorize_item(item):
    """Clasifica cada número de 5 dígitos en una categoría según la frecuencia de aparición de sus dígitos."""
    freq_counts = list(Counter(item).values())
    if 5 in freq_counts: return "Quintilla"                        # Quintilla
    if 4 in freq_counts: return "Poker"                            # Poker
    if 3 in freq_counts and 2 in freq_counts: return "Full House"  # Full House (trío y par)
    if 3 in freq_counts: return "Trio"                             # Trío
    if freq_counts.count(2) == 2: return "2Pares"                  # Dos pares
    if 2 in freq_counts: return "1Par"                             # Un par
    return "Todos Distintos"                                       # Todos distintos

def observe_frequencies(samples):
    """Cuenta las frecuencias observadas de cada categoría en la muestra."""
    observed_freqs = { "Todos Distintos": 0, "1Par": 0, "2Pares": 0, "Full House": 0, "Trio": 0, "Poker": 0, "Quintilla": 0 }
    formatted_samples = format_samples(samples)
    for item in formatted_samples:
        observed_freqs[categorize_item(item)] += 1
    return observed_freqs

def compute_statistic(observed, expected):
    """Calcula el estadístico chi-cuadrado comparando frecuencias observadas y esperadas."""
    return sum(((obs - exp) ** 2) / exp for obs, exp in zip(observed, expected))

def chi_squared_test(alpha, grados_libertad, calculated_value): 
    # Obtener el valor crítico de chi-cuadrado para el nivel de significancia dado y grados de libertad 
    critical_value = stats.chi2.ppf(1 - alpha, grados_libertad) 
    # Comparar el valor calculado con el valor crítico 
    if calculated_value > critical_value: 
        print("Los numeros no provienen de una distribucion uniforme \n" )
    else: 
        print("Los numeros provienen de una distribucion uniforme \n") 



#PRUEBA
# Probabilidades teóricas para cada categoría
category_probabilities = {
    "Todos Distintos": 0.30240, "1Par": 0.50400, "2Pares": 0.10800, "Full House": 0.00900,
    "Trio": 0.07200, "Poker": 0.00450, "Quintilla": 0.00010,
}
sample_size = 100

# Ejemplo de uso
lcg = Congruencial.Congruencial(seed=12345)

random_numbers = lcg.randoms(cantidad_numeros=sample_size)
print("Números generados:", random_numbers,"\n")

# Calcular frecuencias observadas
observed_frequencies = observe_frequencies(random_numbers)
print("Frecuencias observadas:", observed_frequencies,"\n")

# Calcular frecuencias esperadas
expected_frequencies = [round(sample_size * prob, 5) for prob in category_probabilities.values()]
print("Frecuencias esperadas:", expected_frequencies,"\n")

# Calcular el estadístico chi-cuadrado
chi_square_stat = compute_statistic(list(observed_frequencies.values()), expected_frequencies)
print("Estadístico Chi-cuadrado:", chi_square_stat,"\n")

chi_squared_test(alpha=0.05, grados_libertad=6, calculated_value=chi_square_stat)
# Valor crítico chi-cuadrado con α=0.05 y 6 grados de libertad: 12.5916
# Si el estadístico es menor que este valor, la hipótesis de uniformidad no se rechaza.
