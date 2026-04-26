import pandas as pd
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(r'c:\projetinhos\projeto_risco')
DATA_DIR = BASE_DIR / 'data' / 'processed'
METRICS_DIR = BASE_DIR / 'reports' / 'metrics'

def converter_para_padrao_brasil(input_path, output_name):
    try:
        if not input_path.exists():
            print(f"⚠️ Arquivo não encontrado: {input_path.name}")
            return
            
        # Ler o arquivo original (padrao americano)
        df = pd.read_csv(input_path)
        
        # Salvar no padrão brasileiro:
        # sep=';' -> Ponto-e-vírgula como separador de colunas
        # decimal=',' -> Vírgula como separador decimal
        output_path = input_path.parent / output_name
        df.to_csv(output_path, sep=';', decimal=',', index=False, encoding='utf-8-sig')
        print(f"Convertido: {output_name}")
    except Exception as e:
        print(f"Erro ao converter {input_path.name}: {e}")

# Arquivos para converter
arquivos = [
    (DATA_DIR / 'predicoes_risco_credito.csv', 'predicoes_para_powerbi.csv'),
    (METRICS_DIR / 'feature_importance.csv', 'feature_importance_para_powerbi.csv'),
    (METRICS_DIR / 'comparativo_modelos.csv', 'comparativo_modelos_para_powerbi.csv')
]

print("Iniciando conversao para Padrao Brasileiro (Power BI)...\n")

for entrada, saida in arquivos:
    converter_para_padrao_brasil(entrada, saida)

print("\nPRONTO! Agora conecte o Power BI nos arquivos que terminam em '_para_powerbi.csv'.")
