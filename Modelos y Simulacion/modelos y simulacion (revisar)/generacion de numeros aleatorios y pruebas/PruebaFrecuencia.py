##Lauty Galeano##

from LCG import congruencial_lineal  #Nuestro generador de numeros pseudoaleatorios


def distribuirNumeros(numeroIntervalos,numeros):    #distribuye los numeros generados en un arreglo con frecuecias observadas
    tamanioIntervalo = 1/numeroIntervalos
    techo = tamanioIntervalo
    piso = 0
    distribucion = []
        

    for i in range(numeroIntervalos):
        distribucion.append(0)
        for num in numeros:
            if piso < num <= techo:
                distribucion[i] += 1
        piso = techo
        techo += tamanioIntervalo

    return distribucion
    
def calculadoraEstadistico(FO,FE): #devuelve (X^2)_0
    acumulado = 0
    for x in FO: acumulado += (x-FE)**2
    return acumulado/FE

    

numeroIntervalos = 5
tamanioMuestra = 100
fEsperada = tamanioMuestra/numeroIntervalos
numerosAleatorios = congruencial_lineal(num_aleatorios=tamanioMuestra,_0a1 = True)
fObservada = distribuirNumeros(numeroIntervalos,numerosAleatorios)
estadistico = calculadoraEstadistico(fObservada,fEsperada)

print(f"numeros:{numerosAleatorios}")
print(f"frecuencia observada: {fObservada}")
print(f"estadistico: {estadistico}")

