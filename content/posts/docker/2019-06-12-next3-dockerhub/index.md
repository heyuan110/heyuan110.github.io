+++
date = '2019-06-12T20:50:36+08:00'
title = 'Nexus3 Private Docker Registry Setup: Enterprise Container Registry Guide'
description = 'Step-by-step guide to setting up an enterprise Docker private registry with Nexus3, covering hosted, proxy, and group repository types, image push/pull workflows, and client-side insecure-registries configuration.'
toc = true
tags = ['Docker', 'Nexus3', 'Registry', '私有仓库', 'DevOps']
categories = ['Docker']
keywords = ['Nexus3 Docker registry', 'private Docker registry', 'Docker hosted proxy group', 'enterprise container registry', 'Nexus3 setup guide']
+++

[Nexus Repository Manager](https://www.sonatype.com/nexus-repository-oss) is a widely used artifact repository originally built for Maven. Beyond Maven, Nexus 3 supports many formats including Docker, npm, PyPI, and more. For Docker specifically, Nexus 3 lets you host private images, proxy Docker Hub, and group multiple registries behind a single endpoint — making it an excellent choice for enterprise container image management.

## 1. Prerequisites

- **OS:** Ubuntu 16.04 (or any Linux with Docker installed)
- **Docker:** 18.02.0-ce or later

## 2. Pull the Nexus 3 Image

```bash
docker pull sonatype/nexus3
```

## 3. Start the Nexus 3 Container

```bash
docker run -id --privileged=true \
  --name=nexus3 \
  --restart=always \
  -p 9500:8081 \
  -p 9501:9501 \
  -p 9502:9502 \
  -p 9503:9503 \
  -v /usr/local/programs/nexus3/nexus-data:/nexus-data \
  sonatype/nexus3:latest
```

Note the multiple port mappings — each serves a different purpose:

| Port | Type | Purpose |
|------|------|---------|
| 9500 | Nexus Web UI | Administration dashboard (proxied to internal port 8081) |
| 9501 | Docker (hosted) | Private registry — supports both push and pull |
| 9502 | Docker (proxy) | Proxies a remote registry (e.g., Docker Hub) — pull only |
| 9503 | Docker (group) | Combines hosted + proxy — pull only |

In practice, **ops teams push images via port 9501**, while **developers pull images via port 9503** (the group endpoint). All pull operations can be configured for anonymous access.

The `-v` flag mounts a host directory for persistent data storage, so your registry data survives container restarts.

## 4. Configure the Private Registry

Open `http://localhost:9500` in your browser. The default credentials are `admin` / `admin123`.

### Repository Types

Nexus 3 supports three types of Docker repositories:

- **Hosted** — Stores images you build and push internally
- **Proxy** — Caches images pulled from a remote registry (like Docker Hub), saving bandwidth on subsequent pulls
- **Group** — Combines multiple hosted and proxy repositories behind a single URL, so clients only need one endpoint

### Setup Steps

1. **Create blob stores** for each repository type before creating the repositories themselves
2. **Create repositories** and assign each one to its blob store
3. **Create the group** repository, adding the hosted and proxy repos. Set priority so that hosted images take precedence over proxied ones

**Important:** If you enable anonymous pull access, navigate to **Security > Realms** (`http://localhost:9500/#admin/security/realms`) and activate the **Docker Bearer Token Realm**. Without this, anonymous `docker pull` commands will fail with a permission error.

## 5. Client-Side Docker Configuration

To pull from or push to a private registry over HTTP (not HTTPS), you need to tell Docker to trust the registry as "insecure."

### macOS and Windows

Open Docker Desktop settings, go to **Docker Engine** (or **Daemon**), and add the registry URLs to `insecure-registries`:

```json
{
  "insecure-registries": [
    "localhost:9503"
  ]
}
```

If you also need to push images, add `localhost:9501` as well. Restart Docker.

### Ubuntu / Linux

Edit `/etc/docker/daemon.json`:

```json
{
    "insecure-registries": [
        "localhost:9501",
        "localhost:9503"
    ]
}
```

Then restart Docker:

```bash
sudo service docker restart
```

## 6. Managing Images

### Pushing Images

First, log in to the hosted registry:

```bash
docker login localhost:9501
```

Then tag and push your image. For example, to push a local `php:7.0` image:

```bash
# Tag the image for your private registry
docker tag php:7.0 localhost:9501/php:7.0

# Push to the hosted registry
docker push localhost:9501/php:7.0
```

You can verify the upload by browsing to `http://localhost:9500/#browse/browse`.

### Pulling Images

Pull through the group endpoint (port 9503), which checks the hosted registry first, then falls back to the proxy:

```bash
docker pull localhost:9503/php:7.0
```

### Searching Images

Search across all repositories in the group:

```bash
docker search localhost:9503/php
```

Results are returned in the priority order you configured in the group repository.

---

## Related Articles

- [Docker Beginner Tutorial: Images, Containers, Registries, and Dockerfile Explained](/posts/docker/2019-05-13-learn-docker/) — Core Docker concepts and getting started
- [Docker Compose Complete Guide: From Basics to Production](/posts/docker/2026-01-19-docker-compose-complete-guide/) — Multi-container orchestration and best practices
- [Docker Commands Cheat Sheet](/posts/docker/2019-11-14-docker-commands/) — Essential daily reference for Docker commands
