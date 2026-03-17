import pandas as pd
import sqlite3
import google.generativeai as genai
import plotly.express as px

# --- CONFIGURAÇÃO DA IA ---
# Substitua 'SUA_CHAVE_AQUI' pela sua chave real
genai.configure(api_key="AIzaSyBeegLzmcEv7W8YM0flTMOasHXQoSWtl1Y")
model = genai.GenerativeModel('gemini-1.5-flash')

def obter_insight_ia(dados_resumo):
    prompt = f"""
    Abaixo estão os dados de faturamento da minha empresa:
    {dados_resumo}
    
    Como um consultor de negócios experiente, escreva uma única frase curta 
    e impactante para um dashboard, destacando o ponto mais importante ou uma tendência.
    """
    response = model.generate_content(prompt)
    return response.text

def gerar_dashboard_com_ia():
    # 1. Carregar dados do banco SQL
    conn = sqlite3.connect('sistema_vendas.db')
    df = pd.read_sql('SELECT * FROM vendas_diarias', conn)
    conn.close()

    # 2. Preparar um resumo de texto para a IA não ler 1000 linhas à toa
    resumo_vendas = df.groupby('Produto')['Faturamento_Total'].sum().to_string()
    
    # 3. Chamar o Gemini para analisar
    print("🤖 Consultando o Gemini para insights...")
    insight_real = obter_insight_ia(resumo_vendas)

    # 4. Criar o Gráfico
    fig = px.bar(df.groupby('Produto')['Faturamento_Total'].sum().reset_index(), 
                 x='Produto', y='Faturamento_Total',
                 title=f"Dashboard Inteligente<br><sup>{insight_real}</sup>",
                 template="plotly_dark",
                 color_discrete_sequence=['#00f2ff'])

    # 5. Salvar (com o fix da faixa branca que aprendemos)
    # [Aqui você usaria aquele código de salvar com CSS que te mostrei antes]
    fig.write_html('dashboard_ia.html')
    print("🚀 Dashboard com Insight de IA gerado!")

gerar_dashboard_com_ia()