# =============================================================================
# PROJETO FINTECH - RISCO DE CRÉDITO | Fase 3: Modelagem Preditiva
# =============================================================================
# Executar no Google Colab para usar GPU/RAM gratuita
# Upload: credit_risk_clean.csv + requirements.txt
# =============================================================================

# %% [1] SETUP - Instalar dependências (rodar apenas no Colab)
# !pip install -r requirements.txt

# %% [2] IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    roc_curve, precision_recall_curve, f1_score
)

# Balanceamento
from imblearn.over_sampling import SMOTE

# Modelos avançados
from xgboost import XGBClassifier
import lightgbm as lgb

# Explicabilidade
import shap

plt.style.use('dark_background')
COLORS = {
    'primary': '#00D4AA', 'danger': '#FF4757',
    'warning': '#FFA502', 'info': '#3742FA',
    'bg': '#1A1A2E', 'bg_card': '#16213E', 'text': '#E8E8E8'
}

print("✅ Bibliotecas carregadas com sucesso!")

# %% [3] CARREGAR DADOS LIMPOS
# No Colab: fazer upload do credit_risk_clean.csv primeiro
# from google.colab import files
# uploaded = files.upload()

df = pd.read_csv('credit_risk_clean.csv')
print(f"Dataset: {df.shape[0]:,} linhas x {df.shape[1]} colunas")
print(f"Target (loan_status): {df['loan_status'].value_counts().to_dict()}")

# %% [4] SEPARAR FEATURES E TARGET
TARGET = 'loan_status'
X = df.drop(columns=[TARGET])
y = df[TARGET]

print(f"\nFeatures: {X.shape[1]} colunas")
print(f"Target: {y.value_counts().to_dict()}")
print(f"Taxa de Default: {y.mean()*100:.1f}%")

# %% [5] SPLIT TREINO/TESTE (estratificado)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTreino: {X_train.shape[0]:,} | Teste: {X_test.shape[0]:,}")
print(f"Proporção default treino: {y_train.mean()*100:.1f}%")
print(f"Proporção default teste:  {y_test.mean()*100:.1f}%")

# %% [6] BALANCEAMENTO COM SMOTE
print("\n⚖️ Aplicando SMOTE para balancear classes...")
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)
print(f"Antes SMOTE: {dict(pd.Series(y_train).value_counts())}")
print(f"Depois SMOTE: {dict(pd.Series(y_train_bal).value_counts())}")

# %% [7] ESCALAR FEATURES
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_bal)
X_test_scaled = scaler.transform(X_test)

# Salvar scaler para uso futuro
joblib.dump(scaler, 'scaler_credito.pkl')
print("✅ Scaler salvo: scaler_credito.pkl")

# %% [8] TREINAR MODELOS
print("\n" + "="*60)
print("🤖 TREINAMENTO DE MODELOS")
print("="*60)

modelos = {
    'Logistic Regression': LogisticRegression(
        max_iter=1000, random_state=42, class_weight='balanced'
    ),
    'Random Forest': RandomForestClassifier(
        n_estimators=200, max_depth=10, min_samples_split=5,
        random_state=42, n_jobs=-1, class_weight='balanced'
    ),
    'XGBoost': XGBClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        random_state=42, eval_metric='logloss',
        use_label_encoder=False
    ),
    'LightGBM': lgb.LGBMClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        random_state=42, verbose=-1
    ),
}

resultados = {}

for nome, modelo in modelos.items():
    print(f"\n--- {nome} ---")
    
    # Usar dados escalados para Logistic, originais para tree-based
    if nome == 'Logistic Regression':
        modelo.fit(X_train_scaled, y_train_bal)
        y_pred = modelo.predict(X_test_scaled)
        y_proba = modelo.predict_proba(X_test_scaled)[:, 1]
    else:
        modelo.fit(X_train_bal, y_train_bal)
        y_pred = modelo.predict(X_test)
        y_proba = modelo.predict_proba(X_test)[:, 1]
    
    # Métricas
    roc = roc_auc_score(y_test, y_proba)
    f1 = f1_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    resultados[nome] = {
        'modelo': modelo,
        'roc_auc': roc,
        'f1': f1,
        'precision': report['1']['precision'],
        'recall': report['1']['recall'],
        'y_pred': y_pred,
        'y_proba': y_proba,
    }
    
    print(f"  ROC-AUC:   {roc:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"  Precision: {report['1']['precision']:.4f}")
    print(f"  Recall:    {report['1']['recall']:.4f}")

# %% [9] COMPARATIVO DE MODELOS
print("\n" + "="*60)
print("📊 COMPARATIVO FINAL")
print("="*60)

comparativo = pd.DataFrame({
    nome: {
        'ROC-AUC': r['roc_auc'],
        'F1-Score': r['f1'],
        'Precision': r['precision'],
        'Recall': r['recall'],
    }
    for nome, r in resultados.items()
}).T.sort_values('ROC-AUC', ascending=False)

print(comparativo.to_string())

melhor_nome = comparativo.index[0]
melhor = resultados[melhor_nome]
print(f"\n🏆 MELHOR MODELO: {melhor_nome} (ROC-AUC: {melhor['roc_auc']:.4f})")

# %% [10] GRÁFICO - CURVAS ROC
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor(COLORS['bg'])

# ROC Curves
ax = axes[0]
ax.set_facecolor(COLORS['bg_card'])
cores = [COLORS['primary'], COLORS['danger'], COLORS['warning'], COLORS['info']]
for (nome, r), cor in zip(resultados.items(), cores):
    fpr, tpr, _ = roc_curve(y_test, r['y_proba'])
    ax.plot(fpr, tpr, color=cor, linewidth=2, label=f"{nome} (AUC={r['roc_auc']:.3f})")
ax.plot([0,1], [0,1], '--', color='gray', alpha=0.5)
ax.set_title('Curvas ROC - Comparativo', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.set_xlabel('False Positive Rate'); ax.set_ylabel('True Positive Rate')
ax.legend(fontsize=9)

# Barras comparativas
ax = axes[1]
ax.set_facecolor(COLORS['bg_card'])
x = np.arange(len(comparativo))
w = 0.2
metricas = ['ROC-AUC', 'F1-Score', 'Precision', 'Recall']
for i, (met, cor) in enumerate(zip(metricas, cores)):
    ax.bar(x + i*w, comparativo[met], w, label=met, color=cor, alpha=0.85)
ax.set_xticks(x + 1.5*w)
ax.set_xticklabels(comparativo.index, rotation=15, fontsize=9)
ax.set_title('Métricas por Modelo', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.legend(fontsize=9)
ax.set_ylim(0, 1.05)

plt.tight_layout()
plt.savefig('modelo_comparativo.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
plt.show()
print("✅ Gráfico salvo: modelo_comparativo.png")

# %% [11] CONFUSION MATRIX DO MELHOR MODELO
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor(COLORS['bg'])
ax.set_facecolor(COLORS['bg_card'])
cm = confusion_matrix(y_test, melhor['y_pred'])
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd', ax=ax,
            xticklabels=['Pagou (0)', 'Default (1)'],
            yticklabels=['Pagou (0)', 'Default (1)'],
            annot_kws={'size': 16, 'fontweight': 'bold'})
ax.set_title(f'Matriz de Confusão - {melhor_nome}', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.set_xlabel('Predito'); ax.set_ylabel('Real')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
plt.show()
print("✅ Gráfico salvo: confusion_matrix.png")

# %% [12] FEATURE IMPORTANCE
print("\n" + "="*60)
print("📈 IMPORTÂNCIA DAS VARIÁVEIS")
print("="*60)

if melhor_nome in ['Random Forest', 'XGBoost', 'LightGBM']:
    importancias = pd.Series(
        melhor['modelo'].feature_importances_, index=X.columns
    ).sort_values(ascending=False)
else:
    importancias = pd.Series(
        np.abs(melhor['modelo'].coef_[0]), index=X.columns
    ).sort_values(ascending=False)

print(importancias.head(10).to_string())

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor(COLORS['bg'])
ax.set_facecolor(COLORS['bg_card'])
top15 = importancias.head(15)
bars = ax.barh(range(len(top15)), top15.values, color=COLORS['primary'], edgecolor='white', linewidth=0.3)
ax.set_yticks(range(len(top15)))
ax.set_yticklabels(top15.index, fontsize=11)
ax.invert_yaxis()
ax.set_title(f'Top 15 Features - {melhor_nome}', fontsize=14, fontweight='bold', color=COLORS['text'])
ax.set_xlabel('Importância', color=COLORS['text'])
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
plt.show()
print("✅ Gráfico salvo: feature_importance.png")

# Exportar importâncias para Power BI
importancias.reset_index().rename(columns={'index': 'feature', 0: 'importance'}).to_csv(
    'feature_importance.csv', index=False
)

# %% [13] SHAP - EXPLICABILIDADE
print("\n" + "="*60)
print("🔍 SHAP - EXPLICABILIDADE DO MODELO")
print("="*60)

try:
    if melhor_nome in ['Random Forest', 'XGBoost', 'LightGBM']:
        explainer = shap.TreeExplainer(melhor['modelo'])
        shap_values = explainer.shap_values(X_test.iloc[:500])
    else:
        explainer = shap.LinearExplainer(melhor['modelo'], X_test_scaled[:500])
        shap_values = explainer.shap_values(X_test_scaled[:500])
    
    # Se retornar lista (multi-class), pegar a classe positiva
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(COLORS['bg'])
    shap.summary_plot(shap_values, X_test.iloc[:500], plot_type="bar", show=False)
    plt.title(f'SHAP - {melhor_nome}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('shap_summary.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
    plt.show()
    print("✅ Gráfico SHAP salvo: shap_summary.png")
except Exception as e:
    print(f"⚠️ SHAP não disponível para este modelo: {e}")

# %% [14] EXPORTAR MODELO E PREDIÇÕES
print("\n" + "="*60)
print("💾 EXPORTANDO MODELO E RESULTADOS")
print("="*60)

# Salvar o melhor modelo
modelo_path = f'modelo_{melhor_nome.lower().replace(" ", "_")}.pkl'
joblib.dump(melhor['modelo'], modelo_path)
print(f"✅ Modelo salvo: {modelo_path}")

# Gerar dataset com predições para Power BI
df_pred = X_test.copy()
df_pred['loan_status_real'] = y_test.values
df_pred['loan_status_pred'] = melhor['y_pred']
df_pred['probabilidade_default'] = melhor['y_proba']
df_pred['risco_categoria'] = pd.cut(
    melhor['y_proba'],
    bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
    labels=['Muito Baixo', 'Baixo', 'Moderado', 'Alto', 'Muito Alto']
)
df_pred.to_csv('predicoes_risco_credito.csv', index=False)
print(f"✅ Predições salvas: predicoes_risco_credito.csv ({len(df_pred):,} linhas)")

# Comparativo de modelos para documentação
comparativo.to_csv('comparativo_modelos.csv')
print(f"✅ Comparativo salvo: comparativo_modelos.csv")

# Resumo final
print(f"""
{'='*60}
  FASE 3 CONCLUÍDA!
{'='*60}
  Melhor Modelo: {melhor_nome}
  ROC-AUC:       {melhor['roc_auc']:.4f}
  F1-Score:      {melhor['f1']:.4f}
  Precision:     {melhor['precision']:.4f}
  Recall:        {melhor['recall']:.4f}

  Arquivos para download (levar para o PC local):
    1. {modelo_path} (modelo treinado)
    2. scaler_credito.pkl (scaler)
    3. predicoes_risco_credito.csv (predições para Power BI)
    4. feature_importance.csv (importâncias para Power BI)
    5. comparativo_modelos.csv (métricas)
    6. *.png (gráficos)

  Proximo passo: Fase 4+5 - Baixar arquivos e integrar no Power BI
{'='*60}
""")

# %% [15] DOWNLOAD NO COLAB (descomentar quando for rodar lá)
# from google.colab import files
# for f in [modelo_path, 'scaler_credito.pkl', 'predicoes_risco_credito.csv',
#           'feature_importance.csv', 'comparativo_modelos.csv',
#           'modelo_comparativo.png', 'confusion_matrix.png', 'feature_importance.png']:
#     files.download(f)
