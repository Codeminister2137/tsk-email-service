pipeline {
    agent any

    environment {
        POETRY_HOME = "${HOME}/.poetry"
        PATH = "${POETRY_HOME}/bin:${PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Poetry') {
            steps {
                sh '''
                curl -sSL https://install.python-poetry.org | python3 -
                poetry --version
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                poetry install
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                poetry run pytest -v
                '''
            }
        }

        stage('Use Credentials') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: '2c2436c9-9f92-4c8c-b604-8cc288c69255',
                    usernameVariable: 'MAIL_ADRESS',
                    passwordVariable: 'MAIL_PASSWORD'
                )]) {
                    sh '''
                        echo "Username: $MAIL_USERNAME"
                        echo "Password: $MAIL_PASSWORD"
                    '''
                }
            }
        }

        stage('Run app') {
            steps {
                sh '''
                poetry run python manage.py runserver
                '''
            }
        }
    }
}
