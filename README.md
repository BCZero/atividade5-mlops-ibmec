# Atividade 5 - MLOps & CI/CD

**Disciplina**: MLOps & CI/CD  
**Aluno/Grupo**: Grupo 4 - IBMEC  
**Repositório principal**: https://github.com/BCZero/ml-ops-grupo-4-ibmec

## Objetivo

Reproduzir o processo completo apresentado na Aula 07:

| Item | Descrição | Status |
|------|-----------|--------|
| A | Criar repositório de teste | ✅ |
| B | Colocar os dados do material no repositório | ✅ |
| C | Criar a imagem Docker (build) | ⬜ |
| D | Rodar a imagem Docker e verificar resultado | ⬜ |
| E | Instalar Kind e configurar contexto Kubernetes local | ⬜ |
| F | Rodar o Terraform | ⬜ |
| G | Fazer o Deploy de exemplo e verificar réplicas | ⬜ |
| H | (Opcional) Trocar dados / incluir erros para comparar métricas | ⬜ |

## Estrutura

```
Atividade_5/
  docker/               ← Dockerfile + treino_ml_rapido.py + dados
  kind/                 ← kind-config.yaml + deployment_exemplo.yaml
  terraform/            ← providers.tf + main.tf + outputs.tf
  helm/                 ← observabilidade (Prometheus/Grafana) - extra
  pipeline/             ← Kubeflow KFP - extra
  retreino/             ← datasets alterados para item H opcional
  extra-mlflow/         ← MLflow local - extra
  dados_grupo4/         ← dataset do Grupo 4 (ocorrencias_sinteticas.csv)
  evidencias/
    logs/               ← saídas de terminal salvas
    prints/             ← capturas de tela
  relatorio/            ← PDF final
```

## Ordem de execução

```bash
# 1. Build e run da imagem Docker
cd docker
docker build -t aula7-mlops-pcdf:local .
docker run --rm aula7-mlops-pcdf:local

# 2. Criar cluster Kind
cd ../kind
kind create cluster --name aula07-mlops --config kind-config.yaml
kubectl get nodes

# 3. Terraform (namespace + secret + configmap)
cd ../terraform
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
terraform output

# 4. Deploy de exemplo + escalar réplicas
kubectl apply -f ../kind/deployment_exemplo.yaml
kubectl get pods -n mlops
kubectl scale deployment/demo-nginx -n mlops --replicas=3
kubectl get pods -n mlops -w
```

## Notas importantes

- O `providers.tf` usa `config_context = "kind-aula07-mlops"` (correto — Kind prefixa `kind-`)
- O `docker build` deve rodar de dentro da pasta `docker/` (o Dockerfile depende da subpasta `data/`)
- Evidências (logs e prints) são salvas em `evidencias/`
