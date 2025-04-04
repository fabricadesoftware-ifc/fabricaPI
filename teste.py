import pandas as pd
import chardet

def detectar_codificacao(arquivo):
    """Detecta a codificação de um arquivo CSV."""
    with open(arquivo, 'rb') as f:
        resultado = chardet.detect(f.read(10000))  # Lê uma amostra do arquivo
    return resultado['encoding']

def carregar_csv(arquivo):
    """Lê um CSV com a codificação correta e exibe as primeiras linhas."""
    encoding_detectado = detectar_codificacao(arquivo)
    print(f"📌 Codificação detectada: {encoding_detectado}")

    try:
        df = pd.read_csv(arquivo, encoding=encoding_detectado, sep=';')
        print(df.head())  # Mostra as 5 primeiras linhas do CSV
    except Exception as e:
        print(f"❌ Erro ao ler o CSV: {e}")

# 📂 Troque pelo nome do seu arquivo CSV
arquivo_csv = "./LICA_2016_teste.csv"

# Executa a função
carregar_csv(arquivo_csv)
