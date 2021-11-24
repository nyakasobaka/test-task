#!/usr/bin/env groovy
pipeline {
    agent none
    triggers {
    cron('0 */3 * * * %BROWSER=chrome' + '\n 15 */3 * * * %BROWSER=firefox')
    }
    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Select browser')
        string(name: 'THREADS', description: 'Define threads count', defaultValue: '4')
    }
    stages {
        stage ('Run Test') {
            agent {
                dockerfile {
                    args '--net=host'
                }
            }
            steps {
                sh "python -m pytest -B ${params.BROWSER} --alluredir=./report -n ${params.THREADS} --reruns 2"
            }
        }
    }
    post {
        always {
            node (null) {
                echo 'Generating Allure report'
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    results          : [[path: 'report']]
                ])
            }
        }
    }
}