# SalesInsight PY

Repositório desenvolvido para o **Mini Projeto do Módulo 7**. Pipeline automatizado completo em Python (Pandas, NumPy, Matplotlib) contemplando todos os requisitos obrigatórios e bônus de engenharia e análise de dados.

---

## 📋 Requisitos Funcionais Implementados
- **RF01**: Geração de dataset sintético de vendas com dados sujos (`vendas.csv`).
- **RF02**: Inspeção estrutural automatizada do DataFrame.
- **RF03**: Tratamento e conversão de datas inválidas (`datetime`).
- **RF04**: Criação de coluna derivada (`faturamento`).
- **RF05**: Métricas agregadas por agrupamento (`groupby`).
- **RF06**: Segmentação de clientes por nível de gasto (`Alto`, `Médio`, `Baixo`).
- **RF07**: Geração de visualizações gráficas obrigatórias em PNG.
- **RF08**: Modularização do código em funções reutilizáveis.
- **RF09**: Exportação de relatórios em CSV e JSON.
- **RF10**: Ponto de entrada estruturado via `if __name__ == "__main__":`.

## ⭐ Requisitos Bônus Implementados (Opcionais)
- **B01 (Tendência e Média Móvel)**: Projeção de receita mensal baseada em média móvel de 3 meses.
- **B03 (Pivot Table)**: Tabela cruzada detalhando o faturamento por **Mês × Categoria**.
- **B04 (Gráficos Adicionais)**: Geração de gráfico de linha de tendência temporal e Boxplot estatístico de preços.
- **B05 (Percentis e Quartis)**: Cálculo detalhado dos quartis e percentis estatísticos da receita.
- **B06 (Kanban)**: Gestão de fluxo organizada por colunas (*Backlog*, *A Fazer*, *Em Andamento*, *Concluído*).

---

## 📋 Organização do Kanban (B06)
- [x] **Backlog**: Concepção e escopo do pipeline de vendas.
- [x] **A Fazer**: Estruturação do repositório Git e definição de branch `develop`.
- [x] **Em Andamento**: Desenvolvimento dos scripts modulares em Python.
- [x] **Concluído**: Testes, validações, gráficos, relatórios JSON/CSV e documentação final.

---

## 📁 Estrutura do Projeto (`outputs/`)
```text
salesinsight-py/
│
├── outputs/
│   ├── boxplot_preco_unitario.png
│   ├── evolucao_tendencia_faturamento.png
│   ├── faturamento_por_produto.csv
│   ├── faturamento_por_produto.json
│   ├── faturamento_por_produto.png
│   ├── faturamento_por_regiao.csv
│   ├── faturamento_por_regiao.json
│   ├── faturamento_por_regiao.png
│   ├── projecao_tendencia_mensal.csv
│   ├── segmentacao_clientes.csv
│   ├── segmentacao_clientes.json
│   ├── tabela_cruzada_mes_categoria.csv
│   └── vendas_limpo.csv
│
├── .gitignore
├── README.md
├── salesinsight.py
└── vendas.csv