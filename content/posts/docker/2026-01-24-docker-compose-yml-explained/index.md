+++
date = '2026-01-24'
lastmod = '2026-02-23T10:00:00+08:00'
draft = false
title = 'Docker Compose Tutorial: docker-compose.yml Explained with Real Examples (2026)'
description = 'Complete Docker Compose tutorial covering every docker-compose.yml field — services, volumes, networks, healthcheck, ports — with a WordPress + MySQL hands-on example and production-ready templates.'
toc = true
tags = ['Docker', 'Docker Compose', 'Containerization', 'Tutorial', 'YAML']
categories = ['AI Guides']
keywords = ['docker compose tutorial', 'docker-compose.yml explained', 'docker compose configuration', 'compose.yaml', 'docker compose yml', 'docker compose getting started', 'docker compose volumes', 'docker compose networks', 'docker compose ports', 'container orchestration', 'docker compose 2026', 'docker compose yaml tutorial', 'how to write docker-compose.yml', 'docker compose services', 'docker compose healthcheck']
+++

Docker Compose is the go-to tool for running multi-container applications, and **docker-compose.yml** (now officially `compose.yaml`) is its configuration file. Whether you are picking up containers for the first time or brushing up on the finer details, this tutorial walks you through every field you will actually use.

We will cover every key directive in compose.yaml — services, volumes, networks, ports, environment, healthcheck — and put them into practice with a WordPress + MySQL stack you can spin up in seconds. Pair this guide with the [Docker Command Cheat Sheet](/posts/docker/2019-11-14-docker-commands/) for an even smoother workflow.

A compose file can look intimidating at first glance — colons, indentation, nested keys everywhere. It is actually straightforward once you see the pattern. Let's break it down piece by piece.

> **Heads up:** The old `docker-compose` binary (hyphenated) was a standalone Python tool that **reached end-of-life in July 2023**. The replacement is `docker compose` (space-separated), a Go-based plugin built into the Docker CLI. It is faster, better maintained, and the only version covered here.

---

## What Is compose.yaml?

### A Building Analogy

Think of it like constructing a building:

- **Docker images** = building materials (bricks, cement, steel)
- **Docker containers** = finished rooms
- **compose.yaml** = the **blueprint**

The blueprint specifies:
- How many rooms to build
- The size of each room
- How rooms connect to each other
- Where the plumbing and wiring go

compose.yaml tells Docker:
- Which containers to start
- What image each container uses
- How containers communicate
- How ports and data are mapped

### Life Without It

Without a compose file, you launch each container manually:

```bash
# Start the database
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=123456 -v mysql_data:/var/lib/mysql mysql:8.0

# Start Redis
docker run -d --name redis redis:7

# Start the app and link it to both
docker run -d --name app --link mysql --link redis -p 8080:8080 my-app
```

Three containers, three commands, a wall of flags. With compose.yaml, one command does it all:

```bash
docker compose up -d
```

### File Naming History

| Era | Filename | Status |
|-----|----------|--------|
| Legacy (V1) | `docker-compose.yml` | Deprecated |
| Current (V2) | `compose.yaml` (preferred) | Also accepts `compose.yml`, `docker-compose.yml`, `docker-compose.yaml` |

For new projects, stick with `compose.yaml`.

---

## What Does the File Look Like?

Here is the simplest possible example:

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
```

Four lines and you have a running Nginx server. Notice there is **no `version` field** — Compose V2 dropped it entirely.

A slightly more realistic file:

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - api

  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=db
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=123456
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

Let's pull it apart section by section.

---

## YAML Nesting Rules

Before diving into specific directives, it helps to understand the indentation rules that YAML enforces — otherwise you will spend most of your time chasing whitespace errors.

### Core Rules

1. **Indent with spaces, never tabs** — use 2 spaces consistently
2. **Siblings share the same indentation level** — all keys at the same depth must line up
3. **Children are indented 2 more spaces than their parent** — this is how YAML represents hierarchy
4. **A space is required after every colon** — `key: value`, not `key:value`
5. **List items start with `- `** — a dash followed by a space

### Layer-by-Layer Breakdown

Here is a real-world config with each layer annotated:

```yaml
# Layer 0 (root): the top-level key
services:
  # Layer 1: service names (backend, frontend)
  backend:
    # Layer 2: service-level directives
    build:
      # Layer 3: sub-directives of build
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: octomira-backend
    ports:
      # Layer 2 list items
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DEBUG=True
      - DB_HOST=host.docker.internal
    extra_hosts:
      - "host.docker.internal:host-gateway"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: octomira-frontend
    ports:
      - "8087:8087"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_PROXY_TARGET=http://backend:8000
    depends_on:
      - backend
```

### Three YAML Data Types

```yaml
# 1. Key-value pair (mapping)
container_name: octomira-backend
# key: value

# 2. List (sequence)
ports:
  - "8000:8000"
  - "8001:8001"
# dash + space marks each item

# 3. Nested mapping (mapping inside a mapping)
build:
  context: ./backend
  dockerfile: Dockerfile.dev
# context and dockerfile are children of build
```

### Two Ways to Write Lists

```yaml
# Style 1: dash format (most common)
environment:
  - DEBUG=True
  - DB_HOST=localhost

# Style 2: mapping format (also valid)
environment:
  DEBUG: "True"
  DB_HOST: localhost
```

Both are equivalent. Pick one style and stay consistent within a file.

### Common Indentation Mistakes

```yaml
# Wrong: inconsistent indentation
services:
  web:
    image: nginx
     ports:        # one extra space — parser error
      - "80:80"

# Wrong: tab character
services:
	web:             # tab indentation — YAML forbids this
    image: nginx

# Wrong: missing space after colon
services:
  web:
    image:nginx     # no space after colon

# Correct
services:
  web:
    image: nginx
    ports:
      - "80:80"
```

**Tip:** Install the [YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) in VS Code for real-time validation.

---

## Field Reference: Required vs Optional

### Top-Level Keys

A compose.yaml file recognizes these **top-level keys**:

| Key | Required | Purpose |
|-----|----------|---------|
| `services` | Yes | Defines which containers to run — **the only mandatory key** |
| `volumes` | No | Declares named volumes (only needed when you use them) |
| `networks` | No | Declares custom networks (without this, all services share a default network) |
| `configs` | No | Declares config objects (mainly used in Swarm mode) |
| `secrets` | No | Declares sensitive data like passwords and certificates |

### Service-Level Fields

Each entry under `services` accepts these directives:

| Field | Required | Type | Purpose |
|-------|----------|------|---------|
| `image` | One of two | String | Pull a pre-built image |
| `build` | One of two | String or mapping | Build from a Dockerfile |
| `ports` | No | List | Port mapping |
| `volumes` | No | List | Volume / bind mounts |
| `environment` | No | List or mapping | Environment variables |
| `env_file` | No | String or list | Load env vars from a file |
| `depends_on` | No | List or mapping | Startup ordering |
| `networks` | No | List | Networks to join |
| `restart` | No | String | Restart policy |
| `command` | No | String or list | Override the default startup command |
| `entrypoint` | No | String or list | Override the entrypoint |
| `container_name` | No | String | Set a fixed container name |
| `healthcheck` | No | Mapping | Health check configuration |
| `extra_hosts` | No | List | Extra entries for `/etc/hosts` |
| `working_dir` | No | String | Working directory inside the container |
| `user` | No | String | User to run as inside the container |
| `stdin_open` | No | Boolean | Keep stdin open (equivalent to `docker run -i`) |
| `tty` | No | Boolean | Allocate a pseudo-TTY (equivalent to `docker run -t`) |
| `logging` | No | Mapping | Logging driver configuration |
| `deploy` | No | Mapping | Deployment settings (resource limits, etc.) |
| `profiles` | No | List | Profile grouping (start on demand) |
| `platform` | No | String | Target platform (e.g., `linux/amd64`) |

> **Note:** Every service must specify either `image` or `build` (or both — when both are present, the built image is tagged with the name given in `image`).

---

## Core Directives Explained

### 1. services — Required

```yaml
services:
  web:
    # web service config
  api:
    # api service config
  db:
    # database service config
```

**What it does:** Lists every container your application needs. Each service maps to exactly one container at runtime.

**Naming conventions:**
- Use lowercase letters
- Underscores and hyphens are fine
- Choose meaningful names (`backend`, `frontend`, `db`)
- The service name doubles as the DNS hostname for inter-container communication

---

### 2. image

```yaml
services:
  web:
    image: nginx:1.25
```

**Format:** `name:tag`
- `nginx` — defaults to `latest` (avoid in production)
- `nginx:1.25` — pinned version, reproducible
- `mysql:8.0` — MySQL 8.0

**Where to find images:** Search [Docker Hub](https://hub.docker.com/).

---

### 3. build

Short form:

```yaml
services:
  api:
    build: ./api
```

Full form:

```yaml
services:
  api:
    build:
      context: ./api           # Build context directory
      dockerfile: Dockerfile.dev  # Dockerfile filename
      args:                    # Build-time arguments
        - NODE_ENV=development
      target: dev              # Multi-stage build target
```

**`image` vs `build`:**
- `image` — use someone else's pre-built image (nginx, mysql, redis)
- `build` — build your own image from source code and a Dockerfile

---

### 4. ports

```yaml
services:
  web:
    ports:
      - "8080:80"
```

**Format:** `"host_port:container_port"`

```yaml
ports:
  - "80:80"                    # Host 80 → Container 80
  - "8080:80"                  # Host 8080 → Container 80
  - "127.0.0.1:3306:3306"     # Localhost only
  - "8000-8010:8000-8010"     # Port range
```

**Tip:** Always quote port mappings. YAML can misinterpret `xx:yy` as a base-60 number.

---

### 5. volumes

```yaml
services:
  db:
    volumes:
      - db_data:/var/lib/mysql       # Named volume
      - ./config:/etc/mysql/conf.d   # Bind mount
      - /app/node_modules            # Anonymous volume

volumes:
  db_data:     # Declare the named volume at the top level
```

**Three types:**

| Type | Syntax | Use case |
|------|--------|----------|
| Named volume | `name:/container/path` | Persistent data, managed by Docker |
| Bind mount | `./host/path:/container/path` | Live code syncing during development |
| Anonymous volume | `/container/path` | Prevent a bind mount from overwriting a specific directory |

**Important:** Named volumes must be declared in the top-level `volumes` block.

---

### 6. environment

Two equivalent styles:

```yaml
# List format
environment:
  - MYSQL_ROOT_PASSWORD=123456
  - MYSQL_DATABASE=myapp

# Mapping format
environment:
  MYSQL_ROOT_PASSWORD: 123456
  MYSQL_DATABASE: myapp
```

**Better practice:** Use `env_file` or a `.env` file to keep secrets out of version control:

```yaml
services:
  db:
    env_file:
      - ./db.env    # Load variables from file
```

```bash
# db.env (add to .gitignore!)
MYSQL_ROOT_PASSWORD=super_secret_password
```

---

### 7. depends_on

Simple form:

```yaml
services:
  web:
    depends_on:
      - api
      - db
```

With health checks (recommended):

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy    # Wait until db passes its health check
        restart: true                 # Restart api if db restarts

  db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10
```

**Key distinction:** The simple form only controls startup **order** — it does not wait for a service to be ready. Use `condition: service_healthy` when you need to wait for actual readiness.

---

### 8. networks

```yaml
services:
  web:
    networks:
      - frontend

  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
  backend:
```

**Default behavior:** Without explicit networks, all services land on the same default network and can reach each other. Custom networks are only needed when you want isolation (e.g., the web tier should not talk directly to the database).

---

### 9. restart

```yaml
services:
  web:
    restart: unless-stopped
```

| Value | Behavior |
|-------|----------|
| `no` | Never restart (default) |
| `always` | Always restart, including on Docker daemon startup |
| `on-failure` | Restart only on non-zero exit codes |
| `unless-stopped` | Restart unless explicitly stopped with `docker compose stop` |

For production, use `unless-stopped` or `always`.

---

### 10. extra_hosts

```yaml
services:
  backend:
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

**What it does:** Adds entries to the container's `/etc/hosts` file.

**Typical use case:** A container needs to reach a service running on the host machine (e.g., a local MySQL instance). `host.docker.internal` resolves to the host IP.

> Docker Desktop on macOS and Windows provides `host.docker.internal` automatically. On Linux, you need the `host-gateway` mapping shown above.

---

### 11. command and entrypoint

```yaml
services:
  api:
    image: node:18
    command: npm run dev          # Overrides CMD
    # or
    entrypoint: ["node", "app.js"]  # Overrides ENTRYPOINT
```

**Difference:**
- `command` overrides the Dockerfile `CMD` — commonly used to switch between dev and production startup scripts
- `entrypoint` overrides the Dockerfile `ENTRYPOINT` — changes the fundamental executable

---

### 12. container_name

```yaml
services:
  db:
    container_name: my_mysql
```

**Without it:** Docker Compose generates a name in the format `projectname-servicename-1` (e.g., `myproject-db-1`).

**Caveat:** A fixed container name prevents scaling (`docker compose up --scale db=3` will fail because the name collides).

---

### 13. deploy (Resource Limits)

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'         # Max 0.5 CPU cores
          memory: 512M        # Max 512 MB RAM
        reservations:
          cpus: '0.25'        # Reserve 0.25 CPU cores
          memory: 256M        # Reserve 256 MB RAM
```

---

### 14. profiles (On-Demand Services)

```yaml
services:
  web:
    image: nginx

  debug-tools:
    image: busybox
    profiles:
      - debug      # Only starts under the debug profile
```

```bash
# Normal startup — debug-tools stays off
docker compose up -d

# Start services that belong to the debug profile
docker compose --profile debug up -d
```

---

## Real-World Walkthrough

Let's annotate a full frontend + backend configuration line by line:

```yaml
# Top-level key: services (required)
services:

  # Service 1: backend
  backend:
    build:                          # Build from source (no pre-built image)
      context: ./backend            #   Build context = ./backend directory
      dockerfile: Dockerfile.dev    #   Dockerfile to use
    container_name: octomira-backend  # Fixed container name
    ports:
      - "8000:8000"                 # Host 8000 → Container 8000
    volumes:
      - ./backend:/app              # Bind mount — code changes sync instantly
    environment:                    # Environment variables
      - DEBUG=True
      - DB_HOST=host.docker.internal  # Connect to MySQL on the host
      - DB_NAME=octomira
      - DB_USER=octomira
      - DB_PASSWORD=octomira00##
    extra_hosts:
      - "host.docker.internal:host-gateway"  # Resolve host IP on Linux

  # Service 2: frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: octomira-frontend
    ports:
      - "8087:8087"
    volumes:
      - ./frontend:/app             # Sync frontend source
      - /app/node_modules           # Anonymous volume — prevents the bind mount from overwriting installed packages
    environment:
      - VITE_API_PROXY_TARGET=http://backend:8000  # Uses the service name as a hostname
    depends_on:
      - backend                     # Start after backend is up
```

**Key takeaways:**
- `- /app/node_modules` is an anonymous volume that shields the container's installed `node_modules` from being overwritten by the host bind mount
- `http://backend:8000` — `backend` is the service name, and Compose resolves it to the container's IP automatically

---

## Hands-On Example: WordPress Blog Stack

Requirements: WordPress + MySQL + phpMyAdmin (database admin UI)

```yaml
services:
  # WordPress application
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress_password
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress_data:/var/www/html
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  # MySQL database
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress_password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - db_data:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # phpMyAdmin for database management
  phpmyadmin:
    image: phpmyadmin:latest
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: root_password
    depends_on:
      - db

# Declare named volumes
volumes:
  wordpress_data:
  db_data:
```

**How to use it:**

```bash
# Start everything
docker compose up -d

# Access points
# WordPress: http://localhost:8080
# phpMyAdmin: http://localhost:8081

# Check status
docker compose ps

# Follow logs
docker compose logs -f

# Shut down
docker compose down

# Shut down and delete all data
docker compose down -v
```

---

## Troubleshooting

### How do I debug indentation errors?

YAML is whitespace-sensitive and forbids tabs. When something looks right but fails:

```bash
# Validate your config — errors include line numbers
docker compose config
```

### How do containers talk to each other?

Use the service name as the hostname:

```yaml
services:
  api:
    environment:
      - DB_HOST=db    # "db" resolves to the db container's IP

  db:
    image: mysql:8.0
```

Inside the `api` container, `ping db` works out of the box.

### Is the old `docker-compose` command still supported?

If the legacy binary is installed, it still runs — but it is no longer maintained. Switch as soon as you can:

```bash
# Check for the new plugin
docker compose version

# Legacy binary (do not use for new work)
docker-compose --version
```

Every old command has a direct equivalent — just replace the hyphen with a space:

| Legacy | Current |
|--------|---------|
| `docker-compose up` | `docker compose up` |
| `docker-compose down` | `docker compose down` |
| `docker-compose ps` | `docker compose ps` |
| `docker-compose logs` | `docker compose logs` |

### Does the file have to be named compose.yaml?

Docker Compose V2 searches for files in this order:

1. `compose.yaml`
2. `compose.yml`
3. `docker-compose.yaml`
4. `docker-compose.yml`

To use a custom name:

```bash
docker compose -f my-config.yaml up -d
```

### How do I see the final merged configuration?

```bash
# Merges all compose files and env vars, then prints the result
docker compose config
```

This is invaluable when a setting seems to have no effect.

---

## Command Cheat Sheet

| Command | What it does |
|---------|-------------|
| `docker compose up -d` | Start all services in the background |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Stop and remove containers **and** volumes |
| `docker compose ps` | Show running services |
| `docker compose logs -f` | Stream logs from all services |
| `docker compose logs -f web` | Stream logs from a single service |
| `docker compose restart` | Restart all services |
| `docker compose exec web bash` | Open a shell inside the web container |
| `docker compose pull` | Pull the latest images |
| `docker compose build` | Rebuild images |
| `docker compose config` | Validate and print the effective config |
| `docker compose up -d --build api` | Rebuild and restart a single service |

---

## Official References

For the full specification of any field:

- **Compose file reference (authoritative):** [https://docs.docker.com/reference/compose-file/](https://docs.docker.com/reference/compose-file/)
- **Compose quickstart:** [https://docs.docker.com/compose/gettingstarted/](https://docs.docker.com/compose/gettingstarted/)
- **Migrating from V1 to V2:** [https://docs.docker.com/compose/releases/migrate/](https://docs.docker.com/compose/releases/migrate/)
- **YAML specification:** [https://yaml.org/spec/1.2.2/](https://yaml.org/spec/1.2.2/)

---

## Summary

The compose.yaml file boils down to a handful of concepts:

1. **services** (required) — which containers to run
2. **image / build** (pick one) — pre-built image or build from source
3. **ports** — expose containers to the outside world
4. **volumes** — persist data and sync code during development
5. **environment** — pass configuration values
6. **depends_on** — control startup order and dependencies

The mental model:

```
compose.yaml = services (required) + per-service config (image/build required, everything else optional)
```

The only nesting rule that matters: **each child level adds 2 more spaces of indentation**. When in doubt, run `docker compose config` to validate.

---

## docker-compose.yml Best Practices

These habits will save you from the most common production headaches:

1. **Pin image versions** — Never use `latest` in production. Specify exact tags (`nginx:1.25`, `mysql:8.0`) so builds are reproducible.
2. **Externalize secrets** — Keep passwords and API keys out of compose.yaml. Use `env_file` or Docker Secrets, and add `.env` to `.gitignore`.
3. **Always add health checks** — Configure `healthcheck` on infrastructure services (databases, caches) and pair them with `depends_on: condition: service_healthy` so dependent services wait for true readiness.
4. **Persist important data** — Databases, uploads, and anything you cannot regenerate must use named volumes or bind mounts. Without them, data vanishes when the container is removed.
5. **Set resource limits** — Use `deploy.resources` to cap CPU and memory, preventing a single runaway container from starving the host.
6. **Manage log size** — Configure the `logging` driver to rotate logs and cap file sizes. Unmanaged logs can fill a disk surprisingly fast.

```yaml
# Log rotation example
services:
  web:
    image: nginx:1.25
    logging:
      driver: json-file
      options:
        max-size: "10m"    # Max 10 MB per log file
        max-file: "3"      # Keep at most 3 rotated files
```

---

## Docker Compose FAQ

### What is the difference between Docker Compose and Docker Swarm?

Docker Compose handles **single-host, multi-container orchestration** — perfect for development and small-scale production. Docker Swarm is Docker's native **cluster orchestration** tool for deploying across multiple hosts. If your app runs on a single server, Compose is all you need.

### What is the difference between `docker compose up` and `docker compose run`?

`docker compose up` starts all services defined in the compose file (or a specified subset plus their dependencies). It is the standard way to bring your stack online. `docker compose run` executes a one-off command against a single service — for example, `docker compose run api npm test` — then exits. Use it for tests, migrations, or ad-hoc tasks.

### How do I use a .env file with Docker Compose?

Place a `.env` file in the same directory as your compose.yaml. Compose loads it automatically, and you can reference its variables with `${VARIABLE_NAME}` in your compose file. Always add `.env` to `.gitignore` to avoid leaking credentials.

### How do I achieve zero-downtime updates with Docker Compose?

Run `docker compose up -d --no-deps --build <service>` to rebuild and restart a single service without touching the others. For stricter zero-downtime requirements, combine Compose with a reverse proxy (Nginx or Traefik) and implement blue-green or rolling deployments.

### Does volume data survive `docker compose down`?

Named volumes are **preserved** after `docker compose down`. Only the `-v` flag (`docker compose down -v`) deletes them. Bind-mount data lives on the host filesystem and is never affected by `down`.

---

## Further Reading

- [Getting Started with Docker](/posts/docker/2019-05-13-learn-docker/) — Docker fundamentals, installation, and basic concepts
- [Docker Command Cheat Sheet](/posts/docker/2019-11-14-docker-commands/) — Container, image, and network management commands
- [Docker Compose Complete Guide](/posts/docker/2026-01-19-docker-compose-complete-guide/) — End-to-end guide from installation to deployment
- [Linux/macOS Command Cheat Sheet](/posts/linux/2020-03-19-linux-mac-commands/) — Essential commands for DevOps and development
