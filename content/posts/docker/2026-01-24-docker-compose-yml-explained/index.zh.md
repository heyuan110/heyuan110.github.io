+++
date = '2026-01-24'
lastmod = '2026-02-23T10:00:00+08:00'
draft = false
title = 'Docker Compose 教程：docker-compose.yml 配置详解与实战案例（2026）'
description = '最全 Docker Compose 教程：逐字段讲透 docker-compose.yml 的 services、volumes、networks、healthcheck 配置，附 WordPress+MySQL 实战案例和生产级模板。'
toc = true
tags = ['Docker', 'Docker Compose', 'Containerization', 'Tutorial', 'YAML']
categories = ['AI Guides']
keywords = ['docker compose 教程', 'docker-compose.yml 详解', 'docker compose 配置', 'compose.yaml', 'docker compose yml', 'docker compose 入门', 'docker compose volumes', 'docker compose networks', 'docker compose ports', '容器编排', 'docker compose 2026', 'docker compose yaml 教程', 'docker-compose.yml 怎么写', 'docker compose services', 'docker compose healthcheck']
+++

Docker Compose 是目前最流行的多容器编排工具，而 **docker-compose.yml**（新版推荐命名为 `compose.yaml`）就是它的核心配置文件。无论你是刚接触容器化的新手，还是想系统梳理配置细节的老手，这篇 Docker Compose 教程都适合你。

本文将逐字段讲解 compose.yaml 中 services、volumes、networks、ports、environment、healthcheck 等所有配置项的含义和用法，并通过 WordPress + MySQL 等实战案例帮你快速上手。配合 [Docker 常用命令速查](/zh/posts/docker/2019-11-14-docker-commands/) 一起使用效果更佳。

很多人一看到 `compose.yaml` 就头大，一堆冒号、缩进，不知道从何下手。其实它没那么复杂，下面我用最通俗的方式，带你彻底搞懂这个文件。

> **重要提示**：旧版 `docker-compose`（带连字符）是用 Python 写的独立工具，**已于 2023 年 7 月停止维护**。现在应该使用 `docker compose`（空格分隔），它是 Docker CLI 的内置插件，用 Go 重写，性能更好，功能更全。本文所有命令均使用新版语法。

---

## 一、compose.yaml 是什么？

### 用盖房子来理解

想象你要盖一栋房子：

- **Docker 镜像** = 建材（砖头、水泥、钢筋）
- **Docker 容器** = 盖好的房间
- **compose.yaml** = **设计图纸**

设计图纸上写着：
- 要盖几个房间
- 每个房间多大
- 房间之间怎么连通
- 水电怎么接

compose.yaml 就是告诉 Docker：
- 要启动几个容器
- 每个容器用什么镜像
- 容器之间怎么通信
- 端口和数据怎么映射

### 没有它会怎样？

没有 compose.yaml，你要一个个手动启动容器：

```bash
# 先启动数据库
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=123456 -v mysql_data:/var/lib/mysql mysql:8.0

# 再启动 Redis
docker run -d --name redis redis:7

# 最后启动应用，还要连接上面两个
docker run -d --name app --link mysql --link redis -p 8080:8080 my-app
```

三个容器就要敲三行命令，参数一堆。有了 compose.yaml，一个命令搞定：

```bash
docker compose up -d
```

### 文件名的变化

| 时代 | 文件名 | 说明 |
|------|--------|------|
| 旧版 (V1) | `docker-compose.yml` | 已弃用 |
| 新版 (V2) | `compose.yaml`（推荐）| 也兼容 `compose.yml`、`docker-compose.yml`、`docker-compose.yaml` |

新项目建议直接用 `compose.yaml`。

---

## 二、文件长什么样？

先看一个最简单的例子：

```yaml
services:
  web:
    image: nginx
    ports:
      - "80:80"
```

就这么几行，就能启动一个 Nginx 服务器。注意：**不需要写 `version` 了**，Compose V2 已经废弃了 `version` 字段。

再看一个稍微复杂点的：

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

别被吓到，我们一块块拆解。

---

## 三、YAML 嵌套规范

在讲具体配置之前，先搞懂 YAML 的嵌套规则，否则写配置时会一头雾水。

### 核心规则

1. **用空格缩进，禁止用 Tab** — 建议统一用 2 个空格
2. **同级元素缩进相同** — 同一层级的 key 必须对齐
3. **子级比父级多缩进 2 个空格** — 表示从属关系
4. **冒号后面要有空格** — `key: value`，不是 `key:value`
5. **列表项用 `- ` 开头** — 短横线后面要有空格

### 嵌套层级图解

以你给的实际配置为例，逐层拆解：

```yaml
# 第 0 层（顶层）：services 是根 key
services:
  # 第 1 层：服务名（backend、frontend）
  backend:
    # 第 2 层：服务的配置项
    build:
      # 第 3 层：build 的子配置
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: octomira-backend
    ports:
      # 第 2 层的列表项
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

### YAML 的三种数据类型

```yaml
# 1. 键值对（映射 / Map）
container_name: octomira-backend
# key: value

# 2. 列表（序列 / Sequence）
ports:
  - "8000:8000"
  - "8001:8001"
# 短横线 + 空格 表示列表的每一项

# 3. 嵌套映射（映射套映射）
build:
  context: ./backend
  dockerfile: Dockerfile.dev
# build 下面的 context 和 dockerfile 是 build 的子属性
```

### 两种列表写法

```yaml
# 写法一：短横线格式（常用）
environment:
  - DEBUG=True
  - DB_HOST=localhost

# 写法二：键值对格式（也可以）
environment:
  DEBUG: "True"
  DB_HOST: localhost
```

两种等价，但同一个文件里建议统一风格。

### 常见缩进错误

```yaml
# ❌ 错误：缩进不一致
services:
  web:
    image: nginx
     ports:        # 多了一个空格，会报错
      - "80:80"

# ❌ 错误：用了 Tab
services:
	web:             # Tab 缩进，YAML 不允许
    image: nginx

# ❌ 错误：冒号后缺空格
services:
  web:
    image:nginx     # 冒号后没空格

# ✅ 正确
services:
  web:
    image: nginx
    ports:
      - "80:80"
```

**建议**：用 VS Code 装 [YAML 插件](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)，实时检查格式错误。

---

## 四、配置字段全览：哪些必选，哪些可选

### 顶层结构

compose.yaml 有这些**顶层 key**：

| 顶层 key | 必选 | 说明 |
|----------|------|------|
| `services` | ✅ | 定义要运行的容器，**唯一必填项** |
| `volumes` | ❌ | 声明命名卷（用了命名卷才需要） |
| `networks` | ❌ | 声明自定义网络（不声明则所有服务共享默认网络） |
| `configs` | ❌ | 声明配置文件（Swarm 模式用得多） |
| `secrets` | ❌ | 声明敏感数据（如密码、证书） |

### 服务配置字段

每个服务（`services` 下的子项）可以使用以下字段：

| 字段 | 必选 | 类型 | 说明 |
|------|------|------|------|
| `image` | ⚠️ 二选一 | 字符串 | 使用现成镜像 |
| `build` | ⚠️ 二选一 | 字符串或映射 | 从 Dockerfile 构建镜像 |
| `ports` | ❌ | 列表 | 端口映射 |
| `volumes` | ❌ | 列表 | 数据卷/目录挂载 |
| `environment` | ❌ | 列表或映射 | 环境变量 |
| `env_file` | ❌ | 字符串或列表 | 从文件读取环境变量 |
| `depends_on` | ❌ | 列表或映射 | 启动依赖顺序 |
| `networks` | ❌ | 列表 | 加入的网络 |
| `restart` | ❌ | 字符串 | 重启策略 |
| `command` | ❌ | 字符串或列表 | 覆盖默认启动命令 |
| `entrypoint` | ❌ | 字符串或列表 | 覆盖入口点 |
| `container_name` | ❌ | 字符串 | 指定容器名称 |
| `healthcheck` | ❌ | 映射 | 健康检查配置 |
| `extra_hosts` | ❌ | 列表 | 添加额外的 hosts 映射 |
| `working_dir` | ❌ | 字符串 | 容器内工作目录 |
| `user` | ❌ | 字符串 | 容器内运行的用户 |
| `stdin_open` | ❌ | 布尔值 | 保持 stdin 打开（等价于 `docker run -i`） |
| `tty` | ❌ | 布尔值 | 分配伪终端（等价于 `docker run -t`） |
| `logging` | ❌ | 映射 | 日志驱动配置 |
| `deploy` | ❌ | 映射 | 部署相关配置（资源限制等） |
| `profiles` | ❌ | 列表 | 配置文件分组（按需启动） |
| `platform` | ❌ | 字符串 | 指定平台（如 `linux/amd64`） |

> **⚠️ `image` 和 `build` 二选一**：每个服务必须指定 `image`（用现成镜像）或 `build`（自己构建），两者也可以同时写（构建后打上 image 指定的标签）。

---

## 五、逐个讲解核心配置

### 1. services（服务列表）— 必选

```yaml
services:
  web:
    # web 服务的配置
  api:
    # api 服务的配置
  db:
    # 数据库服务的配置
```

**是什么**：你要运行的所有容器，每个服务就是一个容器。

**命名规则**：
- 用小写字母
- 可以用下划线或短横线
- 取个有意义的名字（`backend`、`frontend`、`db`）
- 服务名同时也是容器间互访的主机名

---

### 2. image（使用的镜像）

```yaml
services:
  web:
    image: nginx:1.25
```

**格式**：`镜像名:标签`
- `nginx` → 默认用 latest 标签（不推荐生产环境用 latest）
- `nginx:1.25` → 指定版本，可复现
- `mysql:8.0` → MySQL 8.0

**去哪找镜像**：[Docker Hub](https://hub.docker.com/) 上搜索。

---

### 3. build（自己构建镜像）

简单写法：

```yaml
services:
  api:
    build: ./api
```

完整写法：

```yaml
services:
  api:
    build:
      context: ./api           # 构建上下文目录
      dockerfile: Dockerfile.dev  # 指定 Dockerfile 文件名
      args:                    # 构建参数
        - NODE_ENV=development
      target: dev              # 多阶段构建的目标阶段
```

**`image` vs `build`**：
- `image`：用别人做好的镜像（nginx、mysql、redis）
- `build`：用自己写的代码 + Dockerfile 构建镜像

---

### 4. ports（端口映射）

```yaml
services:
  web:
    ports:
      - "8080:80"
```

**格式**：`"宿主机端口:容器端口"`

```yaml
ports:
  - "80:80"                    # 外部 80 → 容器 80
  - "8080:80"                  # 外部 8080 → 容器 80
  - "127.0.0.1:3306:3306"     # 仅本机可访问
  - "8000-8010:8000-8010"     # 端口范围映射
```

**注意**：端口号建议加引号，因为 YAML 中 `xx:yy` 可能被解析为六十进制数值。

---

### 5. volumes（数据卷/目录挂载）

```yaml
services:
  db:
    volumes:
      - db_data:/var/lib/mysql       # 命名卷
      - ./config:/etc/mysql/conf.d   # 绑定挂载
      - /app/node_modules            # 匿名卷

volumes:
  db_data:     # 顶层声明命名卷
```

**三种类型**：

| 类型 | 写法 | 用途 |
|------|------|------|
| 命名卷 | `name:/container/path` | 持久化数据，Docker 管理存储位置 |
| 绑定挂载 | `./host/path:/container/path` | 开发时同步代码，修改实时生效 |
| 匿名卷 | `/container/path` | 排除某个目录不被绑定挂载覆盖 |

**重要**：用了命名卷，必须在顶层 `volumes` 里声明。

---

### 6. environment（环境变量）

两种等价写法：

```yaml
# 列表格式
environment:
  - MYSQL_ROOT_PASSWORD=123456
  - MYSQL_DATABASE=myapp

# 映射格式
environment:
  MYSQL_ROOT_PASSWORD: 123456
  MYSQL_DATABASE: myapp
```

**更安全的做法**：用 `env_file` 或 `.env` 文件

```yaml
services:
  db:
    env_file:
      - ./db.env    # 从文件读取环境变量
```

```bash
# db.env（不要提交到 Git！加入 .gitignore）
MYSQL_ROOT_PASSWORD=super_secret_password
```

---

### 7. depends_on（启动顺序）

简单写法：

```yaml
services:
  web:
    depends_on:
      - api
      - db
```

带健康检查的写法（推荐）：

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy    # 等 db 健康检查通过才启动
        restart: true                 # db 重启时 api 也跟着重启

  db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10
```

**注意**：简单的 `depends_on` 只保证启动顺序，不保证服务"准备好了"。要等服务真正可用，用 `condition: service_healthy`。

---

### 8. networks（网络）

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

**默认情况**：不写 networks，所有服务自动在同一个网络，可以互相访问。只有需要网络隔离时才需要自定义。

---

### 9. restart（重启策略）

```yaml
services:
  web:
    restart: unless-stopped
```

| 值 | 说明 |
|------|------|
| `no` | 不自动重启（默认） |
| `always` | 总是重启，包括 Docker 启动时 |
| `on-failure` | 只有非正常退出才重启 |
| `unless-stopped` | 除非手动 `docker compose stop`，否则一直重启 |

生产环境推荐 `unless-stopped` 或 `always`。

---

### 10. extra_hosts（额外 hosts 映射）

```yaml
services:
  backend:
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

**是什么**：往容器的 `/etc/hosts` 文件里添加记录。

**典型场景**：容器要连接宿主机上的服务（如本地 MySQL），用 `host.docker.internal` 指向宿主机。

> 注：Docker Desktop（macOS/Windows）自带 `host.docker.internal`，Linux 上需要手动加 `host-gateway`。

---

### 11. command 和 entrypoint

```yaml
services:
  api:
    image: node:18
    command: npm run dev          # 覆盖 CMD
    # 或
    entrypoint: ["node", "app.js"]  # 覆盖 ENTRYPOINT
```

**区别**：
- `command`：覆盖 Dockerfile 中的 `CMD`，常用于切换启动方式
- `entrypoint`：覆盖 Dockerfile 中的 `ENTRYPOINT`，改变程序入口

---

### 12. container_name（指定容器名）

```yaml
services:
  db:
    container_name: my_mysql
```

**不指定会怎样**：Docker Compose 会自动生成，格式为 `项目名-服务名-序号`（如 `myproject-db-1`）。

**注意**：指定了 container_name 就不能做服务扩缩容（`docker compose up --scale db=3` 会冲突）。

---

### 13. deploy（资源限制）

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'         # 最多用 0.5 个 CPU
          memory: 512M        # 最多用 512MB 内存
        reservations:
          cpus: '0.25'        # 预留 0.25 个 CPU
          memory: 256M        # 预留 256MB 内存
```

---

### 14. profiles（按需启动）

```yaml
services:
  web:
    image: nginx

  debug-tools:
    image: busybox
    profiles:
      - debug      # 只在 debug profile 下启动
```

```bash
# 正常启动，debug-tools 不会启动
docker compose up -d

# 启动包含 debug profile 的服务
docker compose --profile debug up -d
```

---

## 六、理解你给的实战配置

回到你提供的例子，逐字段注释：

```yaml
# 顶层 key：services（必选）
services:

  # 第一个服务：backend
  backend:
    build:                          # 自己构建镜像（不用 image 拉现成的）
      context: ./backend            #   构建上下文 = ./backend 目录
      dockerfile: Dockerfile.dev    #   使用的 Dockerfile 文件名
    container_name: octomira-backend  # 固定容器名
    ports:
      - "8000:8000"                 # 宿主机 8000 → 容器 8000
    volumes:
      - ./backend:/app              # 绑定挂载，代码修改实时同步到容器
    environment:                    # 环境变量
      - DEBUG=True
      - DB_HOST=host.docker.internal  # 连接宿主机上的 MySQL
      - DB_NAME=octomira
      - DB_USER=octomira
      - DB_PASSWORD=octomira00##
    extra_hosts:
      - "host.docker.internal:host-gateway"  # Linux 下让容器能找到宿主机

  # 第二个服务：frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: octomira-frontend
    ports:
      - "8087:8087"
    volumes:
      - ./frontend:/app             # 同步前端代码
      - /app/node_modules           # 匿名卷：排除 node_modules，不被上一行覆盖
    environment:
      - VITE_API_PROXY_TARGET=http://backend:8000  # 用服务名 backend 作为主机名
    depends_on:
      - backend                     # frontend 等 backend 启动后再启动
```

**关键点**：
- `- /app/node_modules` 是匿名卷，作用是防止宿主机的绑定挂载覆盖容器里安装好的 node_modules
- `http://backend:8000` 中的 `backend` 是服务名，Compose 自动解析为该容器的 IP

---

## 七、完整实战案例

### 案例：搭建一个博客系统

需求：WordPress + MySQL + phpMyAdmin（数据库管理工具）

```yaml
services:
  # WordPress 主程序
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

  # MySQL 数据库
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

  # phpMyAdmin 数据库管理
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

# 声明命名卷
volumes:
  wordpress_data:
  db_data:
```

**使用方法**：

```bash
# 启动所有服务
docker compose up -d

# 访问
# WordPress: http://localhost:8080
# phpMyAdmin: http://localhost:8081

# 查看运行状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止所有服务
docker compose down

# 停止并删除数据
docker compose down -v
```

---

## 八、常见问题

### Q1：缩进出错怎么排查？

YAML 对缩进敏感，必须用空格，不能用 Tab。

```bash
# 用 docker compose config 验证配置是否正确
docker compose config

# 如果有语法错误，会直接报错并指出行号
```

### Q2：容器之间怎么互相访问？

直接用服务名作为主机名：

```yaml
services:
  api:
    environment:
      - DB_HOST=db    # 直接用服务名 "db"

  db:
    image: mysql:8.0
```

在 api 容器里，`ping db` 就能通。

### Q3：`docker-compose` 还能用吗？

如果你的系统还装着旧版，暂时能用，但建议尽快切换：

```bash
# 检查是否有新版
docker compose version

# 旧版（别再用了）
docker-compose --version
```

所有旧命令都有对应的新命令，只需把 `docker-compose` 换成 `docker compose`：

| 旧命令 | 新命令 |
|--------|--------|
| `docker-compose up` | `docker compose up` |
| `docker-compose down` | `docker compose down` |
| `docker-compose ps` | `docker compose ps` |
| `docker-compose logs` | `docker compose logs` |

### Q4：文件名必须是 compose.yaml 吗？

Docker Compose V2 按以下优先级查找文件：

1. `compose.yaml`
2. `compose.yml`
3. `docker-compose.yaml`
4. `docker-compose.yml`

用其他名字要指定：

```bash
docker compose -f my-config.yaml up -d
```

### Q5：怎么查看最终生效的配置？

```bash
# 合并所有配置文件和环境变量，输出最终结果
docker compose config
```

非常适合排查"为什么配置没生效"的问题。

---

## 九、常用命令速查表

| 命令 | 作用 |
|------|------|
| `docker compose up -d` | 后台启动所有服务 |
| `docker compose down` | 停止并删除容器 |
| `docker compose down -v` | 停止并删除容器和数据卷 |
| `docker compose ps` | 查看运行状态 |
| `docker compose logs -f` | 实时查看日志 |
| `docker compose logs -f web` | 只看某个服务的日志 |
| `docker compose restart` | 重启所有服务 |
| `docker compose exec web bash` | 进入 web 容器 |
| `docker compose pull` | 拉取最新镜像 |
| `docker compose build` | 重新构建镜像 |
| `docker compose config` | 验证并输出最终配置 |
| `docker compose up -d --build api` | 重建某个服务并启动 |

---

## 十、官方参考

想查某个字段的完整用法？这些是权威来源：

- **Compose 文件规范（最全最权威）**：[https://docs.docker.com/reference/compose-file/](https://docs.docker.com/reference/compose-file/)
- **Compose 快速入门**：[https://docs.docker.com/compose/gettingstarted/](https://docs.docker.com/compose/gettingstarted/)
- **从 V1 迁移到 V2**：[https://docs.docker.com/compose/releases/migrate/](https://docs.docker.com/compose/releases/migrate/)
- **YAML 语法速查**：[https://yaml.org/spec/1.2.2/](https://yaml.org/spec/1.2.2/)

---

## 十一、总结

compose.yaml 的核心就这几个：

1. **services**（必选） — 定义要跑哪些容器
2. **image/build**（二选一） — 用现成镜像还是自己构建
3. **ports** — 端口映射，让外部能访问
4. **volumes** — 数据持久化 + 开发时代码同步
5. **environment** — 传配置参数
6. **depends_on** — 控制启动顺序和依赖

记住这个公式：

```
compose.yaml = services（必选）+ 每个服务的配置（image/build 必选，其余按需）
```

嵌套规则只有一条：**每深一层，多缩进 2 个空格**。搞不清楚就跑 `docker compose config` 验证。

---

## 十二、docker-compose.yml 最佳实践

在实际项目中，以下几点经验可以帮你避免常见的坑：

1. **镜像版本锁定** -- 生产环境永远不要用 `latest` 标签，指定明确的版本号（如 `nginx:1.25`、`mysql:8.0`），确保环境可复现
2. **敏感信息外置** -- 密码、密钥等不要直接写在 compose.yaml 中，使用 `env_file` 或 Docker Secrets，并把 `.env` 文件加入 `.gitignore`
3. **健康检查必加** -- 对数据库等基础服务配置 `healthcheck`，配合 `depends_on` 的 `condition: service_healthy`，确保服务真正就绪后再启动依赖服务
4. **数据持久化** -- 重要数据（数据库、上传文件等）必须使用命名卷或绑定挂载，否则容器删除后数据会丢失
5. **资源限制** -- 通过 `deploy.resources` 限制 CPU 和内存使用，防止单个容器耗尽宿主机资源
6. **日志管理** -- 配置 `logging` 驱动限制日志文件大小，避免磁盘被日志撑满

```yaml
# 日志管理示例
services:
  web:
    image: nginx:1.25
    logging:
      driver: json-file
      options:
        max-size: "10m"    # 单个日志文件最大 10MB
        max-file: "3"      # 最多保留 3 个日志文件
```

---

## 十三、Docker Compose 常见问题 FAQ

### Docker Compose 和 Docker Swarm 有什么区别？

Docker Compose 用于**单机多容器编排**，适合开发环境和小规模生产部署；Docker Swarm 是 Docker 原生的**集群编排**方案，用于跨多台主机部署容器。如果你的应用只在一台服务器上运行，用 Docker Compose 就够了。

### docker compose up 和 docker compose run 有什么区别？

`docker compose up` 启动 compose.yaml 中定义的所有服务（或指定服务及其依赖），是最常用的启动命令。`docker compose run` 则是针对某个服务运行一次性命令，比如 `docker compose run api npm test`，执行完就退出，适合跑测试或数据库迁移。

### 如何在 Docker Compose 中使用 .env 文件？

在 compose.yaml 同级目录下创建 `.env` 文件，Docker Compose 会自动加载其中的变量。你可以在 compose.yaml 中通过 `${变量名}` 引用这些变量。务必将 `.env` 加入 `.gitignore` 以避免泄露敏感信息。

### Docker Compose 如何实现零停机更新？

可以使用 `docker compose up -d --no-deps --build <服务名>` 单独重建和重启某个服务，其他服务不受影响。对于更严格的零停机需求，建议结合反向代理（如 Nginx 或 Traefik）实现蓝绿部署或滚动更新。

### compose.yaml 中的 volumes 数据在 docker compose down 后还在吗？

如果使用 `docker compose down`，命名卷（named volumes）中的数据**会保留**。只有加了 `-v` 参数（`docker compose down -v`）才会删除命名卷。绑定挂载（bind mounts）的数据始终在宿主机上，不受影响。

---

## 相关阅读

- [Docker 入门教程](/zh/posts/docker/2019-05-13-learn-docker/) - Docker 基础概念和安装配置
- [Docker 常用命令速查](/zh/posts/docker/2019-11-14-docker-commands/) - 容器、镜像、网络等管理命令
- [Docker Compose 完全指南](/zh/posts/docker/2026-01-19-docker-compose-complete-guide/) - 从安装到部署的全流程指南
- [Linux/macOS 常用命令速查手册](/zh/posts/linux/2020-03-19-linux-mac-commands/) - 运维开发常用命令参考
- [Linux 运维基础 Hub](/zh/posts/linux/linux-ops-basics-hub/)
