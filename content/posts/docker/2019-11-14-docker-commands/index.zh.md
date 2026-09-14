+++
date = '2019-11-14T20:37:13+08:00'
title = 'Docker 常用命令速查（2026更新）：镜像、容器、网络、数据卷一页掌握'
description = '高频 Docker 命令速查：pull/run/exec/logs、镜像清理、网络管理、数据卷挂载，附 MySQL/Nginx/Redis 常用启动示例。'
toc = true
tags = ['Docker', '命令行', '容器', '运维', '速查手册']
categories = ['Docker']

[[params.faqItems]]
question = "Docker 怎么清理没用的镜像释放磁盘？"
answer = "先用 `docker system df` 看镜像、容器、数据卷各占多少空间。虚悬镜像（仓库名和标签都是 none）用 `docker image ls -f dangling=true` 列出、`docker image prune` 清掉。批量删除可以组合命令：`docker image rm $(docker image ls -q)` 删全部，`docker image rm $(docker image ls -q redis)` 只删 redis 仓库的。删镜像支持完整 ID、短 ID 和镜像名三种写法。"

[[params.faqItems]]
question = "怎么批量停止并删除所有已退出的容器？"
answer = "两条管道命令：`docker ps -a | grep Exited | awk '{print $1}' | xargs docker stop` 和把最后的 stop 换成 `docker rm`。更粗暴的写法是 `docker rm $(docker ps -a -q)` 删除所有已停止容器、`docker kill $(docker ps -a -q)` 杀掉所有运行中的容器——这两条慎用。注意容器必须先 stop 才能 rm。"

[[params.faqItems]]
question = "docker run 的 -p、-v、-d 参数分别是什么意思？"
answer = "`-d` 后台运行并返回容器 ID；`-p` 端口映射，格式是「主机端口:容器端口」，比如 `-p 80:80`，大写 `-P` 则是映射到主机随机端口；`-v` 挂载数据卷，格式是「主机目录:容器目录」，必须用绝对路径。还可以绑定到指定网卡，比如 `-p 127.0.0.1:80:8080/tcp` 只让本机访问。`--name` 给容器命名，方便后续 start/stop/exec。"

[[params.faqItems]]
question = "用 Docker 启动 MySQL 该挂载哪些目录？"
answer = "至少挂数据目录，配置和日志按需。完整写法是 `-v /path/conf:/etc/mysql/conf.d -v /path/logs:/logs -v /path/data:/var/lib/mysql`，再用 `-e MYSQL_ROOT_PASSWORD=root` 初始化 root 密码，`-p 3306:3306` 映射端口。不挂 `/var/lib/mysql` 的话，容器一删数据就没了。Nginx 和 PHP 同理，分别挂 `/usr/share/nginx/html`、`/etc/nginx/conf.d` 和 `/var/www/html`。"

[[params.faqItems]]
question = "Windows 下挂载 MongoDB 数据目录报写入权限错误怎么办？"
answer = "不要直接挂主机目录，先创建命名卷再映射：`docker volume create --name=mongodata`，然后 `docker run -d --name mongodb -p 32767:27017 -v mongodata:/data/db mongo:4.2.1`。查看卷用 `docker volume ls` 和 `docker volume inspect xxxx`。想直接翻卷里的文件，可以起一个临时容器把宿主根目录挂进去：`docker run --rm -it -v /:/vm-root alpine sh`。"

[[params.faqItems]]
question = "怎么查看容器的 IP 和在主机容器之间拷文件？"
answer = "查 IP 有两种办法：进容器内部 `cat /etc/hosts`，或者在主机上 `docker inspect 容器id`。拷文件用 `docker cp`：`docker cp /www/xxxx test-container:/www/` 把主机目录拷进容器的 /www 下；写成 `docker cp /www/xxxx test-container:/www` 则是拷进去并重命名为 www。方向反过来也成立，把两个参数调换即可。"
+++

Docker常用命令记录

## 1. 启动、重启或停止docker服务

启动： `service docker start`

停止：`service docker stop`

重启：`service docker restart`

## 2.镜像(images)

### 获取镜像

docker pull [OPTIONS] NAME[:TAG|@DIGEST]

例如：`docker pull ubuntu:16.04`

### 列出镜像

- 查看所有镜像: `docker images`或`docker image ls`, 显示摘要`docker images --digests`
- 查看特定镜像:`docker image ls xxxx`或`docker image xxxx`
- 查看镜像、容器、数据卷所占用的空间:`docker system df`
- 列出虚悬镜像（仓库名和标签名为<none>）:`docker image ls -f dangling=true`,清楚此类镜像`docker image prune`

### 删除镜像

命令`docker image rm [OPTIONS] IMAGE [IMAGE...]` 或 `docker rmi -f xxxx`
例如：

```
root@ubuntu:~# docker image ls redis
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
redis               latest              ce25c7293564        5 days ago          95MB
```
- 根据完整ID删除：`docker image rm 578c3e61a98c`
- 根据短ID删除：`docker image rm 578c3`
- 根据镜像名删除：`docker image rm redis`
- docker image ls配合删除：删除所有镜像`docker image rm $(docker image ls -q)`,删除所有仓库名为redis的镜像`docker image rm $(docker image ls -q redis)`
- 删除所有未打 dangling 标签的镜像`docker rmi $(docker images -q -f dangling=true)`

docker ps -a | grep "Exited" | awk '{print $1 }'|xargs docker stop
docker ps -a | grep "Exited" | awk '{print $1 }'|xargs docker rm
docker images|grep none|awk '{print $3 }'|xargs docker rmi


## 3. 容器(container)

### 创建新容器

- 使用docker镜像nginx:latest以后台模式启动一个容器,并将容器命名为mynginx。

```
root@ubuntu:~# docker run --name mynginx -d nginx:latest
参数：
--name="nginx-lb": 为容器指定一个名称；
-d: 后台运行容器，并返回容器ID；
```

- 使用镜像nginx:latest以后台模式启动一个容器,并将容器的80端口映射到主机随机端口。

```
root@ubuntu:~# docker run -P -d nginx:latest
参数：
-p: 端口映射，格式为：主机(宿主)端口:容器端口;
```

- 使用镜像 nginx:latest，以后台模式启动一个容器,将容器的 80 端口映射到主机的 80 端口,主机的目录 /data 映射到容器的 /data。

```
root@ubuntu:~# docker run -p 80:80 -v /data:/data -d nginx:latest
参数：
-v: 映射数据卷,格式为：主机目录:容器目录，注意是绝对路径;
```
- 绑定容器的 8080 端口，并将其映射到本地主机 127.0.0.1 的 80 端口上。

```
root@ubuntu:~# docker run -p 127.0.0.1:80:8080/tcp ubuntu bash
```
- 使用镜像nginx:latest以交互模式启动一个容器,在容器内执行/bin/bash命令。
```
root@ubuntu:~# docker run -it nginx:latest /bin/bash
```

参考<http://www.runoob.com/docker/docker-run-command.html>

### 其他命令：

```
//查看所有容器
docker ps -a

//查看正在运行的容器
docker ps

//启动一个容器
docker start xxxx

//停止一个容器
docker stop xxxx

//杀死所有正在运行的容器
docker kill $(docker ps -a -q)

//重启一个容器
docker restart xxxx

//删除一个容器，前提是容器是stop
docker rm xxxx

//删除所有已停止容器，慎用！
docker rm $(docker ps -a -q)

//容器与主机之间的数据拷贝
将主机/www/xxxx目录拷贝到容器test-container的/www目录下：
docker cp /www/xxxx test-container:/www/
或
将主机/www/xxxx目录拷贝到容器test-container中，目录重命名为www：
docker cp /www/xxxx test-container:/www

//查看容器ip
方法1：进入容器内部，然后cat /etc/hosts
方法2：docker inspect 容器id
```

## 常用docker

### 1. Grafana

```
//创建相关目录，和配置文件
//下载默认配置模板grafana.ini,修改defaults.ini为grafana.ini
`wget https://raw.githubusercontent.com/grafana/grafana/master/conf/defaults.ini`

//创建grafana容器
 docker run -d --name=grafana \
 -p 3000:3000 \
 -v /usr/local/programs/grafana/data:/var/lib/grafana \
 -v /usr/local/programs/grafana/log:/var/log/grafana \
 -v /usr/local/programs/grafana/conf/grafana.ini:/etc/grafana/grafana.ini \
 -e "GF_SERVER_ROOT_URL=http://s1.s:3000" \
 -e "GF_SECURITY_ADMIN_PASSWORD=123456" \
 docker.patpat.vip:9503/grafana:1.20.0:5.4.2
```

### 2. Portainer

```
docker run -d -p 9000:9000 \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --name portainer \
   docker.patpat.vip:9503/portainer:1.20.0
```

### 3. Prometheus

```
//下载默认配置
wget https://raw.githubusercontent.com/prometheus/prometheus/master/documentation/examples/prometheus.yml

//创建prometheus镜像
docker run -d --name=prometheus \
    -p 9092:9090 \
    -v /usr/local/programs/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v /usr/local/programs/prometheus/data:/prometheus-data \
    prom/prometheus

//创建带alert规则的prometheus镜像
docker run -d --name=prometheus \
    -p 9092:9090 \
    -v /usr/local/programs/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    -v /usr/local/programs/prometheus/alert.rules:/etc/prometheus/alert.rules \
    -v /usr/local/programs/prometheus/data:/prometheus-data \
    prom/prometheus

//创建alertmanager
docker run -d --name=alertmanager \
    -p 9093:9093 \
    -v /usr/local/programs/prometheus/alertmanager/config.yml:/etc/alertmanager/config.yml \
    prom/alertmanager

```

### 4. Mysql

启动mysql5.6镜像
```
docker run -d \
-p 3306:3306 \
--name mysql \
-v /usr/local/programs/mysql/conf:/etc/mysql/conf.d \
-v /usr/local/programs/mysql/logs:/logs \
-v /usr/local/programs/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root \
docker.patpat.vip:9503/mysql:5.6.46
```

启动mysql5.7镜像
```
docker pull docker.patpat.vip:9503/mysql:5.7.28

docker run -d \
-p 3306:3306 \
--name mysql \
-v $PWD/mysql:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root \
docker.patpat.vip:9503/mysql:5.7.28
```
说明:
-p 3306:3306：将容器的3306端口映射到主机的3306端口；
-v $PWD/mysql:/var/lib/mysql：将主机当前目录下的/mysql挂载到容器的/var/lib/mysql；
-e MYSQL_ROOT_PASSWORD=password：初始化root用户的密码；
--name 给容器命名，mysql5719；
-d 表示容器在后台运行

### 5. PHP

```
docker run -d -p 9091:9000 --name webconsole-php \
-v /var/www/webconsole:/var/www/html/ \
-v /usr/local/programs/php7/php7-fpm/conf:/usr/local/etc/php \
-v /usr/local/programs/php7/php7-fpm/logs:/phplogs \
--privileged=true \
docker.patpat.vip:9503/php:7.2-fpm
```

### 6. Nginx

docker run -d -p 8001:80 --name webconsole-nginx \
-v /var/www/webconsole:/usr/share/nginx/html \
-v /usr/local/programs/nginx/conf.d:/etc/nginx/conf.d \
-v /usr/local/programs/nginx/log:/var/log/nginx \
--privileged=true -d docker.patpat.vip:9503/nginx:1.15


### 7. Mongo

```
docker run -d \
--name mongodb \
-p 32767:27017 \
-v /usr/local/programs/mongodb:/data/db \
docker.patpat.vip:9501/mongo:4.2.1
```

windows下会有写入权限问题，所以需要先创建volume，再映射

`docker volume create --name=mongodata`

`docker run -d --name mongodb -p 32767:27017 -v mongodata:/data/db docker.patpat.vip:9503/mongo:4.2.1`

`docker volume`创建卷之后怎么查看？

https://stackoverflow.com/questions/44358328/how-i-can-access-docker-data-volumes-on-windows-machine

查看所有卷 `docker volume ls`

查看具体某一个卷 `docker volume inspect xxxx`

创建一个临时的环境，将docker跟目录挂载进去，登录进去后ls /var-root就可以查看所有路径文件了

`docker run --rm -it -v /:/vm-root alpine:edg sh`

### 8. Redis

```
docker run --name redis -d -p 6379:6379 -v redis-data:/data docker.patpat.vip:9503/redis:5.0.3
```

---

## 相关文章

- [Docker 入门指南：核心概念、安装配置与容器化实践](/zh/posts/docker/2019-05-13-learn-docker/) - Docker 基础概念与入门教程
- [Docker Compose 完全指南：从入门到生产实践](/zh/posts/docker/2026-01-19-docker-compose-complete-guide/) - 多容器编排与生产环境最佳实践
- [使用 Nexus3 搭建 Docker 私有镜像仓库](/zh/posts/docker/2019-06-12-next3-dockerhub/) - 企业级私有仓库搭建方案
