terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.40.0"
    }
  }

  backend "s3" {
    bucket         = "achebeh-bucket"
    key            = "./terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform"
  }
}

provider "aws" {
  region = "us-east-1"
}