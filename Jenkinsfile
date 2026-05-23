// ============================================================
//  WanderLust Travel App — Jenkins CI/CD Pipeline
//  Stages: Checkout → Test → Build → Push → Deploy
// ============================================================

pipeline {

    // Run on any available Jenkins agent
    agent any

    // ── Environment variables ──────────────────────────────
    environment {
        IMAGE_NAME    = "wanderlust-travel"          // Docker image name
        IMAGE_TAG     = "${BUILD_NUMBER}"            // Tag = Jenkins build number (e.g. "42")
        DOCKER_HUB_USER = "kunalnagarkoti" // ← CHANGE THIS
        CONTAINER_NAME  = "wanderlust-app"
        APP_PORT        = "5000"
        HOST_PORT       = "80"
    }

    // ── Triggers ───────────────────────────────────────────
    triggers {
        // Poll GitHub every minute (or use webhooks — see README)
        pollSCM('* * * * *')
    }

    // ── Pipeline options ───────────────────────────────────
    options {
        timestamps()                     // Show timestamps in logs
        buildDiscarder(logRotator(       // Keep last 10 builds only
            numToKeepStr: '10'
        ))
        timeout(time: 15, unit: 'MINUTES') // Fail if pipeline hangs
    }

    stages {

        // ── STAGE 1: Checkout ────────────────────────────────
        stage('Checkout') {
            steps {
                echo '📥 Pulling source code from GitHub...'
                // Jenkins auto-checks out from the configured GitHub repo
                checkout scm
                sh 'echo "Branch: ${GIT_BRANCH}" && echo "Commit: ${GIT_COMMIT}"'
            }
        }

   // ── STAGE 2: Install & Test ──────────────────────────
stage('Test') {
    steps {
        echo '🧪 Installing dependencies and running tests...'
        sh '''
            # Create isolated virtual environment
            python3 -m venv venv
            . venv/bin/activate

            # Install dependencies
            pip install --upgrade pip
            pip install -r requirements.txt

            # Install pytest plugins explicitly
            pip install pytest pytest-flask

            # Run all tests automatically
            pytest -v --tb=short --junit-xml=test-results.xml
        '''
    }

    post {
        always {
            // Publish test results in Jenkins UI
            junit allowEmptyResults: true, testResults: 'test-results.xml'

            // Cleanup virtual environment
            sh 'rm -rf venv'
        }
    }
}
        // ── STAGE 3: Build Docker Image ──────────────────────
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build \
                        -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} \
                        -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest \
                        .

                    echo "Built: ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    docker images | grep ${IMAGE_NAME}
                '''
            }
        }

        // ── STAGE 4: Push to Docker Hub ──────────────────────
        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing image to Docker Hub...'
                // 'dockerhub-credentials' = ID you set in Jenkins Credentials Manager
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }

        // ── STAGE 5: Deploy ───────────────────────────────────
        stage('Deploy') {
            steps {
                echo '🚀 Deploying container...'
                sh '''
                    # Stop & remove old container if running
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm   ${CONTAINER_NAME} 2>/dev/null || true

                    # Run new container
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        -p ${HOST_PORT}:${APP_PORT} \
                        ${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}

                    echo "✅ Container started. App running on port ${HOST_PORT}"
                    docker ps | grep ${CONTAINER_NAME}
                '''
            }
        }

        // ── STAGE 6: Smoke Test ───────────────────────────────
        stage('Smoke Test') {
            steps {
                echo '🔍 Running post-deploy smoke test...'
                sh '''
                    sleep 5   # Give container time to start

                    # Check health endpoint responds with 200
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${HOST_PORT}/health)
                    if [ "$STATUS" = "200" ]; then
                        echo "✅ Smoke test PASSED — app is healthy (HTTP $STATUS)"
                    else
                        echo "❌ Smoke test FAILED — got HTTP $STATUS"
                        exit 1
                    fi
                '''
            }
        }

    } // end stages

    // ── Post actions (always run) ──────────────────────────
    post {
        success {
            echo """
            ╔══════════════════════════════════════╗
            ║  ✅ PIPELINE SUCCESS                  ║
            ║  Build: #${BUILD_NUMBER}              ║
            ║  App deployed on port ${HOST_PORT}    ║
            ╚══════════════════════════════════════╝
            """
        }
        failure {
            echo """
            ╔══════════════════════════════════════╗
            ║  ❌ PIPELINE FAILED                   ║
            ║  Build: #${BUILD_NUMBER}              ║
            ║  Check logs above for errors          ║
            ╚══════════════════════════════════════╝
            """
            // Clean up broken containers
            sh 'docker stop ${CONTAINER_NAME} 2>/dev/null || true'
            sh 'docker rm   ${CONTAINER_NAME} 2>/dev/null || true'
        }
        always {
            // Remove dangling Docker images to save disk space
            sh 'docker image prune -f'
        }
    }

} // end pipeline
