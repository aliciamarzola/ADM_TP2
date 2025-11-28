# Aplicação para Análise da Estrutura de Capital

Esse código cria uma aplicação Streamlit para analisar WACC, estrutura de capital e criação de valor de uma empresa. Primeiro, ele configura a página e define funções essenciais: cálculo do custo do equity via CAPM, cálculo do WACC e a fórmula de Hamada para ajustar o beta conforme a alavancagem. Em seguida, a barra lateral coleta todos os inputs do usuário, como dívida, equity, imposto, custo da dívida, ROIC e parâmetros do CAPM. Com isso, o programa calcula o WACC atual, o spread econômico (ROIC – WACC) e o EVA, valores que são exibidos no topo como métricas.

A interface principal usa abas para organizar a análise. A aba Consultor Inteligente interpreta automaticamente o spread econômico e gera um diagnóstico financeiro explicando se a empresa cria ou destrói valor, oferecendo recomendações práticas. A aba Simulação de Estrutura gera uma curva interativa mostrando como o WACC mudaria com diferentes percentuais de dívida, recalculando o beta (Hamada), custo do equity e custo da dívida para cada cenário. Um gráfico Plotly exibe o WACC simulado, o Ke e marca a posição atual da empresa na curva. Por fim, a aba Detalhes mostra uma tabela com os valores principais da estrutura de capital.

Assim, o código funciona como uma ferramenta completa de análise financeira, combinando cálculo automático, diagnóstico inteligente e simulações visuais de estrutura ótima de capital, tudo de forma interativa e ajustável pelo usuário.

## Como rodar?
Siga os passos abaixo para executar a aplicação localmente:

1. Instale as dependências do projeto
pip install -r requirements.txt


2. Execute a aplicação Streamlit
streamlit run wacc_app.py

A aplicação abrirá automaticamente no navegador, normalmente em http://localhost:8501.
