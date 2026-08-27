package main

default allow = true

allow {
  not is_public_ingress(input)
}

is_public_ingress(resource) {
  resource.Type = "google_compute_firewall"
  resource.Ingress.Allowed[].Ports == ["0-65535"]
  resource.Ingress.Sources == ["0.0.0.0/0"]
}