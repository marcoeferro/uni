class Congruencial:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
    
    def randoms(self,
                cantidad_numeros = 100,
                ): #congruencial mixto
        numeros = []
        for _ in range(cantidad_numeros):
            self.seed = (self.a * self.seed + self.c) % self.m
            self.seed / self.m
            numeros.append(self.seed)
        return numeros

# Ejemplo de uso:
# lcg = Congruencial(seed=12345)  # Puedes cambiar el valor de la semilla
# print(lcg.randoms())
