---
title: "Linux/macOS 常用命令速查手册（持续更新）"
date: 2020-03-19 10:55:52
author: "bruce"
description: "Linux 和 macOS 常用命令速查手册，涵盖文件操作、网络调试、进程管理、文本处理、磁盘管理等日常运维开发必备命令，附带实用示例"
toc: true
tags:
    - Linux
    - macOS
    - Shell
    - 命令行
    - 运维
categories:
    - Linux
---

Linux/macOS 命令行是开发者必备技能。本文整理了日常工作中高频使用的命令，按功能分类便于查找，持续更新中。

## 一、网络相关

### 1. netstat - 查看网络连接

**Linux**：
```bash
# 查看指定端口占用
netstat -ntlp | grep 3000

# 查看指定进程的网络连接
netstat -ntlp | grep nginx

# 查看所有监听端口
netstat -tuln
```

**macOS**：
```bash
# 查看指定端口
netstat -an | grep 3306

# 查看所有监听端口
netstat -an | grep LISTEN
```

> Tips: Linux 下需要加 `sudo` 才能看到进程名称

### 2. lsof - 查看打开的文件/端口

```bash
# 查看端口占用（最常用）
lsof -i:80
lsof -i:3000

# 查看所有监听端口
sudo lsof -i -P | grep LISTEN

# 查看指定进程打开的文件
lsof -p <PID>

# 查看指定用户打开的文件
lsof -u username
```

### 3. ss - 更快的 netstat 替代品

```bash
# 查看所有 TCP 连接
ss -t

# 查看所有监听端口
ss -tuln

# 查看指定端口
ss -tuln | grep :80

# 查看 socket 统计信息
ss -s
```

### 4. ping & telnet - 网络连通性测试

```bash
# 测试网络连通性
ping google.com

# 指定次数
ping -c 4 google.com

# 测试端口连通性
telnet 192.168.1.1 3306

# macOS 下用 nc 替代 telnet
nc -zv 192.168.1.1 3306
```

### 5. dig & nslookup - DNS 查询

```bash
# 查询域名 A 记录
dig example.com

# 查询指定类型记录
dig example.com MX
dig example.com TXT

# 使用指定 DNS 服务器查询
dig @8.8.8.8 example.com

# 简洁输出
dig +short example.com

# nslookup 方式
nslookup example.com
```

### 6. ifconfig & ip - 网卡信息

```bash
# 查看网卡信息
ifconfig
ifconfig en0    # macOS 查看指定网卡

# Linux 推荐使用 ip 命令
ip addr
ip addr show eth0
ip route        # 查看路由表
```

---

## 二、进程管理

### 1. ps - 查看进程

```bash
# 查看所有进程（最常用）
ps aux
ps -ef

# 查找指定进程
ps aux | grep nginx
ps -ef | grep java

# 按 CPU/内存排序
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# 树形显示进程
ps auxf        # Linux
pstree         # 需要安装
```

### 2. kill - 终止进程

```bash
# 正常终止
kill <PID>

# 强制终止
kill -9 <PID>

# 按名称终止
pkill nginx
killall nginx

# 常用信号
# -1 (HUP)  重新加载配置
# -9 (KILL) 强制终止
# -15 (TERM) 正常终止（默认）
```

### 3. top & htop - 实时监控

```bash
# 实时查看系统资源
top

# top 常用快捷键
# P - 按 CPU 排序
# M - 按内存排序
# k - 终止进程
# q - 退出

# htop（更友好，需安装）
htop
```

### 4. nohup & 后台运行

```bash
# 后台运行，忽略挂断信号
nohup ./script.sh &

# 输出重定向
nohup ./script.sh > output.log 2>&1 &

# 查看后台任务
jobs

# 前后台切换
bg %1    # 放到后台
fg %1    # 放到前台
```

### 5. systemctl - 服务管理 (Linux)

```bash
# 启动/停止/重启服务
systemctl start nginx
systemctl stop nginx
systemctl restart nginx

# 查看服务状态
systemctl status nginx

# 开机自启
systemctl enable nginx
systemctl disable nginx

# 查看所有运行的服务
systemctl list-units --type=service --state=running
```

---

## 三、文件操作

### 1. find - 文件查找

```bash
# 按名称查找
find /path -name "*.log"
find . -name "config.yml"

# 忽略大小写
find . -iname "readme*"

# 按类型查找
find . -type f    # 文件
find . -type d    # 目录

# 按时间查找
find . -mtime -7     # 7天内修改的
find . -mtime +30    # 30天前修改的

# 按大小查找
find . -size +100M   # 大于100M
find . -size -1k     # 小于1k

# 找到后执行命令
find . -name "*.tmp" -delete
find . -name "*.log" -exec rm {} \;
find . -type f -name "*.txt" -exec grep "keyword" {} \;
```

### 2. chmod & chown - 权限管理

```bash
# 修改权限
chmod 755 script.sh
chmod +x script.sh      # 添加执行权限
chmod -R 644 ./dir      # 递归修改

# 常用权限数字
# 7 = rwx (读写执行)
# 6 = rw- (读写)
# 5 = r-x (读执行)
# 4 = r-- (只读)

# 修改所有者
chown user:group file
chown -R user:group ./dir
```

### 3. tar - 打包压缩

```bash
# 打包压缩
tar -czvf archive.tar.gz ./dir
tar -cjvf archive.tar.bz2 ./dir

# 解压
tar -xzvf archive.tar.gz
tar -xzvf archive.tar.gz -C /target/dir

# 查看压缩包内容
tar -tzvf archive.tar.gz

# 参数说明
# c - 创建
# x - 解压
# z - gzip
# j - bzip2
# v - 显示过程
# f - 指定文件名
```

### 4. ln - 软链接/硬链接

```bash
# 创建软链接（最常用）
ln -s /path/to/source /path/to/link

# 创建硬链接
ln /path/to/source /path/to/link

# 查看链接指向
ls -la
readlink /path/to/link
```

### 5. rsync - 高效文件同步

```bash
# 本地同步
rsync -av source/ dest/

# 远程同步
rsync -avz source/ user@host:/path/dest/

# 常用选项
# -a 归档模式（保留权限等）
# -v 显示详情
# -z 传输时压缩
# --delete 删除目标多余文件
# --exclude 排除文件

# 排除特定文件
rsync -av --exclude='*.log' source/ dest/
```

---

## 四、文本处理

### 1. grep - 文本搜索

```bash
# 基本搜索
grep "keyword" file.txt

# 递归搜索目录
grep -r "keyword" ./dir

# 忽略大小写
grep -i "keyword" file.txt

# 显示行号
grep -n "keyword" file.txt

# 显示上下文
grep -A 3 "keyword" file.txt   # 后3行
grep -B 3 "keyword" file.txt   # 前3行
grep -C 3 "keyword" file.txt   # 前后3行

# 正则表达式
grep -E "pattern1|pattern2" file.txt

# 反向匹配（排除）
grep -v "keyword" file.txt

# 只显示匹配的文件名
grep -l "keyword" *.txt
```

### 2. awk - 文本处理

```bash
# 打印指定列
awk '{print $1}' file.txt
awk '{print $1, $3}' file.txt

# 指定分隔符
awk -F: '{print $1}' /etc/passwd
awk -F',' '{print $2}' data.csv

# 条件过滤
awk '$3 > 100 {print $1, $3}' file.txt

# 计算求和
awk '{sum += $1} END {print sum}' file.txt

# 统计行数
awk 'END {print NR}' file.txt
```

### 3. sed - 流编辑器

```bash
# 替换文本（打印）
sed 's/old/new/' file.txt
sed 's/old/new/g' file.txt      # 全局替换

# 直接修改文件
sed -i 's/old/new/g' file.txt
sed -i.bak 's/old/new/g' file.txt  # 备份原文件

# 删除行
sed '/pattern/d' file.txt    # 删除匹配行
sed '1d' file.txt            # 删除第1行
sed '1,5d' file.txt          # 删除1-5行

# 打印指定行
sed -n '5p' file.txt         # 第5行
sed -n '5,10p' file.txt      # 5-10行
```

### 4. sort & uniq - 排序去重

```bash
# 排序
sort file.txt
sort -r file.txt       # 逆序
sort -n file.txt       # 数字排序
sort -k2 file.txt      # 按第2列排序

# 去重（需要先排序）
sort file.txt | uniq
sort file.txt | uniq -c    # 统计次数
sort file.txt | uniq -d    # 只显示重复行
```

### 5. head & tail - 查看文件头尾

```bash
# 查看前/后 N 行
head -n 20 file.txt
tail -n 20 file.txt

# 实时追踪日志（最常用）
tail -f app.log
tail -f -n 100 app.log     # 从最后100行开始

# 多文件追踪
tail -f *.log
```

### 6. wc - 统计

```bash
# 统计行数/单词数/字符数
wc file.txt

# 只统计行数
wc -l file.txt

# 统计目录下文件数量
ls | wc -l
find . -type f | wc -l
```

---

## 五、磁盘管理

### 1. df - 磁盘使用情况

```bash
# 查看磁盘使用
df -h

# 查看指定目录所在分区
df -h /var

# 查看 inode 使用情况
df -i
```

### 2. du - 目录大小

```bash
# 查看目录大小
du -sh /var/log
du -sh *

# 按大小排序
du -sh * | sort -hr

# 查看子目录大小
du -h --max-depth=1

# 找出最大的文件/目录
du -a /var | sort -rn | head -10
```

### 3. ncdu - 交互式磁盘分析

```bash
# 安装
sudo apt install ncdu    # Ubuntu
brew install ncdu        # macOS

# 使用
ncdu /var
```

---

## 六、系统信息

### 1. 系统基本信息

```bash
# 系统版本
uname -a
cat /etc/os-release     # Linux
sw_vers                 # macOS

# 主机名
hostname

# 运行时间和负载
uptime
```

### 2. 硬件信息

```bash
# CPU 信息
cat /proc/cpuinfo       # Linux
sysctl -n machdep.cpu.brand_string  # macOS
nproc                   # CPU 核心数

# 内存信息
free -h                 # Linux
vm_stat                 # macOS

# 查看内存使用前10的进程
ps aux --sort=-%mem | head -10
```

### 3. 环境变量

```bash
# 查看所有环境变量
env
printenv

# 查看指定变量
echo $PATH
echo $HOME

# 临时设置
export MY_VAR="value"

# 永久设置（加入配置文件）
echo 'export MY_VAR="value"' >> ~/.zshrc
source ~/.zshrc
```

---

## 七、用户与权限

### 1. 用户管理

```bash
# 当前用户
whoami
id

# 切换用户
su - username
sudo -u username command

# 查看登录用户
who
w
last    # 登录历史
```

### 2. sudo 相关

```bash
# 以 root 执行
sudo command

# 切换到 root
sudo -i
sudo su -

# 编辑 sudoers
sudo visudo
```

---

## 八、实用技巧

### 1. 命令历史

```bash
# 查看历史命令
history
history | grep keyword

# 执行上一条命令
!!

# 执行历史中第N条命令
!N

# 搜索历史命令
Ctrl + R
```

### 2. 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + C` | 终止当前命令 |
| `Ctrl + Z` | 暂停当前命令 |
| `Ctrl + D` | 退出终端 |
| `Ctrl + L` | 清屏 |
| `Ctrl + A` | 移到行首 |
| `Ctrl + E` | 移到行尾 |
| `Ctrl + U` | 删除光标前内容 |
| `Ctrl + K` | 删除光标后内容 |
| `Ctrl + W` | 删除前一个单词 |
| `Ctrl + R` | 搜索历史命令 |

### 3. 管道与重定向

```bash
# 管道
command1 | command2

# 输出重定向
command > file.txt      # 覆盖
command >> file.txt     # 追加

# 错误重定向
command 2> error.log
command > output.log 2>&1   # 标准输出和错误都写入

# 输入重定向
command < input.txt

# 丢弃输出
command > /dev/null 2>&1
```

### 4. pv - 显示进度

```bash
# 安装
sudo apt install pv     # Ubuntu
brew install pv         # macOS

# 文件复制显示进度
pv source.iso > dest.iso

# 限速复制
pv -L 2m source.iso > dest.iso

# MySQL 导入显示进度
pv database.sql | mysql -u root -p dbname
```

---

## 九、macOS 特有命令

### 1. 允许安装任意来源应用

```bash
# 开启任意来源
sudo spctl --master-disable

# 移除安全隔离属性
sudo xattr -r -d com.apple.quarantine /Applications/xxx.app
```

### 2. 剪贴板操作

```bash
# 复制到剪贴板
cat file.txt | pbcopy
echo "hello" | pbcopy

# 从剪贴板粘贴
pbpaste
pbpaste > file.txt
```

### 3. 打开文件/应用

```bash
# 用默认程序打开
open file.pdf
open .                  # 打开当前目录
open -a "Visual Studio Code" file.txt
```

### 4. 系统管理

```bash
# 查看电池状态
pmset -g batt

# 防止休眠（咖啡因模式）
caffeinate -d           # 防止显示器休眠
caffeinate -i           # 防止系统休眠

# DNS 缓存刷新
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

---

## 参考资料

- [Linux 命令大全](https://www.runoob.com/linux/linux-command-manual.html)
- [The Linux Command Line](https://linuxcommand.org/)
- [macOS Terminal 用户指南](https://support.apple.com/zh-cn/guide/terminal/welcome/mac)

---

## 相关文章

- [Oh My Zsh 安装配置指南：打造高效终端环境](/posts/linux/2015-06-17-shell-zsh/) - 强大的 Zsh 配置框架
- [Shell 脚本特殊变量详解：$$、$?、$@、$# 等用法](/posts/linux/2019-05-13-linux-shell-vars/) - Shell 脚本编程必备知识
- [Linux curl 命令完全指南：HTTP 请求调试必备工具](/posts/linux/2020-06-29-curl/) - HTTP 请求调试神器
- [Traceroute 网络诊断命令详解：追踪数据包路由路径](/posts/linux/2020-06-28-traceroute/) - 网络故障定位必备工具


## 相关阅读（Linux / Docker 深度内链）

- [curl 命令大全：从基础到高级用法](/posts/linux/2020-06-29-curl/)
- [traceroute 命令详解：网络路径排障](/posts/linux/2020-06-28-traceroute/)
- [Docker 常用命令速查手册](/posts/docker/2019-11-14-docker-commands/)
- [Docker Compose 完全指南（安装到实战）](/posts/docker/2026-01-19-docker-compose-complete-guide/)
- [docker-compose.yml 详解（字段级拆解）](/posts/docker/2026-01-24-docker-compose-yml-explained/)
