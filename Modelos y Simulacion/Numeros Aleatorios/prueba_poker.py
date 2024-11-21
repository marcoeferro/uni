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


"""
Este código implementa una prueba estadística para evaluar si los números generados por un generador congruencial lineal 
siguen una distribución uniforme al analizar las frecuencias de categorías específicas en los dígitos de los números generados.

1. **Formato de muestras (`format_samples`)**:
    - Convierte una lista de números flotantes a cadenas de 5 dígitos sin el prefijo "0." para analizar sus dígitos.
    - Ejemplo: Un número como `0.12345` se convierte en `"12345"`.

2. **Clasificación de patrones (`categorize_item`)**:
    - Clasifica cada número de 5 dígitos en una categoría según la frecuencia de aparición de sus dígitos:
        - `"Quintilla"`: Todos los dígitos son iguales (ej., `11111`).
        - `"Poker"`: Cuatro dígitos iguales (ej., `11112`).
        - `"Full House"`: Tres dígitos iguales y dos iguales (ej., `11122`).
        - `"Trio"`: Tres dígitos iguales (ej., `11123`).
        - `"2Pares"`: Dos pares distintos (ej., `11223`).
        - `"1Par"`: Un par (ej., `11234`).
        - `"Todos Distintos"`: Todos los dígitos son diferentes (ej., `12345`).

3. **Frecuencias observadas (`observe_frequencies`)**:
    - Recorre las muestras formateadas y clasifica cada una en una de las categorías mencionadas.
    - Cuenta cuántos números corresponden a cada categoría y devuelve un diccionario con las frecuencias observadas.

4. **Estadístico Chi-cuadrado (`compute_statistic`)**:
    - Calcula el estadístico chi-cuadrado utilizando la fórmula:
        \[
        \chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}
        \]
        donde \( O_i \) son las frecuencias observadas y \( E_i \) son las frecuencias esperadas.

5. **Prueba de hipótesis Chi-cuadrado (`chi_squared_test`)**:
    - Determina si los números generados siguen una distribución uniforme.
    - Calcula el valor crítico chi-cuadrado usando la función `stats.chi2.ppf` con el nivel de significancia (\( \alpha \)) y los grados de libertad.
    - Compara el estadístico chi-cuadrado calculado con el valor crítico:
        - Si el valor calculado es mayor que el crítico, se rechaza la hipótesis nula (los números no son uniformes).
        - Si no, no se rechaza la hipótesis nula (los números son uniformes).

6. **Prueba aplicada**:
   - **Probabilidades teóricas**: Define las probabilidades de ocurrencia de cada categoría según la teoría de combinatoria.
   - **Tamaño de muestra**: Se genera una muestra de tamaño 100 utilizando un generador congruencial lineal (`Congruencial`).
   - **Cálculo de frecuencias**:
     - **Observadas**: Cuenta cuántas muestras caen en cada categoría usando `observe_frequencies`.
     - **Esperadas**: Calcula las frecuencias esperadas multiplicando las probabilidades teóricas por el tamaño de la muestra.
   - **Estadístico Chi-cuadrado**: Se calcula comparando frecuencias observadas y esperadas.
   - **Prueba de hipótesis**:
        - Nivel de significancia (\( \alpha \)) es 0.05.
        - Grados de libertad: 6 (número de categorías - 1).
        - Valor crítico chi-cuadrado para α=0.05 y 6 grados de libertad: 12.5916.
        - Se imprime si los números generados provienen de una distribución uniforme o no.

Este código es útil para evaluar la calidad de un generador pseudoaleatorio analizando la distribución de patrones en los dígitos generados.
"""
