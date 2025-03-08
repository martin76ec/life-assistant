variable "environment" {
  description = "The environment to deploy to: dev or prod"
  type        = string
  default     = "prod"
}

variable "local_setup" {
  description = "Enable local setup for dev environment"
  type        = bool
  default     = false
}

variable "ami" {
  description = "AMI to use for the instance"
  type        = string
  default     = "ami-0c02fb55956c7d316" # Prod AMI
}
