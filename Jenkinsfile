pipeline {
    agent any

    parameters {
        booleanParam(name: 'APPLY_INFRASTRUCTURE', defaultValue: false, description: 'Apply Terraform changes')
        booleanParam(name: 'DEPLOY_APPLICATION', defaultValue: true, description: 'Deploy to ECS')
    }

    environment {
        AWS_DEFAULT_REGION = credentials('aws-region')
        AWS_VPC_ID = credentials('aws-vpc-id')
        AWS_SUBNET_IDS = credentials('aws-subnet-ids')
        ECR_REPOSITORY = credentials('ecr-repository')
        ECS_CLUSTER = credentials('ecs-cluster')
        ECS_SERVICE = credentials('ecs-service')
    }

    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install, test, and lint') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -e ".[dev]" && ruff check . && pytest'
            }
        }
        stage('Security scans') {
            steps {
                sh 'python3 -m pip install --user pip-audit'
                sh 'python3 -m pip_audit'
                sh 'trivy fs --ignore-unfixed --severity HIGH,CRITICAL --exit-code 1 .'
            }
        }
        stage('Terraform plan') {
            steps {
                sh 'terraform -chdir=infra fmt -check'
                sh 'terraform -chdir=infra init -backend=false -input=false'
                sh 'terraform -chdir=infra validate'
                sh 'terraform -chdir=infra plan -input=false -var="aws_region=$AWS_DEFAULT_REGION" -var="vpc_id=$AWS_VPC_ID" -var="subnet_ids=[\\"${AWS_SUBNET_IDS//,/\\",\\"}\\"]" -out=tfplan'
                script {
                    if (params.APPLY_INFRASTRUCTURE) {
                        sh 'terraform -chdir=infra apply -input=false tfplan'
                    }
                }
            }
        }
        stage('Build and scan image') {
            steps {
                sh 'docker build -t "$ECR_REPOSITORY:$GIT_COMMIT" .'
                sh 'trivy image --ignore-unfixed --severity HIGH,CRITICAL --exit-code 1 "$ECR_REPOSITORY:$GIT_COMMIT"'
            }
        }
        stage('Push and deploy') {
            when { expression { return params.DEPLOY_APPLICATION } }
            steps {
                sh 'aws ecr get-login-password --region "$AWS_DEFAULT_REGION" | docker login --username AWS --password-stdin "${ECR_REPOSITORY%%/*}"'
                sh 'docker push "$ECR_REPOSITORY:$GIT_COMMIT"'
                sh 'terraform -chdir=infra apply -auto-approve -input=false -var="aws_region=$AWS_DEFAULT_REGION" -var="vpc_id=$AWS_VPC_ID" -var="subnet_ids=[\\"${AWS_SUBNET_IDS//,/\\",\\"}\\"]" -var="image_uri=$ECR_REPOSITORY:$GIT_COMMIT"'
                sh 'aws ecs wait services-stable --cluster "$ECS_CLUSTER" --services "$ECS_SERVICE" --region "$AWS_DEFAULT_REGION"'
            }
        }
    }
}
