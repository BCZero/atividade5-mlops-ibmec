#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aula 05 -- ML rapido e simples (mesmo espirito da Aula 01), agora
fechando o ciclo: o dado que SAIU do DAG do Airflow (bos_tratados.csv,
ja limpo pela task clean) e o dado que ENTRA no treino do modelo.

Pergunta de negocio (ficticia, so para demonstracao):
    dado natureza, bairro e turno da ocorrencia, o modelo consegue
    prever se "houve_violencia"?

Testado com: scikit-learn (pip install scikit-learn pandas)

Uso:
    python3 treino_ml_rapido.py [caminho/para/bos_tratados.csv]
    # se nao passar caminho, usa bos_sinteticos.csv como fallback
"""
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "bos_sinteticos.csv"
    df = pd.read_csv(caminho)
    print(f"Dados carregados de {caminho}: {len(df)} linhas")

    # features categoricas simples -> numeros (LabelEncoder), so para
    # o modelo conseguir processar; produção usaria OneHotEncoder
    colunas_features = ["natureza", "bairro", "turno"]
    df_modelo = df[colunas_features + ["houve_violencia"]].dropna()

    encoders = {}
    for col in colunas_features:
        le = LabelEncoder()
        df_modelo[col] = le.fit_transform(df_modelo[col].astype(str))
        encoders[col] = le

    X = df_modelo[colunas_features]
    y = df_modelo["houve_violencia"].astype(bool)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"\nLinhas de treino: {len(X_train)} | teste: {len(X_test)}")
    print(f"Acuracia no conjunto de teste: {acc:.2%}")
    print("\nImportancia de cada feature (quanto o modelo usou cada uma):")
    for col, imp in zip(colunas_features, modelo.feature_importances_):
        print(f"  {col}: {imp:.2f}")

    print(
        "\nAviso: dataset ficticio e pequeno demais para conclusões reais -- "
        "o objetivo aqui é só mostrar o pipeline dados-limpos -> treino -> métrica funcionando."
    )


if __name__ == "__main__":
    main()
