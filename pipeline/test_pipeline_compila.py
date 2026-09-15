#!/usr/bin/env python3
"""Teste de CI (job "testar" do ci-cd-mlops.yml) -- garante que a pipeline
ainda compila (pega erro de sintaxe/assinatura ANTES de gastar tempo
buildando a imagem e disparando um run de verdade no cluster)."""
import os

from kfp import compiler

from pipeline_kfp_mlops import pipeline_mlops_pcdf

ESPERADOS = {"extrair", "limpar", "treinar", "avaliar", "salvar-modelo"}


def test_pipeline_compila(tmp_path):
    saida = tmp_path / "pipeline.yaml"
    compiler.Compiler().compile(pipeline_mlops_pcdf, str(saida))
    assert saida.exists()
    assert os.path.getsize(saida) > 0


def test_pipeline_tem_os_5_componentes(tmp_path):
    import yaml

    saida = tmp_path / "pipeline.yaml"
    compiler.Compiler().compile(pipeline_mlops_pcdf, str(saida))
    with open(saida) as f:
        ir = yaml.safe_load(f)
    tarefas = set(ir["root"]["dag"]["tasks"].keys())
    assert tarefas == ESPERADOS, f"esperado {ESPERADOS}, veio {tarefas}"
