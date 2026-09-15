#!/usr/bin/env python3
"""
Aula 07 -- Bloco 4, fecho do demo de retreino/governanca: busca os últimos
N runs do experimento "aula07-pcdf-ci" na API do Kubeflow e imprime uma
tabela comparando as métricas logadas (acuracia/precisao/revocacao) de
cada um -- é a prova visual de que o CI/CD/CT está retreinando e
REGISTRANDO cada execução (governança = conseguir responder "qual modelo
está rodando, com qual dado, com qual métrica" a qualquer momento).

Uso (depois do kubectl port-forward -n kubeflow svc/ml-pipeline 8888:8888):
    python3 comparar_metricas.py [quantidade_de_runs]
"""
import sys

from kfp.client import Client

KFP_HOST = "http://localhost:8888"
EXPERIMENT = "aula07-pcdf-ci"


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5

    client = Client(host=KFP_HOST)
    experimento = client.get_experiment(experiment_name=EXPERIMENT)
    runs = client.list_runs(
        experiment_id=experimento.experiment_id,
        page_size=n,
        sort_by="created_at desc",
    )

    if not runs.runs:
        print(f"nenhum run encontrado no experimento '{EXPERIMENT}' ainda.")
        return

    print(f"{'run':<28} {'criado em':<20} {'estado':<12}")
    print("-" * 62)
    for run in runs.runs:
        criado = run.created_at.strftime("%Y-%m-%d %H:%M:%S") if run.created_at else "?"
        print(f"{run.display_name:<28} {criado:<20} {run.state:<12}")

    print(
        "\nPra ver as métricas (acuracia/precisao/revocacao) de cada run em "
        "detalhe, abra o run no Kubeflow UI -- clique no nó 'avaliar' do "
        "grafo e veja a aba 'Visualizations'/'Metrics'."
    )


if __name__ == "__main__":
    main()
