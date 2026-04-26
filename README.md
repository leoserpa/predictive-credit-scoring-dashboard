# 📊 Credit Risk Prediction - Machine Learning

[**Português**](#-credit-risk-prediction---machine-learning-versão-em-português) | [**English**](#-credit-risk-prediction---machine-learning-english-version)

---

# 📊 Credit Risk Prediction - Machine Learning (Versão em Português)

![Version](https://img.shields.io/badge/version-v1.2.0-A278E1?style=flat-square)
![Status](https://img.shields.io/badge/status-Finalizado-00D4AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power--BI-Premium--UI-F2C811?style=flat-square&logo=powerbi&logoColor=black)

Este projeto consiste no desenvolvimento de um motor preditivo de **Risco de Crédito** baseado no **Credit Risk Dataset (Kaggle)**, utilizando algoritmos de última geração para prever a probabilidade de inadimplência (*default*).

O objetivo principal é classificar novos solicitantes de empréstimo em faixas de risco e integrar os resultados em um dashboard de Power BI para suporte à decisão de crédito.

## 🚀 Destaques do Projeto
- **Melhor Modelo:** LightGBM (Gradient Boosting Machine).
- **ROC-AUC:** 0.9456 (Excelente poder de separação).
- **Precisão:** 96.89% (Alta confiança na negação de crédito).
- **Explicabilidade:** Utilização de **SHAP Values** para entender o impacto de cada variável no risco.

## 🖼️ Visualização do Dashboard

Aqui estão os templates de alta fidelidade desenvolvidos para este projeto:

### 1. Menu de Navegação (Início)
O ponto de entrada do sistema, projetado para facilitar o acesso rápido aos diferentes módulos de análise.
![Início](assets/dashboard_inicio.png)

---

### 2. Visão Geral de Risco
Monitoramento estratégico da carteira com 4 KPIs principais (Total de Clientes, Média de Risco, Volume Total e Volume em Risco), além de análises de composição por nível de risco (Donut), perfil de risco por finalidade (Barras) e volume financeiro por categoria (Treemap). Inclui também uma barra lateral com filtros e legenda de risco.
![Visão Geral](assets/visao_geral_de_risco.png)

---

### 3. Performance do Modelo
Análise técnica da precisão do motor preditivo com KPIs de ROC-AUC (Distinção), Recall (Taxa de Detecção), Precisão (Confiança) e F1-Score (Equilíbrio). A página detalha os Fatores Críticos na Previsão de Calote (Feature Importance), o Comparativo de Modelos (Benchmark) e a Eficiência da Categorização de Risco. Inclui uma ficha técnica com as especificações do modelo e a justificativa para a escolha do algoritmo LightGBM Classifier.
![Performance](assets/performance_modelo.png)

---

### 4. Previsão de Risco (Mesa de Operação)
Interface operacional para análise detalhada e suporte à decisão, apresentando o Painel de Avaliação de Risco com o perfil financeiro completo e a probabilidade de calote individualizada por cliente. Inclui 4 KPIs estratégicos (Total de Clientes, Média de Risco, Volume Total e Taxa de Juros Média). Inclui também uma barra lateral com filtros e legenda de risco.
![Previsão](assets/previsao_risco.png)

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
├── assets/             # Capturas de tela e recursos visuais do dashboard
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

### 🔬 Validação Técnica
Para garantir a confiabilidade do motor preditivo, foram realizadas validações estatísticas avançadas:

| Matriz de Confusão | Explicabilidade (SHAP) |
| :---: | :---: |
| ![Confusion Matrix](reports/figures/confusion_matrix.png) | ![SHAP Summary](reports/figures/shap_summary.png) |
| *Avaliação de acertos e erros (Default vs Bom Pagador)* | *Contribuição de cada variável para o risco* |

> 💡 **Nota Técnica:** Também realizamos uma análise exploratória profunda, incluindo o **Mapa de Correlação** das variáveis financeiras:
> ![Correlação](reports/figures/eda_02_correlacao.png)

---
*Este projeto foi desenvolvido como parte de um portfólio profissional de Data Science focado no setor financeiro.*

<br>

---

# 📊 Credit Risk Prediction - Machine Learning (English Version)

![Version](https://img.shields.io/badge/version-v1.2.0-A278E1?style=flat-square)
![Status](https://img.shields.io/badge/status-Finished-00D4AA?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power--BI-Premium--UI-F2C811?style=flat-square&logo=powerbi&logoColor=black)

This project consists of the development of a **Credit Risk** predictive engine based on the **Credit Risk Dataset (Kaggle)**, using state-of-the-art algorithms to predict default probability.

The main objective is to classify new loan applicants into risk tiers and integrate the results into a Power BI dashboard to support credit decision-making.

## 🚀 Project Highlights
- **Best Model:** LightGBM (Gradient Boosting Machine).
- **ROC-AUC:** 0.9456 (Excellent separation power).
- **Precision:** 96.89% (High confidence in credit denial).
- **Explainability:** Use of **SHAP Values** to understand the impact of each variable on risk.

## 🖼️ Dashboard Visualization

Here are the high-fidelity templates developed for this project:

### 1. Navigation Menu (Home)
The system's entry point, designed to facilitate quick access to different analysis modules.
![Home](assets/dashboard_inicio.png)

---

### 2. Risk Overview
Strategic portfolio monitoring with 4 main KPIs (Total Customers, Average Risk, Total Volume, and Volume at Risk), plus composition analysis by risk level (Donut), risk profile by purpose (Bars), and financial volume by category (Treemap). Also includes a sidebar with filters and risk legend.
![Overview](assets/visao_geral_de_risco.png)

---

### 3. Model Performance
Technical analysis of the predictive engine's accuracy with ROC-AUC (Distinction), Recall (Detection Rate), Precision (Confidence), and F1-Score (Balance) KPIs. The page details the Critical Factors in Default Prediction (Feature Importance), Model Comparison (Benchmark), and Risk Categorization Efficiency. Includes a technical sheet with model specifications and the rationale for choosing the LightGBM Classifier algorithm.
![Performance](assets/performance_modelo.png)

---

### 4. Risk Prediction (Operational Desk)
Operational interface for detailed analysis and decision support, featuring the Risk Assessment Panel with a complete financial profile and individualized default probability per customer. Includes 4 strategic KPIs (Total Customers, Average Risk, Total Volume, and Average Interest Rate). Also includes a sidebar with filters and risk legend.
![Prediction](assets/previsao_risco.png)

## 🛠️ Technologies Used
- **Python 3.10+**
- **Pandas & Numpy:** Data manipulation and Feature Engineering.
- **Scikit-Learn:** Modeling and metrics.
- **XGBoost & LightGBM:** High-performance algorithms.
- **Imbalanced-Learn (SMOTE):** Class balancing.
- **SHAP:** Model interpretability.
- **Power BI:** Visualization and Dashboard.

## 📂 Project Structure
```text
├── assets/             # Dashboard screenshots and visual resources
├── data/
│   ├── raw/            # Original dataset (Credit Risk Dataset)
│   └── processed/      # Clean dataset and Final predictions for Power BI
├── models/             # Trained models (.pkl) and Scaler
├── notebooks/          # Scripts for cloud training (Google Colab)
├── src/                # Cleaning and feature engineering source code
├── dashboard/          # .pbix file and Power BI semantic model
├── template_powerbi/   # SVG template generator and dashboard background
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## 📈 Results Obtained
The final model (LightGBM) demonstrated a superior balance between precision and sensitivity:
- **Precision:** 0.9689 (Minimum false positives).
- **Recall:** 0.7234 (Identifies most potential defaults).
- **F1-Score:** 0.8284.

The most important variables for the model were **Interest Rate**, **Loan Grade**, and **Annual Income**.

### 🔬 Technical Validation
To ensure the reliability of the predictive engine, advanced statistical validations were performed:

| Confusion Matrix | Explainability (SHAP) |
| :---: | :---: |
| ![Confusion Matrix](reports/figures/confusion_matrix.png) | ![SHAP Summary](reports/figures/shap_summary.png) |
| *Evaluation of hits and misses (Default vs Good Payer)* | *Contribution of each variable to risk* |

> 💡 **Technical Note:** We also performed a deep exploratory analysis, including the **Correlation Map** of financial variables:
> ![Correlation](reports/figures/eda_02_correlacao.png)

---
*This project was developed as part of a professional Data Science portfolio focused on the financial sector.*
