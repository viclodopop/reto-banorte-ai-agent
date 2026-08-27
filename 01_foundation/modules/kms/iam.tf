resource "google_kms_crypto_key" "my_key" {
  name     = "my-key"
  key_ring = google_kms_key_ring.my_key_ring.id
  rotation_period = "10752h"
}

resource "google_storage_bucket_iam_member" "storage_iam_member" {
  bucket = "your-bucket-name"
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.my_service_account.email}"
}
