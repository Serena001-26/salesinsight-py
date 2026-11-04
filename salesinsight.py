import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt

def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos (RF01)."""
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Computadores",
                  "Teclado": "Perifericos", "Mouse": "Perifericos",
                  "Headset": "Perifericos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
              "Monitor": 1200, "Teclado": 250, "Mouse": 120,
              "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    data_inicio = datetime(2025, 1, 1)
    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        categoria = categorias[produto]
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        data_txt = data.strftime("%Y-%m-%d")
        cliente = f"Cliente_{random.randint(1, 50):03d}"

        if random.random() < 0.03:
            data_txt = "DATA INVALIDA"

        dados.append({
            "id_venda": i + 1,
            "data_venda": data_txt,
            "cliente": cliente,
            "produto": produto,
            "categoria": categoria,
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco,
        })

    return pd.DataFrame(dados)


def inspecionar_dados(df):
    """Exibe as informacoes estruturais do DataFrame (RF02)."""
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Shape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    return df


def tratar_dados(df):
    """Trata o DataFrame de vendas (RF03)."""
    total_inicial = len(df)
    
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()

    df["data_venda_convertida"] = pd.to_datetime(df["data_venda"], errors="coerce")
    invalidas = df["data_venda_convertida"].isnull().sum()
    
    df = df.dropna(subset=["data_venda_convertida"])
    df["data_venda"] = df["data_venda_convertida"]
    df = df.drop(columns=["data_venda_convertida"])

    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").astype(int)
    df["preco_unitario"] = pd.to_numeric(df["preco_unitario"], errors="coerce").astype(float)

    total_final = len(df)

    relatorio = {
        "registros_iniciais": total_inicial,
        "registros_removidos_data_invalida": invalidas,
        "registros_finais": total_final
    }

    print("\n=== RELATORIO DE LIMPEZA ===")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")

    return df, relatorio


def analisar_vendas(df):
    """Realiza analises exploratorias, calculos e agrupamentos (RF04 e RF05)."""
    print("\n=== ANALISE EXPLORATORIA DE VENDAS ===")
    df["faturamento"] = df["quantidade"] * df["preco_unitario"]
    
    fat_produto = df.groupby("produto")["faturamento"].sum().reset_index()
    vendas_regiao = df.groupby("regiao")["faturamento"].sum().reset_index()
    
    return df, fat_produto, vendas_regiao


def segmentar_clientes(df):
    """Segmenta os clientes por nivel de gasto (RF06)."""
    print("\n=== SEGMENTACAO DE CLIENTES ===")
    gasto_cliente = df.groupby("cliente")["faturamento"].sum().reset_index()
    
    quantil_33 = gasto_cliente["faturamento"].quantile(0.33)
    quantil_66 = gasto_cliente["faturamento"].quantile(0.66)
    
    def rotular_cliente(valor):
        if valor >= quantil_66:
            return "Alto"
        elif valor >= quantil_33:
            return "Medio"
        else:
            return "Baixo"
            
    gasto_cliente["nivel_gasto"] = gasto_cliente["faturamento"].apply(rotular_cliente)
    return gasto_cliente


def executar_requisitos_bonus(df):
    """Executa todos os requisitos bonus (B01, B03, B05)."""
    print("\n=== EXECUTANDO REQUISITOS BONUS ===")
    os.makedirs("outputs", exist_ok=True)
    
    # B01 - Projeção simples de tendência (Média móvel de faturamento mensal)
    df["mes"] = df["data_venda"].dt.to_period("M").astype(str)
    fat_mensal = df.groupby("mes")["faturamento"].sum().reset_index()
    fat_mensal["media_movel_3m"] = fat_mensal["faturamento"].rolling(window=3, min_periods=1).mean()
    fat_mensal.to_csv("outputs/projecao_tendencia_mensal.csv", index=False)
    print("B01 - Projeção de tendência e média móvel calculadas.")
    
    # B03 - Tabela Cruzada (Pivot Table): Mês x Categoria
    tabela_pivot = df.pivot_table(index="mes", columns="categoria", values="faturamento", aggfunc="sum", fill_value=0)
    tabela_pivot.to_csv("outputs/tabela_cruzada_mes_categoria.csv")
    print("B03 - Tabela cruzada (Mês x Categoria) gerada.")
    
    # B05 - Percentis e Quartis estatísticos da receita
    quartis = df["faturamento"].quantile([0.25, 0.50, 0.75, 0.90])
    print(f"B05 - Quartis e Percentis de Faturamento:\n{quartis}")
    
    return fat_mensal, tabela_pivot


def gerar_visualizacoes(fat_produto, vendas_regiao, fat_mensal, df_limpo):
    """Gera graficos obrigatorios e adicionais com Matplotlib (RF07 e B04)."""
    os.makedirs("outputs", exist_ok=True)
    
    # Gráfico 1: Faturamento por Produto (RF07)
    plt.figure(figsize=(8, 4))
    plt.bar(fat_produto["produto"], fat_produto["faturamento"], color="skyblue")
    plt.title("Faturamento Total por Produto")
    plt.xlabel("Produto")
    plt.ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/faturamento_por_produto.png")
    plt.close()

    # Gráfico 2: Faturamento por Região (RF07)
    plt.figure(figsize=(8, 4))
    plt.bar(vendas_regiao["regiao"], vendas_regiao["faturamento"], color="salmon")
    plt.title("Faturamento Total por Regiao")
    plt.xlabel("Regiao")
    plt.ylabel("Faturamento (R$)")
    plt.tight_layout()
    plt.savefig("outputs/faturamento_por_regiao.png")
    plt.close()

    # Gráfico B04-1: Evolução Temporal da Receita com Média Móvel (B01 / B04)
    plt.figure(figsize=(10, 4))
    plt.plot(fat_mensal["mes"], fat_mensal["faturamento"], marker="o", label="Faturamento Mensal", color="purple")
    plt.plot(fat_mensal["mes"], fat_mensal["media_movel_3m"], marker="x", linestyle="--", label="Média Móvel (3M)", color="orange")
    plt.title("Evolução Temporal e Tendência de Faturamento")
    plt.xlabel("Mês")
    plt.ylabel("Faturamento (R$)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/evolucao_tendencia_faturamento.png")
    plt.close()

    # Gráfico B04-2: Boxplot da Distribuição de Preço Unitário (B04)
    plt.figure(figsize=(6, 4))
    plt.boxplot(df_limpo["preco_unitario"], patch_artist=True, boxprops=dict(facecolor="lightgreen"))
    plt.title("Distribuição de Preços Unitários (Boxplot)")
    plt.ylabel("Preço Unitário (R$)")
    plt.tight_layout()
    plt.savefig("outputs/boxplot_preco_unitario.png")
    plt.close()
    
    print("\n=== VISUALIZACOES (OBRIGATORIAS E BONUS B04) GERADAS ==p")


def exportar_resultados(df_limpo, fat_produto, vendas_regiao, gasto_cliente):
    """Exporta os resultados em CSV e JSON (RF09)."""
    os.makedirs("outputs", exist_ok=True)
    
    df_limpo.to_csv("outputs/vendas_limpo.csv", index=False)
    fat_produto.to_csv("outputs/faturamento_por_produto.csv", index=False)
    vendas_regiao.to_csv("outputs/faturamento_por_regiao.csv", index=False)
    gasto_cliente.to_csv("outputs/segmentacao_clientes.csv", index=False)
    
    fat_produto.to_json("outputs/faturamento_por_produto.json", orient="records", indent=4)
    vendas_regiao.to_json("outputs/faturamento_por_regiao.json", orient="records", indent=4)
    gasto_cliente.to_json("outputs/segmentacao_clientes.json", orient="records", indent=4)
    
    print("=== EXPORTACAO CONCLUIDA (CSV e JSON) ===")


if __name__ == "__main__":
    df_bruto = gerar_dataset_vendas()
    df_bruto.to_csv("vendas.csv", index=False)
    
    inspecionar_dados(df_bruto)
    df_limpo, _ = tratar_dados(df_bruto)
    
    df_limpo, fat_produto, vendas_regiao = analisar_vendas(df_limpo)
    gasto_cliente = segmentar_clientes(df_limpo)
    
    # Executando Bônus B01, B03 e B05
    fat_mensal, _ = executar_requisitos_bonus(df_limpo)
    
    # Gerando Gráficos Obrigatórios e Bônus B04
    gerar_visualizacoes(fat_produto, vendas_regiao, fat_mensal, df_limpo)
    
    exportar_resultados(df_limpo, fat_produto, vendas_regiao, gasto_cliente)