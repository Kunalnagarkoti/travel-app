<<<<<<< HEAD
# ✈️ WanderLust Travel App — CI/CD with Jenkins + Docker

A Flask travel website fully containerized and automated with Jenkins CI/CD.

## 📁 Project Structure

```
travel-app/
├── app.py                  # Flask application
├── templates/
│   └── index.html          # Frontend (HTML/CSS)
├── tests/
│   └── test_app.py         # Pytest unit tests
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Local dev helper
├── Jenkinsfile             # CI/CD pipeline definition
├── requirements.txt        # Python dependencies
└── .gitignore
```

## 🚀 Quick Start (Local)

```bash
# Option A: Docker Compose (recommended)
docker compose up --build
# Visit http://localhost:5000

# Option B: Plain Python
pip install -r requirements.txt
python app.py
```

## 🔧 Jenkins Setup (Step by Step)

### 1. Prerequisites on Jenkins server
```bash
# Jenkins server needs Docker installed
sudo apt install docker.io -y
sudo usermod -aG docker jenkins   # Allow Jenkins to run Docker
sudo systemctl restart jenkins
```

### 2. Install Jenkins Plugins
Go to **Manage Jenkins → Plugins** and install:
- Git Plugin
- Pipeline Plugin
- Docker Pipeline Plugin
- JUnit Plugin

### 3. Add Docker Hub Credentials
Go to **Manage Jenkins → Credentials → Global → Add Credentials**:
- Kind: `Username with password`
- Username: your Docker Hub username
- Password: your Docker Hub password (or access token)
- ID: `dockerhub-credentials`  ← must match Jenkinsfile exactly

### 4. Create the Pipeline Job
1. Click **New Item** → name it `wanderlust-cicd` → select **Pipeline**
2. Under **Pipeline**:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/YOUR_USERNAME/travel-app`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
3. Save

### 5. (Optional) GitHub Webhook — auto-trigger on push
Instead of poll SCM, use webhooks for instant triggers:
1. In Jenkins job → **Build Triggers** → check **GitHub hook trigger for GITScm polling**
2. In GitHub repo → **Settings → Webhooks → Add webhook**:
   - Payload URL: `http://YOUR_JENKINS_IP:8080/github-webhook/`
   - Content type: `application/json`
   - Events: `Just the push event`

### 6. Update Jenkinsfile
Open `Jenkinsfile` and change:
```groovy
DOCKER_HUB_USER = "your-dockerhub-username"  // ← your real username
```

## 🔄 CI/CD Pipeline Stages

```
Push to GitHub
      │
      ▼
┌─────────────┐
│  1. Checkout │  Pull code from GitHub
└──────┬──────┘
       ▼
┌─────────────┐
│  2. Test    │  Run pytest, publish JUnit results
└──────┬──────┘
       ▼
┌─────────────┐
│  3. Build   │  docker build (multi-stage)
└──────┬──────┘
       ▼
┌─────────────┐
│  4. Push    │  Push to Docker Hub (tagged + latest)
└──────┬──────┘
       ▼
┌─────────────┐
│  5. Deploy  │  Stop old container, run new one
└──────┬──────┘
       ▼
┌─────────────┐
│  6. Smoke   │  curl /health — verify app is live
└─────────────┘
```

## 🐳 Docker Details

The `Dockerfile` uses a **multi-stage build**:
- Stage 1 (`builder`): installs Python packages
- Stage 2 (`final`): copies only what's needed — smaller, secure image
- Runs as **non-root user** for security
- Uses **Gunicorn** (production WSGI server, not Flask dev server)
- Has a **HEALTHCHECK** so Docker knows if app is alive

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Travel website homepage |
| `/health` | GET | Health check (used by Docker + Jenkins) |
| `/api/destinations` | GET | JSON list of destinations |
=======
# travel-app
>>>>>>> 0475a20cae494803c791d03faa30d5015ed1fecf
