# DevSecOps Jenkins CI/CD - AWS ECS Application Deployment

This standalone project builds, scans, provisions, and deploys a containerized FastAPI application to AWS ECS/Fargate through Jenkins.

## Pipeline stages

```text
Checkout
  -> Install, Ruff, pytest
  -> pip-audit and Trivy filesystem scan
  -> Terraform format, validate, and plan
  -> Docker build and Trivy image scan
  -> Push image to ECR
  -> Terraform apply and ECS rollout verification
```

## Contents

- `app/`: sample FastAPI application with `/` and `/health`
- `tests/`: application tests
- `infra/`: Terraform ECS/Fargate, ECR, ALB, IAM, networking, and logging resources
- `Jenkinsfile`: Jenkins pipeline
- `Dockerfile`: non-root application image

## Jenkins setup

Create a Pipeline job from SCM and point it to this repository. The Jenkins agent must have Python 3.11+, Docker, AWS CLI, Terraform, and Trivy.

Create Jenkins secret-text credentials with these IDs:

`aws-region`, `aws-vpc-id`, `aws-subnet-ids`, `ecr-repository`, `ecs-cluster`, and `ecs-service`.

The AWS credential used by the agent should be short-lived or supplied through the Jenkins AWS credentials integration. Grant only ECR push, Terraform target-resource, ECS deployment, and CloudWatch permissions.

## Required AWS values

- Existing VPC ID
- Comma-separated subnet IDs
- ECR repository URI
- ECS cluster name
- ECS service name

The Terraform configuration creates the ECR repository, ECS cluster, task definition, service, load balancer, security groups, IAM execution role, and CloudWatch log group. It expects the VPC and subnets to already exist.

## Running Jenkins

1. Run the job with `DEPLOY_APPLICATION` enabled to deploy the image.
2. Enable `APPLY_INFRASTRUCTURE` when Terraform changes should be applied.
3. Review the Terraform plan before approving infrastructure changes.
4. Confirm the ECS service reaches a stable state.
5. Verify the load balancer health endpoint and CloudWatch logs.

AWS infrastructure can incur charges. Use a protected Jenkins job, review plans, and destroy demonstration resources when finished.
