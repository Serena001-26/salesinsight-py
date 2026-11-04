import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintetico de vendas com dados sujos."""
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

        # --- sujeira proposital para a etapa de limpeza --- 
        if random.random() < 0.03:
            data_txt = "DATA INVALIDA"        # data invalida

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
    """Realiza analises exploratorias e agrupamentos (RF04)."""
    print("\n=== ANALISE EXPLORATORIA DE VENDAS ===")
    
    df["faturamento"] = df["quantidade"] * df["preco_unitario"]
    
    fat_produto = df.groupby("produto")["faturamento"].sum().reset_index()
    print("\nFaturamento por Produto:\n", fat_produto)
    
    vendas_regiao = df.groupby("regiao")["faturamento"].sum().reset_index()
    print("\nFaturamento por Regiao:\n", vendas_regiao)
    
    return df, fat_produto, vendas_regiao


def exportar_resultados(df_limpo, fat_produto, vendas_regiao):
    """Exporta os dados limpos e relatorios para a pasta outputs (RF05)."""
    os.makedirs("outputs", exist_ok=True)
    
    df_limpo.to_csv("outputs/vendas_limpo.csv", index=False)
    fat_produto.to_csv("outputs/faturamento_por_produto.csv", index=False)
    vendas_regiao.to_csv("outputs/faturamento_por_regiao.csv", index=False)
    
    print("\n=== EXPORTACAO CONCLUIDA ===")
    print("Arquivos salvos na pasta 'outputs/'.")


if __name__ == "__main__":
    df_bruto = gerar_dataset_vendas()
    df_bruto.to_csv("vendas.csv", index=False)
    print(f"Dataset gerado com {len(df_bruto)} registros e salvo em vendas.csv.")

    inspecionar_dados(df_bruto)
    df_limpo, _ = tratar_dados(df_bruto)
    
    df_limpo, fat_produto, vendas_regiao = analisar_vendas(df_limpo)
    exportar_resultados(df_limpo, fat_produto, vendas_regiao)