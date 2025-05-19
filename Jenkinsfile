pipeline {
    agent any 

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'  // Leave this unless told otherwise
        DOCKER_IMAGE = 'cithit/perezi3'             // Use your MiamiID
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/iliannaperez/225-lab5-1.git'
        KUBECONFIG = credentials('perezi3-225')     // Use your kubeconfig Jenkins credential
    }

    stages {
        stage('Checkout Code') {
            steps {
                cleanWs()
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        stage('Static Code Test') {
            steps {
                sh 'pip install --quiet pycodestyle'
                sh 'pycodestyle main.py || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Dev Environment') {
            steps {
                script {
                    def kubeConfig = readFile(KUBECONFIG)
                    sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                    sh "kubectl apply -f deployment-dev.yaml"
                }
            }
        }

        stage('Check Kubernetes Cluster') {
            steps {
                sh "kubectl get all"
            }
        }
    }

    post {
        success {
            slackSend color: "good", message: "✅ Build #${BUILD_NUMBER} completed successfully."
        }
        failure {
            slackSend color: "danger", message: "❌ Build #${BUILD_NUMBER} failed."
        }
    }
}
