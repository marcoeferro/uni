import numpy as np
from scipy.stats import kstest, chisquare

def prueba_frecuencias(numeros):
    frecuencias = np.bincount(numeros)
    chi2, p = chisquare(frecuencias)
    return chi2, p

def prueba_promedios(numeros):
    promedio = np.mean(numeros)
    return promedio

def prueba_smirmov(numeros):
    d, p = kstest(numeros, 'uniform', args=(min(numeros), max(numeros) - min(numeros)))
    return d, p

def prueba_poker(numeros, m):
    from collections import Counter
    grupos = [tuple(numeros[i:i + m]) for i in range(0, len(numeros), m)]
    conteo = Counter(grupos)
    chi2, p = chisquare(list(conteo.values()))
    return chi2, p


