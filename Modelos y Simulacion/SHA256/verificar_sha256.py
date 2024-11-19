import hashlib
from sha256 import sha256


def calculate_sha256_hash(message):
    """
    Calcula el hash SHA-256 de un mensaje utilizando la librería hashlib.
    """
    # Convertir el mensaje a bytes
    message_bytes = message.encode('utf-8')
    # Crear el objeto hash
    sha256_hash = hashlib.sha256()
    # Alimentar el mensaje al objeto hash
    sha256_hash.update(message_bytes)
    # Obtener el hash final en formato hexadecimal
    return sha256_hash.hexdigest()

# Mensaje de ejemplo
mensaje = "abc"

# Calcular hash con hashlib
hash_resultado = calculate_sha256_hash(mensaje)

# Imprimir resultado
print(f"Mensaje: {mensaje}")
print(f"Hash SHA-256: {hash_resultado}")

# Hash esperado para "abc" (verificado en estándares y herramientas externas)
hash_esperado = sha256(mensaje)
print(f"Hash esperado: {hash_esperado}")
print(f"¿El hash coincide?: {'Sí' if hash_resultado == hash_esperado else 'No'}")
