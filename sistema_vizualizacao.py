import pandas as pd
import sqlite3
import plotly.express as px

def gerar_dashboard_sistema():
    # 1. Busca dados do Banco de Dados SQL
    conn = sqlite3.connect('sistema_vendas.db')
    df = pd.read_sql('SELECT * FROM vendas_diarias', conn)
    conn.close()

    # 2. Lógica de "IA" Simples (Regra de Negócio)
    melhor_produto = df.groupby('Produto')['Vendas'].sum().idxmax()
    total = df['Faturamento_Total'].sum()
    insight = f"IA Insight: O produto '{melhor_produto}' é o seu motor de vendas. O faturamento acumulado é R$ {total:,.2f}."

    # 3. Criar Gráfico Interativo
    fig = px.area(df, x='Data', y='Faturamento_Total', color='Regiao', 
                  title=f"Evolução Temporal do Sistema<br><sup>{insight}</sup>",
                  template="plotly_dark")

    # 4. Salvar com o fix da faixa branca
    fig.write_html('dashboard_sistema.html')
    print("🚀 Dashboard do Sistema Atualizado!")

gerar_dashboard_sistema()