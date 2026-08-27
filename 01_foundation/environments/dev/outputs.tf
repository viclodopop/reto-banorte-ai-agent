output "kms_key_id" {
  value = module.kms.key_id
}

output "network_vpc_id" {
  value = module.networking.vpc_id
}