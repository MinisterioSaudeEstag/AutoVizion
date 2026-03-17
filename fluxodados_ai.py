import pandas as pd
import sqlite3
import os
import google.generativeai as genai
import plotly.express as px

# 1. CONFIGURAÇÕES INICIAIS
NOME_BANCO = 'fluxodata_sistema.db'
API_KEY = "AIzaSyBeegLzmcEv7W8YM0flTMOasHXQoSWtl1Y" # Coloque sua chave do Google AI Studio aqui

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def inicializar_sistema():
    """Apenas garante que o banco pode ser criado"""
    conn = sqlite3.connect(NOME_BANCO)
    conn.close()
    print(f"🗄️ Banco de dados '{NOME_BANCO}' inicializado.")

def integrar_excel_ao_banco(caminho_excel):
    """Lê a planilha e cria a tabela automaticamente com todas as colunas"""
    if not os.path.exists(caminho_excel):
        print(f"❌ Erro: O arquivo {caminho_excel} não foi encontrado!")
        return
    
    conn = sqlite3.connect(NOME_BANCO)
    df_novo = pd.read_excel(caminho_excel)
    
   # if_exists='append' adiciona dados se a tabela existir
    # Se a tabela não existir, o pandas cria ela com TODAS as colunas do Excel
    df_novo.to_sql('vendas', conn, if_exists='append', index=False)
    conn.close()
    print(f"📥 Dados de '{caminho_excel}' armazenados com sucesso (incluindo Preço Unitário).")
    
def gerar_insight_e_grafico():
    """Lê do banco, pede insight ao Gemini e gera o Dashboard"""
    conn = sqlite3.connect(NOME_BANCO)
    df = pd.read_sql('SELECT * FROM vendas', conn)
    conn.close()

    if df.empty:
        print("⚠️ O banco de dados está vazio.")
        return

    # Resumo para a IA (Top 3 produtos e faturamento total)
    resumo = df.groupby('Produto')['Faturamento_Total'].sum().sort_values(ascending=False).head(3).to_string()
    
    print("🤖 Gemini analisando tendências...")
    prompt = f"Analise estes dados de vendas: {resumo}. Dê um insight curto de negócio."
    try:
        insight = model.generate_content(prompt).text
    except:
        insight = "Insight indisponível (verifique sua API Key)."

    # Criando o gráfico (Timeline de Faturamento)
    fig = px.line(df, x='Data', y='Faturamento_Total', color='Produto',
                  title=f"FluxoData AI - Monitoramento Executivo<br><sup>{insight}</sup>",
                  template="plotly_dark")

    # Salvando em HTML (estilo Dark Mode total)
    fig.update_layout(paper_bgcolor="#111111", plot_bgcolor="#111111")
    fig.write_html('dashboard_inteligente.html')
    print("🎨 Dashboard atualizado em 'dashboard_inteligente.html'!")

# --- EXECUÇÃO DO FLUXO ---
inicializar_sistema()
integrar_excel_ao_banco('base_dados_grande.xlsx') # Use a planilha que geramos antes
gerar_insight_e_grafico()