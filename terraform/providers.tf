# Aula 07 -- Terraform didatico: cria recursos DENTRO do cluster Kind que
# ja esta de pe (Bloco 2, Passo B2-1). O provider "kubernetes" fala com o
# cluster pelo MESMO kubeconfig que o kubectl usa -- nao cria o cluster em
# si (isso e trabalho do Kind, ferramenta feita pra isso).
terraform {
  required_version = ">= 1.9"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.35"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "kind-aula07-mlops" # criado pelo "kind create cluster --name aula07-mlops"
}
