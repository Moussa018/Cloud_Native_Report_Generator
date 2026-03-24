#pour csv
resource "aws_s3_bucket" "data_bucket" {
   bucket = "report-data-storage"
}
#pour report final
resource "aws_s3_bucket" "reports_bucket" {
  bucket = "report-output-storage"
}