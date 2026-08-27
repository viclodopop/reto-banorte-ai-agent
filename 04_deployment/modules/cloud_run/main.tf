# Módulo de Terraform para desplegar el Agente CV en Cloud Run
# Diseño con variables para inyección segura de secretos desde Secret Manager

resource "google_cloud_run_v2_service" "cv_agent" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.container_image
      
      env {
        name  = "API_KEY"
        value = var.agent_api_key
      }
      env {
        name = "GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = var.gemini_secret_id
            version = "latest"
          }
        }
      }
    }
    scaling {
      max_instance_count = 5 # Límite de costos
    }
  }
}