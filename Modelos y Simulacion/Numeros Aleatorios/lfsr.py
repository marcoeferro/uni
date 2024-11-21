def rng_number(seed, taps):
    # taps selection
    upper_bit = seed[taps[0]]
    lower_bit = seed[taps[1]]

    xor_bit = upper_bit ^ lower_bit

    output = seed[-1]
    
    # Desplazamiento de los valores un lugar a la derecha
    for idx in range(len(seed) - 1, 0, -1):
        seed[idx] = seed[idx - 1]

    seed[0] = xor_bit
    # print(f"OLD SEED {seed}")
    # print(output)
    return output

def generate_multiple(n, seed, taps):
    digits = []
    seed = [int(i) for i in str(seed)]
    for i in range(n):
        for j in range(4):
            output = rng_number(seed, taps)
            digits.append(output)
        
        decimal = int(''.join(map(str, digits)), 2)
        print(f"El número aleatorio {i + 1} en decimal es: {decimal}")
        digits = []

generate_multiple(seed=1001, n=10, taps=[2, 3])