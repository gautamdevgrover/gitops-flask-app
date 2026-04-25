pipeline {
agent any

environment {
    DOCKER_IMAGE = "gautamdevgrover/gitops-flask-app"
    IMAGE_TAG = "${BUILD_NUMBER}"
    GITOPS_REPO = "https://github.com/gautamdevgrover/gitops-flask-app-manifests.git"
    GITOPS_BRANCH = "main"
}

stages {

    stage('Checkout Code') {
        steps {
            git branch: 'main', url: 'https://github.com/gautamdevgrover/gitops-flask-app.git'
        }
    }

    stage('Build Docker Image') {
        steps {
            script {
                sh """
                docker build -t $DOCKER_IMAGE:$IMAGE_TAG .
                docker tag $DOCKER_IMAGE:$IMAGE_TAG $DOCKER_IMAGE:latest
                """
            }
        }
    }

    stage('Run Container for Testing') {
        steps {
            script {
                sh """
                docker stop test-container --signal KILL || true
                docker rm test-container || true
                docker run -d -p 5000:5000 --name test-container $DOCKER_IMAGE:$IMAGE_TAG
                sleep 5
                """
            }
        }
    }

    stage('Test Application') {
        steps {
            script {
                sh """
                curl -f http://localhost:5000/health
                """
            }
        }
    }

    stage('Cleanup Test Container') {
        steps {
            script {
                sh """
                docker stop test-container || true
                docker rm test-container || true
                """
            }
        }
    }

    stage('Push Docker Image') {
        steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS')]) {

                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin

                    docker push $DOCKER_IMAGE:$IMAGE_TAG
                    docker push $DOCKER_IMAGE:latest

                    docker logout
                    '''
                }
            }
        }

    stage('Update GitOps Repo') {
        steps {
            script {
                sh """
                rm -rf gitops-repo
                git clone ${GITOPS_REPO} gitops-repo
                cd gitops-repo

                sed -i "s/tag:.*/tag: \"${BUILD_NUMBER}\"/" flask-app/values.yaml
                sed -i "s/version:.*/version: \"${BUILD_NUMBER}\"/" flask-app/values.yaml             

                git config user.email "gautamdevgrover@gmail.com"
                git config user.name "gautamdevgrover"

                git add .
                git commit -m "Update image to ${IMAGE_TAG}"
                git push origin ${GITOPS_BRANCH}
                """
            }
        }
    }
}

post {
    always {
        sh """
        docker stop test-container || true
        docker rm test-container || true
        """
    }

    success {
        echo "✅ Build ${BUILD_NUMBER} tested and deployed successfully!"
    }

    failure {
        echo "❌ Pipeline failed during testing or deployment!"
    }
}


}

