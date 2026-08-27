resource "google_kms_key_ring" "my_key_ring" {
  name     = "my-key-ring"
  location = var.region
}

resource "google_service_account" "my_service_account" {
  account_id   = "my-service-account"
  display_name = "My Service Account"
}
