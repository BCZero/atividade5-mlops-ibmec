# 🚀 Atividade 5 - MLOps & CI/CD

**Disciplina**: MLOps & CI/CD  
**Instituição**: IBMEC  
**Aluno/Grupo**: Grupo 4 - IBMEC (Bruno Cesar Sampaio Ribeiro de Assis)  
**Repositório principal**: [BCZero/ml-ops-grupo-4-ibmec](https://github.com/BCZero/ml-ops-grupo-4-ibmec)  
**Repositório desta atividade**: [BCZero/atividade5-mlops-ibmec](https://github.com/BCZero/atividade5-mlops-ibmec)

---

## 📌 Visão Geral e Objetivos

Esta atividade reproduz e valida na prática o pipeline de MLOps e CI/CD conforme o roteiro da **Aula 07**:

1. **Containerização de Modelo ML com Docker**: Build multi-stage, usuário não-root `mlops` (uid 1000), execução isolada e cálculo de métricas de acurácia.
2. **Orquestração de Kubernetes Local com Kind**: Cluster multinó com 1 *control-plane* e 1 *worker* (`aula07-mlops`).
3. **Provisionamento de Infraestrutura como Código via Terraform**: Criação do Namespace Kubernetes `mlops`, Secret `app-credentials` e ConfigMap `app-config`.
4. **Deploy e Escalonamento no Kubernetes**: Deployment `demo-nginx` com 3 réplicas escaladas dinamicamente em modo distribuído.
5. **Reavaliação de Modelo (Item H Opcional)**: Retreino com dataset alterado `v2`, demonstrando degradação determinística de acurácia de **91.67%** para **35.29%**.

---

## 📊 Tabela de Status das Atividades

| Item | Descrição | Status | Resultado Alcançado |
| :---: | :--- | :---: | :--- |
| **A** | Criar repositório de teste + `git init` + commit inicial | ✅ **CONCLUÍDO** | Repositório estruturado e versionado. Log em `evidencias/logs/item_A_git_init.log`. |
| **B** | Colocar os dados do material no repositório | ✅ **CONCLUÍDO** | Datasets de treino colocados em `docker/data/` e `dados_grupo4/`. Log em `evidencias/logs/item_B_dados.log`. |
| **C** | Criar imagem Docker (`aula7-mlops-pcdf:local`) | ✅ **CONCLUÍDO** | Build multi-stage `python:3.11-slim` concluído com sucesso. |
| **D** | Executar imagem Docker e verificar resultado | ✅ **CONCLUÍDO** | Modelo DecisionTree treinado. **Acurácia de 91.67%**. Log em `evidencias/logs/docker_run_metricas.log`. |
| **E** | Instalar Kind e criar cluster Kubernetes local | ✅ **CONCLUÍDO** | Cluster `aula07-mlops` ativo com 2 nós (`control-plane` + `worker`) em estado `Ready`. |
| **F** | Rodar Terraform no Kubernetes local | ✅ **CONCLUÍDO** | Provider `hashicorp/kubernetes` aplicou Namespace `mlops`, Secret e ConfigMap. |
| **G** | Deploy de exemplo e escalonamento de réplicas | ✅ **CONCLUÍDO** | Deployment `demo-nginx` aplicado e escalado para **3 réplicas em status `Running`**. |
| **H** | *(Opcional)* Retreino com dataset alterado (`v2`) | ✅ **CONCLUÍDO** | Imagem `aula7-mlops-pcdf:v2` executada. **Acurácia caiu para 35.29%**. Log em `evidencias/logs/docker_run_v2_metricas.log`. |

---

## 🏆 Resultados Alcançados

### 1. Treinamento do Modelo com Dados Originais (Item D)
* **Dataset**: `docker/data/bos_sinteticos.csv` (40 linhas).
* **Treino/Teste**: 28 linhas de treino / 12 linhas de teste.
* **Acurácia**: **91.67%**
* **Importância das Features**:
  - `natureza`: 0.67
  - `bairro`: 0.33
  - `turno`: 0.00
* **Log de Evidência**: `evidencias/logs/docker_run_metricas.log`

### 2. Infraestrutura Kubernetes & Terraform (Itens E, F e G)
* **Cluster Kind**: `aula07-mlops` (1 control-plane, 1 worker).
* **Terraform**: Criou o namespace `mlops` e injetou as configurações via ConfigMap (`LIMIAR_MINIMO_ACURACIA = 0.60`).
* **Deploy Nginx**: 3 Pods rodando em modo distribuído no worker do Kind:
  ```text
  NAME                          READY   STATUS    NODE
  demo-nginx-6776488fbc-96lzs   1/1     Running   aula07-mlops-worker
  demo-nginx-6776488fbc-l5dzf   1/1     Running   aula07-mlops-worker
  demo-nginx-6776488fbc-s2w62   1/1     Running   aula07-mlops-worker
  ```

### 3. Comparativo de Retreino com Novo Lote / Ruído (Item H Opcional)
Ao retreinar a imagem Docker com o dataset estendido e com ruído `bos_sinteticos_v2.csv` (55 linhas):
* **Dataset**: `retreino/bos_sinteticos_v2.csv` (55 linhas).
* **Treino/Teste**: 38 linhas de treino / 17 linhas de teste.
* **Acurácia**: **35.29%** (Queda acentuada em relação aos 91.67% iniciais).
* **Conclusão MLOps**: A degradação da acurácia para 35.29% (ficando abaixo do limiar de 60% definido no ConfigMap `LIMIAR_MINIMO_ACURACIA`) demonstra a eficácia do pipeline automatizado em detectar queda de performance de modelos expostos a novas distribuições de dados antes de qualquer eventual promoção em produção.
* **Log de Evidência**: `evidencias/logs/docker_run_v2_metricas.log`

---

## 📂 Estrutura do Repositório

```text
atividade5-mlops-ibmec/
├── .github/
│   └── workflows/          ← Workflow de CI/CD GitHub Actions
├── docker/
│   ├── Dockerfile          ← Multi-stage build (python:3.11-slim, usuario mlops uid 1000)
│   ├── requirements.txt    ← scikit-learn, pandas, numpy
│   ├── treino_ml_rapido.py ← Script de treino DecisionTreeClassifier
│   └── data/
│       └── bos_sinteticos.csv ← Dataset sintético principal (40 linhas)
├── kind/
│   ├── kind-config.yaml    ← Configuração do cluster Kind (1 control-plane + 1 worker)
│   └── deployment_exemplo.yaml ← Deployment demo-nginx + Service + Ingress
├── terraform/
│   ├── providers.tf        ← Configuração do provider Kubernetes (context: kind-aula07-mlops)
│   ├── main.tf             ← Namespace mlops + Secret app-credentials + ConfigMap app-config
│   └── outputs.tf          ← Outputs do Terraform
├── retreino/
│   ├── bos_sinteticos_v2.csv ← Dataset de teste com ruído/novas linhas (55 linhas)
│   └── comparar_metricas.py ← Script comparador
├── dados_grupo4/           ← Datasets de apoio do Grupo 4
├── evidencias/
│   └── logs/
│       ├── item_A_git_init.log
│       ├── item_B_dados.log
│       ├── docker_run_metricas.log   ← Log do container original (91.67%)
│       └── docker_run_v2_metricas.log← Log do retreino v2 (35.29%)
├── PLANO_ATIVIDADE_5.md    ← Documento completo de plano e handoff
└── README.md               ← Documentação principal do repositório
```

---

## 🛠️ Comandos de Execução

```powershell
# 1. Build e Execução Docker
cd docker
docker build -t aula7-mlops-pcdf:local .
docker run --rm aula7-mlops-pcdf:local

# 2. Criar cluster Kind multinó
cd ../
kind create cluster --name aula07-mlops --config kind/kind-config.yaml
kubectl get nodes

# 3. Aplicar infraestrutura via Terraform
cd terraform
terraform init
terraform apply -auto-approve

# 4. Deploy da aplicação e escalonamento de réplicas
cd ../
kubectl apply -f kind/deployment_exemplo.yaml
kubectl scale deployment/demo-nginx -n mlops --replicas=3
kubectl get pods -n mlops -o wide
```
