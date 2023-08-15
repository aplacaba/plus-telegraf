pipeline {
    environment {
        registry = 'https://932146903359.dkr.ecr.ap-southeast-1.amazonaws.com/plus-telegraf'
        registryCredentialID = 'jenkins-aws'
        dockerImage = ''
    }

    agent any

    stages {
        stage('build docker image and push to ecr') {
            steps {
                script {
                    def dockerImage = docker.build "plus-telegraf";

                    docker.withRegistry(registry, "ecr:ap-southeast-1:" + registryCredentialID) {
                        dockerImage.push("$GIT_COMMIT")
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('deploy to ecs') {
            steps {
                sh "aws ecs update-service --cluster plusgen --service plus-telegraf --force-new-deployment"
            }
        }
    }

    post {
        success {
            slackSend color: "good", channel: "#build-status", message: "Build deployed successfully - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
        failure {
            sh 'echo bad'
            slackSend color: "bad", channel: "#build-status", failOnError: true, message: "Build failed  - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
        always {
            cleanWs()
        }
    }
}
