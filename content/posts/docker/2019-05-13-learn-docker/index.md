+++
date = '2019-05-13T20:33:33+08:00'
title = 'Docker Beginner Tutorial: Images, Containers, Registries, and Dockerfile Explained'
description = 'A comprehensive Docker tutorial for beginners covering the three core concepts — images, containers, and registries — along with layered storage, Dockerfile instructions (FROM, RUN, COPY, CMD, ENTRYPOINT), data volumes, and networking fundamentals.'
toc = true
tags = ['Docker', 'Dockerfile', '容器化', 'DevOps', '镜像']
categories = ['Docker']
keywords = ['Docker tutorial', 'Docker beginner guide', 'Dockerfile instructions', 'Docker images containers', 'Docker registry', 'Docker data volumes']
+++

Docker is an open-source container engine built with Go. It lets developers package applications and their dependencies into lightweight, portable containers that run consistently across any Linux host.

## 1. Three Core Concepts

Docker revolves around three fundamental building blocks:

- **Image** — A read-only template used to create containers
- **Container** — A running instance of an image
- **Registry (Repository)** — A service that stores and distributes images

## 2. Images

A Docker image is a special filesystem that bundles everything a container needs at runtime: application code, libraries, resources, configuration files, and runtime parameters (anonymous volumes, environment variables, user settings, etc.). Once built, an image is immutable — its contents never change.

### Layered Storage

An image is not a single monolithic file like an ISO. Instead, it consists of multiple filesystem layers stacked on top of each other using a union filesystem.

During the build process, each instruction creates a new layer. Once a layer is committed, it becomes read-only — any changes in subsequent layers only affect those layers. This is why you should keep each layer minimal and clean up temporary files before the layer is finalized.

## 3. Containers

The relationship between an image and a container is similar to a class and an instance in object-oriented programming. An image is a static definition; a container is a running entity created from that image. Containers can be created, started, stopped, paused, and deleted.

### Container Storage Layer

Containers also use layered storage. When a container runs, Docker creates a thin read-write layer on top of the image's read-only layers. This is the **container storage layer**.

The container storage layer has the same lifecycle as the container itself — when the container is removed, this layer is gone. For this reason, containers should remain **stateless**. Any data that needs to persist should be written to **volumes** or **bind mounts**, which bypass the container storage layer and write directly to the host filesystem (or network storage) for better performance and reliability.

## 4. Docker Registry

After building an image, you can run it on the local host easily. But to use it on other servers, you need a centralized service to store and distribute images — that is what a Docker Registry does.

A single Docker Registry can host multiple **repositories**. Each repository can contain multiple **tags**, and each tag corresponds to a specific image version.

## 5. Docker Commit

The `docker commit` command creates a new image from a container's current state:

```bash
docker commit [OPTIONS] <CONTAINER_ID_OR_NAME> [REPOSITORY[:TAG]]
```

Example:

```bash
docker commit \
  --author "John Doe <john@example.com>" \
  --message "Updated default page" \
  webserver \
  nginx:v2
```

**Avoid using `docker commit` for production images.** It makes images bloated and hard to reproduce. The proper way to build custom images is with a Dockerfile. The `commit` command is mainly useful for learning purposes or preserving a container's state after an incident (e.g., for forensic analysis).

## 6. Dockerfile

A Dockerfile is a plain text file containing a series of instructions. Each instruction creates a new layer in the image, describing how that layer should be built.

### FROM — Base Image

Every Dockerfile must start with a `FROM` instruction to specify the base image:

```dockerfile
FROM ubuntu:22.04
```

Use `FROM scratch` to start from a completely empty image (common for statically compiled Go binaries).

### RUN — Execute Commands

`RUN` executes commands during the build process. It has two forms:

**Shell form:**

```dockerfile
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```

**Exec form:**

```dockerfile
RUN ["executable", "param1", "param2"]
```

**Key insight: Every `RUN` instruction creates a new layer.** You are not writing a shell script — you are defining how each layer should be constructed. Combine related commands with `&&` and use `\` for line continuation to minimize layers:

```dockerfile
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
```

### Building Images

Use `docker build` to create an image from a Dockerfile:

```bash
docker build [OPTIONS] <CONTEXT_PATH>
```

For example, run this from the directory containing your Dockerfile:

```bash
docker build -t nginx:v3 .
```

### Build Context

Docker uses a client-server architecture. When you run `docker build`, the CLI client packages up everything in the specified **context path** and sends it to the Docker daemon. The daemon then uses these files to process `COPY` and `ADD` instructions.

This means that `COPY ./package.json /app/` copies `package.json` from the **build context directory** — not from the directory where you ran the command, and not necessarily from where the Dockerfile lives.

Docker also supports building from Git repositories, tar archives, and stdin.

### COPY — Copy Files

```dockerfile
COPY <src>... <dest>
COPY ["<src>", ... "<dest>"]
```

`COPY` transfers files from the build context into the image. The source can use wildcards:

```dockerfile
COPY hom* /mydir/
COPY hom?.txt /mydir/
```

The destination can be an absolute path or a path relative to `WORKDIR`. If the destination directory does not exist, Docker creates it automatically. File metadata (permissions, timestamps) is preserved.

### ADD — Advanced Copy

`ADD` works like `COPY` but with two extra capabilities:

1. The source can be a **URL** — Docker downloads it automatically (with 600 permissions)
2. If the source is a **tar/gzip/bzip2 archive**, `ADD` automatically extracts it to the destination

Prefer `COPY` for straightforward file copying — it has clearer semantics and better build cache behavior. Only use `ADD` when you need automatic extraction.

### CMD — Default Command

`CMD` specifies the default command to run when the container starts:

```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

Remember: Docker containers are processes, not virtual machines. Applications inside containers must run in the **foreground**. There is no concept of background services in a container.

A common mistake:

```dockerfile
CMD service nginx start
```

This gets interpreted as `CMD ["sh", "-c", "service nginx start"]`. Once the `service` command finishes, `sh` exits, and the container stops. The correct approach is to run the process directly in the foreground.

### ENTRYPOINT — Entry Point

`ENTRYPOINT` also specifies the container's startup command, but it changes how `CMD` behaves. When both are present, `CMD` arguments are passed to `ENTRYPOINT`:

```
<ENTRYPOINT> <CMD>
```

This is useful for two scenarios:

**1. Making the image behave like a command:**

```dockerfile
ENTRYPOINT ["curl", "-s", "https://httpbin.org/get"]
```

Now you can pass additional flags: `docker run myimage -I` appends `-I` as an argument to `curl`.

**2. Running initialization scripts before the main process.**

### ENV — Environment Variables

```dockerfile
ENV NODE_VERSION=18.0.0
```

Environment variables set with `ENV` are available to all subsequent instructions and at container runtime. This makes version upgrades easy — change the variable in one place.

### ARG — Build Arguments

```dockerfile
ARG VERSION=latest
```

`ARG` defines variables that users can pass at build time with `--build-arg`. Unlike `ENV`, `ARG` values are not available at runtime (though they are visible in `docker history` — never store secrets in `ARG`).

### VOLUME — Define Mount Points

```dockerfile
VOLUME /data
```

This tells Docker to automatically create an anonymous volume at `/data` when the container starts, ensuring that writes to this path do not go to the container storage layer. You can override this at runtime:

```bash
docker run -d -v mydata:/data myimage
```

### EXPOSE — Declare Ports

```dockerfile
EXPOSE 8080
```

`EXPOSE` documents which ports the container listens on. It does **not** publish the port — you still need `-p` at runtime to map it to a host port.

### WORKDIR — Set Working Directory

```dockerfile
WORKDIR /app
```

Sets the working directory for all subsequent `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions.

A common beginner mistake:

```dockerfile
RUN cd /app
RUN echo "hello" > world.txt
```

This does **not** create `/app/world.txt` because each `RUN` runs in a separate container. The `cd` in the first `RUN` has no effect on the second. Use `WORKDIR` instead.

### Other Instructions

- **USER** — Set the user for subsequent instructions and container runtime
- **HEALTHCHECK** — Define a command to check container health (returns 0 for healthy, 1 for unhealthy)
- **ONBUILD** — Add a trigger instruction that executes when the image is used as a base for another build

## 7. Migrating Images

Docker provides `docker save` and `docker load` for offline image transfer:

```bash
# Export an image to a tar file
docker save alpine | gzip > alpine-latest.tar.gz

# Import the image on another machine
docker load -i alpine-latest.tar.gz
```

Combined with SSH/SCP, this is useful for air-gapped environments. However, using a registry is generally preferred.

## 8. Removing Images

```bash
docker rmi [OPTIONS] <IMAGE> [IMAGE...]
```

Do not confuse `docker rmi` (remove images) with `docker rm` (remove containers).

Image deletion involves two steps: **Untagged** and **Deleted**. An image can have multiple tags, so removing a tag does not necessarily delete the underlying layers. Actual deletion only occurs when:

1. All tags pointing to the image are removed
2. No other images depend on those layers
3. No containers (running or stopped) use the image

Batch deletion examples:

```bash
# Remove all dangling images
docker rmi $(docker images -q -f dangling=true)

# Remove all redis images
docker rmi $(docker images -q redis)

# Remove images older than a specific one
docker rmi $(docker images -q -f before=mongo:3.2)
```

## 9. Working with Containers

### Starting a Container

When you run `docker run`, Docker performs these steps behind the scenes:

1. Checks for the image locally; pulls from the registry if not found
2. Creates a container from the image
3. Allocates a filesystem with a read-write layer on top of the image
4. Bridges a virtual network interface from the host
5. Assigns an IP address from the pool
6. Runs the specified command
7. Stops the container when the command exits

```bash
# Interactive mode
docker run -it ubuntu:22.04 /bin/bash

# Background (detached) mode
docker run -d ubuntu:22.04
```

### Common Container Commands

```bash
docker logs <container>      # View container logs
docker start <container>     # Start a stopped container
docker stop <container>      # Stop a running container
docker restart <container>   # Restart a container
docker rm <container>        # Remove a stopped container
docker rm $(docker ps -aq)   # Remove all stopped containers
```

### Exporting and Importing Containers

```bash
# Export a container snapshot
docker export <container> > ubuntu.tar

# Import a snapshot as a new image
cat ubuntu.tar | docker import - test/ubuntu:v1.0
```

The difference between `docker load` (image file) and `docker import` (container snapshot): snapshots discard history and metadata, resulting in smaller files. Image files preserve the full layer history.

## 10. Registries

### Docker Hub

The official public registry at [hub.docker.com](https://hub.docker.com/):

```bash
docker search nginx
docker pull nginx
```

### Private Registry

Set up a basic private registry:

```bash
docker run --name=myregistry -d -p 8085:5000 \
  -v /usr/local/programs/docker/myregistry:/var/lib/registry \
  registry
```

Tag and push images:

```bash
docker tag myimage 172.16.166.130:8085/myimage
docker push 172.16.166.130:8085/myimage
```

Browse the catalog:

```bash
curl http://172.16.166.130:8085/v2/_catalog
```

To pull from a private registry using HTTP, add it to `/etc/docker/daemon.json`:

```json
{
    "insecure-registries": [
        "172.16.166.130:8085"
    ]
}
```

## 11. Data Volumes

A data volume is a specially designated directory that bypasses the Union File System, providing several benefits:

- Volumes can be shared and reused across containers
- Changes take effect immediately
- Volume updates do not affect the image
- Volumes persist even after the container is deleted

### Creating Volumes

```bash
# Create and mount a volume inline
docker run -d -P --name web -v /webapp training/webapp

# Mount a host directory
docker run -d -P --name web -v /src/webapp:/opt/webapp training/webapp

# Read-only mount
docker run -d -P --name web -v /src/webapp:/opt/webapp:ro training/webapp
```

Note: Bind-mounting host directories is not supported in Dockerfiles (paths differ across operating systems).

### Inspecting Volumes

```bash
docker inspect web
```

## 12. Data Volume Containers

For data that needs to be shared across multiple containers, create a dedicated **data volume container**:

```bash
# Create the data volume container
docker run -d -v /dbdata --name dbdata training/postgres

# Mount volumes from dbdata into another container
docker run -d --volumes-from dbdata --name db1 training/postgres
```

Even if all containers using the volume are removed, the volume itself persists. To delete a volume, use `docker rm -v` when removing the last container that references it.

### Backup and Restore

```bash
# Backup
docker run --volumes-from dbdata -v $(pwd):/backup ubuntu \
  tar cvf /backup/backup.tar /dbdata

# Restore to a new container
docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
docker run --volumes-from dbdata2 -v $(pwd):/backup ubuntu \
  tar xvf /backup/backup.tar
```

## 13. Networking

### Port Mapping

To make container services accessible from outside, use port mapping:

```bash
# Random host port
docker run -d -P nginx

# Specific host port
docker run -d -p 8081:80 nginx

# Bind to specific IP
docker run -d -p 127.0.0.1:5000:5000 training/webapp

# Random port on specific IP
docker run -d -p 127.0.0.1::5000 training/webapp

# UDP port
docker run -d -p 127.0.0.1:5000:5000/udp training/webapp

# Multiple ports
docker run -d -p 5000:5000 -p 3000:80 training/webapp
```

Check port mappings with `docker port <container>`.

### Container Linking (Legacy)

The `--link` flag creates a secure tunnel between containers:

```bash
# Create a database container
docker run -d --name db training/postgres

# Link a web container to the database
docker run -d -P --name web --link db:db training/webapp
```

Docker exposes connection information through environment variables and `/etc/hosts` entries. The linked container gets variables like `DB_PORT`, `DB_PORT_5432_TCP_ADDR`, etc.

> **Note:** Container linking is a legacy feature. Modern Docker deployments should use **user-defined networks** for inter-container communication.

### Network Architecture

When Docker starts, it creates a `docker0` virtual bridge on the host. This bridge acts as a software switch, forwarding packets between containers and the host network. All containers on the same bridge can communicate with each other, similar to machines connected to a physical switch.

## 14. Docker Architecture

Docker uses a **client-server architecture**. The Docker daemon runs as a background service and accepts requests via a REST API. The `docker` CLI tool communicates with the daemon through this API. The client and server can run on the same machine or communicate remotely over a network socket.

---

## Related Articles

- [Docker Compose Complete Guide: From Basics to Production](/posts/docker/2026-01-19-docker-compose-complete-guide/) — Multi-container orchestration and production best practices
- [Docker Commands Cheat Sheet](/posts/docker/2019-11-14-docker-commands/) — Essential daily reference for Docker commands
- [Nexus3 Private Docker Registry Setup](/posts/docker/2019-06-12-next3-dockerhub/) — Enterprise container registry guide
