import numpy as np
from ShaHelperFunctions import *

def mensaje_convertidor(mensaje):
    # Procesamiento de mensaje
    mensaje = ''.join(format(ord(c), '08b') for c in mensaje)  # String a binario
    mensaje_bin_1 = mensaje + '1'  # Añadir bit "1" al final
    x = (448 - len(mensaje_bin_1)) % 512  # Calcular X
    mensaje_bin_1x = mensaje_bin_1 + '0' * x #añadimos X cantidad de 0's al final
    longitud_bin = format(len(mensaje), '064b')  # Longitud del mensaje original en bits (64 bits)
    return mensaje_bin_1x + longitud_bin #Menssaje extendido

def sha256(mensaje):
    # Valores iniciales hash
    h0 = int('6a09e667', 16)
    h1 = int('bb67ae85', 16)
    h2 = int('3c6ef372', 16)
    h3 = int('a54ff53a', 16)
    h4 = int('510e527f', 16)
    h5 = int('9b05688c', 16)
    h6 = int('1f83d9ab', 16)
    h7 = int('5be0cd19', 16)

    k = [int(x, 16) for x in [
        '428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5',
        'd807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174',
        'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da',
        '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967',
        '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85',
        'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070',
        '19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3',
        '748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2'
    ]]

    # dividimos el mensaje en bloques de 512 bits
    bloques = [mensaje[i:i+512] for i in range(0, len(mensaje), 512)]

    for bloque in bloques:
        #creamos un array w vacio de 64 palabras, y luego insertamos el bloque repartido en las 16 posiciones
        w = [int(bloque[i:i+32], 2) for i in range(0, 512, 32)] + [0] * 48
        #lazo 1 - asignamos valores desde w[16] hasta w[64]
        for i in range(16, 64):
            s0 = sigma0(w[i - 15])
            s1 = sigma1(w[i - 2])
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) % 2**32

        # Inicializar valores de trabajo
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        # Lazo 2 - compresion para cada palabra del arreglo w
        for i in range(64):
            S1 = sum1(e)
            ch_val = ch(e, f, g)
            temp1 = (h + S1 + ch_val + k[i] + w[i]) % 2**32
            S0 = sum0(a)
            maj = Maj(a, b, c)
            temp2 = (S0 + maj) % 2**32

            h = g
            g = f
            f = e
            e = (d + temp1) % 2**32
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % 2**32

        # al final de cada iteracion, sumamos h_n con su respectiva variable usando suma mod 2^32
        h0 = (h0 + a) % 2**32
        h1 = (h1 + b) % 2**32
        h2 = (h2 + c) % 2**32
        h3 = (h3 + d) % 2**32
        h4 = (h4 + e) % 2**32
        h5 = (h5 + f) % 2**32
        h6 = (h6 + g) % 2**32
        h7 = (h7 + h) % 2**32

    # por ultimo concatenamos todo en un hash final
    hash_final = ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4, h5, h6, h7])
    return hash_final


#MAIN
mensaje = "Lautaro Galeano 2024"
mensaje_bin = mensaje_convertidor(mensaje)
resultado_hash = sha256(mensaje_bin)
print(resultado_hash)
