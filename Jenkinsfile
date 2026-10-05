pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Descargando el proyecto desde GitHub...'
            }
        }

        stage('Install dependencies') {
            steps {
                echo 'Instalando dependencias de Python...'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Verificando el código Python...'
                bat 'python -m compileall app'
            }
        }
    }
}
