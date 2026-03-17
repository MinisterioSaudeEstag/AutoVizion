import pandas as pd
import sqlite3

def importar_planilha(caminho_excel):
    # 1. Conectar ao banco de dados (cria se não existir)
    conn = sqlite3.connect('sistema_vendas.db')
    
    # 2. Ler a planilha de exportação
    df_novo = pd.read_excel(caminho_excel)
    
    # 3. Salvar no Banco de Dados (Append = adiciona ao final)
    df_novo.to_sql('vendas_diarias', conn, if_exists='append', index=False)
    
    conn.close()
    print(f"✅ Dados de {caminho_excel} integrados ao Banco de Dados!")

# Simulação: Importando a planilha que criamos antes
importar_planilha('base_dados_grande.xlsx')