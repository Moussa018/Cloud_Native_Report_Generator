# Archive le code Python
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../app/report_generator.py"
  output_path = "${path.module}/function.zip"
}

# Rôle IAM pour la Lambda
resource "aws_iam_role" "lambda_role" {
  name = "business_report_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# La Fonction Lambda
resource "aws_lambda_function" "report_lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "business-report-generator"
  role             = aws_iam_role.lambda_role.arn
  handler          = "report_generator.lambda_handler" 
  runtime          = "python3.9"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      DATA_BUCKET    = "report-data-storage"  
      REPORTS_BUCKET = "report-output-storage" 
      EMAIL_ADDRESS  = "jacksnow0187@gmail.com"
    }
  }
}