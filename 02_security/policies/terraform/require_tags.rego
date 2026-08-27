package main

default allow = true

allow {
  count(input.Tags) > 0
}

allow {
  input.Type = "google_compute_instance"
  count(input.Tags) > 0
}

allow {
  input.Type = "google_storage_bucket"
  count(input.Tags) > 0
}

allow {
  input.Type = "google_compute_vpc_network"
  count(input.Tags) > 0
}