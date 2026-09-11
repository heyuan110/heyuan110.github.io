+++
date = '2026-01-19T10:00:00+08:00'
title = 'Docker Compose Complete Guide (2026): Install, Configure, and Deploy Multi-Container Apps'
description = 'Master Docker and Docker Compose from scratch: installation, core concepts, docker-compose.yml deep dive, WordPress and Node.js deployment examples, plus production best practices.'
toc = true
tags = ['Docker', 'Docker Compose', 'Containers', 'DevOps']
categories = ['Docker']
keywords = ['Docker Compose tutorial', 'docker-compose.yml guide', 'Docker for beginners', 'multi-container deployment', 'Docker best practices']
+++
![Docker Complete Guide](docker-cover.webp)

Every developer has heard (or said) this at least once: "But it works on my machine!" Docker was built to eliminate that problem for good. This guide takes you from zero to proficient with Docker and Docker Compose, covering everything you need to deploy real-world multi-container applications.

---

## Part 1: Why Docker Exists

### 1. The Pain Points of Software Deployment

Think of moving to a new apartment. The traditional approach is to disassemble all your furniture, haul it over, reassemble everything, and then discover you're missing a few screws.

Software deployment has the same kinds of headaches:

**Problem 1: Environment Inconsistency**
- Dev machine: Windows + Python 3.8 + MySQL 5.7
- Staging server: Ubuntu + Python 3.9 + MySQL 8.0
- Production: CentOS + Python 3.7 + MySQL 5.6

The developer says "it works," ops says "it's broken in production."

**Problem 2: Dependency Hell**
- Project A requires Node.js 14
- Project B requires Node.js 18
- Project C requires Node.js 16

How do you run all three on the same machine?

**Problem 3: Resource Waste**
- Traditional approach: one VM per application
- Each VM consumes at least 1-2 GB of RAM
- 10 apps = 10 VMs = 10-20 GB just for operating systems

### 2. The Evolution of Virtualization

**Bare Metal Era**
- One server, one application
- Extremely low resource utilization
- Difficult to scale

**Virtual Machine Era (VMware, VirtualBox)**
- Multiple VMs on a single physical host
- Each VM includes a full guest operating system
- Heavy resource usage, slow boot times (minutes)

**Container Era (Docker)**
- Containers share the host kernel
- Lightweight, fast startup (seconds)
- Minimal resource overhead

Here's a side-by-side comparison:

```
┌─────────────────────────────────┬───────────────────────────────┐
│       Virtual Machines          │          Containers           │
├─────────────────────────────────┼───────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐       │  ┌─────┐ ┌─────┐ ┌─────┐     │
│  │App A│ │App B│ │App C│       │  │App A│ │App B│ │App C│     │
│  ├─────┤ ├─────┤ ├─────┤       │  ├─────┤ ├─────┤ ├─────┤     │
│  │Bins │ │Bins │ │Bins │       │  │Bins │ │Bins │ │Bins │     │
│  │Libs │ │Libs │ │Libs │       │  │Libs │ │Libs │ │Libs │     │
│  ├─────┤ ├─────┤ ├─────┤       │  └──┬──┘ └──┬──┘ └──┬──┘     │
│  │Guest│ │Guest│ │Guest│       │     └───────┼───────┘         │
│  │ OS  │ │ OS  │ │ OS  │       │      ┌──────┴──────┐          │
│  └──┬──┘ └──┬──┘ └──┬──┘       │      │   Docker    │          │
│     └───────┼───────┘          │      │   Engine    │          │
│      ┌──────┴──────┐           │      └──────┬──────┘          │
│      │ Hypervisor  │           │             │                  │
│      └──────┬──────┘           │      ┌──────┴──────┐          │
│      ┌──────┴──────┐           │      │   Host OS   │          │
│      │   Host OS   │           │      └──────┬──────┘          │
│      └──────┬──────┘           │      ┌──────┴──────┐          │
│      ┌──────┴──────┐           │      │  Hardware   │          │
│      │  Hardware   │           │      └─────────────┘          │
│      └─────────────┘           │                                │
├─────────────────────────────────┼───────────────────────────────┤
│  Traits:                        │  Traits:                       │
│  • Full OS per VM               │  • Shared host kernel          │
│  • Boot time: minutes           │  • Boot time: seconds          │
│  • Memory: GB-scale             │  • Memory: MB-scale            │
│  • Isolation: strong            │  • Isolation: good             │
└─────────────────────────────────┴───────────────────────────────┘
```

### 3. The Birth of Docker

In **2013**, a PaaS company called dotCloud (later renamed Docker Inc.) open-sourced their internal containerization project. It changed software deployment forever.

**Why Docker took off:**

1. **Standardized packaging** — like shipping containers: no matter what's inside, the outside is a standard size
2. **Lightweight** — shares the host kernel, boots in seconds
3. **Portable** — "Build once, run anywhere"
4. **Version-controlled** — images can be tagged and managed just like code
5. **Rich ecosystem** — Docker Hub hosts millions of ready-to-use images

**Docker at a Glance**

| Feature | Traditional Deployment | Docker Deployment |
|---------|----------------------|-------------------|
| Environment consistency | Manual config, error-prone | Image guarantees identical env |
| Startup speed | Minutes | Seconds |
| Resource usage | GB-scale | MB-scale |
| Isolation | Requires full VM | Native container isolation |
| Scaling | Complex | Simple, one command |

---

## Part 2: Docker Core Concepts

### 4. The Three Pillars

Think of Docker in terms of a shipping analogy:

**Image — The Blueprint**

- A read-only template containing everything an app needs: code, runtime, libraries, environment variables, config files
- A snapshot of a complete environment at a specific point in time
- You can create multiple containers from a single image

**Container — The Running Instance**

- A container is a running instance of an image
- Each container is isolated with its own filesystem, network, and process space
- Containers can be created, started, stopped, and deleted
- Data inside a container is ephemeral by default (unless you use volumes)

**Registry — The Warehouse**

- Stores and distributes images
- Docker Hub is the largest public registry (similar to GitHub for code)
- Organizations can run private registries

### 5. Docker Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                        Docker Architecture                        │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Client                                Docker Host                │
│  ┌─────────────────┐                 ┌───────────────────────────┐│
│  │ docker build    │                 │     Docker Daemon         ││
│  │ docker pull     │  ──REST API──>  │     (dockerd)             ││
│  │ docker run      │                 │  ┌─────────────────────┐  ││
│  └─────────────────┘                 │  │    Containers       │  ││
│                                      │  │ ┌───┐ ┌───┐ ┌───┐   │  ││
│                                      │  │ │ C │ │ C │ │ C │   │  ││
│                                      │  │ └───┘ └───┘ └───┘   │  ││
│                                      │  └─────────────────────┘  ││
│                                      │  ┌─────────────────────┐  ││
│                                      │  │      Images         │  ││
│                                      │  │ ┌───┐ ┌───┐ ┌───┐   │  ││
│                                      │  │ │ I │ │ I │ │ I │   │  ││
│                                      │  │ └───┘ └───┘ └───┘   │  ││
│                                      │  └─────────────────────┘  ││
│                                      └───────────────────────────┘│
│                                                    ▲               │
│                                                    │               │
│                                               pull/push            │
│                                                    │               │
│                                                    ▼               │
│                                      ┌───────────────────────────┐│
│                                      │       Registry            ││
│                                      │     (Docker Hub)          ││
│                                      │  ┌─────────────────────┐  ││
│                                      │  │ nginx, mysql, redis │  ││
│                                      │  │ node, python, ...   │  ││
│                                      │  └─────────────────────┘  ││
│                                      └───────────────────────────┘│
└───────────────────────────────────────────────────────────────────┘
```

**Components:**

- **Docker Client** — the CLI tool you use to interact with the Docker Daemon
- **Docker Daemon (dockerd)** — the background service that manages images, containers, networks, and storage
- **Docker Registry** — image repository for storing and distributing images

---

## Part 3: Getting Started with Docker

### 6. Installing Docker

#### macOS

The recommended approach is Docker Desktop:

1. Visit the [Docker website](https://www.docker.com/products/docker-desktop/)
2. Download Docker Desktop for Mac
3. Drag to install
4. Launch Docker Desktop

Or use Homebrew:

```bash
brew install --cask docker
```

#### Linux (Ubuntu/Debian)

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group (avoids needing sudo)
sudo usermod -aG docker $USER
```

#### Linux (CentOS/RHEL)

```bash
# Install prerequisites
sudo yum install -y yum-utils

# Add the repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker Engine
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to the docker group
sudo usermod -aG docker $USER
```

#### Windows

1. Make sure WSL 2 is enabled
2. Download and install Docker Desktop for Windows
3. Enable WSL 2 integration in settings

#### Verify the Installation

```bash
# Check version
docker --version
# Docker version 24.0.7, build afdd53b

# View detailed info
docker info

# Run the test container
docker run hello-world
```

### 7. Your First Container

Let's run the classic hello-world:

```bash
docker run hello-world
```

**What happens behind the scenes?**

```
┌─────────────────────────────────────────────────────────────┐
│            docker run hello-world — step by step            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. The Docker client sends the command to the Daemon       │
│                    │                                        │
│                    ▼                                        │
│  2. The Daemon checks for a local hello-world image         │
│                    │                                        │
│           ┌───────┴───────┐                                 │
│           │  Image found  │                                 │
│           │   locally?    │                                 │
│           └───────┬───────┘                                 │
│           No      │       Yes                               │
│           │       └────────────────┐                        │
│           ▼                        │                        │
│  3. Pulls the image from Docker Hub│                        │
│           │                        │                        │
│           └────────────────────────┤                        │
│                                    ▼                        │
│  4. Creates a container from the image                      │
│                    │                                        │
│                    ▼                                        │
│  5. Runs the container, prints "Hello from Docker!"         │
│                    │                                        │
│                    ▼                                        │
│  6. Container finishes and stops automatically              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 8. Working with Images

#### Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `docker images` | List local images | `docker images` |
| `docker pull` | Pull an image | `docker pull nginx:latest` |
| `docker search` | Search for images | `docker search mysql` |
| `docker rmi` | Remove an image | `docker rmi nginx:latest` |
| `docker tag` | Tag an image | `docker tag nginx:latest myrepo/nginx:v1` |
| `docker build` | Build an image | `docker build -t myapp:v1 .` |
| `docker push` | Push an image | `docker push myrepo/myapp:v1` |

#### Hands-On Examples

```bash
# Search for nginx images
docker search nginx

# Pull the official nginx image
docker pull nginx:latest

# List local images
docker images

# Inspect image details
docker inspect nginx:latest

# View image layer history
docker history nginx:latest

# Remove an image
docker rmi nginx:latest
```

### 9. Working with Containers

#### Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `docker run` | Create and start a container | `docker run -d nginx` |
| `docker ps` | List running containers | `docker ps` |
| `docker ps -a` | List all containers | `docker ps -a` |
| `docker start` | Start a stopped container | `docker start container_id` |
| `docker stop` | Stop a container | `docker stop container_id` |
| `docker restart` | Restart a container | `docker restart container_id` |
| `docker rm` | Remove a container | `docker rm container_id` |
| `docker exec` | Run a command in a container | `docker exec -it container_id bash` |
| `docker logs` | View container logs | `docker logs -f container_id` |

#### Hands-On Examples

```bash
# Run an nginx container
# -d: detached (background)
# -p: port mapping (host:container)
# --name: container name
docker run -d -p 8080:80 --name my-nginx nginx

# List running containers
docker ps

# View logs
docker logs my-nginx

# Follow logs in real time
docker logs -f my-nginx

# Open a shell inside the container
docker exec -it my-nginx bash

# Run a single command inside the container
docker exec my-nginx cat /etc/nginx/nginx.conf

# Stop the container
docker stop my-nginx

# Start it again
docker start my-nginx

# Stop and remove
docker stop my-nginx && docker rm my-nginx

# Force-remove a running container
docker rm -f my-nginx
```

#### Common `docker run` Flags

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

# Frequently used OPTIONS
-d, --detach          # Run in background
-p, --publish         # Port mapping (host_port:container_port)
-v, --volume          # Mount a volume (host_path:container_path)
-e, --env             # Set environment variable
--name                # Assign a container name
--restart             # Restart policy: no, on-failure, always, unless-stopped
--network             # Specify a network
-it                   # Interactive terminal (-i keeps STDIN open, -t allocates a pseudo-TTY)
--rm                  # Automatically remove the container when it stops
```

### 10. Data Persistence

Containers are stateless by default — delete the container, lose the data. Docker offers two persistence mechanisms:

#### Volumes

Managed by Docker. This is the recommended approach.

```bash
# Create a volume
docker volume create my-data

# List volumes
docker volume ls

# Use a volume
docker run -d \
  --name mysql-db \
  -v my-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=123456 \
  mysql:8.0

# Inspect a volume
docker volume inspect my-data

# Remove a volume
docker volume rm my-data

# Remove all unused volumes
docker volume prune
```

#### Bind Mounts

Mount a host directory directly into the container.

```bash
# Mount the current directory
docker run -d \
  --name nginx-web \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html \
  nginx

# Read-only mount (container cannot write)
docker run -d \
  --name nginx-web \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx
```

#### Volumes vs Bind Mounts

| Feature | Volumes | Bind Mounts |
|---------|---------|-------------|
| Managed by | Docker | You |
| Storage location | Docker's internal directory | Any host path |
| Portability | High | Depends on host paths |
| Best for | Persistent data (databases) | Config files, source code sharing |

### 11. Networking

Docker provides several network modes:

#### Network Modes

| Mode | Description |
|------|-------------|
| bridge | Default. Containers connect through a virtual bridge |
| host | Container shares the host's network stack directly |
| none | Networking disabled |
| container | Share another container's network namespace |

#### Common Commands

```bash
# List networks
docker network ls

# Create a custom network
docker network create my-network

# Run a container on a specific network
docker run -d --name app --network my-network nginx

# Connect an existing container to a network
docker network connect my-network container_name

# Inspect a network
docker network inspect my-network

# Remove a network
docker network rm my-network
```

#### Container-to-Container Communication

Containers on the same network can reach each other by name:

```bash
# Create a network
docker network create app-network

# Start MySQL
docker run -d \
  --name mysql \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=123456 \
  mysql:8.0

# Start the app — it can reach the database using the hostname "mysql"
docker run -d \
  --name app \
  --network app-network \
  -e DATABASE_HOST=mysql \
  my-app
```

---

## Part 4: Dockerfile Deep Dive

### 12. What Is a Dockerfile?

A Dockerfile is a text file containing step-by-step instructions for building a Docker image. Think of it as a recipe that tells Docker exactly how to assemble the environment your app needs.

```dockerfile
# A simple Dockerfile example
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
```

### 13. Key Instructions Explained

#### FROM — Base Image

Every Dockerfile starts with `FROM`, which specifies the base image:

```dockerfile
# Official Node.js image
FROM node:18-alpine

# Official Python image
FROM python:3.11-slim

# Minimal Alpine image
FROM alpine:3.18

# Build from scratch (empty base)
FROM scratch
```

#### RUN — Execute Commands

Run commands during the image build process:

```dockerfile
# Shell form
RUN apt-get update && apt-get install -y curl

# Exec form
RUN ["apt-get", "install", "-y", "curl"]

# Multi-line (recommended — fewer layers)
RUN apt-get update && \
    apt-get install -y \
    curl \
    vim \
    git && \
    rm -rf /var/lib/apt/lists/*
```

#### COPY vs ADD

```dockerfile
# COPY — straightforward file copy
COPY package.json /app/
COPY . /app/

# ADD — also supports auto-extraction and remote URLs (not recommended; prefer COPY)
ADD archive.tar.gz /app/
ADD https://example.com/file.txt /app/
```

**Recommendation:** Prefer `COPY`. It's explicit and predictable.

#### WORKDIR — Working Directory

```dockerfile
WORKDIR /app
# All subsequent commands run inside /app
```

#### ENV — Environment Variables

```dockerfile
ENV NODE_ENV=production
ENV APP_PORT=3000

# Multiple variables
ENV NODE_ENV=production \
    APP_PORT=3000
```

#### EXPOSE — Declare Ports

```dockerfile
# Document which ports the container listens on
EXPOSE 3000
EXPOSE 80 443
```

Note: `EXPOSE` is purely documentation. You still need `-p` at runtime to publish ports.

#### CMD vs ENTRYPOINT

This is the most commonly confused pair:

```dockerfile
# CMD — default command (easily overridden by docker run arguments)
CMD ["node", "app.js"]
CMD ["npm", "start"]

# ENTRYPOINT — fixed command (arguments are appended, not replaced)
ENTRYPOINT ["python", "app.py"]
```

**Comparison:**

| Scenario | CMD | ENTRYPOINT |
|----------|-----|------------|
| Overridden by `docker run` args | Completely replaced | Args appended |
| Best for | Default commands with flexibility | Fixed entry point with parameterization |

**Best practice — combine them:**

```dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]

# docker run myapp                  -> python app.py --port 8080
# docker run myapp --port 3000      -> python app.py --port 3000
```

#### Multi-Stage Builds

The key technique for keeping final images small:

```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
# Copy only the build output
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm install --production
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### 14. Dockerfile Best Practices

#### Minimize Image Size

```dockerfile
# 1. Use alpine base images
FROM node:18-alpine  # instead of node:18

# 2. Use multi-stage builds (see above)

# 3. Combine RUN commands and clean up caches
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# 4. Use .dockerignore to exclude unnecessary files
```

**.dockerignore example:**

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
*.md
```

#### Leverage the Build Cache

Place instructions that change less frequently earlier in the Dockerfile:

```dockerfile
FROM node:18-alpine
WORKDIR /app

# Copy package.json first (rarely changes)
COPY package*.json ./
RUN npm install

# Then copy source code (changes often)
COPY . .

RUN npm run build
```

#### Security Considerations

```dockerfile
# 1. Don't run as root
FROM node:18-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# 2. Never store secrets in the image
# Use environment variables or a secrets manager instead

# 3. Pin specific version tags, not "latest"
FROM node:18.19.0-alpine  # instead of node:latest
```

---

## Part 5: Docker Compose In-Depth

### 15. Why Docker Compose?

When your application involves multiple containers working together (e.g., a web app + database + cache), managing them manually becomes painful:

```bash
# The nightmare of managing multiple containers by hand
docker network create myapp
docker run -d --name mysql --network myapp -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0
docker run -d --name redis --network myapp redis:alpine
docker run -d --name app --network myapp -p 3000:3000 -e DB_HOST=mysql -e REDIS_HOST=redis myapp
```

Docker Compose lets you define and run multi-container applications with a single YAML file and a single command.

### 16. Docker Compose Basics

#### Installation

Docker Desktop includes Docker Compose out of the box. If you installed Docker Engine on Linux separately, the Compose plugin is included.

Verify:

```bash
docker compose version
```

#### Basic docker-compose.yml Structure

```yaml
# Version declaration (optional in modern Docker Compose)
version: "3.8"

# Service definitions
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: 123456

# Network definitions (optional)
networks:
  default:
    driver: bridge

# Volume definitions (optional)
volumes:
  db-data:
```

### 17. Configuration Reference

#### services — Defining Services

```yaml
services:
  # Service name
  app:
    # Use a pre-built image
    image: node:18-alpine

    # Or build from a Dockerfile
    build:
      context: .
      dockerfile: Dockerfile

    # Container name
    container_name: my-app

    # Port mappings
    ports:
      - "3000:3000"      # host_port:container_port
      - "3001:3001"

    # Environment variables
    environment:
      - NODE_ENV=production
      - DB_HOST=mysql
    # Or load from a file
    env_file:
      - .env

    # Volume mounts
    volumes:
      - ./src:/app/src        # bind mount
      - node_modules:/app/node_modules  # named volume

    # Service dependencies
    depends_on:
      - mysql
      - redis

    # Restart policy
    restart: unless-stopped

    # Network
    networks:
      - app-network

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

#### networks — Network Configuration

```yaml
services:
  app:
    networks:
      - frontend
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # internal only, no external access
```

#### volumes — Data Volumes

```yaml
services:
  mysql:
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
    driver: local
```

#### Full Configuration Example

```yaml
version: "3.8"

services:
  app:
    build: .
    container_name: my-app
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
      DB_HOST: mysql
      DB_PORT: 3306
      DB_NAME: myapp
      REDIS_HOST: redis
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./logs:/app/logs
    networks:
      - app-network
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-123456}
      MYSQL_DATABASE: myapp
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: redis-cache
    volumes:
      - redis-data:/data
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  mysql-data:
  redis-data:
```

### 18. Essential Commands

| Command | Description |
|---------|-------------|
| `docker compose up` | Create and start all services |
| `docker compose up -d` | Run in detached mode |
| `docker compose down` | Stop and remove all containers |
| `docker compose down -v` | Also remove volumes |
| `docker compose ps` | List service status |
| `docker compose logs` | View logs |
| `docker compose logs -f app` | Follow logs for a specific service |
| `docker compose exec app bash` | Open a shell in a running service |
| `docker compose build` | Build images |
| `docker compose build --no-cache` | Build without cache |
| `docker compose restart` | Restart all services |
| `docker compose stop` | Stop services (without removing) |
| `docker compose start` | Start previously stopped services |
| `docker compose pull` | Pull the latest images |

---

## Part 6: Real-World Examples

### 19. Example 1: Nginx Static Website

The simplest starting point:

**Directory structure:**

```
project/
├── docker-compose.yml
└── html/
    └── index.html
```

**docker-compose.yml:**

```yaml
version: "3.8"

services:
  nginx:
    image: nginx:alpine
    container_name: nginx-web
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    restart: unless-stopped
```

**html/index.html:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Hello Docker</title>
</head>
<body>
    <h1>Hello from Docker!</h1>
</body>
</html>
```

**Run it:**

```bash
docker compose up -d
# Visit http://localhost
```

### 20. Example 2: WordPress Blog

**docker-compose.yml:**

```yaml
version: "3.8"

services:
  wordpress:
    image: wordpress:latest
    container_name: wordpress
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: mysql
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress_password
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress-data:/var/www/html
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - wp-network
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    container_name: wordpress-db
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress_password
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - wp-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

networks:
  wp-network:
    driver: bridge

volumes:
  wordpress-data:
  mysql-data:
```

**Run it:**

```bash
docker compose up -d
# Visit http://localhost:8080 to complete the WordPress setup wizard
```

### 21. Example 3: Node.js + MySQL + Redis Dev Environment

**Directory structure:**

```
project/
├── docker-compose.yml
├── .env
├── Dockerfile
├── package.json
└── src/
    └── index.js
```

**docker-compose.yml:**

```yaml
version: "3.8"

services:
  app:
    build: .
    container_name: node-app
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: development
      DB_HOST: mysql
      DB_PORT: 3306
      DB_NAME: ${DB_NAME:-myapp}
      DB_USER: ${DB_USER:-root}
      DB_PASSWORD: ${DB_PASSWORD:-123456}
      REDIS_HOST: redis
      REDIS_PORT: 6379
    volumes:
      - ./src:/app/src          # hot reload: mount source code
      - /app/node_modules       # protect node_modules
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - dev-network
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    container_name: mysql-db
    ports:
      - "3306:3306"  # expose for local dev tools
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD:-123456}
      MYSQL_DATABASE: ${DB_NAME:-myapp}
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - dev-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"  # expose for local dev tools
    volumes:
      - redis-data:/data
    networks:
      - dev-network
    restart: unless-stopped

networks:
  dev-network:
    driver: bridge

volumes:
  mysql-data:
  redis-data:
```

**Dockerfile:**

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

EXPOSE 3000

# Use nodemon for hot reload in development
CMD ["npm", "run", "dev"]
```

**.env:**

```
DB_NAME=myapp
DB_USER=root
DB_PASSWORD=123456
```

### 22. Example 4: Lightweight Log Collection (Loki + Grafana)

Compared to the ELK stack, Loki + Grafana is much lighter and works well for small-to-medium projects.

**docker-compose.yml:**

```yaml
version: "3.8"

services:
  # Log aggregation
  loki:
    image: grafana/loki:2.9.0
    container_name: loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yml:/etc/loki/local-config.yaml
      - loki-data:/loki
    command: -config.file=/etc/loki/local-config.yaml
    networks:
      - monitoring
    restart: unless-stopped

  # Log collection agent
  promtail:
    image: grafana/promtail:2.9.0
    container_name: promtail
    volumes:
      - ./promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml
    networks:
      - monitoring
    restart: unless-stopped

  # Visualization dashboard
  grafana:
    image: grafana/grafana:10.0.0
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - loki
    networks:
      - monitoring
    restart: unless-stopped

  # Demo app (generates logs)
  app:
    image: nginx:alpine
    container_name: demo-app
    ports:
      - "80:80"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - monitoring
    restart: unless-stopped

networks:
  monitoring:
    driver: bridge

volumes:
  loki-data:
  grafana-data:
```

**loki-config.yml:**

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: false
  retention_period: 0s
```

**promtail-config.yml:**

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*log
    pipeline_stages:
      - json:
          expressions:
            output: log
            stream: stream
            time: time
      - output:
          source: output
```

---

## Part 7: Advanced Topics and Best Practices

### 23. Production Considerations

#### Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

#### Log Management

```yaml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "100m"   # max size per log file
        max-file: "5"      # number of files to retain
```

#### Security Hardening

```yaml
services:
  app:
    # Run as non-root user
    user: "1000:1000"

    # Read-only filesystem
    read_only: true

    # Writable temp directory
    tmpfs:
      - /tmp

    # Security options
    security_opt:
      - no-new-privileges:true
```

### 24. Troubleshooting Common Issues

#### Container Won't Start

```bash
# Check container logs
docker logs container_name

# Inspect container details
docker inspect container_name

# Common causes:
# 1. Port conflict
# 2. Volume permission issues
# 3. Dependency services not ready
```

#### Network Connectivity Problems

```bash
# Check networks
docker network ls
docker network inspect network_name

# Test connectivity between containers
docker exec container1 ping container2

# Common causes:
# 1. Containers not on the same network
# 2. Typo in service name
# 3. Port not exposed
```

#### Running Out of Disk Space

```bash
# Check disk usage
docker system df

# Clean up unused resources
docker system prune

# Clean everything (including unused images)
docker system prune -a

# Clean up volumes
docker volume prune
```

### 25. The Docker Ecosystem and Beyond

#### Kubernetes at a Glance

When you're running dozens or hundreds of containers, Docker Compose is no longer enough. Kubernetes (K8s) is the industry standard for container orchestration:

- Auto-scaling
- Service discovery and load balancing
- Rolling updates and rollbacks
- Self-healing

#### Docker Swarm

Docker's built-in orchestration tool, simpler than Kubernetes:

```bash
# Initialize Swarm
docker swarm init

# Deploy a stack
docker stack deploy -c docker-compose.yml myapp
```

#### Cloud-Native Trends

- **Container runtimes**: containerd and CRI-O are gradually replacing Docker Engine as the underlying runtime
- **Serverless containers**: AWS Fargate, Google Cloud Run
- **Service mesh**: Istio, Linkerd

---

## Summary

Here's a quick recap of the key takeaways:

**Docker Core Concepts:**
- **Images** — standardized, portable application packages
- **Containers** — running instances of images
- **Registries** — centralized storage and distribution for images

**Docker Compose Value Proposition:**
- Define multi-container applications in a single YAML file
- Spin up entire application stacks with one command
- Streamline development, testing, and deployment workflows

**Best Practices:**
- Use multi-stage builds to minimize image size
- Use `.dockerignore` to exclude unnecessary files
- Leverage the build cache by ordering instructions wisely
- Set resource limits and log rotation policies in production

**Further Reading:**
- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)

Container technology is now a fundamental part of modern software development. Mastering Docker and Docker Compose is your gateway to the cloud-native world.

---

## Related Articles

- [Docker 入门指南：核心概念、安装配置与容器化实践](/posts/docker/2019-05-13-learn-docker/) - Docker 基础概念与入门教程
- [Docker 常用命令速查手册](/posts/docker/2019-11-14-docker-commands/) - 日常开发必备命令参考
- [使用 Nexus3 搭建 Docker 私有镜像仓库](/posts/docker/2019-06-12-next3-dockerhub/) - 企业级私有仓库搭建方案

---

## Related Reading

- [docker-compose.yml 详解](/posts/docker/2026-01-24-docker-compose-yml-explained/)
- [Docker 常用命令速查](/posts/docker/2019-11-14-docker-commands/)
