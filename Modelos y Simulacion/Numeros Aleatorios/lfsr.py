from pruebas import prueba_frecuencias,prueba_poker,prueba_promedios,prueba_smirmov

def lfsr(seed, taps, length, amount):
    state = seed
    result = []
    for _ in range(length * amount):
        xor = 0
        for t in taps:
            xor ^= (state >> t) & 1
        state = (state >> 1) | (xor << (len(bin(seed)) - 3))
        result.append(state & 1)
    return result

def binary_to_decimal(binary_list, m):
    groups = [binary_list[i:i + m] for i in range(0, len(binary_list), m)]
    decimal_numbers = [int("".join(map(str, group)), 2) for group in groups]
    return decimal_numbers

def generador(amount, seed=0b1101, taps=[3, 2], length=8):
    random_bits = lfsr(seed=seed, taps=taps, length=length, amount=amount)
    decimal_numbers = binary_to_decimal(binary_list=random_bits, m=length)
    return decimal_numbers

# Ejemplo de uso
amount = 1000
seed = 0b1101
taps = [3, 2]
length = 8

numeros = generador(amount=amount, seed=seed, taps=taps, length=length)

# Prueba de Frecuencias
chi2_frec, p_frec = prueba_frecuencias(numeros)
print(f"Prueba de Frecuencias: chi2 = {chi2_frec}, p = {p_frec}")

# Prueba de Promedios
promedio = prueba_promedios(numeros)
print(f"Prueba de Promedios: promedio = {promedio}")

# Prueba de Smirnov
d_smirnov, p_smirnov = prueba_smirmov(numeros)
print(f"Prueba de Smirnov: D = {d_smirnov}, p = {p_smirnov}")

# Prueba de Poker
chi2_poker, p_poker = prueba_poker(numeros, m=length)
print(f"Prueba de Poker: chi2 = {chi2_poker}, p = {p_poker}")