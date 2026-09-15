#!/usr/bin/env bash
# Aula 07 -- Passo B2-4 / Bloco 3: instala Prometheus + Grafana no cluster
# via Helm (kube-prometheus-stack, prometheus-community). Rode a partir de
# aula7_material/helm/.
set -euo pipefail

echo "== 1) Adicionar o repositório do chart =="
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

echo ""
echo "== 2) Instalar (usa os values customizados pro tamanho de um Kind local) =="
helm install kube-prom-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  -f values-kube-prometheus-stack.yaml \
  --wait --timeout 5m

echo ""
echo "== 3) Confirmar que os pods subiram =="
kubectl get pods -n monitoring

echo ""
echo "== 4) Abrir o Grafana (deixe rodando numa aba/terminal separado) =="
echo "kubectl port-forward -n monitoring svc/kube-prom-stack-grafana 3000:80"
echo "Depois acesse http://localhost:3000  (usuário: admin / senha: aula07admin)"
