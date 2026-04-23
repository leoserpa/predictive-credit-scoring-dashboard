# 📊 Fintech Credit Risk Model - Machine Learning
![Version](https://img.shields.io/badge/version-v1.0.0-A278E1?style=flat-square)
![Status](https://img.shields.io/badge/status-em--desenvolvimento-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power--BI-Premium--UI-F2C811?style=flat-square&logo=powerbi&logoColor=black)

Este projeto consiste no desenvolvimento de um motor preditivo de **Risco de Crédito** para uma Fintech, utilizando algoritmos de última geração para prever a probabilidade de inadimplência (*default*).

O objetivo principal é classificar novos solicitantes de empréstimo em faixas de risco e integrar os resultados em um dashboard de Power BI para suporte à decisão de crédito.

## 🚀 Destaques do Projeto
- **Melhor Modelo:** LightGBM (Gradient Boosting Machine).
- **ROC-AUC:** 0.9456 (Excelente poder de separação).
- **Precisão:** 96.89% (Alta confiança na negação de crédito).
- **Explicabilidade:** Utilização de **SHAP Values** para entender o impacto de cada variável no risco.

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+**
- **Pandas & Numpy:** Manipulação de dados e Feature Engineering.
- **Scikit-Learn:** Modelagem e métricas.
- **XGBoost & LightGBM:** Algoritmos de alto desempenho.
- **Imbalanced-Learn (SMOTE):** Balanceamento de classes.
- **SHAP:** Interpretabilidade de modelos.
- **Power BI:** Visualização e Dashboard.

## 📂 Estrutura do Projeto
```text
├── data/
│   ├── raw/            # Dataset original (Credit Risk Dataset)
│   └── processed/      # Dataset limpo e Predições finais para Power BI
├── models/             # Modelos treinados (.pkl) e Scaler
├── notebooks/          # Scripts para treinamento em nuvem (Google Colab)
├── src/                # Código fonte de limpeza e engenharia de features
├── dashboard/          # Arquivo .pbix e modelo semântico do Power BI
├── template_powerbi/   # Gerador de template SVG e background do dashboard
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

## 📈 Resultados Obtidos
O modelo final (LightGBM) demonstrou um equilíbrio superior entre precisão e sensibilidade:
- **Precision:** 0.9689 (Mínimo de falsos positivos).
- **Recall:** 0.7234 (Identifica a maioria dos potenciais calotes).
- **F1-Score:** 0.8284.

As variáveis mais importantes para o modelo foram a **Taxa de Juros**, o **Grau do Empréstimo** e a **Renda Anual**.

---
*Este projeto foi desenvolvido como parte de um portfólio profissional de Data Science focado no setor financeiro.*
