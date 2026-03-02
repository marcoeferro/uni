##Lauty Galeano##

from LCG import congruencial_lineal
import scipy.stats as stats
import math

def buscar_z_alpha2(alpha):
    z_alpha_2 = stats.norm.ppf(1 - alpha / 2)
    return z_alpha_2

def prueba_promedio(muestra,tolerancia):
    media = sum(muestra) / cantElementos
    Z_zero = ((media - 1/2)*math.sqrt(cantElementos))/math.sqrt(1/12)
    print(f"Z_0 es :{abs(Z_zero)}")
    print(f"media: {media}")

    alfa = 1 - tolerancia

    z_alpha_2 = buscar_z_alpha2(alfa)
    print(f"Z_alpha/2: {z_alpha_2}")

    if abs(Z_zero) < z_alpha_2:
        print("La distribución es uniforme.")
    else:
        print("La distribución no es uniforme.")

cantElementos = 30
muestra = congruencial_lineal(num_aleatorios=cantElementos,_0a1 = True) ## semilla seed, multiplicador a, incremento c, modulo m , min , max
print(muestra)
prueba_promedio(muestra, tolerancia=0.95)
