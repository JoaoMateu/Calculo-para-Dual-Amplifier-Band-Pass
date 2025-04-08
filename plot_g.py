import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import re

def parse_entrada(entrada):
    """
    Extrai o valor numérico e o prefixo (n, u, m, etc.) da string.
    Permite entrada como '2.2u', '10n', 'capacitor de 100n', etc.
    """
    padrao = r'([\d\.]+)\s*([numkp]?)f?'
    match = re.search(padrao, entrada.lower())
    
    if match:
        valor = float(match.group(1))   # número (ex: 2.2)
        sufixo = match.group(2).lower()   # unidade (ex: u)
        return valor, sufixo
    return None, None

def calcular_resistores(C, f0=4000, Q=10):
    """
    Calcula os resistores para que a frequência central do passa-banda seja f0 (Hz).
    
    Para um capacitor C, definimos:
      R2 = R3 = 1/(2π f0 C)
      R1 = Q/(2π f0 C)
    """
    R2 = 1 / (2 * np.pi * f0 * C)
    R3 = R2
    R1 = Q / (2 * np.pi * f0 * C)
    return R1, R2, R3

def criar_funcao_transferencia(R1, R2, R3, C):
    """
    Monta a função de transferência:
         H(s) = [ s * (2/(R1*C)) ] / [ s^2 + s*(1/(R1*C)) + 1/(R2*R3*C^2) ]
    Para o caso R2=R3, 1/(R2*R3*C^2) = 1/(R2^2 * C^2).
    """
    a = 1.0 / (R1 * C)
    b = 1.0 / (R2 * R3 * C**2)
    
    num = [2.0 / (R1 * C), 0.0]  # Numerador: (2/(R1*C)) * s
    den = [1.0, a, b]            # Denominador: s^2 + (1/(R1*C))*s + 1/(R2^2*C^2)
    
    return signal.TransferFunction(num, den)

def calcular_frequencias_corte(R1, R2, R3, C):
    """
    Calcula as frequências de corte f1 e f2 (em Hz) para o filtro passa-banda.
    f0 = frequência central, BW = largura de banda.
    """
    f0 = (1 / (2 * np.pi)) * np.sqrt(1 / (R2 * R3 * C**2))  # Frequência central
    BW = 1 / (2 * np.pi * R1 * C)  # Largura de banda
    f1 = f0 - (BW / 2)  # Frequência de corte inferior
    f2 = f0 + (BW / 2)  # Frequência de corte superior
    return f1, f2

def plot_bode(sys, w_min=10, w_max=1e6):
    """
    Plota o diagrama de Bode (magnitude e fase) para o sistema `sys`
    no intervalo de frequência em Hz, convertido de rad/s [w_min, w_max].
    """
    w = np.logspace(np.log10(w_min), np.log10(w_max), 500)  # varredura logarítmica em rad/s
    w, mag, phase = signal.bode(sys, w=w)
    f = w / (2 * np.pi)  # Converte rad/s para Hz
    
    plt.figure(figsize=(8, 6))
    
    # Magnitude (dB)
    plt.subplot(2, 1, 1)
    plt.semilogx(f, mag, 'b')  # Usa f (Hz) no eixo x
    plt.title("Diagrama de Bode")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True, which="both", ls=":")
    
    # Fase (graus)
    plt.subplot(2, 1, 2)
    plt.semilogx(f, phase, 'r')  # Usa f (Hz) no eixo x
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Fase (graus)")
    plt.grid(True, which="both", ls=":")
    
    plt.tight_layout()
    plt.show()  # Exibe o gráfico

# -----------------------------------------------------------
# 1) Entrada do usuário
entrada = input("Digite o valor do capacitor (ex: 2.2u, capacitor de 10n): ")
valor, sufixo = parse_entrada(entrada)

if valor is None:
    print("❌ Entrada inválida. Use algo como '2.2u' ou '10n'.")
    exit()

# 2) Converte o valor para Farads
multiplicadores = {
    '': 1,
    'n': 1e-9,
    'u': 1e-6,
    'm': 1e-3,
    'k': 1e3,
    'p': 1e-12,
}
fator = multiplicadores.get(sufixo, 1)
C = valor * fator

# 3) Define a frequência central desejada e o fator Q
f0 = 4000  # Hz
Q = 10     # Fator de qualidade

# 4) Calcula os resistores para essa frequência de corte
R1, R2, R3 = calcular_resistores(C, f0=f0, Q=Q)

# 5) Calcula as frequências de corte
f1, f2 = calcular_frequencias_corte(R1, R2, R3, C)

print("\n==> Valores calculados:")
print(f"Capacitor: {valor}{sufixo}F = {C:.3e} F")
print(f"R1 = {R1:.2f} ohms")
print(f"R2 = R3 = {R2:.2f} ohms")
print(f"Frequência central definida: {f0} Hz")
print(f"Frequência de corte inferior (f1): {f1:.2f} Hz")
print(f"Frequência de corte superior (f2): {f2:.2f} Hz")

# 6) Monta a função de transferência e plota o diagrama de Bode
sistema = criar_funcao_transferencia(R1, R2, R3, C)
plot_bode(sistema, w_min=10, w_max=1e6)