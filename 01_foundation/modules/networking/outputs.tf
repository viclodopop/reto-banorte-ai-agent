output "vpc_id" {
  value = google_compute_vpc_network.main_vpc.self_link
}

output "subnet_id" {
  value = google_compute_subnetwork.main_subnet.self_link
}
