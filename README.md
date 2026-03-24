# 📊 Automated Report Generation

> Pipeline serverless de génération automatique de rapports métiers quotidiens, déployé sur AWS (LocalStack) via Terraform.

---

## Description

Ce projet automatise la génération de rapports CSV à partir de données de ventes et d'inventaire stockées dans S3. Une fonction AWS Lambda récupère les fichiers source, calcule les statistiques clés (ventes totales, stock, ratio ventes/inventaire), produit un rapport consolidé, le sauvegarde dans un bucket S3 de sortie, et l'envoie par e-mail via Amazon SES.

L'ensemble de l'infrastructure est provisionné avec **Terraform** et testé localement grâce à **LocalStack**.

---

## Architecture

```
S3 (data)          Lambda                  S3 (reports)
────────────  →  ─────────────────────  →  ──────────────
sales CSV          generate_report()        daily_report_
inventory CSV      send_email_report()      YYYYMMDD.csv
                        ↓
                   SES (email)
```

---

## Stack technique

| Composant      | Technologie              |
|----------------|--------------------------|
| Compute        | AWS Lambda (Python 3.9)  |
| Stockage       | AWS S3                   |
| Email          | AWS SES                  |
| IaC            | Terraform ~5.0           |
| Local dev      | LocalStack + Docker       |

---

## Lancement rapide

### 1. Démarrer LocalStack

```bash
docker-compose up -d
```

### 2. Provisionner l'infrastructure

```bash
cd infra
terraform init
terraform apply -auto-approve
```

### 3. Uploader les données

```bash
awslocal s3 cp data/samples_sales.csv s3://report-data-storage/sales/samples_sales.csv
awslocal s3 cp data/samples_data.csv  s3://report-data-storage/inventory/samples_data.csv
```

### 4. Invoquer la Lambda

```bash
bash scripts/lambda.sh
```

---

## Structure du projet

```
.
├── app/
│   └── report_generator.py   # Handler Lambda
├── data/
│   ├── samples_sales.csv     # Données de ventes (exemple)
│   ├── samples_data.csv      # Données d'inventaire (exemple)
│   └── resultat.csv          # Rapport de sortie (exemple)
├── infra/
│   ├── provider.tf           # Configuration AWS / LocalStack
│   ├── infra.tf              # Buckets S3
│   └── lambda.tf             # Fonction Lambda + rôle IAM
├── scripts/
│   ├── setup.sh              # Installation Terraform & awslocal
│   ├── test.sh               # Démarrage complet (LocalStack + Terraform)
│   └── lambda.sh             # Invocation manuelle de la Lambda
└── docker-compose.yaml       # LocalStack
```

---

## Variables d'environnement (Lambda)

| Variable         | Valeur par défaut        | Description                        |
|------------------|--------------------------|------------------------------------|
| `DATA_BUCKET`    | `report-data-storage`    | Bucket contenant les CSV sources   |
| `REPORTS_BUCKET` | `report-output-storage`  | Bucket de destination des rapports |
| `EMAIL_ADDRESS`  | *(à configurer)*         | Adresse SES expéditeur/destinataire|
