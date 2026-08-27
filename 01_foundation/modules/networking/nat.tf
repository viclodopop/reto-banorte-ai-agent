resource "google_compute_router" "my_router" {
  name    = "my-router"
  network = google_compute_vpc_network.main_vpc.name
  region  = var.region
}

resource "google_compute_router_nat" "my_nat" {
  name                = "my-nat"
  router              = google_compute_router.my_router.name
  region              = var.region
  nat_ip_allocate_option = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}
