resource "google_vpc_access_connector" "my_vpc_connector" {
  name    = "my-vpc-connector"
  network = google_compute_vpc_network.main_vpc.name
  region  = var.region
  ip_cidr_range = "192.168.86.0/28"
}

output "vpc_connector_id" {
  value = google_vpc_access_connector.my_vpc_connector.id
}
