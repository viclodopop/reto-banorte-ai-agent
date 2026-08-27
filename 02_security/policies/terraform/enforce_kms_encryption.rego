package main

default allow = true

allow {
  input.Type != "google_storage_bucket"
}

allow {
  input.Type = "google_storage_bucket"
  input.Encryption.KmsKeyName != ""
}