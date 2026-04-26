# =============================================================================
# 📊 PROJETO FINTECH - MODELO PREDITIVO DE RISCO DE CRÉDITO
# =============================================================================
# Fase 1: Entendimento e Perfilamento dos Dados (EDA)
# Fase 2: Limpeza e Engenharia de Features
#
# Compatível com: Python 3.10+ | Google Colab | Local Windows
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para salvar gráficos
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================
# Detectar se está rodando no Colab ou Local
try:
    from google.colab import files
    AMBIENTE = 'COLAB'
    BASE_DIR = Path('/content')
except ImportError:
    AMBIENTE = 'LOCAL'
    BASE_DIR = Path(r'c:\projetinhos\projeto_risco')

INPUT_FILE = BASE_DIR / 'credit_risk_dataset.csv'
OUTPUT_DIR = BASE_DIR / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)

# Estilo visual premium (Dark Mode - Fintech)
plt.style.use('dark_background')
COLORS = {
    'primary': '#00D4AA',     # Verde Fintech
    'danger': '#FF4757',      # Vermelho Risco
    'warning': '#FFA502',     # Amarelo Alerta
    'info': '#3742FA',        # Azul Info
    'neutral': '#747D8C',     # Cinza
    'bg': '#1A1A2E',          # Fundo escuro
    'bg_card': '#16213E',     # Fundo cards
    'text': '#E8E8E8',        # Texto claro
}
sns.set_palette([COLORS['primary'], COLORS['danger'], COLORS['warning'], COLORS['info']])

print(f"""
╔══════════════════════════════════════════════════════════════╗
║   🏦 PROJETO FINTECH - RISCO DE CRÉDITO                    ║
║   Fase 1: Entendimento e Perfilamento dos Dados (EDA)       ║
║   Ambiente: {AMBIENTE:<48s}║
╚══════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# FASE 1: CARREGAR E PERFILAR OS DADOS
# =============================================================================
print("📥 [1/8] Carregando dataset...")
df = pd.read_csv(INPUT_FILE)
print(f"   ✅ Dataset carregado: {df.shape[0]:,} linhas x {df.shape[1]} colunas")

# --- 1.1 Dicionário de Dados ---
print("\n" + "="*60)
print("📖 DICIONÁRIO DE DADOS")
print("="*60)
dicionario = {
    'person_age': 'Idade do solicitante',
    'person_income': 'Renda anual (USD)',
    'person_home_ownership': 'Tipo de moradia (RENT/OWN/MORTGAGE/OTHER)',
    'person_emp_length': 'Tempo de emprego (anos)',
    'loan_intent': 'Finalidade do empréstimo',
    'loan_grade': 'Grau de risco do empréstimo (A=melhor, G=pior)',
    'loan_amnt': 'Valor do empréstimo solicitado (USD)',
    'loan_int_rate': 'Taxa de juros (%)',
    'loan_status': '⭐ VARIÁVEL ALVO: 0=Pagou | 1=Default (Calote)',
    'loan_percent_income': 'Razão empréstimo/renda',
    'cb_person_default_on_file': 'Histórico de default no bureau (Y/N)',
    'cb_person_cred_hist_length': 'Tempo de histórico de crédito (anos)',
}
for col, desc in dicionario.items():
    tipo = str(df[col].dtype)
    nulos = df[col].isnull().sum()
    print(f"   {col:<35s} | {tipo:<8s} | Nulos: {nulos:>5d} | {desc}")

# --- 1.2 Análise da Variável Alvo ---
print("\n" + "="*60)
print("🎯 ANÁLISE DA VARIÁVEL ALVO (loan_status)")
print("="*60)
target_counts = df['loan_status'].value_counts()
total = len(df)
print(f"   Pagou (0):   {target_counts[0]:>6,} ({target_counts[0]/total*100:.1f}%)")
print(f"   Default (1): {target_counts[1]:>6,} ({target_counts[1]/total*100:.1f}%)")
print(f"   Proporção Default/Total: 1:{total//target_counts[1]:.0f}")
print(f"   ⚠️  Dataset DESBALANCEADO - Considerar técnicas de balanceamento (SMOTE/Undersampling)")

# --- 1.3 Detecção de Outliers ---
print("\n" + "="*60)
print("🔍 DETECÇÃO DE ANOMALIAS E OUTLIERS")
print("="*60)

anomalias = []

# Idade > 100 anos (impossível)
idade_anomala = df[df['person_age'] > 100]
if len(idade_anomala) > 0:
    anomalias.append(('person_age', f'{len(idade_anomala)} registros com idade > 100 anos (max: {df["person_age"].max()})'))
    print(f"   🚨 person_age: {len(idade_anomala)} registros com idade > 100 anos (max: {df['person_age'].max()})")

# Tempo de emprego > 60 anos (improvável)
emp_anomala = df[df['person_emp_length'] > 60]
if len(emp_anomala) > 0:
    anomalias.append(('person_emp_length', f'{len(emp_anomala)} registros com tempo de emprego > 60 anos (max: {df["person_emp_length"].max()})'))
    print(f"   🚨 person_emp_length: {len(emp_anomala)} registros com emprego > 60 anos (max: {df['person_emp_length'].max()})")

# Renda muito alta (> 1M)
renda_anomala = df[df['person_income'] > 1_000_000]
if len(renda_anomala) > 0:
    anomalias.append(('person_income', f'{len(renda_anomala)} registros com renda > $1M'))
    print(f"   ⚠️  person_income: {len(renda_anomala)} registros com renda > $1M (possíveis outliers)")

# Valores nulos
print(f"\n   📋 Valores Nulos:")
print(f"      person_emp_length: {df['person_emp_length'].isnull().sum():>5,} ({df['person_emp_length'].isnull().mean()*100:.1f}%)")
print(f"      loan_int_rate:     {df['loan_int_rate'].isnull().sum():>5,} ({df['loan_int_rate'].isnull().mean()*100:.1f}%)")

# =============================================================================
# FASE 1: GRÁFICOS DE EDA
# =============================================================================
print("\n" + "="*60)
print("📊 GERANDO VISUALIZAÇÕES DE EDA...")
print("="*60)

# --- Gráfico 1: Distribuição da Variável Alvo ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.patch.set_facecolor(COLORS['bg'])
fig.suptitle('📊 EDA - Credit Risk Dataset | Análise Exploratória', 
             fontsize=18, fontweight='bold', color=COLORS['text'], y=0.98)

# 1.1 - Distribuição Target
ax = axes[0, 0]
ax.set_facecolor(COLORS['bg_card'])
bars = ax.bar(['Pagou (0)', 'Default (1)'], target_counts.values, 
              color=[COLORS['primary'], COLORS['danger']], edgecolor='white', linewidth=0.5)
for bar, val in zip(bars, target_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, 
            f'{val:,}\n({val/total*100:.1f}%)', ha='center', va='bottom', 
            fontsize=12, fontweight='bold', color=COLORS['text'])
ax.set_title('Distribuição da Variável Alvo', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.set_ylabel('Quantidade', color=COLORS['text'])

# 1.2 - Distribuição de Idade
ax = axes[0, 1]
ax.set_facecolor(COLORS['bg_card'])
df_age_clean = df[df['person_age'] <= 100]
ax.hist(df_age_clean[df_age_clean['loan_status']==0]['person_age'], bins=30, alpha=0.7, 
        label='Pagou', color=COLORS['primary'], edgecolor='white', linewidth=0.3)
ax.hist(df_age_clean[df_age_clean['loan_status']==1]['person_age'], bins=30, alpha=0.7, 
        label='Default', color=COLORS['danger'], edgecolor='white', linewidth=0.3)
ax.set_title('Distribuição de Idade por Status', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.set_xlabel('Idade', color=COLORS['text'])
ax.legend()

# 1.3 - Taxa de Default por Grau
ax = axes[1, 0]
ax.set_facecolor(COLORS['bg_card'])
grade_default = df.groupby('loan_grade')['loan_status'].mean().sort_index()
colors_grade = [COLORS['primary'] if v < 0.3 else COLORS['warning'] if v < 0.5 else COLORS['danger'] 
                for v in grade_default.values]
bars = ax.bar(grade_default.index, grade_default.values * 100, color=colors_grade, 
              edgecolor='white', linewidth=0.5)
for bar, val in zip(bars, grade_default.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
            f'{val*100:.1f}%', ha='center', va='bottom', fontsize=11, 
            fontweight='bold', color=COLORS['text'])
ax.set_title('Taxa de Default por Grau do Empréstimo', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.set_ylabel('Taxa de Default (%)', color=COLORS['text'])
ax.set_xlabel('Grau (A=Melhor → G=Pior)', color=COLORS['text'])

# 1.4 - Finalidade do Empréstimo
ax = axes[1, 1]
ax.set_facecolor(COLORS['bg_card'])
intent_default = df.groupby('loan_intent')['loan_status'].agg(['mean', 'count']).sort_values('mean', ascending=True)
bars = ax.barh(intent_default.index, intent_default['mean'] * 100, 
               color=COLORS['info'], edgecolor='white', linewidth=0.5)
for bar, val in zip(bars, intent_default['mean'].values):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
            f'{val*100:.1f}%', ha='left', va='center', fontsize=11, color=COLORS['text'])
ax.set_title('Taxa de Default por Finalidade', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.set_xlabel('Taxa de Default (%)', color=COLORS['text'])

plt.tight_layout(rect=[0, 0, 1, 0.95])
eda_path = OUTPUT_DIR / 'eda_01_visao_geral.png'
plt.savefig(eda_path, dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
plt.close()
print(f"   ✅ Gráfico 1 salvo: {eda_path}")

# --- Gráfico 2: Correlação ---
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor(COLORS['bg'])
ax.set_facecolor(COLORS['bg_card'])

numeric_cols = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn_r', 
            center=0, ax=ax, linewidths=0.5, linecolor=COLORS['bg'],
            cbar_kws={'label': 'Correlação'},
            annot_kws={'size': 10, 'fontweight': 'bold'})
ax.set_title('Matriz de Correlação - Variáveis Numéricas', 
             fontsize=16, fontweight='bold', color=COLORS['text'], pad=20)
plt.tight_layout()
corr_path = OUTPUT_DIR / 'eda_02_correlacao.png'
plt.savefig(corr_path, dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
plt.close()
print(f"   ✅ Gráfico 2 salvo: {corr_path}")


# =============================================================================
# FASE 2: LIMPEZA E ENGENHARIA DE FEATURES
# =============================================================================
print("\n" + "="*60)
print("🧹 FASE 2: LIMPEZA E ENGENHARIA DE FEATURES")
print("="*60)

df_clean = df.copy()
log_limpeza = []

# --- 2.1 Remover Outliers Impossíveis ---
print("\n[2.1] Removendo outliers impossíveis...")

# Idade > 100 (biologicamente impossível para crédito)
antes = len(df_clean)
df_clean = df_clean[df_clean['person_age'] <= 100]
removidos = antes - len(df_clean)
log_limpeza.append(f"Removidos {removidos} registros com idade > 100 anos")
print(f"   ✅ Removidos {removidos} registros com idade > 100 anos")

# Tempo de emprego > 60 (impossível)
antes = len(df_clean)
df_clean = df_clean[df_clean['person_emp_length'].isna() | (df_clean['person_emp_length'] <= 60)]
removidos = antes - len(df_clean)
log_limpeza.append(f"Removidos {removidos} registros com tempo de emprego > 60 anos")
print(f"   ✅ Removidos {removidos} registros com emprego > 60 anos")

# --- 2.2 Tratamento de Valores Nulos ---
print("\n[2.2] Tratamento estratégico de valores nulos...")

# person_emp_length: Preencher com mediana (estratégia conservadora para crédito)
mediana_emp = df_clean['person_emp_length'].median()
nulos_emp = df_clean['person_emp_length'].isnull().sum()
df_clean['person_emp_length'] = df_clean['person_emp_length'].fillna(mediana_emp)
log_limpeza.append(f"person_emp_length: {nulos_emp} nulos preenchidos com mediana ({mediana_emp:.1f} anos)")
print(f"   ✅ person_emp_length: {nulos_emp} nulos → mediana ({mediana_emp:.1f} anos)")

# loan_int_rate: Preencher com mediana por loan_grade (mais inteligente)
nulos_rate = df_clean['loan_int_rate'].isnull().sum()
df_clean['loan_int_rate'] = df_clean.groupby('loan_grade')['loan_int_rate'].transform(
    lambda x: x.fillna(x.median())
)
# Se ainda houver nulos (grupo inteiro vazio), usar mediana geral
df_clean['loan_int_rate'] = df_clean['loan_int_rate'].fillna(df_clean['loan_int_rate'].median())
log_limpeza.append(f"loan_int_rate: {nulos_rate} nulos preenchidos com mediana por grau do empréstimo")
print(f"   ✅ loan_int_rate: {nulos_rate} nulos → mediana por loan_grade (estratégia inteligente)")

# --- 2.3 Engenharia de Features (Novas Variáveis) ---
print("\n[2.3] Engenharia de Features (criando variáveis Fintech)...")

# DTI - Debt-to-Income Ratio (padrão da indústria bancária)
df_clean['dti_ratio'] = df_clean['loan_amnt'] / df_clean['person_income']
log_limpeza.append("Criada feature: dti_ratio (Debt-to-Income)")
print("   ✅ dti_ratio: Razão Dívida/Renda (padrão bancário)")

# Faixa etária (categorização útil para análise de risco)
bins_age = [0, 25, 35, 45, 55, 100]
labels_age = ['18-25', '26-35', '36-45', '46-55', '56+']
df_clean['faixa_etaria'] = pd.cut(df_clean['person_age'], bins=bins_age, labels=labels_age)
log_limpeza.append("Criada feature: faixa_etaria (categorização)")
print("   ✅ faixa_etaria: Categorização por faixa etária")

# Risco da taxa de juros (acima da média = alto risco)
media_rate = df_clean['loan_int_rate'].mean()
df_clean['taxa_juros_alta'] = (df_clean['loan_int_rate'] > media_rate).astype(int)
log_limpeza.append(f"Criada feature: taxa_juros_alta (1 se > {media_rate:.2f}%)")
print(f"   ✅ taxa_juros_alta: Flag se taxa > {media_rate:.2f}% (média)")

# Comprometimento de renda (categorias de risco)
df_clean['risco_comprometimento'] = pd.cut(
    df_clean['loan_percent_income'],
    bins=[0, 0.10, 0.20, 0.35, 1.0],
    labels=['Baixo', 'Moderado', 'Alto', 'Crítico']
)
log_limpeza.append("Criada feature: risco_comprometimento (Baixo/Moderado/Alto/Crítico)")
print("   ✅ risco_comprometimento: Nível de comprometimento da renda")

# --- 2.4 Encoding de Variáveis Categóricas ---
print("\n[2.4] Encoding de variáveis categóricas...")

# Label Encoding para variáveis ordinais
grade_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
df_clean['loan_grade_num'] = df_clean['loan_grade'].map(grade_map)
log_limpeza.append("loan_grade: Label Encoding ordinal (A=1 → G=7)")
print("   ✅ loan_grade → loan_grade_num (A=1, B=2... G=7)")

# Binary Encoding
df_clean['cb_default_flag'] = (df_clean['cb_person_default_on_file'] == 'Y').astype(int)
log_limpeza.append("cb_person_default_on_file: Binary Encoding (Y=1, N=0)")
print("   ✅ cb_person_default_on_file → cb_default_flag (Y=1, N=0)")

# One-Hot Encoding para variáveis nominais
df_clean = pd.get_dummies(df_clean, columns=['person_home_ownership', 'loan_intent'], 
                          prefix=['home', 'intent'], drop_first=False, dtype=int)
log_limpeza.append("person_home_ownership e loan_intent: One-Hot Encoding")
print("   ✅ One-Hot Encoding: person_home_ownership, loan_intent")

# --- 2.5 Remover colunas originais já transformadas ---
cols_drop = ['loan_grade', 'cb_person_default_on_file', 'faixa_etaria', 'risco_comprometimento']
df_clean = df_clean.drop(columns=cols_drop, errors='ignore')
log_limpeza.append(f"Removidas colunas originais já transformadas: {cols_drop}")
print(f"   ✅ Removidas colunas originais: {cols_drop}")

# =============================================================================
# VALIDAÇÃO FINAL
# =============================================================================
print("\n" + "="*60)
print("✅ VALIDAÇÃO FINAL DO DATASET LIMPO")
print("="*60)
print(f"   Linhas originais:     {len(df):>8,}")
print(f"   Linhas após limpeza:  {len(df_clean):>8,}")
print(f"   Linhas removidas:     {len(df) - len(df_clean):>8,} ({(len(df)-len(df_clean))/len(df)*100:.2f}%)")
print(f"   Colunas originais:    {df.shape[1]:>8}")
print(f"   Colunas após eng.:    {df_clean.shape[1]:>8}")
print(f"   Valores nulos rest.:  {df_clean.isnull().sum().sum():>8}")
print(f"\n   Colunas finais:")
for i, col in enumerate(df_clean.columns, 1):
    tipo = str(df_clean[col].dtype)
    print(f"      {i:>2}. {col:<40s} ({tipo})")

# =============================================================================
# EXPORTAÇÃO
# =============================================================================
print("\n" + "="*60)
print("💾 EXPORTANDO DADOS LIMPOS...")
print("="*60)

# CSV limpo para Power BI e Colab
csv_path = OUTPUT_DIR / 'credit_risk_clean.csv'
df_clean.to_csv(csv_path, index=False)
print(f"   ✅ CSV salvo: {csv_path} ({csv_path.stat().st_size / 1024:.0f} KB)")

# Log de limpeza (auditoria)
log_path = OUTPUT_DIR / 'log_limpeza.txt'
with open(log_path, 'w', encoding='utf-8') as f:
    f.write("=" * 60 + "\n")
    f.write("LOG DE LIMPEZA - CREDIT RISK DATASET\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Dataset Original: {df.shape[0]:,} linhas x {df.shape[1]} colunas\n")
    f.write(f"Dataset Limpo:    {df_clean.shape[0]:,} linhas x {df_clean.shape[1]} colunas\n\n")
    for i, log in enumerate(log_limpeza, 1):
        f.write(f"  {i}. {log}\n")
print(f"   ✅ Log salvo: {log_path}")

# Relatório de perfil para referência rápida
perfil_path = OUTPUT_DIR / 'perfil_dataset.csv'
perfil = pd.DataFrame({
    'coluna': df_clean.columns,
    'tipo': df_clean.dtypes.values,
    'nulos': df_clean.isnull().sum().values,
    'unicos': df_clean.nunique().values,
    'min': df_clean.min(numeric_only=False).reindex(df_clean.columns).values,
    'max': df_clean.max(numeric_only=False).reindex(df_clean.columns).values,
})
perfil.to_csv(perfil_path, index=False)
print(f"   ✅ Perfil salvo: {perfil_path}")

print(f"""
╔══════════════════════════════════════════════════════════════╗
║   ✅ FASE 1 + FASE 2 CONCLUÍDAS COM SUCESSO!               ║
║                                                              ║
║   📁 Arquivos gerados em: {str(OUTPUT_DIR):<33s}║
║      • credit_risk_clean.csv  (dados para modelagem)        ║
║      • eda_01_visao_geral.png (visualização EDA)            ║
║      • eda_02_correlacao.png  (matriz de correlação)         ║
║      • log_limpeza.txt        (auditoria das decisões)      ║
║      • perfil_dataset.csv     (perfil das colunas)          ║
║                                                              ║
║   ➡️  Próximo passo: Fase 3 - Modelagem no Google Colab     ║
╚══════════════════════════════════════════════════════════════╝
""")
