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

        stage('Run app') {
            steps {
                sh '''
                poetry run python manage.py runserver
                '''
            }
        }
    }
}
