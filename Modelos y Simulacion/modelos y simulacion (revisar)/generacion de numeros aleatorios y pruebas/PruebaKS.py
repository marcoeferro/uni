from LCG import congruencial_lineal

def calculadoraKS(distribucionAcumulada,muestra):
    return max([abs(f_xi - x_i) for f_xi,x_i in zip(distribucionAcumulada,muestra)])

tamanioMuestra = 10
numerosAleatorios = congruencial_lineal(num_aleatorios=tamanioMuestra,_0a1=True) #generacion de numeros aleatorios en el rango de 0 a 1
numerosAleatorios.sort() #ordenamos
print(f"muestra generada: {numerosAleatorios}")
distribucionAcumulada = [i/tamanioMuestra for i in range(len(numerosAleatorios)+1)] #aplicamos formula de distribucion acumulada
print(f"distribucion acumulada: {distribucionAcumulada}")
estadisticoKS = calculadoraKS(distribucionAcumulada,numerosAleatorios)
print(f"estadistico: {round(estadisticoKS,3)}")