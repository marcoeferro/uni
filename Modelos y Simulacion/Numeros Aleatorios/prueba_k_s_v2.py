import numpy as np

# Tabla de valores críticos D_alpha para KS (extraída de tu imagen)
# Formato: tabla[n][alpha]
KS_TABLE = {
    1:  {0.10: 0.950, 0.05: 0.975, 0.01: 0.995},
    2:  {0.10: 0.776, 0.05: 0.842, 0.01: 0.929},
    3:  {0.10: 0.642, 0.05: 0.708, 0.01: 0.829},
    4:  {0.10: 0.564, 0.05: 0.624, 0.01: 0.734},
    5:  {0.10: 0.510, 0.05: 0.563, 0.01: 0.669},
    6:  {0.10: 0.470, 0.05: 0.521, 0.01: 0.618},
    7:  {0.10: 0.438, 0.05: 0.486, 0.01: 0.577},
    8:  {0.10: 0.411, 0.05: 0.457, 0.01: 0.543},
    9:  {0.10: 0.388, 0.05: 0.432, 0.01: 0.514},
    10: {0.10: 0.368, 0.05: 0.409, 0.01: 0.486},
    11: {0.10: 0.352, 0.05: 0.391, 0.01: 0.468},
    12: {0.10: 0.338, 0.05: 0.375, 0.01: 0.450},
    13: {0.10: 0.352, 0.05: 0.361, 0.01: 0.433},
    14: {0.10: 0.314, 0.05: 0.349, 0.01: 0.418},
    15: {0.10: 0.304, 0.05: 0.338, 0.01: 0.404},
    16: {0.10: 0.295, 0.05: 0.328, 0.01: 0.392},
    17: {0.10: 0.286, 0.05: 0.318, 0.01: 0.381},
    18: {0.10: 0.278, 0.05: 0.309, 0.01: 0.371},
    19: {0.10: 0.272, 0.05: 0.301, 0.01: 0.363},
    20: {0.10: 0.264, 0.05: 0.294, 0.01: 0.352},
    25: {0.10: 0.240, 0.05: 0.264, 0.01: 0.317},
    30: {0.10: 0.220, 0.05: 0.242, 0.01: 0.290},
    35: {0.10: 0.210, 0.05: 0.230, 0.01: 0.270},
    40: {0.10: 0.210, 0.05: 0.210, 0.01: 0.252},
    50: {0.10: 0.188, 0.05: 0.188, 0.01: 0.226},
    60: {0.10: 0.172, 0.05: 0.172, 0.01: 0.207},
    70: {0.10: 0.160, 0.05: 0.160, 0.01: 0.192},
    80: {0.10: 0.150, 0.05: 0.150, 0.01: 0.180},
    90: {0.10: 0.141, 0.05: 0.141, 0.01: 0.170},
    100:{0.10: 0.134, 0.05: 0.134, 0.01: 0.160}
}

# Constantes para n > 100 (según la tabla)
KS_CONSTANTS = {0.10: 1.22, 0.05: 1.36, 0.01: 1.63}

def ks_test(sample, alpha=0.05):
    """
    Prueba de Kolmogorov-Smirnov para Uniforme(0,1).

    Parámetros:
        sample: lista/array de números reales en [0,1]
        alpha : nivel de significancia (0.10, 0.05, 0.01)

    Retorna:
        D          : estadístico KS
        D_critical : valor crítico según tabla
        accept     : True si NO se rechaza H0
    """
    sample = np.sort(np.array(sample))
    n = len(sample)

    # Fn(x)
    F_emp = np.arange(1, n+1) / n

    # D = max |Fn(x) - F(x)| con F(x)=x
    D = np.max(np.abs(F_emp - sample))

    # Buscar el valor crítico
    if n <= 100:
        if alpha not in KS_TABLE[n]:
            raise ValueError(f"No hay valor en la tabla KS para alpha={alpha}")
        D_critical = KS_TABLE[n][alpha]
    else:
        # Aproximación para grandes n
        c = KS_CONSTANTS.get(alpha)
        if c is None:
            raise ValueError("alpha debe ser 0.10, 0.05 o 0.01")
        D_critical = c / np.sqrt(n)

    # Decisión
    accept = D <= D_critical

    return D, D_critical, accept


# -----------------------------------------------------
# EJEMPLO DE USO
# -----------------------------------------------------
if __name__ == "__main__":
    sample = np.random.random(50)
    D, Dc, ok = ks_test(sample, alpha=0.05)
    print("D =", D)
    print("D crítico =", Dc)
    print("¿Aceptar H0 (uniforme)?", ok)
