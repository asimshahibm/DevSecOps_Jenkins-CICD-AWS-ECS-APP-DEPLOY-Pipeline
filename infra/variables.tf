variable "aws_region" {
  type = string
}

variable "project_name" {
  type    = string
  default = "devsecops-ecs-sample"
}

variable "image_uri" {
  type    = string
  default = "public.ecr.aws/docker/library/python:3.12-slim"
}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

variable "container_port" {
  type    = number
  default = 8000
}
