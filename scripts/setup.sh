#!/bin/bash
set -e

echo "Réparation et Installation de Terraform..."
# On ignore le dépôt Yarn qui bloque tout
sudo rm -f /etc/apt/sources.list.d/yarn.list

sudo apt-get update
sudo apt-get install -y gnupg software-properties-common curl

# Installation officielle HashiCorp
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt-get update
sudo apt-get install -y terraform

echo "Installation de awslocal..."
pip install awscli-local

echo "✅ Terraform installé : $(terraform --version)"