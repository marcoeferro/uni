import scipy.stats as stats

# Valor crítico Z para un nivel de significancia de 0.05 (dos colas)
alpha = 0.05
z_alpha_2 = stats.norm.ppf(1 - alpha / 2)
print(f"Z_alpha/2 para alpha={alpha}: {z_alpha_2}")

# Probabilidad acumulada hasta un valor Z
z_value = 1.96
probabilidad = stats.norm.cdf(z_value)
print(f"Probabilidad acumulada hasta Z={z_value}: {probabilidad}")

# Función de densidad de probabilidad para Z
densidad = stats.norm.pdf(z_value)
print(f"Densidad de probabilidad para Z={z_value}: {densidad}")