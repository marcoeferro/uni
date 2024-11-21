import Congruencial
import scipy.stats as stats
import math

def calculate_z_score(alpha):
    """Calcula el valor crítico Z correspondiente al nivel de confianza dado."""
    return stats.norm.ppf(1 - alpha / 2)

def uniformity_test(sample, confidence):
    """Realiza la prueba de uniformidad utilizando el promedio de la muestra y un estadístico Z."""
    n = len(sample)
    mean_sample = sum(sample) / n
    z_statistic = ((mean_sample - 0.5) * math.sqrt(n)) / math.sqrt(1 / 12)
    print(f"Estadístico Z: {abs(z_statistic):.4f}")
    print(f"Media muestral: {mean_sample:.4f}")

    alpha = 1 - confidence
    critical_z = calculate_z_score(alpha)
    print(f"Valor crítico Z (α/2): {critical_z:.4f}")

    if abs(z_statistic) < critical_z:
        print("La muestra sigue una distribución uniforme.")
    else:
        print("La muestra no sigue una distribución uniforme.")

"""
Este código evalúa si una muestra generada por un generador congruencial lineal sigue una distribución uniforme, 
utilizando una prueba basada en el promedio de los valores de la muestra y el estadístico Z.

1. **Importación de bibliotecas y funciones auxiliares**:
    - `Congruencial`: Contiene la clase para generar números pseudoaleatorios mediante un generador congruencial lineal.
    - `scipy.stats`: Se utiliza para calcular el valor crítico Z correspondiente al nivel de confianza.
    - `math`: Proporciona funciones matemáticas para realizar cálculos.

2. **Cálculo del valor crítico Z (`calculate_z_score`)**:
    - Esta función toma como entrada el nivel de significancia (`alpha`) y calcula el valor crítico Z para un intervalo de confianza de 
        \( 1 - \alpha \).
    - Usa la función `stats.norm.ppf` para obtener el percentil de la distribución normal estándar.

3. **Prueba de uniformidad (`uniformity_test`)**:
    - Toma una muestra de números y un nivel de confianza como entrada.
    - Calcula los siguientes valores:
    - `mean_sample`: Promedio de los valores en la muestra.
    - `z_statistic`: Estadístico Z que mide la desviación del promedio muestral respecto al esperado (0.5 para una distribución uniforme).
        Este cálculo se realiza con la fórmula:
        \[
        Z = \frac{\text{mean_sample} - 0.5}{\sqrt{\frac{1}{12}}} \cdot \sqrt{n}
        \]
        donde \( n \) es el tamaño de la muestra y \( \frac{1}{12} \) es la varianza de una distribución uniforme continua en [0,1].
    - Calcula el valor crítico Z para el nivel de confianza dado.
    - Compara el valor absoluto del estadístico Z con el valor crítico Z:
    - Si \( |Z| < Z_{\text{crítico}} \), no se rechaza la hipótesis nula, y se concluye que la muestra podría provenir de una distribución uniforme.
    - De lo contrario, se rechaza la hipótesis nula.

4. **Generación de la muestra**:
    - Se usa la clase `Congruencial` para generar una muestra de tamaño 100 con un generador congruencial lineal.
    - Los números generados se almacenan en `random_sample`.

5. **Prueba de uniformidad en acción**:
    - Llama a `uniformity_test` con la muestra generada y un nivel de confianza del 90% (0.90).
    - Imprime el estadístico Z, el valor crítico y una conclusión sobre si la muestra sigue una distribución uniforme.

Este código es útil para evaluar la calidad de un generador de números pseudoaleatorios al verificar si los números generados
parecen uniformemente distribuidos en el intervalo [0,1].
"""

# Ejemplo de uso
sample_size = 100
lcg = Congruencial.Congruencial(seed=12345)

random_sample = lcg.randoms(cantidad_numeros=sample_size)
uniformity_test(random_sample, confidence=0.90)
