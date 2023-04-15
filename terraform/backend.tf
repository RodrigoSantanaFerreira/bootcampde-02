terraform {
  backend "s3" {
    # Edit the bucket name and region
    bucket         = "stack-terraform-backend-872226808963"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
  }
}