provider "aws" {
  region = "us-east-1"
  count  = var.environment == "prod" ? 1 : 0
}

module "local_dev" {
  source = "./local_dev"
  enabled = var.environment == "dev"
}

resource "aws_security_group" "allow_http" {
  count = var.environment == "prod" ? 1 : 0

  ingress {
    from_port   = 80
    to_port     = 80
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
