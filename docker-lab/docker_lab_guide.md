# 🐳 Docker Lab — Complete Step-by-Step Guide
### Flask To-Do App + MongoDB | Docker Networking | Docker Hub

---

## 📋 Task Requirements Checklist

| Requirement | Solution |
|---|---|
| Web-based application | Python Flask To-Do App |
| Containerized with Dockerfile | ✅ `Dockerfile` created |
| Run locally with port mapping | ✅ `localhost:5000` → container port `5000` |
| Communicate with another container | ✅ Flask ↔ MongoDB via Docker network |
| Push image to Docker Hub | ✅ Step 6 below |

---

## 📁 Project Structure

```
docker-lab/
├── app.py              ← Flask web application
├── requirements.txt    ← Python dependencies
├── Dockerfile          ← Instructions to build the image
├── docker-compose.yml  ← Multi-container orchestration
└── .dockerignore       ← Files excluded from build context
```

---

## 🔧 Step 1 — Prerequisites

Make sure the following are installed:

- **Docker Desktop** → [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- **Docker Hub Account** → [https://hub.docker.com](https://hub.docker.com) (free)

Verify installation:
```powershell
docker --version
docker compose version
```

---

## 🐍 Step 2 — Understanding the Application

### `app.py` — Flask Web Application
- Connects to **MongoDB** using `pymongo`
- `MONGO_URI` is set via **environment variable** → `mongodb://mongo:27017/`
- `mongo` is the **hostname** of the MongoDB container on the Docker network
- Exposes 3 routes:
  - `GET /` → renders the To-Do UI
  - `POST /add` → inserts a task into MongoDB
  - `DELETE /delete/<id>` → removes a task by ID

> **Key concept:** Inside Docker, containers on the same network resolve each other by **service name** (not IP). That's why the URI uses `mongo` instead of `localhost`.

---

## 🏗️ Step 3 — Understanding the Dockerfile

```dockerfile
FROM python:3.11-slim       # Lightweight base image
WORKDIR /app                # Sets working directory inside container
COPY requirements.txt .     # Copy deps first (caching optimization)
RUN pip install -r requirements.txt   # Install Flask + pymongo
COPY . .                    # Copy all source files
EXPOSE 5000                 # Document that container listens on 5000
CMD ["python", "app.py"]    # Start the app
```

**Why `python:3.11-slim`?**  
The `-slim` variant strips dev tools, reducing image size from ~1GB → ~150MB.

**Why copy `requirements.txt` separately?**  
Docker caches layers. If only `app.py` changes, it reuses the cached pip layer → faster rebuilds.

---

## 🌐 Step 4 — Understanding Docker Compose (Multi-Container Networking)

```yaml
services:
  web:
    build: .              # Build Flask image from our Dockerfile
    ports:
      - "5000:5000"       # HOST:CONTAINER port mapping
    environment:
      - MONGO_URI=mongodb://mongo:27017/
    depends_on:
      - mongo             # Wait for mongo to start
    networks:
      - app-network       # Join shared network

  mongo:
    image: mongo:7.0      # Pull official MongoDB image
    volumes:
      - mongo-data:/data/db  # Persist data
    networks:
      - app-network       # Same shared network

networks:
  app-network:
    driver: bridge        # Creates an isolated virtual network

volumes:
  mongo-data:             # Named volume for persistence
```

**Key concepts:**
- `ports: "5000:5000"` → Maps `localhost:5000` to container port `5000`
- `networks: app-network` → Both containers share this network, so `web` can reach `mongo` by name
- `volumes: mongo-data` → Data survives container restarts
- `depends_on` → Ensures MongoDB starts before Flask

---

## 🚀 Step 5 — Build and Run Locally

### Open PowerShell and navigate to the project:
```powershell
cd d:\CLOUD_LAB\docker-lab
```

### Option A: Using Docker Compose (Recommended)
```powershell
# Build images and start all containers
docker compose up --build

# To run in background (detached mode)
docker compose up --build -d
```

### Option B: Manual Docker Commands

```powershell
# 1. Create the Docker network
docker network create app-network

# 2. Start MongoDB container on the network
docker run -d `
  --name mongodb `
  --network app-network `
  -v mongo-data:/data/db `
  mongo:7.0

# 3. Build your Flask image
docker build -t flask-todo-app .

# 4. Run Flask container on same network
docker run -d `
  --name flask_app `
  --network app-network `
  -p 5000:5000 `
  -e MONGO_URI=mongodb://mongo:27017/ `
  flask-todo-app
```

### Verify containers are running:
```powershell
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE            PORTS                    NAMES
abc123         flask-todo-app   0.0.0.0:5000->5000/tcp   flask_app
def456         mongo:7.0        27017/tcp                mongodb
```

### Open the app:
```
http://localhost:5000
```

---

## 🔍 Step 5b — Verify Container Communication

Test that Flask can reach MongoDB:
```powershell
# Exec into Flask container and ping mongo
docker exec -it flask_app sh
# Inside container:
python -c "from pymongo import MongoClient; c = MongoClient('mongodb://mongo:27017/'); print(c.list_database_names())"
```

Check logs:
```powershell
docker logs flask_app
docker logs mongodb
```

---

## 📤 Step 6 — Push Image to Docker Hub

### 6.1 — Login to Docker Hub
```powershell
docker login
# Enter your Docker Hub username and password
```

### 6.2 — Tag your image
The format must be: `<your-dockerhub-username>/<image-name>:<tag>`
```powershell
# Replace 'yourusername' with your actual Docker Hub username
docker tag flask-todo-app yourusername/flask-todo-app:v1.0
```

### 6.3 — Push the image
```powershell
docker push yourusername/flask-todo-app:v1.0
```

### 6.4 — Verify on Docker Hub
Go to: `https://hub.docker.com/r/yourusername/flask-todo-app`

You should see your image listed there! ✅

### 6.5 — Pull and run from Docker Hub (proof it works)
```powershell
# Anyone can now pull and run your image:
docker pull yourusername/flask-todo-app:v1.0
docker run -p 5000:5000 -e MONGO_URI=mongodb://mongo:27017/ yourusername/flask-todo-app:v1.0
```

---

## 🛑 Stopping Everything

```powershell
# If using Docker Compose
docker compose down

# To also remove volumes (deletes MongoDB data)
docker compose down -v

# If using manual commands
docker stop flask_app mongodb
docker rm flask_app mongodb
docker network rm app-network
```

---

## 🗺️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Your Computer (Host)                  │
│                                                         │
│   Browser → http://localhost:5000                       │
│                       │                                 │
│              Port Mapping 5000:5000                     │
│                       │                                 │
│  ┌────────────────────▼──────────────────────────────┐  │
│  │              Docker Network: app-network           │  │
│  │                                                   │  │
│  │  ┌─────────────────┐    ┌──────────────────────┐  │  │
│  │  │  flask_app      │    │  mongodb             │  │  │
│  │  │  (Flask:5000)   │───▶│  (Mongo:27017)       │  │  │
│  │  │                 │    │                      │  │  │
│  │  │  Image: your    │    │  Image: mongo:7.0    │  │  │
│  │  │  custom image   │    │  (from Docker Hub)   │  │  │
│  │  └─────────────────┘    └──────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
              docker push │
                          ▼
                   Docker Hub Registry
              yourusername/flask-todo-app:v1.0
```

---

## 📝 Key Concepts Summary

| Concept | Explanation |
|---|---|
| `FROM python:3.11-slim` | Base image — Python pre-installed |
| `EXPOSE 5000` | Documents port (doesn't actually open it) |
| `-p 5000:5000` | Opens host port 5000 → container port 5000 |
| `app-network` | Bridge network allowing containers to talk |
| `mongo` hostname | Service name used as DNS hostname inside the network |
| `depends_on` | Controls startup order of services |
| `volumes` | Persists database data beyond container lifetime |
| `docker push` | Uploads image to Docker Hub registry |

---

> [!TIP]
> For your submission, take screenshots of: (1) `docker ps` showing both containers running, (2) the app at `localhost:5000`, (3) your image page on Docker Hub.

> [!NOTE]
> Your project is already created at `d:\CLOUD_LAB\docker-lab\`. Just replace `yourusername` with your actual Docker Hub username in the push commands!
