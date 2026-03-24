#!/bin/bash
set -e

PROJECT_ROOT="/workspaces/codespaces-blank"

echo "Lancement de LocalStack..."
cd $PROJECT_ROOT
docker-compose up -d
sleep 5

echo "Lancement de l'infrastructure..."
cd $PROJECT_ROOT/infra
terraform init
terraform apply -auto-approve

echo "Succès ! Liste des buckets :"
awslocal s3 ls