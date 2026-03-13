+++
date = '2019-06-12T20:50:36+08:00'
title = 'Nexus3 搭建 Docker 私有镜像仓库：企业级 Registry 完整教程'
description = '使用 Nexus3 搭建企业级 Docker 私有镜像仓库完整教程，详解 hosted、proxy、group 三种仓库类型配置，实现镜像的推送和拉取，附 Ubuntu 客户端 insecure-registries 配置'
toc = true
tags = ['Docker', 'Nexus3', 'Registry', '私有仓库', 'DevOps']
categories = ['Docker']
+++

[Nexus](https://www.sonatype.com/nexus-repository-oss)是有名的Maven仓库管理器。如果你使用Maven，你可以从Maven中央仓库下载所需要的构件（artifact），但这通常不是一个好的做法，你应该在本地架设一个Maven仓库服务器，在代理远程仓库的同时维护本地仓库，以节省带宽和时间，Nexus就可以满足这样的需要。此外，他还提供了强大的仓库管理功能，构件搜索功能，它基于REST，友好的UI是一个extjs的REST客户端，它占用较少的内存，基于简单文件系统而非数据库。这些优点使其日趋成为最流行的Maven仓库管理器。除此之外，最新Nexus3还可以管理多种格式的镜像，如下：

## 1.环境

系统：ubuntu16.04
docker：18.02.0-ce

## 2.获取nexus3镜像

`docker pull sonatype/nexus3`

## 3.启动镜像

```
docker run -id --privileged=true --name=nexus3 --restart=always -p 9500:8081 -p 9501:9501 -p 9502:9502 -p 9503:9503 -v /usr/local/programs/nexus3/nexus-data:/nexus-data sonatype/nexus3:latest
```

端口(注意映射了多个端口)：

- 9500: nexus3网页端
- 9501：docker(hosted)私有仓库，可以pull和push
- 9502：docker(proxy)代理远程仓，只能pull
- 9503：docker(group)私有仓库和代理的组，只能pull

运维人员维护镜像试用9501端口，项目pull镜像使用9503端口，全部可匿名pull。

数据：在宿主机创建目录/usr/local/programs/nexus3/nexus-data，/nexus-data为docker容器数据存储目录。所以-v设置映射关系后数据将会存到宿主机/usr/local/programs/nexus3/nexus-data

## 4.配置私有仓库

访问<http://localhost:9500>默认账号admin/admin123

几种repository的类型

- hosted，本地仓库，自己创建的镜像上传到这一类型的仓库。
- proxy，代理仓库，它们被用来代理远程的公共仓库，如dockerhub官方仓库。
- group，仓库组，用来合并多个hosted/proxy仓库，当你的项目希望在多个repository使用资源时就不需要多次引用了，只需要引用一个group即可。

创建仓库前先创建对应的blob stores，在创建仓库时选择对应的blob，创建group组时调整好优先级，一般是host高于proxy。

**注意**：创建仓库时如果勾选匿名可pull项，需找到security->realms页面(<http://localhost:9500/#admin/security/realms>)，将docker bearer token realm项添加到右边激活，否则匿名docker pull会报错无权限.

## 5. 用户侧docker添加私有仓

### mac和win

打开docker的设置，选择daemon，在insecure registries里添加

```
http://localhost:9503
```

如果是运维人员，要push镜像，再添加一条 `http://localhost:9501`

重启docker。

### ubuntu

命令`vi /etc/docker/daemon.json`，插入下面内容:

```
{
    "insecure-registries": [
        "http://localhost:9501",
        "http://localhost:9503"
    ]
}
```

执行`sudo service docker restart`重启docker。

## 6.管理镜像

### 添加镜像

先登录到localhost:9501私有仓，执行`docker login localhost:9501`登录，看到login success表示登录成功。

例如本地有一个php:7.0镜像,需推送到私有仓,步骤如下：

1. 用docker tag命令打一个新tag，`docker tag php:7.0 localhost:9501/php:7.0`

2. 推送：`docker push localhost:9501/php:7.0`

可以打开<http://localhost:9500/#browse/browse>查看上传镜像。

### 拉取镜像

从docker group端口9503拉取，例如：`docker pull localhost:9503/php:7.0`

### 搜索镜像
从docker group端口9503搜索，例如：`docker search localhost:9503/php:7.0`，会从docker group包含的仓库按照设置的优先级搜索。

---

## 相关文章

- [Docker 入门指南：核心概念、安装配置与容器化实践](/posts/docker/2019-05-13-learn-docker/) - Docker 基础概念与入门教程
- [Docker Compose 完全指南：从入门到生产实践](/posts/docker/2026-01-19-docker-compose-complete-guide/) - 多容器编排与生产环境最佳实践
- [Docker 常用命令速查手册](/posts/docker/2019-11-14-docker-commands/) - 日常开发必备命令参考
