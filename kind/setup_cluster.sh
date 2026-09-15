#!/usr/bin/env bash
# Aula 07 -- Passo B2-1: sobe o cluster Kind e confirma que o kubectl
# enxerga ele. Rode a partir da pasta aula7_material/kind/.
set -euo pipefail

echo "== 1) Criando o cluster (1 control-plane + 1 worker) =="
kind create cluster --name aula07-mlops --config kind-config.yaml

echo ""
echo "== 2) Confirmando o contexto do kubectl =="
kubectl config current-context
# esperado: kind-aula07-mlops -- é o MESMO nome que providers.tf usa em
# config_context (Kind sempre prefixa "kind-" no nome do cluster).

echo ""
echo "== 3) Confirmando os nós =="
kubectl get nodes -o wide

echo ""
echo "ok: cluster de pé. Próximo passo: terraform init/apply (Passo B2-2)."
