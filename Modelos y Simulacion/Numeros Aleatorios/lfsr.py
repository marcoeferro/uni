def lfsr(seed, taps, length):
    state = seed
    result = []
    for _ in range(length):
        xor = 0
        for t in taps:
            xor ^= (state >> t) & 1
        state = (state >> 1) | (xor << (len(bin(seed)) - 3))
        result.append(state & 1)
    return result, state  # También retornamos el nuevo estado


def generador(cantidad, seed=0b1101, taps=[3, 2], length=8):
    current_seed = seed  # Mantener el estado del LFSR entre iteraciones
    
    for _ in range(cantidad):
        random_bits, current_seed = lfsr(current_seed, taps, length)  # Actualizamos la semilla

        # Convertir la lista de bits a una cadena binaria
        bin_str = ''.join(map(str, random_bits))

        # Convertir la cadena binaria a un número decimal
        decimal_number = int(bin_str, 2)

        print(f"Los bits son: {bin_str}, el número en decimal es: {decimal_number}")


# Ejemplo de uso
generador(5, seed=0b1101, taps=[3, 2], length=8)
