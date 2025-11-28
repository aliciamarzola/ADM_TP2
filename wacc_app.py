import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configuração da Página
st.set_page_config(page_title="Análise WACC", layout="wide")

# Funções de Cálculo

def calcular_ke_capm(rf, beta, rm):
    """Calcula Custo do Equity (Ke) via CAPM."""
    return rf + beta * (rm - rf)

def calcular_wacc(D, E, rD, rE, T):
    """Calcula o WACC clássico."""
    V = D + E
    if V == 0: return 0
    wD = D / V
    wE = E / V
    return wE * rE + wD * rD * (1 - T)

def hamada_relever_beta(beta_unlevered, D, E, T):
    """
    Re-alavanca o Beta baseada na estrutura de capital D/E.
    Fórmula de Hamada: Beta_L = Beta_U * [1 + (1-T)*(D/E)]
    rE aumenta conforme a dívida aumenta
    """
    if E == 0: return beta_unlevered # Evitar divisão por zero
    return beta_unlevered * (1 + (1 - T) * (D / E))

# Inputs do Usuário via Sidebar
st.sidebar.header("1. Estrutura de Capital Atual")
D_input = st.sidebar.number_input("Dívida Total (D) - R$", value=500000.0, step=10000.0)
E_input = st.sidebar.number_input("Equity / Valor de Mercado (E) - R$", value=1000000.0, step=10000.0)
T_input = st.sidebar.slider("Alíquota de Imposto (T)", 0.0, 0.50, 0.34, 0.01)

st.sidebar.header("2. Custos e Retornos")
rD_input = st.sidebar.number_input("Custo da Dívida (rD) - %", value=8.0, step=0.1) / 100
roic_input = st.sidebar.number_input("Retorno sobre Capital (ROIC) - %", value=12.0, help="O quanto seu projeto gera de retorno operacional") / 100

st.sidebar.header("3. Parâmetros CAPM (Opcional)")
usar_capm = st.sidebar.checkbox("Calcular rE pelo CAPM?", value=True)

if usar_capm:
    rf_input = st.sidebar.number_input("Risk Free (Rf) - %", value=4.0) / 100
    beta_input = st.sidebar.number_input("Beta da Empresa", value=1.1)
    rm_input = st.sidebar.number_input("Retorno de Mercado (Rm) - %", value=10.0) / 100
    # Calcula rE
    rE_final = calcular_ke_capm(rf_input, beta_input, rm_input)
else:
    rE_manual = st.sidebar.number_input("Custo do Equity Manual (rE) - %", value=12.0) / 100
    rE_final = rE_manual

# Cálculo do WACC Atual
wacc_atual = calcular_wacc(D_input, E_input, rD_input, rE_final, T_input)
spread_economico = roic_input - wacc_atual
eva = (D_input + E_input) * spread_economico # Valor Econômico Adicionado

# Layout Principal
st.title("Calculadora e Otimizador de WACC")
st.markdown("---")

# Métricas no topo
col1, col2, col3, col4 = st.columns(4)
col1.metric("WACC Atual", f"{wacc_atual:.2%}", delta=f"Target: {wacc_atual*0.9:.2%}", delta_color="inverse")
col2.metric("Custo Equity (Ke)", f"{rE_final:.2%}")
col3.metric("Custo Dívida Líquido (Kd)", f"{rD_input*(1-T_input):.2%}")
col4.metric("Criação de Valor (Spread)", f"{spread_economico:.2%}", delta_color="normal" if spread_economico > 0 else "inverse")

# Abas de Navegação
tab1, tab2, tab3 = st.tabs(["Consultor Inteligente", "Simulação de Estrutura", "Detalhes"])

with tab1:
    st.subheader("Diagnóstico do seu Negócio")
    
    # Lógica de decisão
    if spread_economico > 0.02:
        st.success(f"**Excelente!** Sua empresa cria valor real. O retorno ({roic_input:.1%}) supera o custo de capital ({wacc_atual:.1%}) com folga.")
        st.markdown("**Recomendação:** Acelere investimentos em projetos similares. Você tem 'gordura' para tomar mais dívida se precisar expandir.")
    elif spread_economico > 0:
        st.warning(f"**Atenção:** Você cria valor, mas a margem é apertada ({spread_economico:.2%}).")
        st.markdown("**Recomendação:** Foque em eficiência operacional para subir o ROIC ou tente renegociar dívidas para baixar o rD.")
    else:
        st.error(f"**PERIGO:** Destruição de valor detectada. Cada real investido custa mais do que retorna.")
        st.markdown("**Ação Imediata:** Pare novos investimentos. Considere vender ativos improdutivos ou aporte de capital para reduzir a dívida cara.")

    st.write(f"**Valor Econômico Adicionado (EVA):** R$ {eva:,.2f}")

with tab2:
    st.subheader("Curva de Otimização: WACC vs Alavancagem")
    st.markdown("Este gráfico simula o que aconteceria com seu WACC se você alterasse a proporção de dívida (D/E). Ao aumentar a dívida, o risco do acionista sobe (Beta aumenta), encarecendo o Equity.")
    
    # Simulação Avançada com Hamada
    # 1. Desalavancar o Beta atual para achar o risco puro do negócio
    beta_atual = beta_input if usar_capm else 1.0 # fallback
    beta_unlevered = beta_atual / (1 + (1 - T_input) * (D_input/E_input))
    
    leverage_ratios = np.linspace(0.0, 0.95, 50) # 0% a 95% de dívida sobre capital total
    wacc_simulado = []
    ke_simulado = []
    kd_simulado = []
    
    rf_sim = rf_input if usar_capm else 0.04
    rm_sim = rm_input if usar_capm else 0.10
    
    for wd in leverage_ratios:
        we = 1 - wd
        # Simula D/E para este ponto
        if we <= 0.01: 
            de_ratio = 99 
        else:
            de_ratio = wd / we
            
        # Re-alavanca Beta (Hamada)
        beta_relevered = hamada_relever_beta(beta_unlevered, wd*100, we*100, T_input)
        
        # Novo Ke
        new_ke = rf_sim + beta_relevered * (rm_sim - rf_sim)
        
        # Custo da dívida (suposição simplificada: sobe muito se alavancagem > 70%)
        risk_premium_debt = 0 if wd < 0.5 else (wd - 0.5) ** 2 * 0.5
        new_kd = rD_input + risk_premium_debt
        
        # Novo WACC
        new_wacc = we * new_ke + wd * new_kd * (1 - T_input)
        
        wacc_simulado.append(new_wacc)
        ke_simulado.append(new_ke)
        
    # Plotly Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=leverage_ratios*100, y=np.array(wacc_simulado)*100, mode='lines', name='WACC', line=dict(width=4, color='blue')))
    fig.add_trace(go.Scatter(x=leverage_ratios*100, y=np.array(ke_simulado)*100, mode='lines', name='Custo Equity (Ke)', line=dict(dash='dot', color='green')))
    
    # Marca o ponto atual
    debt_ratio_atual = D_input / (D_input + E_input)
    fig.add_trace(go.Scatter(x=[debt_ratio_atual*100], y=[wacc_atual*100], mode='markers', name='Sua Posição Atual', marker=dict(size=12, color='red')))

    fig.update_layout(title="Estrutura Ótima de Capital", xaxis_title="% de Dívida no Capital Total", yaxis_title="Taxa (%)", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Nota: O modelo assume que o custo da dívida começa a subir exponencialmente se a dívida passar de 50% do capital total (Risco de Falência).")

with tab3:
    st.subheader("Resumo dos Dados")
    df_resumo = pd.DataFrame({
        "Item": ["Valor da Dívida (D)", "Valor do Equity (E)", "Total (V)", "Peso Dívida", "Peso Equity"],
        "Valor": [f"R$ {D_input:,.2f}", f"R$ {E_input:,.2f}", f"R$ {D_input+E_input:,.2f}", f"{D_input/(D_input+E_input):.2%}", f"{E_input/(D_input+E_input):.2%}"]
    })
    st.table(df_resumo)