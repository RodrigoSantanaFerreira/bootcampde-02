data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "buckets-stack" {
  count  = length(var.bucket_names)
  bucket = "${var.project_name}-${var.bucket_names[count.index]}-${var.environment}-${data.aws_caller_identity.current.account_id}"
  force_destroy = true
    tags = {
    Bucket_Name    = "${var.project_name}-${var.bucket_names[count.index]}-${var.environment}"
    environment = var.environment
    Cost_Center = "TI"
    Project_Name = var.project_name
   }
  }

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket-encryption" {
  count  = length(var.bucket_names)
  bucket = "${var.project_name}-${var.bucket_names[count.index]}-${var.environment}-${data.aws_caller_identity.current.account_id}"
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
    depends_on = [
    aws_s3_bucket.buckets-stack
  ]
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  count  = length(var.bucket_names)
  bucket = "${var.project_name}-${var.bucket_names[count.index]}-${var.environment}-${data.aws_caller_identity.current.account_id}"
  acl    = "private"
    depends_on = [
    aws_s3_bucket.buckets-stack
  ]

}

resource "aws_s3_bucket_public_access_block" "public_access_block" {
  count  = length(var.bucket_names)
  bucket = "${var.project_name}-${var.bucket_names[count.index]}-${var.environment}-${data.aws_caller_identity.current.account_id}"

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  depends_on = [
    aws_s3_bucket.buckets-stack
  ]
}