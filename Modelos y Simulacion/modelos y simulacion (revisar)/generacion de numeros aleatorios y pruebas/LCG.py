##lauty galeano##
import time

def congruencial_lineal(
    seed = int(time.time_ns()), 
    a = 1664525, 
    c = 1013904223, 
    m = 4294967296, 
    num_aleatorios= 100,
    min = None,
    max = None,
    _0a1 = False):

  numeros = []  #lista vacia de numeros
  x = seed
  for _ in range(num_aleatorios):
    x = (a * x + c) % m
    numeros.append(x)
  if _0a1==True :numeros=normalizador0a1(numeros,m)
  elif (min!=None and max!=None):numeros = normalizador(min,max,numeros)
  
  return numeros

def normalizador(min,max,numeros):
  return [((num % (max-min+1))+min) for num in numeros]

def normalizador0a1(numeros,modulo,):
  return [round(float(num)/modulo,5) for num in numeros]
  

#Ejemplo de uso:
seed = 99923192  #semilla inicial
a = 1664525  #Multiplicador
c = 1013904223   #incremento
m = 4294967296   #modulo ; tambien define el rango 
num_aleatorios = 100 #numero de numeros aleatorios a generar 
resultado = congruencial_lineal(seed, a, c, m, num_aleatorios,max=20,min=0) #alternativo
#resultado = congruencial_lineal()
print(resultado)