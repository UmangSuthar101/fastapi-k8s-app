pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_REPO = "umang101/fastapi-k8s-app"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    def IMAGE_TAG = "${env.BUILD_NUMBER}"   // Jenkins build number
                    sh "docker build -t $DOCKERHUB_REPO:$IMAGE_TAG ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    sh "docker push $DOCKERHUB_REPO:${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        sed -i 's|image: $DOCKERHUB_REPO:.*|image: $DOCKERHUB_REPO:${env.BUILD_NUMBER}|' k8s/deployment.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                    """
                }
            }
        }
    }
}
