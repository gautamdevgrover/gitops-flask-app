pipeline {
agent any

environment {
    DOCKER_IMAGE = "gautamdevgrover/gitops-flask-app"
    IMAGE_TAG = "${BUILD_NUMBER}"
    GITOPS_REPO = "https://${GIT_USER}:${GIT_PASS}@github.com/gautamdevgrover/gitops-flask-app-manifests.git"
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
                docker run -d -p 5001:5000 --name test-container $DOCKER_IMAGE:$IMAGE_TAG
                sleep 5
                """
            }
        }
    }

    stage('Test Application') {
        steps {
            script {
                sh """
                curl -f http://localhost:5001/health
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
              withCredentials([usernamePassword(credentialsId: 'gitops-repo-cred', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                sh """
                rm -rf gitops-repo
                git clone https://${GIT_USER}:${GIT_PASS}@github.com/gautamdevgrover/gitops-flask-app-manifests.git gitops-repo

                git config --global --add safe.directory /var/lib/jenkins/workspace/gitops-node-app-pipeline/gitops-repo

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
}

post {
        success {
            emailext (
                subject: "✅ SUCCESS: Build #${BUILD_NUMBER}",
                mimeType: 'text/html',
                body: """
                <html>
                <body style="font-family: Arial;">

                    <h2 style="color: green;">Build Successful 🚀</h2>

                    <table border="1" cellpadding="10" cellspacing="0">
                        <tr>
                            <th>Project</th>
                            <td>${JOB_NAME}</td>
                        </tr>
                        <tr>
                            <th>Build Number</th>
                            <td>${BUILD_NUMBER}</td>
                        </tr>
                        <tr>
                            <th>Docker Image</th>
                            <td>${DOCKER_IMAGE}</td>
                        </tr>
                    </table>

                    <br>

                    <a href="${BUILD_URL}" style="color: blue;">
                        🔗 View Build Details
                    </a>

                </body>
                </html>
                """,
                to: "gautamaws777@gmail.com"
            )
        }

        failure {
            emailext (
                subject: "❌ FAILED: Build #${BUILD_NUMBER}",
                mimeType: 'text/html',
                body: """
                <html>
                <body style="font-family: Arial;">

                    <h2 style="color: red;">Build Failed ❌</h2>

                    <p><b>Project:</b> ${JOB_NAME}</p>
                    <p><b>Build Number:</b> ${BUILD_NUMBER}</p>

                    <a href="${BUILD_URL}" style="color: blue;">
                        🔗 Check Logs
                    </a>

                </body>
                </html>
                """,
                to: "gautamaws777@gmail.com"
            )
        }

        always {
            sh 'docker rm -f test-container || true'
        }
    }
}
}

