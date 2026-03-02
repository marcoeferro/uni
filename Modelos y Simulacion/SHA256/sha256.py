import struct

# Constantes SHA-256
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


# Funciones auxiliares
def rotr(x, n, w=32):
    return (x >> n) | ((x << (w - n)) & (2**w - 1))

def sha256_compress(chunk, H):
    # Extender los bloques
    W = list(struct.unpack(">16L", chunk)) + [0] * 48
    for t in range(16, 64):
        s0 = rotr(W[t - 15], 7) ^ rotr(W[t - 15], 18) ^ (W[t - 15] >> 3)
        s1 = rotr(W[t - 2], 17) ^ rotr(W[t - 2], 19) ^ (W[t - 2] >> 10)
        W[t] = (W[t - 16] + s0 + W[t - 7] + s1) & 0xFFFFFFFF

    # Inicializar variables
    a, b, c, d, e, f, g, h = H

    # Rondas de compresión
    for t in range(64):
        S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        temp1 = (h + S1 + ch + K[t] + W[t]) & 0xFFFFFFFF
        S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & 0xFFFFFFFF
        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF

    # Actualizar valores de hash
    return [
        (H[0] + a) & 0xFFFFFFFF,
        (H[1] + b) & 0xFFFFFFFF,
        (H[2] + c) & 0xFFFFFFFF,
        (H[3] + d) & 0xFFFFFFFF,
        (H[4] + e) & 0xFFFFFFFF,
        (H[5] + f) & 0xFFFFFFFF,
        (H[6] + g) & 0xFFFFFFFF,
        (H[7] + h) & 0xFFFFFFFF,
    ]

# Preprocesamiento
def sha256_padding(message):
    message_bytes = bytearray(message, 'ascii')
    original_length = len(message_bytes) * 8
    message_bytes.append(0x80)
    while len(message_bytes) % 64 != 56:
        message_bytes.append(0)
    message_bytes += struct.pack(">Q", original_length)
    return message_bytes

# Algoritmo SHA-256
def sha256(message):
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]
    padded_message = sha256_padding(message)
    for i in range(0, len(padded_message), 64):
        chunk = padded_message[i:i + 64]
        H = sha256_compress(chunk, H)
    return ''.join(f'{x:08x}' for x in H)

# Prueba del algoritmo
mensaje = "abc"
print("Hash SHA-256:", sha256(mensaje))


"""
Este script implementa una versión educativa y compacta del algoritmo de hash SHA-256.

1) Importación y constantes:
   - Se importa 'struct' para empacar/desempacar bytes en enteros y viceversa.
   - 'K' define los 64 valores constantes específicos del estándar SHA-256, usados en cada ronda
     del proceso de compresión.

2) Función auxiliar: rotación a la derecha (rotr):
   - rotr(x, n, w=32) realiza una rotación a la derecha de 'x' por 'n' bits en un ancho de 32 bits.
   - Combina desplazamiento y enmascarado para simular aritmética de 32 bits (mod 2^32).

3) Función sha256_compress(chunk, H):
   - Entrada:
     * 'chunk': bloque de 64 bytes del mensaje preprocesado.
     * 'H': lista de 8 enteros de 32 bits que representan el estado actual del hash.
   - Extensión del mensaje (W):
     * Desempaqueta 'chunk' en 16 palabras de 32 bits (big-endian).
     * Genera 64 palabras totales (W[0..63]), donde W[16..63] se calculan con las funciones
       σ0 y σ1 (pequeñas sigmas) conforme al estándar:
         s0 = rotr(W[t-15], 7) ^ rotr(W[t-15], 18) ^ (W[t-15] >> 3)
         s1 = rotr(W[t-2], 17) ^ rotr(W[t-2], 19) ^ (W[t-2] >> 10)
       * Cada nueva palabra se limita a 32 bits con & 0xFFFFFFFF.
   - Inicializa variables de trabajo (a..h) copiando H.
   - 64 rondas de compresión:
     * Calcula funciones:
         S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)   (Σ1 grande)
         ch = (e & f) ^ (~e & g)                        (choose)
         S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)    (Σ0 grande)
         maj = (a & b) ^ (a & c) ^ (b & c)              (majority)
     * temp1 = h + S1 + ch + K[t] + W[t] (mod 2^32)
     * temp2 = S0 + maj (mod 2^32)
     * Actualiza el estado (a..h) desplazando y combinando temp1 y temp2.
   - Actualización del hash:
     * Suma (mod 2^32) cada registro a..h al estado H original y devuelve el nuevo H.

4) Preprocesamiento: sha256_padding(message):
   - Convierte el 'message' (string ASCII) a 'bytearray'.
   - Calcula la longitud original en bits.
   - Añade el byte 0x80 (bit '1' seguido de ceros).
   - Rellena con ceros hasta que la longitud sea congruente a 56 mod 64 (dejando 8 bytes finales).
   - Añade 8 bytes (big-endian) con la longitud original en bits.
   - Devuelve el mensaje preparado en bloques de 64 bytes.

5) Función principal: sha256(message):
   - Inicializa H con los 8 valores iniciales estándar de SHA-256.
   - Aplica el padding al mensaje para obtener 'padded_message'.
   - Itera sobre 'padded_message' en pasos de 64 bytes:
     * Para cada 'chunk', llama a sha256_compress y actualiza H.
   - Devuelve el hash final como cadena hexadecimal de 64 caracteres (8 enteros de 32 bits).

6) Prueba:
   - Define 'mensaje = "abc"'.
   - Imprime "Hash SHA-256:" seguido del resultado de sha256("abc").

Notas:
- Esta implementación sigue el flujo estándar de SHA-256: padding → división en bloques →
  extensión del mensaje → 64 rondas por bloque → actualización del estado.
- Todas las operaciones se limitan a 32 bits para replicar el comportamiento de la aritmética modular
  requerida por SHA-256.
"""
