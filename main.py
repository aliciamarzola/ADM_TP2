import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import os
from datetime import datetime

def calcular_wacc(D, E, rD, rE, T=0.0, considerar_impostos=True):
    """
    Calcula o WACC (custo médio ponderado de capital).
    
    D: valor da dívida
    E: valor do equity
    rD: custo da dívida (decimal, ex: 0.08)
    rE: custo do equity (decimal, ex: 0.12)
    T: alíquota do imposto (decimal, ex: 0.34)
    considerar_impostos: se True, aplica benefício fiscal da dívida
    """
    V = D + E  # Valor total da empresa
    wD = D / V
    wE = E / V

    if considerar_impostos:
        wacc = wE * rE + wD * rD * (1 - T)
    else:
        wacc = wE * rE + wD * rD
        
    return wacc


def interface_usuario():
    print("\n=== Calculadora de WACC ===\n")

    D = float(input("Informe o valor da dívida (D): "))
    E = float(input("Informe o valor do equity (E): "))
    rD = float(input("Informe o custo da dívida rD (ex: 0.08): "))
    rE = float(input("Informe o custo do equity rE (ex: 0.12): "))
    T = float(input("Informe a alíquota de impostos T (ex: 0.34): "))

    wacc_com = calcular_wacc(D, E, rD, rE, T, considerar_impostos=True)
    wacc_sem = calcular_wacc(D, E, rD, rE, T, considerar_impostos=False)

    print("\nResultados:")
    print(f"WACC (com impostos): {wacc_com:.4f}")
    print(f"WACC (sem impostos): {wacc_sem:.4f}")

    return D, E, rD, rE, T


def grafico_wacc_vs_alavancagem(E, rD, rE, T):
    """
    Gera um gráfico mostrando como o WACC se comporta
    conforme a alavancagem D/E aumenta.
    """
    razoes_DE = np.linspace(0, 5, 100)  # de 0 a 500% de alavancagem
    wacc_vals = []

    for de in razoes_DE:
        D = de * E
        wacc = calcular_wacc(D, E, rD, rE, T, considerar_impostos=True)
        wacc_vals.append(wacc)

    plt.figure(figsize=(8, 5))
    plt.plot(razoes_DE, wacc_vals, linewidth=2)
    plt.xlabel("Alavancagem (D/E)")
    plt.ylabel("WACC")
    plt.title("WACC vs. Alavancagem (com impostos)")
    plt.grid(True)

    timestamp = datetime.now()
    filename = os.path.join(f"graficos/WACC_Alavancagem_{timestamp}.png")
    print(f"\nSalvo em {filename}")
    plt.savefig(filename, dpi=150)
    plt.close()

def calcular_rE_MM(rU, rD, D, E):
    """
    Proposição II de Modigliani-Miller:
    rE = rU + (D/E) * (rU - rD)
    """
    return rU + (D/E) * (rU - rD)

def simular_proposicao_MM(rU, rD, E):
    """
    Gera uma tabela e um gráfico mostrando como o custo do equity (rE)
    aumenta com a alavancagem D/E.
    """
    DE_ratios = np.linspace(0, 5, 40)  # de 0x a 5x alavancagem
    rE_vals = []

    for de in DE_ratios:
        D = de * E
        rE = calcular_rE_MM(rU, rD, D, E)
        rE_vals.append(rE)

    # ---- TABELA ----
    tabela = pd.DataFrame({
        "D/E": DE_ratios,
        "rE (alavancado)": rE_vals
    })

    print("\n=== Tabela da Proposição II de MM ===\n")
    print(tabela.round(4))

    plt.figure(figsize=(8, 5))
    plt.plot(DE_ratios, rE_vals, linewidth=2)
    plt.xlabel("Alavancagem (D/E)")
    plt.ylabel("Custo do Equity rE")
    plt.title("Proposição II de Modigliani-Miller\nCrescimento de rE conforme alavancagem")
    plt.grid(True)
    timestamp = datetime.now()
    filename = os.path.join(f"graficos/Crescimento_rE_Alavancagem_{timestamp}.png")
    print(f"\nSalvo em {filename}")
    plt.savefig(filename, dpi=150)
    plt.close()


    return tabela

if __name__ == "__main__":
    D, E, rD, rE, T = interface_usuario()
    grafico_wacc_vs_alavancagem(E, rD, rE, T)

    rU = float(input("\nInforme o custo do capital para empresa não alavancada (rU): "))
    simular_proposicao_MM(rU, rD, E)
