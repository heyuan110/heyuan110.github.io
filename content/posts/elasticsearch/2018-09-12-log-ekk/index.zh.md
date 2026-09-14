+++
date = '2018-09-12T18:52:59+08:00'
title = 'AWS EKK 日志系统搭建：Elasticsearch + Kinesis + Kibana 实战教程'
description = '基于 AWS 托管服务搭建 EKK 日志系统完整教程，使用 Amazon Elasticsearch Service、Kinesis 和 Kibana 实现 Nginx 日志收集分析，比 ELK 更易运维'
toc = true
tags = ['Elasticsearch', 'AWS', 'Kinesis', 'Kibana', '日志分析']
categories = ['Elasticsearch']

[[params.faqItems]]
question = "EKK 是什么？和 ELK 有什么区别？"
answer = "EKK 指 Elasticsearch + Kinesis + Kibana，和 ELK 是同一套日志思路，区别是用 Kinesis 替掉 Logstash，且全部组件都是 AWS 托管服务。Amazon Elasticsearch Service 负责集群和 Kibana，Kinesis 负责采集投递，不用自己维护 Logstash 集群。代价是数据加工灵活性下降，原本 Logstash filter 干的活要挪到 Lambda 或索引模板里。"

[[params.faqItems]]
question = "怎么把 EC2 上的 Nginx 日志通过 Kinesis 送进 Elasticsearch？"
answer = "先装 Kinesis Agent：clone `amazon-kinesis-agent`，装 openjdk-8-jdk，跑 `sudo ./setup --install`。再改 `/etc/aws-kinesis/agent.json`，填 IAM Key、对应区域 endpoint 和一个 flow——`filePattern` 指向 access.log，目的地填 `deliveryStream`（Firehose）或 `kinesisStream`。最后 `sudo service aws-kinesis-agent start` 启动，改配置后要 restart。"

[[params.faqItems]]
question = "Kinesis Agent 解析不出自定义字段怎么办？"
answer = "因为内置的 COMMONAPACHELOG 只认标准 Apache 字段，你自己加的 upstream_response_time、request_time 它一概忽略。做法是保留 `optionName: LOGTOJSON`，同时自己写 `matchPattern` 正则，并用 `customFieldNames` 按捕获组顺序列出字段名。还有一个高频坑：Kinesis Agent 是 Java 程序，正则必须用 Java 语法和 Java 的转义规则，不能照搬 Python 或 PCRE 写法。"

[[params.faqItems]]
question = "matchPattern 正则怎么在上线前验证？"
answer = "拿真实日志行去跑一遍 Java 再写进 agent.json。用在线 Java 运行器，`Pattern.compile()` 编译你的正则，`matcher(line).find()` 之后把每个 `m.group(n)` 都打印出来，确认分组顺序和 customFieldNames 一一对应。特别注意转义：JSON 配置里的一个反斜杠，写成 Java 字符串字面量要变成两个。分组全部打印正确了再拷回 matchPattern。"

[[params.faqItems]]
question = "为什么日志进了 ES，所有字段都是 text 类型？"
answer = "因为没给映射，ES 动态推断默认全按 text 处理，结果是字节数没法做范围查询、时间字段也建不了时序图表。解法是在数据写入前建好索引模板：`PUT _template/nginx-access-log_template`，`template` 填通配符 `*-nginx-access-log-*`，这样 api-nginx-access-log-2018-08-02 这类按天索引会自动套用。body_bytes_sent 和 connection_serial_number 映射成 long，两个耗时字段用 double，文本字段加 keyword 子字段方便聚合。"

[[params.faqItems]]
question = "datetime 字段一直解析失败是什么原因？"
answer = "因为 Nginx 的 time_local 不是 ISO 8601 格式。默认日志写出来是 `12/Sep/2018:03:59:12`，映射必须写成 `format: dd/MMM/YYYY:HH:mm:ss`，套常见的 ISO 格式根本匹配不上，字段就退回成 text。这个细节能坑掉好几个小时。另外这套管道有两个已知缺口：没有地理位置、没有解析浏览器和设备信息，补救办法是在 Firehose 和 ES 之间加一个 Lambda 做 GeoIP 和 User-Agent 解析。"
+++

EKK是一套基于AWS相关服务搭建的日志收集系统，包含Amazon Elasticsearch Service, Amazon Kinesis, and Kibana，简称EKK.相比ELK搭建维护运维复杂，EKK更加简便。下图是EKK基本架构：

![EKK](https://d2908q01vomqb2.cloudfront.net/472b07b9fcf2c2451e8781e944bf5f77cd8457c8/2017/09/07/1-2.png)

本文重点记录nginx日志怎样收集和以正确格式存到es，不会就每一步详细讲解。

## 一、准备工作：

1. 开一台ec2，选择ubuntu16.04，搭建nginx一个nginx服务，设置nginx日志格式:

```
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for" '
                      '$connection "$upstream_addr" '
                      'upstream_response_time $upstream_response_time request_time $request_time';
```

最终access.log里的日志格式如下：

```
192.168.13.1 - - [12/Sep/2018:03:59:12 +0000]
"GET /v1/home HTTP/1.1" 2002787 "https://test.com/product/Sweet-Ice-Cream-Short-sleeve-Top-and-Pink-Shorts-for-Toddler-Baby.html" "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 [FBAN/FBIOS;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Telekom.de;FBID/phone;FBLC/de_DE;FBOP/5;FBRV/123725744]" "2002:c7:6f02:9801:d506:6bda:e6ca:b6f9, 112.118.106.116" 12340 "127.0.0.1:9000" upstream_response_time 0.11 request_time 0.11
```

2. 创建可访问Kinesis stream或Kinesis firehose, AWS ES服务的IAM账号，保存awsAccessKeyId和awsSecretAccessKey。
3. AWS上启动ES服务TestES，创建时类型务必选择public，后面再做安全策略。
4.  创建Kinesis firehose(如果有一个源对多个标的的需求可以使用Kinesis stream)，数据流向选择上面创建的TestES。

准备工作大概完成。

## 二、收集日志

1. 在ec2上安装Amazon Kinesis Agent:

```
1. 下载源码
git clone https://github.com/awslabs/amazon-kinesis-agent.git

2. 在aws的ubuntu16.04上需再安装java jdk
sudo apt-get install openjdk-8-jdk

3. 开始安装
sudo ./setup --install

完成没报错会有安装成功提示，并提示怎么配置和启动服务

```

2. 编辑agent配置文件/etc/aws-kinesis/agent.json，默认如下：

```
{
    "cloudwatch.emitMetrics": true,
    "kinesis.endpoint": "https://your/kinesis/endpoint",
    "firehose.endpoint": "https://your/firehose/endpoint",
    "flows": [
        {
            "filePattern": "/tmp/app1.log*",
            "kinesisStream": "yourkinesisstream"
        },
        {
            "filePattern": "/tmp/app2.log*",
            "deliveryStream": "yourfirehosedeliverystream"
        }
    ]
}
```

cloudwatch.emitMetrics：是否开启cloudwatch监控
kinesis.endpoint： Kinesis stream的endpoint设置
firehose.endpoint：firehose的endpoint
各end point地址: <https://docs.aws.amazon.com/general/latest/gr/rande.html>

这里不搬教程，关于上面参数详细参考<https://docs.aws.amazon.com/streams/latest/dev/writing-with-agents.html>

官方默认的那个配置有点坑，直接贴可以用的agent.json:

**配置1**

```
{
"awsAccessKeyId": "xxxxx",
"awsSecretAccessKey": "xxxxxxxxxxxxxxxxx",
"cloudwatch.emitMetrics": false,
"firehose.endpoint": "firehose.us-west-2.amazonaws.com",
"cloudwatch.endpoint": "https://monitoring.us-west-2.amazonaws.com",
"kinesis.endpoint": "https://kinesis.us-west-2.amazonaws.com",
  "flows": [
    {
      "filePattern": "/usr/local/programs/nginx/logs/access.log",
      "deliveryStream": "api-nginx-access-log",
      "dataProcessingOptions": [
                {
                    "optionName": "LOGTOJSON",
                    "logFormat": "COMMONAPACHELOG",
                    "matchPattern": "^([\\d.]+) \\S+ \\S+ \\[([\\w:/]+)\\s[+\\-]\\d{4}\\] \"([A-Z]+) (.+?) ([\\w./]+)\" (\\d{3}) (\\d+) \"(.+?)\" \"(.+?)\" \"(.+?)\" (\\d+) \"(.+?)\" upstream_response_time (\\d.+) request_time (\\d.+)",
                                "customFieldNames": ["remote_addr", "datetime", "request_type", "request_url", "http_version", "response_status", "body_bytes_sent", "http_referer", "http_user_agent", "http_x_forwarded_for", "connection_serial_number", "upstream_addr", "upstream_response_time", "request_time"]
                }
        ]
    }
  ]
}

```

**配置2**

```
{
"awsAccessKeyId": "xxxxx",
"awsSecretAccessKey": "xxxxxxxxxxxxxxxxxxxx",
"cloudwatch.emitMetrics": false,
"cloudwatch.endpoint": "https://monitoring.us-west-2.amazonaws.com",
"kinesis.endpoint": "https://kinesis.us-west-2.amazonaws.com",
  "flows": [
    {
      "filePattern": "/usr/local/programs/nginx/logs/access.log",
      "kinesisStream": "api-nginx-access-log",
      "partitionKeyOption": "RANDOM",
      "dataProcessingOptions": [
                {
                    "optionName": "LOGTOJSON",
                    "logFormat": "COMMONAPACHELOG"
                }
        ]
    }
  ]
}
```

配置1是firehose收集，配置2 kinesis stream收集。

awsAccessKeyId和awsSecretAccessKey访问授权的，注意end-point是分区域的，每个区域地址不一样。

logFormat用COMMONAPACHELOG默认格式无法解析到全部想要字段，需要自定义正则和字段去解析，Kinesis agent是java程序，所以这里的matchPattern要用java格式正则，这个必须要注意。

找到了一个好的调试办法，打开<https://tool.lu/coderunner>,选择java语言粘贴如下代码：

```
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RegexMatches
{
	public static void main( String args[] ){

		// 按指定模式在字符串查找
		String line = "132.31.43.24 - - [12/Sep/2018:05:58:36 +0000] \"POST /v1/tracks/hello HTTP/1.1\" 200 79993 \"https://test.com/category/Baby-Toddlers.html?category_id=27&son_category_id=%5B%5D&tag_id=&last_id=0&filter=%7B%22On%20Sale%22%3A%5B%5D,%22Size%22%3A%5B%5D,%22Color%22%3A%5B%5D,%22Season%22%3A%5B%5D,%22Style%22%3A%5B%5D,%22Occasion%22%3A%5B%5D,%22Price%22%3A%5B%5D%7D&sort=3&page=1&is_sale=&start_price=&end_price=&utm_source=FB&utm_medium=Dannie&utm_campaign=09-06-Baby-Toddlers-12&adlk_id=30051\" \"Mozilla/5.0 (iPhone; CPUiPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1\" \"17.47.23.134, 12.128.106.104\" 74518 \"127.0.0.1:9000\" upstream_response_time 20.186 request_time 0.186";

		String pattern = "^([\\d.]+) (\\S+) (\\S+) \\[([\\w:/]+\\s[+\\-]\\d{4})\\] \"([A-Z]+) (.+?) ([\\w./]+)\" (\\d{3}) (\\d+) \"(.+?)\" \"(.+?)\" \"(.+?)\" (\\d+) \"(.+?)\" upstream_response_time (\\d.+) request_time (\\d.+)";

		// 创建 Pattern 对象
		Pattern r = Pattern.compile(pattern);

		// 现在创建 matcher 对象
		Matcher m = r.matcher(line);
		if (m.find( )) {
			System.out.println("remote_addr: " + m.group(1) );
			System.out.println("ident: " + m.group(2) );
			System.out.println("authuser: " + m.group(3) );
			System.out.println("datetime: " + m.group(4) );
			System.out.println("request_type: " + m.group(5) );
			System.out.println("request_url: " + m.group(6) );
			System.out.println("http_version: " + m.group(7) );
			System.out.println("response_status: " + m.group(8) );
			System.out.println("body_bytes_sent: " + m.group(9) );
			System.out.println("http_referer: " + m.group(10) );
			System.out.println("http_user_agent: " + m.group(11) );
			System.out.println("http_x_forwarded_for: " + m.group(12) );
			System.out.println("connection_serial_number: " + m.group(13) );
			System.out.println("upstream_addr: " + m.group(13) );
			System.out.println("connection_serial_number: " + m.group(13) );
			System.out.println("upstream_addr: " + m.group(14) );
			System.out.println("upstream_response_time: " + m.group(15) );
			System.out.println("request_time: " + m.group(16) );
		} else {
			System.out.println("NO MATCH");
		}
	}
}

```

字符串要java转义过的，可以用下面网站先转义再用<http://tool.what21.com/tool/javaStr.html>

可以自己改上面的源字符串和正则调试。当正则调好符合要求时把它复制到matchPattern配置里。

Kinesis agent相关操作：
启动： `sudo service aws-kinesis-agent start`
重启：`sudo service aws-kinesis-agent restart`
停止：`sudo service aws-kinesis-agent status`

每次调整了配置重启即可

## 三、配置ES索引模板

上面的数据直接从agent->firehose->eS可以直接跑通，但有字段类型问题，全部是text类型，例如我们希望进去的datetime是date类型，怎么办？通过ES template解决。创建如下的ES Template:

```
 curl -i -XPUT https://192.168.11.120:9200/_template/nginx-access-log_template -d '{
    "template": "*-nginx-access-log-*",
    "mappings": {
        "log": {
            "_all": { "enabled": false },
            "properties": {
                "remote_addr": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "request_type": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "request_url": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "http_version": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "response_status": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "body_bytes_sent": {
                    "type": "long"
                },
                "http_referer": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "http_user_agent": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "http_x_forwarded_for": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "connection_serial_number": {
                    "type": "long"
                },
                "upstream_addr": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "upstream_response_time": {
                    "type": "double"
                },
                "request_time": {
                    "type": "double"
                },
                "datetime": {
                    "type": "date",
                    "format": "dd/MMM/YYYY:HH:mm:ss"
                }
            }
        }
    }
}'

```

模板名称nginx-access-log_template，设置模板套用规则\*-nginx-access-log-\*，例如aaaa-nginx-access-log-2018-08-02，bbbbb-ccc-nginx-access-log-2018-08-08类似的索引会自动套用，非常方便~

\**需要注意datetime字段类型是date，format格式和常见的不太一样，这个坑被忽略爬了半天~_~,nginx log的时间默认是time_local，常见的是time_iso8601*


怎么查询模板，删除模板，查看索引，删除索引可以在es专栏查看。

## 四、完成

贴一张日志传到kibana的截图：

![EKK](/uploads/2018/kb.png)

未解决：没有国家信息，浏览器设备信息没细化，解决思路在Firehose往ES传输之间增加lambda处理

---

## 相关文章

- [Elasticsearch 入门教程：索引、分词、DSL 查询与高级搜索实战](/zh/posts/elasticsearch/2018-09-12-elasticsearch/) - ES 核心概念与查询语法详解
- [ELK 日志系统搭建教程：Elasticsearch + Logstash + Kibana + Kafka 完整指南](/zh/posts/elasticsearch/2018-09-11-log-elk/) - 企业级日志收集分析平台搭建
- [Amazon Redshift 性能优化指南：VACUUM、ANALYZE 与运维最佳实践](/zh/posts/datawarehouse/2018-08-09-dw-redshift/) - Kinesis 管道之外，数据落到数仓后的 SQL 分析与性能维护
