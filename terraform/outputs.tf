output "namespace_criado" {
  value       = kubernetes_namespace.mlops.metadata[0].name
  description = "Confirma o nome do namespace criado -- confira com: kubectl get ns"
}

output "configmap_criado" {
  value       = kubernetes_config_map.app_config.metadata[0].name
  description = "Confira com: kubectl get configmap -n mlops"
}

output "secret_criado" {
  value       = kubernetes_secret.app_credentials.metadata[0].name
  description = "Confira com: kubectl get secret -n mlops (o VALOR não aparece em texto puro)"
}
