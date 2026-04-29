# Microservices Infrastructure & Observability

##  Project Overview
This repository contains the Infrastructure as Code (IaC) configurations and deployment files for a containerized microservices architecture. It demonstrates automated infrastructure provisioning on Google Cloud Platform (GCP) and container orchestration integrated with a full Site Reliability Engineering (SRE) monitoring stack.

This project was developed as part of **Assignments 4 & 5**.

##  Technologies Used
* **Infrastructure as Code:** Terraform
* **Cloud Provider:** Google Cloud Platform (GCP)
* **Containerization:** Docker, Docker Compose
* **Monitoring & Observability:** Prometheus, Grafana
* **Operating System:** Ubuntu 20.04 LTS

## Prerequisites
Before deploying the infrastructure, ensure you have the following installed on your local machine:
* [Terraform](https://www.terraform.io/downloads.html)
* [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (`gcloud`)
* An active GCP account with the **Compute Engine API** enabled.

##  Infrastructure Setup (Terraform)
The infrastructure consists of an `e2-micro` instance with customized firewall rules allowing traffic on essential operational ports (22, 80, 3000, 9090).

1. **Authenticate with Google Cloud:**
   ```bash
   gcloud auth application-default login
   gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>

2. **Initialize Terraform:**
   terraform init
   
3. Review the deployment plan:
   terraform plan

4. Apply the configuration:
   terraform apply -auto-approve

Note: Upon successful completion, Terraform will output the public_ip of the newly created instance.

 Application Deployment
Once the virtual machine is provisioned, you can deploy the microservices stack:

SSH into the server using the generated Public IP.

Clone this repository (or transfer the application files).

Start the services using Docker Compose:

docker-compose up -d

Accessing the Services
Once deployed, the services will be available at the following endpoints (replace <PUBLIC_IP> with the IP outputted by Terraform):


