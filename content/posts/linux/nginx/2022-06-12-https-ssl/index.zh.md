+++
date = '2014-03-18T23:15:02+08:00'
draft = true
title = 'Nginx 自签名 SSL 证书配置 HTTPS 完整教程'
description = '使用 OpenSSL 生成自签名 SSL 证书并配置 Nginx 实现 HTTPS 加密访问的完整教程，包含私钥生成、证书签署和 Nginx 配置步骤'
toc = true
tags = ['Nginx', 'HTTPS', 'SSL', 'OpenSSL', '证书']
categories = ['Linux']
+++
![image](/images/https-ssl/https.webp)

## 安装openssl

ssl证书有很多第三方厂商，可购买也有一些提供免费证书。ssl证书也可自签，通常会用到openssl。检查是否安装openssl `openssl version -a`, 如未安装请执行：

```
sudo apt-get install openssl
sudo apt-get install openssl-devel
```

## 生成私钥和证书

生成私钥,命令行执行`openssl genrsa -des3 -out app.key 1024`，截图如下

[![QQ20140318-1](/images/https-ssl/QQ20140318-1.webp)](/images/https-ssl/QQ20140318-1.webp)

很清晰了吧，下面继续生成签署申请`openssl req -new -key app.key -out app.csr`执行这个后下面会需要填一些信息，截图如下，密码的地方可以都输同一个

[![QQ20140318-2](/images/https-ssl/QQ20140318-2.webp)](/images/https-ssl/QQ20140318-2.webp)

生成服务器的私钥 `openssl rsa -in app.key -out app_server.key` ,截图如下

[![QQ20140318-3](/images/https-ssl/QQ20140318-3.webp)](/images/https-ssl/QQ20140318-3.webp)

给网站服务器签署证书
`openssl req -new -x509 -days 3650 -key app_server.key -out app_server.crt`

执行后步骤和第一部差不多，填写完，需要注意的是Common Name一定要填对。

至此我们得到了四个文件,下面配置Nginx

## 配置Nginx

将app_server.crt和app_server.key两个文件拷贝到/etc/nginx/conf.d目录下，打开test_nginx.conf(nginx配置文件) `sudo vi test_nginx.conf`

端口设置为443：

```
ssl on;
ssl_certificate /etc/nginx/conf.d/app_server.crt;
ssl_certificate_key /etc/nginx/conf.d/app_server.key;
```

**注意crt和key文件是绝对路径,需重启nginx。**

配置完成截图

[![QQ20140318-4](/images/https-ssl/QQ20140318-4.webp)](/images/https-ssl/QQ20140318-4.webp)

重启nginx，`sudo service nginx restart`。


