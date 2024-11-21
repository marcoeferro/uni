import Congruencial

def calculate_ks_statistic(cumulative_distribution, sample):
    return max([abs(f_xi - x_i) for f_xi, x_i in zip(cumulative_distribution, sample)])


def kolmogorov_smirnov_table(): 
    # Aquí se incluirá una parte de la tabla de Kolmogorov-Smirnov como un diccionario para referencia rápida 
    ks_table = { 
                0.01: [0,1.63, 1.95, 2.10, 2.22, 2.32], # alfa = 0.01 
                0.05: [0,1.36, 1.48, 1.56, 1.62, 1.68], # alfa = 0.05 
                0.10: [0,0.950, 0.36, 1.41, 1.48, 1.51] # alfa = 0.10 
                } 
    return ks_table 

def get_ks_value(sample_size, alpha): 
    ks_table = kolmogorov_smirnov_table() 
    if alpha not in ks_table: 
        raise ValueError("Alpha no válido. Por favor, use 0.01, 0.05 o 0.10.") 
    if sample_size <= 5: index = sample_size - 1 
    else: # Para simplificar, usamos el último valor para sample_size > 5 
        index = 4 
    
    return ks_table[alpha][index]


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
"""

sample_size = 10
lcg = Congruencial.Congruencial(seed=12345)

random_numbers = lcg.randoms(cantidad_numeros=sample_size)
random_numbers.sort()
print(f"Generated sample: {random_numbers}")

cumulative_probabilities = [i / sample_size for i in range(sample_size)]
print(f"Cumulative probabilities: {cumulative_probabilities}")

ks_statistic = calculate_ks_statistic(cumulative_probabilities, random_numbers)
print(f"KS statistic: {round(ks_statistic, 3)}")

d = get_ks_value(sample_size=sample_size,alpha=0.05)

print(f"d_alpha statistic: {d}")

test = kolmogorov_smirnov_table()
print(test[0.10][1])
print(f"Los NUMEROS provienen de una distribucion uniforme") if ks_statistic < d else print(f"Los NUMEROS no provienen de una distribucion uniforme") 