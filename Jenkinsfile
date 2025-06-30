pipeline {
  agent {
    docker {
      image 'docker/compose:latest'
      args '-v /var/run/docker.sock:/var/run/docker.sock'
    }
  }

  stages {

    stage('Checkout Code') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Images') {
      steps {
        script {
          sh 'docker-compose build'
        }
      }
    }

    stage('Run Docker Compose') {
      steps {
        script {
          sh 'docker-compose up -d'
        }
      }
    }

    stage('Verify Running Services') {
      steps {
        script {
          sh 'docker ps'
        }
      }
    }

  }

  post {
    success {
      echo "Pipeline completed successfully!"
    }
    failure {
      echo "Pipeline failed."
    }
  }
}
