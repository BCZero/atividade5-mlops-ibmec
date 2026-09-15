# Plano de Implementacao - Atividade 5

Disciplina: MLOps & CI/CD  
Atividade: Atividade 5 - 25 pontos  
Repositorio desta atividade: `https://github.com/BCZero/atividade5-mlops-ibmec`  
Repositorio do grupo: `https://github.com/BCZero/ml-ops-grupo-4-ibmec`  
Ultima revisao: 2026-09-15 19:17 (handoff para computador pessoal)

---

## HANDOFF — Ponto de Parada e Proximo Passo

> **Resumo**: o projeto foi configurado no computador do MBA e enviado para o
> GitHub. A continuacao deve ser feita no **computador pessoal**, que tem Docker
> funcionando. Clone o repositorio e siga a partir do Item C.

### O que ja foi feito (computador MBA)

| Item | Descricao | Status |
|------|-----------|--------|
| A | Criar repositorio de teste + `git init` + commit inicial | ✅ CONCLUIDO |
| B | Dados do material colocados no repositorio | ✅ CONCLUIDO |
| C | Docker build da imagem | ⛔ Nao executado (Docker Desktop com falha) |
| D | Rodar imagem Docker | ⛔ Nao executado |
| E | Kind instalado (v0.29.0) / cluster nao criado | 🔧 Kind OK, cluster pendente |
| F | Rodar Terraform | ⏳ PENDENTE |
| G | Deploy + replicas | ⏳ PENDENTE |
| H | Opcional com dados alterados | ⏳ PENDENTE |

### O que esta pronto no repositorio

```text
Atividade_5/
  docker/
    Dockerfile              <- multi-stage python:3.11-slim, usuario mlops
    treino_ml_rapido.py     <- script de treino (DecisionTreeClassifier)
    requirements.txt
    data/bos_sinteticos.csv <- 40 linhas, dataset principal da Aula 07
  kind/
    kind-config.yaml        <- cluster "aula07-mlops" (1 control-plane + 1 worker)
    deployment_exemplo.yaml <- Deployment demo-nginx + Service
    setup_cluster.sh
  terraform/
    providers.tf            <- BUG JA CORRIGIDO: config_context = "kind-aula07-mlops"
    main.tf                 <- namespace mlops + secret + configmap
    outputs.tf
  retreino/
    bos_sinteticos_v2.csv   <- 55 linhas, para o item H (derruba acuracia p/ 35.29%)
    bos_sinteticos_ruido.csv
    comparar_metricas.py
    novos_bos_lote2.csv
    gerar_dado_ruidoso.py
  dados_grupo4/
    ocorrencias_sinteticas_grupo4.csv  <- dataset do Grupo 4
    bos_sinteticos_aula05.csv
    bos_sinteticos_sujo_aula05.csv
  evidencias/
    logs/item_A_git_init.log
    logs/item_B_dados.log
  README.md
  PLANO_ATIVIDADE_5.md      <- este arquivo
```

### Como continuar no computador pessoal

```bash
# 1. Clonar o repositorio
git clone https://github.com/BCZero/atividade5-mlops-ibmec.git
cd atividade5-mlops-ibmec

# 2. Validar que Docker esta rodando
docker run --rm hello-world

# 3. ITEM C — Build da imagem (EXECUTAR DENTRO DE docker/)
cd docker
docker build -t aula7-mlops-pcdf:local .
docker images aula7-mlops-pcdf

# 4. ITEM D — Rodar e salvar saida
docker run --rm aula7-mlops-pcdf:local | tee ../evidencias/logs/docker_run_metricas.log
# Saida esperada: acuracia ~91.67% com o dataset de 40 linhas

# 5. ITEM E — Criar cluster Kind (Kind precisa estar instalado)
cd ..
kind create cluster --name aula07-mlops --config kind/kind-config.yaml
kubectl config current-context   # deve retornar: kind-aula07-mlops
kubectl get nodes                # control-plane + worker em Ready

# 6. ITEM F — Rodar Terraform
cd terraform
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
terraform output
kubectl get namespace mlops
kubectl get secret -n mlops
kubectl get configmap -n mlops

# 7. ITEM G — Deploy de exemplo e escalar replicas
cd ..
kubectl apply -f kind/deployment_exemplo.yaml
kubectl get pods -n mlops
kubectl scale deployment/demo-nginx -n mlops --replicas=3
kubectl get pods -n mlops -o wide
# Aguardar todos os pods em Running e salvar evidencia

# 8. ITEM H (Opcional) — Rebuild com dados alterados
cp retreino/bos_sinteticos_v2.csv docker/data/bos_sinteticos.csv
cd docker
docker build -t aula7-mlops-pcdf:v2 .
docker run --rm aula7-mlops-pcdf:v2 | tee ../evidencias/logs/docker_run_v2_metricas.log
# Saida esperada: acuracia ~35.29% (abaixo do limiar de 60%)

# 9. Fazer commit das evidencias e push
cd ..
git add evidencias/
git commit -m "feat: evidencias C-G (docker build/run, kind, terraform, deploy)"
git push
```

### Atencao: instalacao do Kind no computador pessoal

Se o Kind nao estiver instalado:

```bash
# Linux/WSL2:
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind
kind version

# macOS:
brew install kind

# Windows (PowerShell como admin):
# Baixar de https://kind.sigs.k8s.io/dl/v0.29.0/kind-windows-amd64 e colocar no PATH
```

---

## Status de Execucao

| Item | Descricao | Status |
|------|-----------|--------|
| A | Criar repositorio de teste | ✅ CONCLUIDO |
| B | Colocar os dados no repositorio | ✅ CONCLUIDO |
| C | Docker build da imagem | ⛔ PENDENTE (computador pessoal) |
| D | Rodar imagem Docker | ⛔ PENDENTE (computador pessoal) |
| E | Kind instalado / cluster pendente | 🔧 PARCIAL |
| F | Rodar Terraform | ⏳ PENDENTE |
| G | Deploy + replicas | ⏳ PENDENTE |
| H | Opcional com dados alterados | ⏳ PENDENTE |

### Ferramentas no computador MBA (para referencia)

| Ferramenta | Versao |
|------------|--------|
| Docker client | 29.8.0 (Desktop com falha no daemon) |
| Kind | v0.29.0 |
| kubectl | v1.36.1 |
| Terraform | v1.15.8 |

## Status de Execucao

| Item | Descricao | Status |
|------|-----------|--------|
| A | Criar repositorio de teste | ✅ CONCLUIDO |
| B | Colocar os dados no repositorio | ✅ CONCLUIDO |
| C | Docker build da imagem | ⛔ BLOQUEADO |
| D | Rodar imagem Docker | ⛔ BLOQUEADO |
| E | Kind instalado / cluster pendente | 🔧 PARCIAL |
| F | Rodar Terraform | ⏳ PENDENTE |
| G | Deploy + replicas | ⏳ PENDENTE |
| H | Opcional com dados alterados | ⏳ PENDENTE |

**Bloqueador atual**: Docker Desktop retorna `Docker Desktop is unable to start`.
Solucao documentada na Secao 12.

### O que ja foi executado

- `Atividade_5/` criada com estrutura completa (31 arquivos, commit `7d50d6d`).
- Bug `providers.tf` corrigido: `kd3-aula07-mlops` → `kind-aula07-mlops`.
- Kind v0.29.0 instalado no Windows via binario oficial.
- Evidencias A e B salvas em `Atividade_5/evidencias/logs/`.

### Ferramentas disponiveis no Windows

| Ferramenta | Versao | Origem |
|------------|--------|--------|
| Docker client | 29.8.0 | Docker Desktop |
| Kind | v0.29.0 | Instalado via binario oficial |
| kubectl | v1.36.1 | Windows PATH |
| Terraform | v1.15.8 | Windows PATH |
| Git | — | Windows PATH |

## 1. Correcao de escopo desta analise

A analise correta da Atividade 5 deve partir da pasta:

```text
C:\Users\17212677\Documents\MBA\MLOps_atividade_2
```

Essa pasta contem mais materiais do que o repositorio enxuto usado para a Entrega
3. Ela inclui as entregas anteriores, as Aulas 05, 06 e 07, o material alterado
da Aula 05 e um `providers.tf` solto que pertence ao Terraform didatico da Aula
07.

## 2. Materiais encontrados

### 2.1 Entregas ja feitas

```text
Entrega_atividade_2_individual/
  README_ATIVIDADE_2.md
  STATUS_ATIVIDADE_2.md
  logs/
  evidencias/
  terraform-exemplos/
  relatorio/
    Relatorio_Atividade2_Bruno_Cesar_Sampaio_Ribeiro_de_Assis.pdf

Entrega_3_Grupo4/
  Relatorio_Entrega3_Grupo4_FINAL.pdf
  Relatorio_Entrega3_Grupo4_FINAL.md
  prompt_criacao_dados.md
  evidencias_terraform_cloud_shell.md
  pcdf-tipificacao-procedimentos/
    README.md
    data/ocorrencias_sinteticas.csv
    terraform/main.tf
```

A Entrega da Atividade 2 ja tem evidencias de ambiente, exemplos de ML e
Terraform locais. A Entrega 3 ja tem dataset do grupo, estrutura de projeto e
Terraform Azure.

### 2.2 Aulas e materiais disponiveis

```text
Aula 05/
  Slides - Aula 05.pptx
  Manual - Aula 05.docx
  Material Aula 05.zip

Zip Aula 05 alterado/Material Aula 05/
  LEIA-ME.txt
  bos_sinteticos.csv
  bos_sinteticos_sujo.csv
  dag_ingestao_bo.py
  docker-compose.override.yml
  gerar_dados_sujos.py
  PROMPT_gerar_dados_sujos.txt
  pipeline_kfp_exemplo.py
  pipeline_bos_pcdf.yaml
  treino_ml_rapido.py
  requirements_aula5.txt

Aula 06/
  Slides - Aula 06.pptx
  Manual - Aula 06.docx
  Material Aula 06.zip

Aula 07/
  Slides - Aula 07.pptx
  Manual - Aula 07.docx
  Material Aula 07.zip

providers.tf
```

### 2.3 Conteudo confirmado do Material Aula 07 (verificado apos extracao)

O arquivo `Aula 07/Aula 07/Material Aula 07.zip` foi extraido para:

```text
Aula 07/Aula 07/Material_Aula_07_extraido/Material Aula 07/
```

Conteudo verificado em disco:

```text
Material Aula 07/
  LEIA-ME.txt
  docker/
    Dockerfile          <- multi-stage, python:3.11-slim, usuario mlops
    .dockerignore
    requirements.txt
    treino_ml_rapido.py <- script de treino (accuracy_score apenas, sem precision/recall)
    data/
      bos_sinteticos.csv

  kind/
    setup_cluster.sh
    kind-config.yaml    <- cluster "aula07-mlops", 1 control-plane + 1 worker
    deployment_exemplo.yaml <- Deployment demo-nginx + Service + Ingress (referencia)

  terraform/
    providers.tf        <- ATENCAO: contem typo "kd3-aula07-mlops" (ver Secao 6.6)
    main.tf             <- namespace mlops + secret app-credentials + configmap app-config
    outputs.tf

  helm/
    instalar_observabilidade.sh
    values-kube-prometheus-stack.yaml
    prometheusrule_exemplo.yaml

  pipeline/
    requirements-dev.txt
    pipeline_kfp_mlops.py
    pipeline_mlops_pcdf.yaml
    disparar_pipeline.py
    test_pipeline_compila.py

  retreino/
    novos_bos_lote2.csv
    bos_sinteticos_v2.csv   <- 55 linhas; derruba acuracia p/ 35.29% (ideal para item H)
    bos_sinteticos_ruido.csv
    gerar_dado_ruidoso.py
    comparar_metricas.py

  .github/workflows/
    ci-cd-mlops.yml

  extra-mlflow/
    requirements.txt
    registrar_run_mlflow.py
```

## 3. Interpretacao correta do enunciado

O enunciado da Atividade 5 pede:

```text
a - Criar repositorio de teste como mostrado (Slides)
b - Colocar os dados do material fornecido no repositorio
c - Criar a imagem do arquivo (build e Execucao)
d - Rodar a imagem docker e verificar o resultado
e - Instalar o Kind e configurar o contexto no Kubernets local
f - Rodar o Terraform seguindo os slides
g - Fazer o Deploy de exemplo e verificar as replicas subindo
h - Opcional: Troque o passo 6 pelos seus dados ou inclua erros nos dados
    originais para ver se a limpeza mudou algo ou se as metricas mudaram
```

Esse roteiro corresponde diretamente aos Blocos 1 e 2 da Aula 07:

- Bloco 1: Containerizacao com Docker.
- Bloco 2: Kubernetes local com Kind + Terraform.

O material de Aula 05 entra como suporte para dados sujos/limpeza/treino de ML.
O material de Aula 06 entra como base conceitual anterior de Kubeflow/GitHub
Actions. O material de Aula 07 e o principal para cumprir a Atividade 5.

## 4. Estado atual reaproveitavel

### 4.1 Podemos reaproveitar da Entrega da Atividade 2

- Evidencias de ambiente local.
- Docker instalado e ja usado em exemplo Terraform Docker.
- Terraform instalado e ja usado.
- Logs de ML e Terraform locais.

### 4.2 Podemos reaproveitar da Entrega 3

- Repositorio GitHub principal: `https://github.com/BCZero/ml-ops-grupo-4-ibmec`.
- Dataset do grupo:

```text
Entrega_3_Grupo4/pcdf-tipificacao-procedimentos/data/ocorrencias_sinteticas.csv
```

- Projeto guia e README.
- Experiencia previa com Terraform no Azure Cloud Shell.

### 4.3 Nao devemos confundir com a Atividade 5

O Terraform da Entrega 3 usa `azurerm` e cria recursos no Azure.  
O Terraform da Aula 07 usa `hashicorp/kubernetes` e cria recursos dentro de um
cluster Kind local.

Portanto, para a Atividade 5, o Terraform principal deve ser o da Aula 07:

```text
Material Aula 07/terraform/providers.tf
Material Aula 07/terraform/main.tf
Material Aula 07/terraform/outputs.tf
```

## 5. Decisao de organizacao

Criar uma nova pasta dedicada para a Atividade 5 dentro da pasta correta:

```text
C:\Users\17212677\Documents\MBA\MLOps_atividade_2\Atividade_5
```

Estrutura planejada:

```text
Atividade_5/
  README.md
  docker/
  kind/
  terraform/
  helm/
  pipeline/
  retreino/
  extra-mlflow/
  .github/workflows/
  dados_grupo4/
  evidencias/
    logs/
    prints/
  relatorio/
```

Essa estrutura segue o Cenario A do manual da Aula 07: repositorio de
demonstracao criado do zero ou area isolada de teste. Se depois decidirmos
implementar dentro do repositorio GitHub principal, copiamos essa pasta para o
repo e fazemos commit/push.

## 6. Plano de implementacao por item do enunciado

### 6.1 Item A - Criar repositorio de teste como mostrado nos slides

Base do material:

- Manual Aula 07, secao A0.
- `Material Aula 07/LEIA-ME.txt`.

Plano:

1. Criar pasta local de teste:

```powershell
mkdir Atividade_5
cd Atividade_5
git init
```

2. Copiar o material da Aula 07 para a raiz dessa pasta:

```text
docker/
kind/
terraform/
helm/
pipeline/
retreino/
extra-mlflow/
.github/workflows/ci-cd-mlops.yml
```

3. Criar `README.md` explicando que a pasta reproduz a Aula 07 para a Atividade
   5.
4. Fazer commit inicial.
5. Decidir se criaremos repositorio separado no GitHub ou se usaremos o
   repositorio principal do grupo.

Evidencias:

```powershell
git status -sb
git log --oneline -5
git remote -v
```

### 6.2 Item B - Colocar os dados do material fornecido no repositorio

Base do material:

```text
Material Aula 07/docker/data/bos_sinteticos.csv
Zip Aula 05 alterado/Material Aula 05/bos_sinteticos.csv
Zip Aula 05 alterado/Material Aula 05/bos_sinteticos_sujo.csv
```

Plano:

1. Manter o dataset da Aula 07 em:

```text
Atividade_5/docker/data/bos_sinteticos.csv
```

2. Copiar datasets auxiliares para comparacao:

```text
Atividade_5/dados_grupo4/bos_sinteticos_aula05.csv
Atividade_5/dados_grupo4/bos_sinteticos_sujo_aula05.csv
Atividade_5/dados_grupo4/ocorrencias_sinteticas_grupo4.csv
```

3. A copia do nosso dataset deve vir de:

```text
Entrega_3_Grupo4/pcdf-tipificacao-procedimentos/data/ocorrencias_sinteticas.csv
```

Evidencias:

```powershell
Get-ChildItem -Recurse Atividade_5\docker\data
Get-ChildItem -Recurse Atividade_5\dados_grupo4
Get-Content Atividade_5\docker\data\bos_sinteticos.csv -TotalCount 5
```

### 6.3 Item C - Criar a imagem do arquivo: build e execucao

Base do material:

```text
Material Aula 07/docker/Dockerfile
Material Aula 07/docker/requirements.txt
Material Aula 07/docker/treino_ml_rapido.py
Material Aula 07/docker/data/bos_sinteticos.csv
```

O Dockerfile confirmado no material (arquivo lido e verificado):

- usa `python:3.11-slim` em build multi-stage (estagio `builder` + estagio final);
- instala dependencias com `pip install --user --no-cache-dir` no stage `builder`;
- copia `/root/.local` do builder para `/home/mlops/.local` no final;
- cria usuario nao-root `mlops` (uid 1000);
- copia `data/bos_sinteticos.csv` para `/app/data/bos_sinteticos.csv`;
- copia `treino_ml_rapido.py` para `/app/treino_ml_rapido.py`;
- usa `ENTRYPOINT ["python", "treino_ml_rapido.py"]`;
- usa `CMD ["data/bos_sinteticos.csv"]`;
- define `ENV PYTHONUNBUFFERED=1` para saida de log em tempo real.

> **Atencao**: o build DEVE ser executado de dentro da pasta `docker/` (context `.`),
> pois o `COPY data/bos_sinteticos.csv` depende da subpasta `data/` relativa ao context.

Plano:

```powershell
cd Atividade_5\docker
docker build -t aula7-mlops-pcdf:local .
docker images aula7-mlops-pcdf
```

Evidencias:

- log do `docker build` sem erro;
- imagem aparecendo em `docker images`.

### 6.4 Item D - Rodar a imagem Docker e verificar o resultado

Plano:

```powershell
cd Atividade_5\docker
docker run --rm aula7-mlops-pcdf:local
```

Resultado esperado (verificado no codigo-fonte do `treino_ml_rapido.py`):

- o container executa `treino_ml_rapido.py`;
- imprime numero de linhas carregadas;
- imprime tamanho de treino e teste;
- imprime **acuracia** (accuracy_score) — o script nao calcula precision/recall;
- imprime importancia de cada feature (natureza, bairro, turno);
- imprime aviso sobre dataset ficticio.

Exemplo de saida esperada com `bos_sinteticos.csv` (40 linhas, acuracia ~91.67%):

```text
Dados carregados de data/bos_sinteticos.csv: 40 linhas
Linhas de treino: 28 | teste: 12
Acuracia no conjunto de teste: 91.67%
Importancia de cada feature (quanto o modelo usou cada uma):
  natureza: 0.XX
  bairro: 0.XX
  turno: 0.XX
Aviso: dataset ficticio e pequeno demais para conclusoes reais ...
```

Evidencias:

```powershell
docker run --rm aula7-mlops-pcdf:local
```

Salvar saida em:

```text
Atividade_5/evidencias/logs/docker_run_metricas.log
```

### 6.5 Item E - Instalar o Kind e configurar o contexto no Kubernetes local

Base do material:

```text
Material Aula 07/kind/kind-config.yaml
Material Aula 07/kind/setup_cluster.sh
```

O `kind-config.yaml` cria:

- 1 control-plane;
- 1 worker;
- cluster chamado `aula07-mlops`.

Plano:

```powershell
kind version
docker ps
cd Atividade_5\kind
kind create cluster --name aula07-mlops --config kind-config.yaml
kubectl config current-context
kubectl get nodes
```

Resultado esperado:

```text
kind-aula07-mlops
```

E nodes parecidos com:

```text
aula07-mlops-control-plane   Ready
aula07-mlops-worker          Ready
```

Evidencias:

- `kind version`;
- `kind create cluster`;
- `kubectl config current-context`;
- `kubectl get nodes`.

### 6.6 Item F - Rodar o Terraform seguindo os slides

Base do material:

```text
Material Aula 07/terraform/providers.tf
Material Aula 07/terraform/main.tf
Material Aula 07/terraform/outputs.tf
providers.tf solto na raiz de MLOps_atividade_2
```

Atencao importante -- BUG CONFIRMADO no ZIP:

O arquivo `terraform/providers.tf` dentro do ZIP tem um **typo confirmado**:

```hcl
# ERRADO (como esta no ZIP):
config_context = "kd3-aula07-mlops"

# CORRETO (como deve ficar em Atividade_5/terraform/providers.tf):
config_context = "kind-aula07-mlops"
```

O `providers.tf` solto na raiz do projeto (`C:\...\MLOps_atividade_2\providers.tf`) ja
esta **correto** com `kind-aula07-mlops` e pode ser usado como referencia ou copiado
diretamente.

O Kind sempre prefixa `kind-` no nome do contexto ao criar o cluster. O nome correto e
obrigatoriamente:

```text
kind-aula07-mlops
```

Portanto, ao copiar o terraform do ZIP para `Atividade_5/terraform/`, corrija o
`providers.tf` ANTES de rodar `terraform init`.

O Terraform da Aula 07 cria:

- namespace `mlops`;
- secret `app-credentials`;
- configmap `app-config`.

Plano:

```powershell
cd Atividade_5\terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply -auto-approve
terraform output
kubectl get namespace mlops
kubectl get secret -n mlops
kubectl get configmap -n mlops
```

Evidencias:

- provider `hashicorp/kubernetes` inicializado;
- `terraform validate` com sucesso;
- `terraform apply` criando namespace/secret/configmap;
- `kubectl` confirmando recursos no namespace `mlops`.

### 6.7 Item G - Fazer o Deploy de exemplo e verificar replicas subindo

Base do material:

```text
Material Aula 07/kind/deployment_exemplo.yaml
```

Esse manifesto contem:

- Deployment `demo-nginx` no namespace `mlops`;
- imagem `nginx:1.27-alpine`;
- `replicas: 2` inicialmente;
- Service `demo-nginx`;
- Ingress apenas como referencia de sintaxe.

Plano:

```powershell
kubectl apply -f Atividade_5\kind\deployment_exemplo.yaml
kubectl get pods -n mlops
kubectl get deployments -n mlops
kubectl get svc -n mlops
kubectl scale deployment/demo-nginx -n mlops --replicas=3
kubectl get pods -n mlops -w
```

Resultado esperado:

- Deployment `demo-nginx` criado;
- 2 pods iniciais em `Running`;
- apos scale, 3 replicas em `Running`;
- Service `demo-nginx` criado.

Evidencias:

- `kubectl get deployments -n mlops` mostrando `READY 3/3`;
- `kubectl get pods -n mlops -o wide` mostrando pods em `Running`;
- print/log do momento em que as replicas sobem.

### 6.8 Item H - Opcional com nossos dados ou dados com erro

Base do material:

```text
Zip Aula 05 alterado/Material Aula 05/bos_sinteticos_sujo.csv
Zip Aula 05 alterado/Material Aula 05/gerar_dados_sujos.py
Zip Aula 05 alterado/Material Aula 05/PROMPT_gerar_dados_sujos.txt
Material Aula 07/retreino/bos_sinteticos_v2.csv
Material Aula 07/retreino/bos_sinteticos_ruido.csv
Material Aula 07/retreino/comparar_metricas.py
Entrega_3_Grupo4/pcdf-tipificacao-procedimentos/data/ocorrencias_sinteticas.csv
```

Opcoes (em ordem de complexidade crescente):

1. **Mais recomendado**: Usar `bos_sinteticos_v2.csv` (55 linhas) — resultado
   **deterministico e documentado**: acuracia CAI de 91.67% para 35.29%, abaixo
   do limiar de 60%. Isso demonstra claramente que dado de qualidade melhor revelou
   vies no modelo antigo. Ideal para o relatorio.
2. Usar `bos_sinteticos_ruido.csv` — embaralha rotulos aleatoriamente; resultado
   **nao e deterministico** (dataset pequeno), nao recomendado para demo ao vivo.
3. Usar o dataset sujo da Aula 05 (`bos_sinteticos_sujo.csv`) e comparar limpeza.
4. Usar nosso dataset da Entrega 3 — requer adaptacao do script (schema diferente).

Plano recomendado:

- Primeiro cumprir os itens A-G exatamente com os dados oficiais da Aula 07.
- Depois fazer o opcional com `bos_sinteticos_v2.csv` (opcao 1 acima) — deterministico
  e ja no schema esperado pelo script, sem nenhuma adaptacao.
- So depois tentar o dataset do Grupo 4, pois tem colunas diferentes.

Comandos para opcional com `bos_sinteticos_v2.csv` (deterministico):

```powershell
# No WSL2:
cp Atividade_5/retreino/bos_sinteticos_v2.csv Atividade_5/docker/data/bos_sinteticos.csv
cd Atividade_5/docker
docker build -t aula7-mlops-pcdf:v2 .
docker run --rm aula7-mlops-pcdf:v2
# Resultado esperado: Acuracia no conjunto de teste: 35.29% (abaixo do limiar de 60%)
```

Comparar e salvar as duas saidas:

```text
docker run --rm aula7-mlops-pcdf:local  -> acuracia ~91.67% (dataset original)
docker run --rm aula7-mlops-pcdf:v2     -> acuracia ~35.29% (v2 com novos rotulos)
```

Evidencias:

- metricas com dataset original;
- metricas com dataset alterado/sujo;
- conclusao curta comparando mudanca nas metricas.

## 7. Observabilidade e CI/CD: usar ou nao usar na Atividade 5

O enunciado da Atividade 5 para esta entrega termina em deploy e replicas. Ele
nao exige explicitamente:

- Helm;
- Prometheus/Grafana;
- Kubeflow Pipelines standalone;
- self-hosted runner;
- GitHub Actions completo;
- MLflow.

Esses itens aparecem na Aula 07, mas parecem exceder o escopo minimo do
enunciado. Portanto:

- Implementar A-G primeiro.
- Fazer H opcional se houver tempo.
- Guardar Helm/Kubeflow/CI/CD/MLflow como extensao, nao como requisito inicial.

## 8. Evidencias minimas para o PDF final

1. Capa com identificacao do aluno/grupo, disciplina e Atividade 5.
2. Print/listagem do repositorio de teste criado.
3. Print/listagem dos dados copiados para o repositorio.
4. `docker build -t aula7-mlops-pcdf:local .` concluido.
5. `docker images` mostrando a imagem.
6. `docker run --rm aula7-mlops-pcdf:local` imprimindo metricas.
7. `kind version` e `kind create cluster --name aula07-mlops`.
8. `kubectl config current-context` mostrando `kind-aula07-mlops`.
9. `kubectl get nodes` mostrando control-plane e worker `Ready`.
10. `terraform init`, `terraform validate`, `terraform plan`, `terraform apply`.
11. `kubectl get namespace mlops`.
12. `kubectl get secret -n mlops` e `kubectl get configmap -n mlops`.
13. `kubectl apply -f kind/deployment_exemplo.yaml`.
14. `kubectl get deployments -n mlops`.
15. `kubectl scale deployment/demo-nginx -n mlops --replicas=3`.
16. `kubectl get pods -n mlops -o wide` mostrando replicas em `Running`.
17. Opcional: comparacao de metricas com dados alterados.

## 9. Ordem de trabalho recomendada

> **Ambiente atualizado**: toda a execucao sera feita no **PowerShell do Windows**,
> usando Docker Desktop (modo Linux containers), Kind para Windows e Terraform/kubectl
> nativos do Windows. O `~/.kube/config` e gerado automaticamente pelo Kind no perfil
> do usuario Windows (`%USERPROFILE%\.kube\config`).

1. **[✅ FEITO]** Extrair `Material Aula 07.zip`
   → Em `Aula 07/Aula 07/Material_Aula_07_extraido/Material Aula 07/`
2. **[✅ FEITO]** Criar `Atividade_5/` e inicializar como repositorio Git
   → Commit `7d50d6d` com 31 arquivos em `Atividade_5/`
3. **[✅ FEITO]** Copiar `docker/`, `kind/`, `terraform/`, `pipeline/`, `helm/`,
   `retreino/`, `extra-mlflow/` e `.github/` para `Atividade_5/`
4. **[✅ FEITO]** Corrigir `Atividade_5/terraform/providers.tf`
   → `kd3-aula07-mlops` substituido por `kind-aula07-mlops`
5. **[✅ FEITO]** Kind v0.29.0 instalado no Windows
6. **[⛔ BLOQUEADO]** Resolver Docker Desktop (ver Secao 12), depois:
   ```powershell
   cd Atividade_5\docker
   docker build -t aula7-mlops-pcdf:local .
   docker run --rm aula7-mlops-pcdf:local
   ```
7. **[PENDENTE]** Subir Kind cluster:
   ```powershell
   cd Atividade_5\kind
   kind create cluster --name aula07-mlops --config kind-config.yaml
   kubectl config current-context
   kubectl get nodes
   ```
8. **[PENDENTE]** Rodar Terraform:
   ```powershell
   cd Atividade_5\terraform
   terraform init
   terraform validate
   terraform plan
   terraform apply -auto-approve
   terraform output
   ```
9. **[PENDENTE]** Aplicar deploy e escalar replicas:
   ```powershell
   kubectl apply -f Atividade_5\kind\deployment_exemplo.yaml
   kubectl scale deployment/demo-nginx -n mlops --replicas=3
   kubectl get pods -n mlops -o wide
   ```
10. Salvar logs e prints em `Atividade_5\evidencias\`
11. Opcional Item H: rebuild com `bos_sinteticos_v2.csv`
12. Gerar relatorio PDF final

## 10. Riscos e cuidados

### 10.1 Docker no Windows x WSL2

O material da Aula 07 recomenda Docker Engine nativo no WSL2, nao Docker
Desktop. Como a maquina ja usou Docker Desktop antes, precisamos confirmar qual
ambiente sera usado para executar a atividade. O mais fiel ao manual e WSL2.

### 10.2 Kind depende do Docker funcionando

Antes de `kind create cluster`, validar:

```powershell
docker ps
```

Se der erro de daemon, iniciar Docker Desktop ou o Docker Engine do WSL2.

### 10.3 Contexto do Terraform Kubernetes

O erro mais provavel e o Terraform apontar para contexto errado. Validar antes:

```powershell
kubectl config current-context
```

O valor esperado e:

```text
kind-aula07-mlops
```

### 10.4 Secret didatico

O Terraform da Aula 07 cria um Secret com senha ficticia. Nao usar senha real e
nao colocar segredos reais em `.tf`.

### 10.5 Dataset do Grupo 4 tem schema diferente

Nosso CSV da Entrega 3 tem colunas de tipificacao criminal diferentes do
`bos_sinteticos.csv` da Aula 07. Para o opcional, ele so deve ser usado se
adaptarmos o script de treino ou criarmos um mapeamento de colunas.

## 11. Proximo passo imediato

**Itens A e B ja estao concluidos.** O unico bloqueador restante e o Docker Desktop.
Apos resolver (ver Secao 12), os proximos comandos sao:

```powershell
# Item C — Build da imagem (executar de dentro de docker/)
cd C:\Users\17212677\Documents\MBA\MLOps_atividade_2\Atividade_5\docker
docker build -t aula7-mlops-pcdf:local .
docker images aula7-mlops-pcdf

# Item D — Rodar e salvar saida
docker run --rm aula7-mlops-pcdf:local | Tee-Object -FilePath ..\.\evidencias\logs\docker_run_metricas.log

# Item E — Criar cluster Kind
cd ..
kind create cluster --name aula07-mlops --config kind\kind-config.yaml
kubectl config current-context   # esperado: kind-aula07-mlops
kubectl get nodes

# Item F — Terraform
cd terraform
terraform init
terraform validate
terraform plan
terraform apply -auto-approve
terraform output
kubectl get namespace mlops
kubectl get secret -n mlops
kubectl get configmap -n mlops

# Item G — Deploy e escala
kubectl apply -f ..\kind\deployment_exemplo.yaml
kubectl get pods -n mlops
kubectl scale deployment/demo-nginx -n mlops --replicas=3
kubectl get pods -n mlops -o wide
```

## 12. Diagnostico e Solucao do Docker Desktop

### 12.1 Erro observado

Ao tentar iniciar o Docker Desktop, o daemon retorna:

```text
Error response from daemon: Docker Desktop is unable to start
```

O Docker Desktop fica preso em "Engine starting" por minutos sem progredir.

### 12.2 Causas mais comuns e solucoes

**Tentativa 1 — Reinicio limpo (mais simples):**

```powershell
# 1. Clique com botao direito no icone do Docker na bandeja > Quit Docker Desktop
# 2. Aguarde 10s
# 3. Abra o Docker Desktop normalmente pelo menu Iniciar
# 4. Aguarde o icone ficar verde (pode levar 2-3 min)
docker run hello-world   # valida que esta funcionando
```

**Tentativa 2 — Reset do mecanismo WSL/HyperV:**

```powershell
# No PowerShell como Administrador:
wsl --shutdown
Start-Sleep 5
# Entao abrir o Docker Desktop normalmente
```

**Tentativa 3 — Reset para padroes de fabrica (perde containers/imagens locais):**

```text
Docker Desktop > Settings (engrenagem) > Troubleshoot > Reset to factory defaults
```

**Tentativa 4 — Reinstalar Docker Desktop:**

```text
Painel de Controle > Desinstalar > Instalar versao mais recente de
https://www.docker.com/products/docker-desktop/
```

### 12.3 Validacao apos recuperacao

```powershell
docker info
docker run --rm hello-world
kind version   # v0.29.0 (ja instalado)
```

### 12.4 Alternativa: usar Docker Engine dentro do WSL2

Se o Docker Desktop continuar falhando, e possivel usar Docker Engine nativo no
WSL2 (Ubuntu), que e inclusive o ambiente recomendado pelo LEIA-ME do material:

```bash
# Dentro do WSL2 (Ubuntu)
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
# Fechar e reabrir o terminal WSL2
docker run hello-world
```

Nesse caso, o Kind e o Terraform tambem precisam estar instalados dentro do WSL2
(ou usar os binarios do Windows apontando para o socket do WSL2).
