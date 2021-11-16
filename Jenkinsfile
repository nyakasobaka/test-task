#!/usr/bin/env groovy
pipeline {
    agent none

    triggers { cron('0 * * * *') }

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Select browser')
        string(name: 'THREADS', description: 'Define threads count', defaultValue: '4')
    }

    stages {
        stage ('Run Test') {
            agent {
                docker {
                    image 'python:3.9-alpine'
                    args '-u root --net=host'
                }
            }
            steps {
                sh 'python -m venv venv'
                sh 'source venv/bin/activate'
                sh 'python -m pip install -r requirements.txt --user'
                sh "python -m pytest -k test_search_by_text -B ${params.BROWSER} --alluredir=./report -n ${params.THREADS}"
            }
        }
    }

    post {
        always {
            node (null) {
                echo 'Generating Allure report'
                sh 'ls -al report'
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    results          : [[path: 'report']]
                ])
            }
        }
    }
}
