def ch(x, y, z):
    return (x & y) ^ (~x & z)

def Maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def rightShift(value, shift):
    return value >> shift

def rotR(value, shift):
    return (value >> shift) | (value << (32 - shift) & 0xFFFFFFFF)

def sigma0(x):
    return rotR(x, 7) ^ rotR(x, 18) ^ rightShift(x, 3)

def sigma1(x):
    return rotR(x, 17) ^ rotR(x, 19) ^ rightShift(x, 10)

def sum0(x):
    return rotR(x, 2) ^ rotR(x, 13) ^ rotR(x, 22)

def sum1(x):
    return rotR(x, 6) ^ rotR(x, 11) ^ rotR(x, 25)