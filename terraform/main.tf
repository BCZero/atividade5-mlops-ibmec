# Aula 07 -- Namespace + Secret + ConfigMap do projeto-guia PCDF, criados
# via Terraform (mesma disciplina de IaC das Aulas 02/03), agora apontando
# pro Kubernetes em vez do Azure.

resource "kubernetes_namespace" "mlops" {
  metadata {
    name = "mlops"
    labels = {
      projeto = "pcdf-bo-triagem"
      aula    = "07"
    }
  }
}

# Secret didatico -- credencial FICTICIA so pra demonstrar o recurso; nao
# use segredo real aqui (o valor entra em texto no .tf, sem qualquer
# criptografia -- em projeto de verdade isso viria de uma variavel
# sensivel ou de um cofre de segredos, nunca hardcoded).
resource "kubernetes_secret" "app_credentials" {
  metadata {
    name      = "app-credentials"
    namespace = kubernetes_namespace.mlops.metadata[0].name
  }

  data = {
    username = "pcdf-mlops-demo"
    password = "trocar-em-producao"
  }

  type = "Opaque"
}

resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "app-config"
    namespace = kubernetes_namespace.mlops.metadata[0].name
  }

  data = {
    LIMIAR_MINIMO_ACURACIA = "0.60"
    PROJETO_GUIA           = "pcdf-bo-triagem"
  }
}
