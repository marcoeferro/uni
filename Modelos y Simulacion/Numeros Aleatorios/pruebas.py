import numpy as np
from scipy.stats import kstest, chisquare, chi2
from collections import Counter

def prueba_frecuencias(numeros):
    frecuencias = np.bincount(numeros)
    chi2, p = chisquare(frecuencias)
    return chi2, p

def prueba_promedios(numeros):
    promedio = np.mean(numeros)
    estadistico = ((promedio-(1/2))*np.sqrt(len(numeros)))/np.sqrt(1/12)
    p_value = kstest([estadistico], 'norm').pvalue
    return estadistico, p_value

def prueba_smirmov(numeros):
    d, p = kstest(numeros, 'uniform', args=(min(numeros), max(numeros) - min(numeros)))
    return d, p

def prueba_poker(numbers, group_size=5):
    """
    Realiza la prueba de Póker para un conjunto de números.

    Args:
        numbers: Lista de números a evaluar.
        group_size: Tamaño de cada grupo de números.

    Returns:
        Un diccionario con las frecuencias observadas y esperadas de cada tipo de mano.
    """

    # Calcular las frecuencias esperadas de cada tipo de mano
    total_groups = len(numbers) // group_size
    expected_freq = {
        'quintilla': total_groups * 0.1,
        'poker': total_groups * 0.45,
        'full': total_groups * 0.9,
        'tercia': total_groups * 7.2,
        'dos_pares': total_groups * 10.8,
        'par': total_groups * 50.4,
        'diferentes': total_groups * 30.24
    }

    # Agrupar los números y contar las frecuencias observadas
    observed_freq = {k: 0 for k in expected_freq}
    for i in range(0, len(numbers), group_size):
        group = tuple(sorted(numbers[i:i+group_size]))
        counts = Counter(group)
        if len(counts) == 1:
            observed_freq['quintilla'] += 1
        elif len(counts) == 2:
            if 4 in counts.values():
                observed_freq['poker'] += 1
            else:
                observed_freq['full'] += 1
        elif len(counts) == 3:
            if 3 in counts.values():
                observed_freq['tercia'] += 1
            else:
                observed_freq['dos_pares'] += 1
        elif len(counts) == 4:
            observed_freq['par'] += 1
        elif len(counts) == 5:
            observed_freq['diferentes'] += 1

    # Calcular el estadístico de prueba (chi-cuadrado)
    chi_squared = 0
    for hand, observed in observed_freq.items():
        expected = expected_freq[hand]
        chi_squared += (observed - expected)**2 / expected

    # Calcular el valor p
    df = len(expected_freq) - 1  # Grados de libertad
    p_value = 1 - chi2.cdf(chi_squared, df)

    return chi_squared, p_value

def evaluar_pruebas(numeros, tolerancia=0.05):
    resultados = {}
    
    # Ejecutar pruebas
    pruebas = {
        'Frecuencias': prueba_frecuencias,
        'Promedios': prueba_promedios,
        'Smirnov': prueba_smirmov,
        'Poker': prueba_poker
    }

    for nombre, prueba in pruebas.items():
        chi2_val, p_value = prueba(numeros)
        pasa_prueba = p_value >= tolerancia  # Verificación contra la tolerancia
        resultados[nombre] = {
            'chi2': chi2_val,
            'p': p_value,
            'pasa': pasa_prueba
        }
    
    return resultados

# Ejemplo de uso:
numeros = np.random.randint(0, 10, 100)
tolerancia = 0.05
resultados = evaluar_pruebas(numeros, tolerancia)

for prueba, resultado in resultados.items():
    print(f"Prueba {prueba}:")
    print(f"  Valor Chi2: {resultado['chi2']}")
    print(f"  Valor p: {resultado['p']}")
    print(f"  Pasa la prueba: {'Sí' if resultado['pasa'] else 'No'}")