#!/usr/bin/env python3
"""
Aula 07 -- pipeline Kubeflow de 5 componentes (extracao, limpeza, treino,
avaliacao, salvar modelo), rodando de VERDADE num cluster Kubernetes (Kind),
nao mais via kfp.local (Aula 06). Os 5 componentes usam a MESMA imagem
Docker custom (construida no Bloco 1) como base_image -- ela ja tem
pandas/scikit-learn/joblib instalados e o dataset de exemplo embutido, entao
nenhum componente precisa instalar nada em tempo de execucao.

Tema: mesmo projeto-guia PCDF (Boletins de Ocorrencia) das Aulas 05/06 --
o modelo prediz "houve_violencia" a partir de natureza/bairro/turno.
"""
from kfp import dsl
from kfp import compiler
from kfp.dsl import Input, Output, Dataset, Model, Metrics

# --------------------------------------------------------------------------
# IMAGEM CUSTOM (Bloco 1) -- troque SEU-USUARIO-DOCKERHUB pelo SEU usuario
# do Docker Hub (ou registry que voce estiver usando). E a mesma imagem que
# o workflow ci-cd-mlops.yml builda e pusha a cada push na branch main.
# --------------------------------------------------------------------------
IMAGE_REF = "SEU-USUARIO-DOCKERHUB/aula7-mlops-pcdf:latest"

LIMIAR_MINIMO = 0.60  # mesmo limiar didatico usado no teste de modelo da Aula 06


@dsl.component(base_image=IMAGE_REF, install_kfp_package=False)
def extrair(saida: Output[Dataset]):
    """Simula a extracao de uma fonte de dados bruta. Em producao seria um
    banco de dados ou uma API; aqui e o CSV que ja vem EMBUTIDO na imagem
    Docker (copiado em /app/data/bos_sinteticos.csv no Dockerfile) -- por
    isso alterar o dado de treino = editar o CSV + rebuild da imagem."""
    import shutil

    shutil.copy("/app/data/bos_sinteticos.csv", saida.path)
    print(f"extracao: copiado /app/data/bos_sinteticos.csv -> {saida.path}")


@dsl.component(base_image=IMAGE_REF, install_kfp_package=False)
def limpar(entrada: Input[Dataset], saida: Output[Dataset]):
    """Mesma normalizacao (minusculas + strip) e validacao de schema da
    Aula 06 (src/etl_utils.py) -- aqui reescrita inline porque cada
    componente KFP roda isolado, em seu proprio pod."""
    import pandas as pd

    REQUIRED_COLUMNS = [
        "id", "texto_relato", "natureza", "bairro", "turno",
        "dia_semana", "houve_violencia", "valor_prejuizo_reais",
        "idade_vitima", "reincidencia",
    ]

    df = pd.read_csv(entrada.path)

    faltando = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if faltando:
        raise ValueError(f"colunas faltando no dataset: {faltando}")

    for col in ("natureza", "bairro", "turno"):
        df[col] = df[col].astype(str).str.lower().str.strip()

    df.to_csv(saida.path, index=False)
    print(f"limpeza: {len(df)} linhas normalizadas -> {saida.path}")


@dsl.component(base_image=IMAGE_REF, install_kfp_package=False)
def treinar(entrada: Input[Dataset], modelo: Output[Model], random_state: int = 42):
    """Treina o mesmo DecisionTreeClassifier das Aulas 05/06, agora dentro
    de um pod do cluster. Salva o modelo treinado com joblib."""
    import joblib
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.tree import DecisionTreeClassifier

    FEATURE_COLS = ["natureza", "bairro", "turno"]
    TARGET_COL = "houve_violencia"

    df = pd.read_csv(entrada.path)
    df_modelo = df[FEATURE_COLS + [TARGET_COL]].dropna()

    for col in FEATURE_COLS:
        le = LabelEncoder()
        df_modelo[col] = le.fit_transform(df_modelo[col].astype(str))

    X = df_modelo[FEATURE_COLS]
    y = df_modelo[TARGET_COL].astype(bool)

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.3, random_state=random_state
    )

    clf = DecisionTreeClassifier(max_depth=3, random_state=random_state)
    clf.fit(X_train, y_train)

    joblib.dump(clf, modelo.path)
    print(f"treino: modelo salvo em {modelo.path} ({len(X_train)} linhas de treino)")


@dsl.component(base_image=IMAGE_REF, install_kfp_package=False)
def avaliar(
    entrada: Input[Dataset],
    modelo: Input[Model],
    metricas: Output[Metrics],
    random_state: int = 42,
) -> float:
    """Refaz o MESMO split (mesmo random_state) pra isolar o conjunto de
    teste que o treino nao viu, e calcula acuracia/precisao/revocacao.
    Devolve a acuracia -- e o valor que salvar_modelo usa como gate."""
    import joblib
    import pandas as pd
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    FEATURE_COLS = ["natureza", "bairro", "turno"]
    TARGET_COL = "houve_violencia"

    df = pd.read_csv(entrada.path)
    df_modelo = df[FEATURE_COLS + [TARGET_COL]].dropna()

    for col in FEATURE_COLS:
        le = LabelEncoder()
        df_modelo[col] = le.fit_transform(df_modelo[col].astype(str))

    X = df_modelo[FEATURE_COLS]
    y = df_modelo[TARGET_COL].astype(bool)

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.3, random_state=random_state
    )

    clf = joblib.load(modelo.path)
    y_pred = clf.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))

    metricas.log_metric("acuracia", acc)
    metricas.log_metric("precisao", prec)
    metricas.log_metric("revocacao", rec)

    print(f"avaliacao: acuracia={acc:.2%} precisao={prec:.2%} revocacao={rec:.2%}")
    return acc


@dsl.component(base_image=IMAGE_REF, install_kfp_package=False)
def salvar_modelo(
    modelo: Input[Model],
    acuracia: float,
    destino: Output[Model],
    limiar_minimo: float = LIMIAR_MINIMO,
):
    """Gate de governanca: só promove o modelo se a acuracia bater o
    limiar minimo -- do contrario FALHA o pipeline de proposito (mesmo
    espirito do tests/test_model_threshold.py da Aula 06, agora como
    etapa do próprio pipeline, nao só do CI)."""
    import shutil

    if acuracia < limiar_minimo:
        raise RuntimeError(
            f"acuracia {acuracia:.2%} abaixo do limiar minimo de "
            f"{limiar_minimo:.0%} -- pipeline NAO deve promover este modelo"
        )

    shutil.copy(modelo.path, destino.path)
    print(f"modelo promovido: acuracia {acuracia:.2%} >= limiar {limiar_minimo:.0%}")


@dsl.pipeline(
    name="pipeline-mlops-pcdf",
    description="Extracao -> limpeza -> treino -> avaliacao -> salvar modelo, rodando no cluster Kind (Aula 07).",
)
def pipeline_mlops_pcdf(limiar_minimo: float = LIMIAR_MINIMO):
    passo_extrair = extrair()
    passo_limpar = limpar(entrada=passo_extrair.outputs["saida"])
    passo_treinar = treinar(entrada=passo_limpar.outputs["saida"])
    passo_avaliar = avaliar(
        entrada=passo_limpar.outputs["saida"],
        modelo=passo_treinar.outputs["modelo"],
    )
    salvar_modelo(
        modelo=passo_treinar.outputs["modelo"],
        acuracia=passo_avaliar.outputs["Output"],
        limiar_minimo=limiar_minimo,
    )


if __name__ == "__main__":
    OUT = "pipeline_mlops_pcdf.yaml"
    compiler.Compiler().compile(pipeline_mlops_pcdf, OUT)
    print(f"ok: pipeline compilada -> {OUT}")
    print(
        "\nPra rodar de verdade no cluster (depois do kubectl port-forward\n"
        "do Passo B4-3, ver LEIA-ME):\n\n"
        "    from kfp.client import Client\n"
        "    client = Client(host=\"http://localhost:8888\")\n"
        "    client.create_run_from_pipeline_package(\n"
        f"        \"{OUT}\", arguments={{}}, experiment_name=\"aula07-pcdf\"\n"
        "    )\n"
    )
