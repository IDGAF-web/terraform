provider "google" {
  project = "project-0db10634-1fc8-4bf5-971"
  region  = var.region
}

# Настройка портов согласно п. 6.2 задания
resource "google_compute_firewall" "assignment_sg" {
  name    = "microservices-firewall"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "3000", "9090"]
  }

  source_ranges = ["0.0.0.0/0"]
}

# Создание инстанса согласно п. 6.2 задания
resource "google_compute_instance" "app_server" {
  name         = "microservices-host"
  machine_type = var.instance_type
  zone         = "${var.region}-a"

  boot_disk {
  initialize_params {
    image = "ubuntu-os-cloud/ubuntu-2204-lts"
  }
}
  network_interface {
    network = "default"
    access_config {} 
  }
}