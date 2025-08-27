pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // DockerHub creds in Jenkins
        DOCKERHUB_REPO = "umang101/fastapi-k8s-app"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // define IMAGE_TAG as a local variable
                    def IMAGE_TAG = "${env.BUILD_NUMBER}"   // Jenkins build number
                    sh "docker build -t $DOCKERHUB_REPO:${IMAGE_TAG} ."
                    sh "echo \"IMAGE_TAG=${IMAGE_TAG}\" > image_tag.txt"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    // read back IMAGE_TAG
                    def IMAGE_TAG = readFile('image_tag.txt').trim()
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    sh "docker push $DOCKERHUB_REPO:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // read back IMAGE_TAG
                    def IMAGE_TAG = readFile('image_tag.txt').trim()
                    sh """
                        sed -i 's|image: $DOCKERHUB_REPO:.*|image: $DOCKERHUB_REPO:${IMAGE_TAG}|' k8s/deployment.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                    """
                }
            }
        }
    }
}
