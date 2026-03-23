terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# S3 Bucket for execution logs or Merkle snapshots
resource "aws_s3_bucket" "neuro_core_bucket" {
  bucket = "neuro-core-immutable-logs-2026"
}

resource "aws_s3_bucket_versioning" "neuro_core_bucket_versioning" {
  bucket = aws_s3_bucket.neuro_core_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Security group for the EC2 Edge Nodes
resource "aws_security_group" "neuro_core_sg" {
  name        = "neuro_core_sg"
  description = "Allow inbound traffic for edge nodes"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Application port"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Autonomous EC2 Instance Provisioning
resource "aws_instance" "neuro_core_edge_node" {
  count         = 3
  ami           = "ami-0c7217cdde317cfec" # Example Ubuntu 22.04 LTS AMI in us-east-1
  instance_type = "t3.medium"
  security_groups = [aws_security_group.neuro_core_sg.name]

  tags = {
    Name = "Neuro-Core-Edge-Node-${count.index}"
    Role = "PredictorNode"
  }
}
