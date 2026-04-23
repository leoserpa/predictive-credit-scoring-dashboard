# 📑 Relatório de Performance e Explicabilidade do Modelo
**Projeto:** Previsão de Risco de Crédito (Fintech)  
**Versão do Modelo:** 1.0 (LightGBM)  
**Data:** 22/04/2026

## 1. Resumo Executivo
O modelo desenvolvido apresenta um desempenho excepcional na identificação de inadimplentes (*default*). Com uma área sob a curva ROC (**AUC**) de **0.9456**, o motor preditivo demonstra uma capacidade superior de diferenciar clientes saudáveis de clientes de risco, superando significativamente benchmarks de mercado para este tipo de dataset (geralmente situados entre 0.85 e 0.90).

## 2. Análise de Métricas (Performance Técnica)

### 2.1. Precisão vs. Recall (O Trade-off Financeiro)
- **Precisão (0.9689):** Este é o ponto mais forte do modelo. Significa que, de cada 100 clientes que o modelo marcou como "Risco", **96 ou 97 realmente seriam inadimplentes**. 
    - *Impacto para a Fintech:* Baixíssima taxa de "rejeição injusta". Isso garante que o banco não perca bons clientes e mantenha uma boa experiência do usuário.
- **Recall (0.7234):** O modelo consegue capturar **72.3% de todos os calotes** que ocorreriam. 
    - *Impacto para a Fintech:* Embora não pegue 100% dos calotes (o que é impossível sem negar crédito para todo mundo), ele filtra a grande maioria do prejuízo potencial, protegendo o caixa da empresa.

### 2.2. ROC-AUC (0.9456)
O valor de 0.94 indica que, se pegarmos um cliente que pagou e um que deu calote aleatoriamente, o modelo tem **94.5% de chance** de classificar o caloteiro com uma probabilidade de risco maior que o bom pagador.

## 3. Explicabilidade do Modelo (SHAP & Feature Importance)
Baseado na análise de valores SHAP e importância de variáveis, identificamos os 3 principais pilares do risco:

1.  **loan_int_rate (Taxa de Juros):** O principal preditor. Existe uma correlação direta onde taxas de juros mais altas estão associadas a perfis de risco mais elevados. O modelo capturou que a precificação de juros já reflete parte do risco intrínseco.
2.  **person_income (Renda Anual):** A renda atua como um fator de proteção. Clientes com renda mais alta apresentam um SHAP value negativo (diminuem a probabilidade de default), enquanto rendas baixas aumentam drasticamente o risco.
3.  **loan_percent_income (Percentual da Renda):** O comprometimento da renda é crucial. Clientes que solicitam empréstimos que representam mais de 30% de sua renda anual entram automaticamente em zonas de alerta do modelo.

## 4. Matriz de Confusão e Decisão de Negócio
O modelo tende a ser "conservador" na negação. Ele prefere deixar passar um caloteiro (Falso Negativo) do que negar crédito para um cliente excelente (Falso Positivo). Para uma Fintech em fase de crescimento (*growth*), esta é a configuração ideal para não barrar a expansão da base de clientes.

## 5. Próximos Passos Recomendados
1.  **Monitoramento de Drift:** Monitorar se o perfil dos novos solicitantes muda ao longo do tempo.
2.  **Ajuste de Threshold:** Dependendo do apetite de risco da Fintech, podemos baixar o limiar de decisão de 0.50 para 0.35 para capturar ainda mais calotes (aumentar Recall), mesmo que isso custe um pouco de Precisão.
3.  **Integração BI:** Consumir o campo `probabilidade_default` no Power BI para criar faixas de juros personalizadas baseadas no risco individual.

---
*Relatório gerado automaticamente para fins de documentação de portfólio sênior.*
