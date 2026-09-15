#!/usr/bin/env python3
"""
Aula 07 -- PARTE EXTRA (opcional, "se der tempo"): registra o mesmo
treino/avaliação num MLflow local -- outra ferramenta de tracking de
experimentos, fora do Kubeflow. Roda 100% local, sem servidor MLflow
remoto (usa um arquivo sqlite como backend).

Uso:
    pip install mlflow --break-system-packages
    python3 registrar_run_mlflow.py <caminho_csv>
    mlflow ui --backend-store-uri sqlite:///mlflow_aula07.db
    # depois abra http://localhost:5000
"""
import sys

import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

FEATURE_COLS = ["natureza", "bairro", "turno"]
TARGET_COL = "houve_violencia"
RANDOM_STATE = 42


def main():
    caminho_csv = sys.argv[1] if len(sys.argv) > 1 else "bos_sinteticos.csv"

    mlflow.set_tracking_uri("sqlite:///mlflow_aula07.db")
    mlflow.set_experiment("aula07-pcdf-mlflow")

    with mlflow.start_run(run_name=f"treino-{caminho_csv}"):
        df = pd.read_csv(caminho_csv)
        df_modelo = df[FEATURE_COLS + [TARGET_COL]].dropna()

        for col in FEATURE_COLS:
            le = LabelEncoder()
            df_modelo[col] = le.fit_transform(df_modelo[col].astype(str))

        X = df_modelo[FEATURE_COLS]
        y = df_modelo[TARGET_COL].astype(bool)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=RANDOM_STATE
        )

        max_depth = 3
        modelo = DecisionTreeClassifier(max_depth=max_depth, random_state=RANDOM_STATE)
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)

        # parametros -- o que descreve COMO o modelo foi treinado
        mlflow.log_param("dataset", caminho_csv)
        mlflow.log_param("linhas_treino", len(X_train))
        mlflow.log_param("linhas_teste", len(X_test))
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", RANDOM_STATE)

        # metricas -- o que descreve o RESULTADO
        mlflow.log_metric("acuracia", acc)
        mlflow.log_metric("precisao", prec)
        mlflow.log_metric("revocacao", rec)

        # o modelo em si, versionado junto com params/metricas do mesmo run
        mlflow.sklearn.log_model(modelo, name="modelo")

        print(f"run registrado -- acuracia={acc:.2%} precisao={prec:.2%} revocacao={rec:.2%}")
        print("rode 'mlflow ui --backend-store-uri sqlite:///mlflow_aula07.db' pra ver na interface")


if __name__ == "__main__":
    main()
