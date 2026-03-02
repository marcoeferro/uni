from LCG import congruencial_lineal
from collections import Counter

def formatter(muestra): #funcion auxiliar 1, formatea el arreglo de numeros aleatorios en un arreglo de numeros de 5 digitos
    muestraString = ["{:.5f}".format(num) for num in muestra]
    return [item.replace("0.","") for item in muestraString]    

def clasificador(item): #funcion auxiliar 2, devuelve el indice del diccionario segun la frecuencia de digitos observada
    frecuencias = list(Counter(item).values())
    if 5 in frecuencias: return "Q"
    if 4 in frecuencias: return "P"
    if 3 in frecuencias and 2 in frecuencias: return "TP"
    if 3 in frecuencias: return "T"
    if frecuencias.count(2) == 2: return "2P"
    if 2 in frecuencias: return "1P"
    return "TD"

def getFrecuenciasObservadas(muestra): #hace un conteo de frecuenciasobservadas
    frecuenciaObservada= {
        "TD":0, #todos distintos - 1
        "1P":0, #1 par - 2
        "2P":0, #2 pares - 3
        "TP":0, #1 trio 2 pares - 4
        "T":0,  #1 trio - 5
        "P":0,  #Poker - 6
        "Q":0,  #quintilla - 7
    }
    muestra = formatter(muestra)
    for item in muestra:
        frecuenciaObservada[clasificador(item)] += 1

    return frecuenciaObservada

def calcularEstadistico(frecuenciaObservada,frecuenciaEsperada):
    return sum([((FO - FE)**2)/FE for FO,FE in zip(frecuenciaObservada,frecuenciaEsperada)])


probabilidadCategoria= {
        "TD":0.30240, #todos distintos
        "1P":0.50400, #1 par
        "2P":0.10800, #2 pares
        "TP":0.00900, #1 trio 2 pares
        "T":0.07200,  #1 trio 
        "P":0.00450,  #Poker 
        "Q":0.00010,  #quintilla -
    }
n = 100
numerosAleatorios = congruencial_lineal(num_aleatorios=n,_0a1=True)
print(f"numeros: {numerosAleatorios}")

frecuenciaObservada = getFrecuenciasObservadas(numerosAleatorios)
print(f"frecuencias observada: {frecuenciaObservada}")

frecuenciaEsperada = [round(n*probabilidad,5) for probabilidad in list(probabilidadCategoria.values())]
print(f"frecuencia esperada: {frecuenciaEsperada}")

estadistico = calcularEstadistico(list(frecuenciaObservada.values()),frecuenciaEsperada)
print(f"estadistico: {estadistico}")
#X^2_alfa_6 = 12,5916 ; si el estadistico es menor que este valor, entonces podemos decir que es una distribucion uniforme
