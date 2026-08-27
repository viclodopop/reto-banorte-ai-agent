resource "google_compute_vpc_network" "main_vpc" {
  name = "main-vpc"
  auto_create_subnetworks = true
}

resource "google_compute_subnetwork" "main_subnet" {
  name          = "main-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  vpc_network   = google_compute_vpc_network.main_vpc.self_link
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_vpc_network.main_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_tags = ["ssh"]
}

resource "google_compute_firewall" "allow_http" {
  name    = "allow-http"
  network = google_compute_vpc_network.main_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_tags = ["http"]
}
