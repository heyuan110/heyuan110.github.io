+++
date = '2019-11-14T20:37:13+08:00'
title = 'Docker Commands Cheat Sheet: Images, Containers, Networks, and Volumes'
description = 'A practical Docker command reference covering image management, container lifecycle, port mapping, volume mounting, and ready-to-use run commands for MySQL, Nginx, Redis, MongoDB, Prometheus, and Grafana.'
toc = true
tags = ['Docker', '命令行', '容器', '运维', '速查手册']
categories = ['Docker']
keywords = ['Docker commands', 'Docker cheat sheet', 'docker run examples', 'Docker container commands', 'Docker image commands', 'Docker volume commands']
+++

A quick-reference guide to the Docker commands you will use most often in daily development and operations work.

## 1. Docker Service Management

```bash
# Start Docker
service docker start

# Stop Docker
service docker stop

# Restart Docker
service docker restart
```

## 2. Image Management

### Pulling Images

```bash
docker pull [OPTIONS] NAME[:TAG|@DIGEST]

# Example
docker pull ubuntu:22.04
```

### Listing Images

```bash
# List all images
docker images
docker image ls

# Show image digests
docker images --digests

# List specific images
docker image ls redis

# Check disk usage (images, containers, volumes)
docker system df

# List dangling images (untagged)
docker image ls -f dangling=true

# Remove dangling images
docker image prune
```

### Removing Images

```bash
# Remove by full ID
docker image rm 578c3e61a98c

# Remove by short ID
docker image rm 578c3

# Remove by name
docker image rm redis

# Remove all images
docker image rm $(docker image ls -q)

# Remove all redis images
docker image rm $(docker image ls -q redis)

# Remove all dangling images
docker rmi $(docker images -q -f dangling=true)
```

### Cleanup Shortcuts

```bash
# Stop all exited containers
docker ps -a | grep "Exited" | awk '{print $1}' | xargs docker stop

# Remove all exited containers
docker ps -a | grep "Exited" | awk '{print $1}' | xargs docker rm

# Remove all <none> images
docker images | grep none | awk '{print $3}' | xargs docker rmi
```

## 3. Container Management

### Creating Containers

**Run in background (detached mode):**

```bash
docker run --name mynginx -d nginx:latest
```

- `--name` assigns a container name
- `-d` runs in the background

**With random port mapping:**

```bash
docker run -P -d nginx:latest
```

- `-P` maps all exposed ports to random host ports

**With specific port and volume mapping:**

```bash
docker run -p 80:80 -v /data:/data -d nginx:latest
```

- `-p host:container` maps a specific port
- `-v host_path:container_path` mounts a host directory (must be absolute path)

**Bind to a specific IP:**

```bash
docker run -p 127.0.0.1:80:8080/tcp ubuntu bash
```

**Interactive mode:**

```bash
docker run -it nginx:latest /bin/bash
```

- `-i` keeps stdin open
- `-t` allocates a pseudo-TTY

### Common Container Commands

```bash
# List all containers (including stopped)
docker ps -a

# List running containers
docker ps

# Start a stopped container
docker start <container>

# Stop a running container
docker stop <container>

# Kill all running containers
docker kill $(docker ps -a -q)

# Restart a container
docker restart <container>

# Remove a stopped container
docker rm <container>

# Remove all stopped containers
docker rm $(docker ps -a -q)
```

### Copying Files

```bash
# Copy from host to container
docker cp /www/myfiles test-container:/www/

# Copy from container to host
docker cp test-container:/www/myfiles /local/path/
```

### Finding Container IP

```bash
# Method 1: Enter the container and check /etc/hosts
docker exec -it <container> cat /etc/hosts

# Method 2: Use docker inspect
docker inspect <container>
```

## Common Docker Run Examples

### 1. Grafana

```bash
# Download the default config template first
wget https://raw.githubusercontent.com/grafana/grafana/master/conf/defaults.ini
# Rename to grafana.ini and customize

docker run -d --name=grafana \
  -p 3000:3000 \
  -v /usr/local/programs/grafana/data:/var/lib/grafana \
  -v /usr/local/programs/grafana/log:/var/log/grafana \
  -v /usr/local/programs/grafana/conf/grafana.ini:/etc/grafana/grafana.ini \
  -e "GF_SERVER_ROOT_URL=http://your-server:3000" \
  -e "GF_SECURITY_ADMIN_PASSWORD=your-password" \
  grafana/grafana
```

### 2. Portainer

```bash
docker run -d -p 9000:9000 \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name portainer \
  portainer/portainer-ce
```

### 3. Prometheus

```bash
# Download default config
wget https://raw.githubusercontent.com/prometheus/prometheus/master/documentation/examples/prometheus.yml

# Basic setup
docker run -d --name=prometheus \
  -p 9090:9090 \
  -v /usr/local/programs/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v /usr/local/programs/prometheus/data:/prometheus \
  prom/prometheus

# With alerting rules
docker run -d --name=prometheus \
  -p 9090:9090 \
  -v /usr/local/programs/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v /usr/local/programs/prometheus/alert.rules:/etc/prometheus/alert.rules \
  -v /usr/local/programs/prometheus/data:/prometheus \
  prom/prometheus

# Alertmanager
docker run -d --name=alertmanager \
  -p 9093:9093 \
  -v /usr/local/programs/prometheus/alertmanager/config.yml:/etc/alertmanager/config.yml \
  prom/alertmanager
```

### 4. MySQL

```bash
# MySQL 5.7
docker run -d \
  -p 3306:3306 \
  --name mysql \
  -v /usr/local/programs/mysql/conf:/etc/mysql/conf.d \
  -v /usr/local/programs/mysql/logs:/logs \
  -v /usr/local/programs/mysql/data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=your-password \
  mysql:5.7
```

Key flags explained:
- `-p 3306:3306` — Maps MySQL port to the host
- `-v .../data:/var/lib/mysql` — Persists database files on the host
- `-e MYSQL_ROOT_PASSWORD` — Sets the root password on first run

### 5. Nginx

```bash
docker run -d -p 80:80 --name nginx \
  -v /var/www/html:/usr/share/nginx/html \
  -v /usr/local/programs/nginx/conf.d:/etc/nginx/conf.d \
  -v /usr/local/programs/nginx/log:/var/log/nginx \
  nginx:latest
```

### 6. MongoDB

```bash
# Linux
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v /usr/local/programs/mongodb:/data/db \
  mongo:latest

# Windows (use named volume to avoid permission issues)
docker volume create --name=mongodata
docker run -d --name mongodb -p 27017:27017 -v mongodata:/data/db mongo:latest
```

Volume management commands:

```bash
# List all volumes
docker volume ls

# Inspect a volume
docker volume inspect <volume_name>
```

### 7. Redis

```bash
docker run --name redis -d \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:latest
```

### 8. PHP-FPM

```bash
docker run -d -p 9000:9000 --name php-fpm \
  -v /var/www/html:/var/www/html \
  -v /usr/local/programs/php/conf:/usr/local/etc/php \
  php:8.2-fpm
```

---

## Related Articles

- [Docker Beginner Tutorial: Images, Containers, Registries, and Dockerfile Explained](/posts/docker/2019-05-13-learn-docker/) — Core Docker concepts and getting started
- [Docker Compose Complete Guide: From Basics to Production](/posts/docker/2026-01-19-docker-compose-complete-guide/) — Multi-container orchestration and best practices
- [Nexus3 Private Docker Registry Setup](/posts/docker/2019-06-12-next3-dockerhub/) — Enterprise container registry guide
