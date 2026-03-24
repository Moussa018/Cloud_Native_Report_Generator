## Cloud Native Report Generator

This project automates the generation of CSV reports from sales and inventory data stored in S3. An AWS Lambda function retrieves the source files, computes key statistics (total sales, inventory levels, sales-to-inventory ratio), generates a consolidated report, stores it in an output S3 bucket, and sends it via email using Amazon SES.

The entire infrastructure is provisioned using Terraform and tested locally using LocalStack.

## Architecture

<p align="center">
  <img src="./schemas.png" alt="Cloud Native Architecture" width="800">
</p>


## Tech Stack
| Component | Technology              |
| --------- | ----------------------- |
| Compute   | AWS Lambda (Python 3.9) |
| Storage   | AWS S3                  |
| Email     | AWS SES                 |
| IaC       | Terraform ~5.0          |
| Local dev | LocalStack + Docker     |


## Quick Start

### 1. Start LocalStack

```bash
docker-compose up -d
```

### 2. Provision Infrastructure

```bash
cd infra
terraform init
terraform apply -auto-approve
```

### 3.Upload Data

```bash
awslocal s3 cp data/samples_sales.csv s3://report-data-storage/sales/samples_sales.csv
awslocal s3 cp data/samples_data.csv  s3://report-data-storage/inventory/samples_data.csv
```

### 4. Invoke Lambda

```bash
bash scripts/lambda.sh
```


## Project Structure

```
.
├── app/
│   └── report_generator.py   # Lambda handler
├── data/
│   ├── samples_sales.csv     # Sample sales data
│   ├── samples_data.csv      # Sample inventory data
│   └── resultat.csv          # Output report example
├── infra/
│   ├── provider.tf           # AWS / LocalStack configuration
│   ├── infra.tf              # S3 buckets
│   └── lambda.tf             # Lambda function + IAM role
├── scripts/
│   ├── setup.sh              # Install Terraform & awslocal
│   ├── test.sh               # Full startup (LocalStack + Terraform)
│   └── lambda.sh             # Manual Lambda invocation
└── docker-compose.yaml       # LocalStack setup

```

## Email Simulation (AWS SES)

In this project, email sending via Amazon SES is fully simulated. Since LocalStack operates as an isolated sandbox environment, no emails are actually sent over the Internet. This allows testing notification logic without configuring real domains or risking spam during development.

### Verify Email Sending

To confirm that the Lambda function successfully triggered the report email and to inspect its content, you can query the local SES API.

Run the following command :

```bash
awslocal sesv2 list-emails
```

## Lambda Environment Variables

| Variable         | Default Value           | Description                        |
| ---------------- | ----------------------- | ---------------------------------- |
| `DATA_BUCKET`    | `report-data-storage`   | Bucket containing source CSV files |
| `REPORTS_BUCKET` | `report-output-storage` | Destination bucket for reports     |
| `EMAIL_ADDRESS`  | *(to configure)*        | SES sender/receiver email address  |
