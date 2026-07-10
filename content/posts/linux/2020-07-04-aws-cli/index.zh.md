+++
title = 'AWS CLI 完全指南：安装配置、S3/EC2 常用命令与权限排错'
date = 2020-07-04T00:16:54+08:00
description = 'AWS CLI 从零上手：安装、aws configure、S3/EC2/IAM 高频命令、常见报错与权限问题排查，适合运维与开发日常使用。'
toc = true
tags = ["AWS", "AWS CLI", "S3", "EC2", "Cloud Computing", "DevOps", "CLI"]
categories = ["Linux"]
keywords = ["AWS CLI", "AWS 命令行", "S3 命令", "EC2 命令", "aws configure"]
+++
![AWS CLI 命令行工具完全指南](cover.webp)

**AWS CLI**（Amazon Web Services Command Line Interface）是 AWS 官方提供的统一命令行工具，让你能够通过终端直接管理所有 AWS 服务。本文将详细介绍 AWS CLI 的安装配置方法和常用命令，帮助你快速上手云资源管理。

## 一、安装 AWS CLI

AWS CLI 目前推荐使用 **v2 版本**，它更快、更安全，且支持所有最新特性。

### 1. macOS 安装

**方式一：使用 Homebrew（推荐）**

```bash
brew install awscli
```

**方式二：使用官方安装包**

```bash
# 下载安装包
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"

# 安装
sudo installer -pkg AWSCLIV2.pkg -target /
```

### 2. Linux 安装

```bash
# x86_64 架构
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# ARM64 架构
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### 3. Windows 安装

下载并运行 MSI 安装程序：

```
https://awscli.amazonaws.com/AWSCLIV2.msi
```

### 4. 验证安装

```bash
aws --version
# 输出示例: aws-cli/2.27.41 Python/3.11.6 Darwin/24.0.0
```

![验证 AWS CLI 安装版本](aws-version.webp)

## 二、配置 AWS CLI

### 1. 快速配置

使用 `aws configure` 命令进行交互式配置：

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

配置完成后会在 `~/.aws/` 目录下生成两个文件：

| 文件 | 内容 |
|------|------|
| `~/.aws/credentials` | 存储访问密钥 |
| `~/.aws/config` | 存储区域和输出格式 |

### 2. 多配置文件管理

为不同环境创建独立配置：

```bash
# 配置生产环境
aws configure --profile prod

# 配置测试环境
aws configure --profile dev
```

使用指定配置：

```bash
# 方式一：命令行参数
aws s3 ls --profile prod

# 方式二：环境变量
export AWS_PROFILE=prod
aws s3 ls
```

### 3. 环境变量配置

通过环境变量覆盖配置文件（优先级更高）：

```bash
# Linux/macOS
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-west-2

# Windows PowerShell
$Env:AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
$Env:AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
$Env:AWS_DEFAULT_REGION="us-west-2"
```

### 4. 验证配置

```bash
# 检查当前身份
aws sts get-caller-identity

# 输出示例
{
    "UserId": "AIDAEXAMPLEUSERID",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/username"
}
```

## 三、S3 存储操作

S3 是 AWS 最常用的对象存储服务，CLI 提供了丰富的操作命令。

### 1. 存储桶管理

```bash
# 列出所有存储桶
aws s3 ls

# 创建存储桶
aws s3 mb s3://my-bucket-name

# 创建指定区域的存储桶
aws s3 mb s3://my-bucket-name --region ap-northeast-1

# 删除空存储桶
aws s3 rb s3://my-bucket-name

# 强制删除非空存储桶（包含所有对象）
aws s3 rb s3://my-bucket-name --force
```

### 2. 对象操作

```bash
# 列出存储桶内容
aws s3 ls s3://my-bucket

# 列出带前缀的对象
aws s3 ls s3://my-bucket/folder/

# 查看目录大小（递归统计）
aws s3 ls --summarize --human-readable --recursive s3://my-bucket
```

### 3. 上传与下载

```bash
# 上传单个文件
aws s3 cp local-file.txt s3://my-bucket/

# 下载单个文件
aws s3 cp s3://my-bucket/remote-file.txt ./

# 递归上传整个目录
aws s3 cp ./local-folder s3://my-bucket/folder/ --recursive

# 递归下载整个目录
aws s3 cp s3://my-bucket/folder/ ./local-folder --recursive

# 排除特定文件
aws s3 cp ./local-folder s3://my-bucket/ --recursive --exclude "*.log"

# 仅包含特定文件
aws s3 cp ./local-folder s3://my-bucket/ --recursive --include "*.jpg" --exclude "*"
```

### 4. 同步目录

`sync` 命令只传输变化的文件，适合增量备份：

```bash
# 本地同步到 S3
aws s3 sync ./local-folder s3://my-bucket/folder/

# S3 同步到本地
aws s3 sync s3://my-bucket/folder/ ./local-folder

# 同步并删除目标中多余的文件
aws s3 sync ./local-folder s3://my-bucket/folder/ --delete

# 指定存储类别
aws s3 sync ./local-folder s3://my-bucket/ --storage-class STANDARD_IA
```

### 5. 移动与删除

```bash
# 移动/重命名对象
aws s3 mv s3://my-bucket/old-name.txt s3://my-bucket/new-name.txt

# 移动整个目录
aws s3 mv s3://source-bucket/ s3://dest-bucket/ --recursive

# 删除单个对象
aws s3 rm s3://my-bucket/file.txt

# 递归删除目录
aws s3 rm s3://my-bucket/folder/ --recursive
```

### 6. 访问控制

```bash
# 上传并设置公开读取权限
aws s3 cp file.txt s3://my-bucket/ --acl public-read

# 授予特定用户权限
aws s3 cp file.txt s3://my-bucket/ --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers
```

### 7. 流式传输

```bash
# 从标准输入上传
echo "Hello World" | aws s3 cp - s3://my-bucket/hello.txt

# 输出到标准输出
aws s3 cp s3://my-bucket/hello.txt -

# 管道处理（压缩后上传）
aws s3 cp s3://my-bucket/large-file - | gzip | aws s3 cp - s3://my-bucket/large-file.gz
```

## 四、EC2 实例管理

### 1. 实例查询

```bash
# 列出所有实例
aws ec2 describe-instances

# 查看指定实例
aws ec2 describe-instances --instance-ids i-1234567890abcdef0

# 按状态筛选（运行中）
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"

# 按标签筛选
aws ec2 describe-instances --filters "Name=tag:Name,Values=my-server"

# 按实例类型筛选
aws ec2 describe-instances --filters "Name=instance-type,Values=t2.micro"

# 使用 JMESPath 提取特定字段
aws ec2 describe-instances --query "Reservations[].Instances[].InstanceId"
```

### 2. 实例控制

```bash
# 启动实例
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# 停止实例
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# 重启实例
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# 终止实例（删除）
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

### 3. 创建实例

```bash
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --count 1 \
    --instance-type t2.micro \
    --key-name MyKeyPair \
    --security-group-ids sg-903004f8 \
    --subnet-id subnet-6e7f829e
```

### 4. 标签管理

```bash
# 添加标签
aws ec2 create-tags --resources i-1234567890abcdef0 --tags Key=Name,Value=MyInstance

# 添加多个标签
aws ec2 create-tags --resources i-1234567890abcdef0 \
    --tags Key=Name,Value=MyInstance Key=Environment,Value=Production
```

### 5. 安全组管理

```bash
# 列出安全组
aws ec2 describe-security-groups

# 创建安全组
aws ec2 create-security-group \
    --group-name my-sg \
    --description "My security group" \
    --vpc-id vpc-1234567890abcdef0

# 添加入站规则（允许 SSH）
aws ec2 authorize-security-group-ingress \
    --group-id sg-903004f8 \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
```

## 五、Kinesis 数据流

```bash
# 列出所有数据流
aws kinesis list-streams

# 写入数据
aws kinesis put-record \
    --stream-name my-stream \
    --partition-key 123 \
    --data "Hello Kinesis"

# 获取分片迭代器
aws kinesis get-shard-iterator \
    --stream-name my-stream \
    --shard-id shardId-000000000000 \
    --shard-iterator-type TRIM_HORIZON

# 读取数据
aws kinesis get-records --shard-iterator <iterator>
```

## 六、SQS 消息队列

```bash
# 列出队列
aws sqs list-queues

# 发送消息
aws sqs send-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
    --message-body "Hello SQS"

# 接收消息
aws sqs receive-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
    --attribute-names All \
    --max-number-of-messages 10

# 删除消息
aws sqs delete-message \
    --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
    --receipt-handle <handle>
```

## 七、SNS 推送服务

```bash
# 列出主题
aws sns list-topics

# 列出平台应用
aws sns list-platform-applications

# 发布消息
aws sns publish \
    --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
    --message "Hello SNS"

# 订阅主题
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
    --protocol email \
    --notification-endpoint user@example.com
```

## 八、实用技巧

### 1. 输出格式

```bash
# JSON（默认）
aws s3 ls --output json

# 表格格式（易读）
aws ec2 describe-instances --output table

# 纯文本（便于脚本处理）
aws ec2 describe-instances --output text

# YAML 格式
aws ec2 describe-instances --output yaml
```

### 2. JMESPath 查询

```bash
# 提取实例 ID
aws ec2 describe-instances --query "Reservations[].Instances[].InstanceId"

# 提取指定字段
aws ec2 describe-instances \
    --query "Reservations[].Instances[].[InstanceId,InstanceType,State.Name]" \
    --output table

# 条件筛选
aws ec2 describe-instances \
    --query "Reservations[].Instances[?State.Name=='running'].InstanceId"
```

### 3. 分页处理

```bash
# 限制返回数量
aws s3api list-objects-v2 --bucket my-bucket --max-items 100

# 使用分页令牌
aws s3api list-objects-v2 --bucket my-bucket --starting-token <token>
```

### 4. 获取帮助

```bash
# 查看服务列表
aws help

# 查看特定服务命令
aws s3 help

# 查看子命令帮助
aws s3 cp help
```

### 5. 预演模式

```bash
# 检查权限但不执行
aws ec2 run-instances --dry-run --image-id ami-123456
```

## 九、常见问题

### 1. 凭证错误

```
An error occurred (InvalidAccessKeyId): The AWS Access Key Id you provided does not exist
```

**解决方法**：检查 Access Key ID 是否正确，确认 IAM 用户状态正常。

### 2. 权限不足

```
An error occurred (AccessDenied): Access Denied
```

**解决方法**：确认 IAM 用户或角色拥有所需的权限策略。

### 3. 区域配置错误

```
Could not connect to the endpoint URL
```

**解决方法**：检查区域配置是否正确，某些服务仅在特定区域可用。

## 总结

AWS CLI 是管理云资源的强大工具，掌握常用命令可以大幅提升运维效率。核心要点：

1. **安装推荐 v2 版本**，支持所有最新特性
2. **多配置文件管理**不同环境的凭证
3. **S3 命令**：`cp`/`sync`/`mv`/`rm` 覆盖日常操作
4. **EC2 命令**：配合 `--query` 和 `--filters` 精准定位资源
5. **善用帮助命令**：`aws <service> help` 查看详细用法

## 参考资料

- [AWS CLI 官方文档](https://docs.aws.amazon.com/cli/latest/userguide/)
- [AWS CLI S3 命令参考](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html)
- [AWS CLI EC2 命令参考](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2.html)
- [AWS 架构图标](https://aws.amazon.com/architecture/icons/)

## 相关阅读

- [curl 命令完全指南](/zh/posts/linux/2020-06-29-curl/)
- [Oh My Zsh 配置指南](/zh/posts/linux/2015-06-17-shell-zsh/)
- [Docker 常用命令速查](/zh/posts/docker/2019-11-14-docker-commands/)
