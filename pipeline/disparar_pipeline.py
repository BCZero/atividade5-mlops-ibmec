#!/usr/bin/env python3
"""
Aula 07 -- chamado pelo ci-cd-mlops.yml (job "treinar-e-avaliar") depois
do kubectl port-forward já estar de pé. Compila a pipeline (garante que
está usando a MESMA imagem que acabou de ser buildada/pushada neste run) e
dispara uma execução real no cluster via a API do Kubeflow Pipelines.

Sai com código != 0 se a execução falhar (ex.: acuracia abaixo do limiar
no gate de salvar_modelo) -- assim o job do GitHub Actions também fica
vermelho, refletindo a falha de governança no próprio CI/CD/CT.
"""
import sys
import time

from kfp import compiler
from kfp.client import Client

from pipeline_kfp_mlops import pipeline_mlops_pcdf

IR_PATH = "pipeline_mlops_pcdf.yaml"
KFP_HOST = "http://localhost:8888"  # via kubectl port-forward -n kubeflow svc/ml-pipeline 8888:8888
EXPERIMENT = "aula07-pcdf-ci"
TIMEOUT_SEGUNDOS = 600


def main() -> int:
    compiler.Compiler().compile(pipeline_mlops_pcdf, IR_PATH)
    print(f"pipeline compilada -> {IR_PATH}")

    client = Client(host=KFP_HOST)

    run = client.create_run_from_pipeline_package(
        IR_PATH,
        arguments={},
        experiment_name=EXPERIMENT,
        run_name=f"ci-run-{int(time.time())}",
    )
    print(f"run disparado: id={run.run_id}")
    print(f"acompanhe em: {KFP_HOST}/#/runs/details/{run.run_id}")

    resultado = run.wait_for_run_completion(timeout=TIMEOUT_SEGUNDOS)
    estado = resultado.state
    print(f"estado final do run: {estado}")

    if estado != "SUCCEEDED":
        print("FALHA: o run não terminou com SUCCEEDED -- ver logs no Kubeflow UI.")
        return 1

    print("ok: run concluído com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
