output "public_ip" {
  description = "The public IP address of the deployed instance"
  value       = google_compute_instance.app_server.network_interface[0].access_config[0].nat_ip
}