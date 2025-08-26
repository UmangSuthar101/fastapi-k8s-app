pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Jenkins → Manage Credentials
        DOCKERHUB_REPO = "umang101/fastapi-k8s-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/UmangSuthar101/fastapi-k8s-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def IMAGE_TAG = "${env.BUILD_NUMBER}"   // ✅ declare with def
                    sh "docker build -t $DOCKERHUB_REPO:$IMAGE_TAG ."
                    env.IMAGE_TAG = IMAGE_TAG   // ✅ export to env for later stages
                }
            }
        }


        stage('Push to DockerHub') {
            steps {
                script {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    sh "docker push $DOCKERHUB_REPO:$IMAGE_TAG"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Replace image tag dynamically in deployment.yaml
                    sh """
                        sed -i 's|image: $DOCKERHUB_REPO:.*|image: $DOCKERHUB_REPO:$IMAGE_TAG|' k8s/deployment.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                    """
                }
            }
        }
    }
}
