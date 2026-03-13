+++
date = '2018-09-12T18:52:59+08:00'
title = 'AWS EKK Log System Setup: Elasticsearch + Kinesis + Kibana Hands-On Guide'
description = 'Step-by-step tutorial for building an EKK log collection system on AWS using Amazon Elasticsearch Service, Kinesis, and Kibana to collect and analyze Nginx access logs with custom field parsing'
toc = true
tags = ['Elasticsearch', 'AWS', 'Kinesis', 'Kibana', '日志分析']
categories = ['Elasticsearch']
keywords = ['AWS EKK setup', 'Kinesis Elasticsearch Kibana', 'AWS log collection', 'Nginx log analysis AWS', 'Amazon Elasticsearch Service']
+++

EKK is a log collection stack built entirely on AWS managed services: **Amazon Elasticsearch Service**, **Amazon Kinesis**, and **Kibana**. Compared to a self-managed ELK stack, EKK is significantly easier to set up and maintain since AWS handles the infrastructure. Here is the basic architecture:

![EKK Architecture](https://d2908q01vomqb2.cloudfront.net/472b07b9fcf2c2451e8781e944bf5f77cd8457c8/2017/09/07/1-2.png)

This guide focuses on the practical aspects of collecting Nginx logs and getting them into Elasticsearch with the correct field mappings, rather than covering every AWS console click.

## Prerequisites

1. **Launch an EC2 instance** (Ubuntu 16.04) with Nginx installed. Configure a custom log format:

```nginx
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                  '$status $body_bytes_sent "$http_referer" '
                  '"$http_user_agent" "$http_x_forwarded_for" '
                  '$connection "$upstream_addr" '
                  'upstream_response_time $upstream_response_time request_time $request_time';
```

This produces access log entries like:

```
192.168.13.1 - - [12/Sep/2018:03:59:12 +0000] "GET /v1/home HTTP/1.1" 200 2787 "https://test.com/product/example.html" "Mozilla/5.0 ..." "2002:c7:6f02:9801:..." 12340 "127.0.0.1:9000" upstream_response_time 0.11 request_time 0.11
```

2. **Create an IAM user** with permissions to access Kinesis Stream/Firehose and Amazon Elasticsearch Service. Save the `awsAccessKeyId` and `awsSecretAccessKey`.

3. **Launch an Amazon Elasticsearch Service domain** (e.g., "TestES"). Choose **public access** during creation -- you can add security policies later.

4. **Create a Kinesis Firehose delivery stream** with the destination set to your ES domain. If you need to fan out one source to multiple destinations, use Kinesis Data Streams instead.

## Collecting Logs with Kinesis Agent

### Install the Amazon Kinesis Agent

```bash
# Clone the source
git clone https://github.com/awslabs/amazon-kinesis-agent.git

# Install Java JDK (required on Ubuntu 16.04)
sudo apt-get install openjdk-8-jdk

# Run the installer
sudo ./setup --install
```

### Configure the Agent

Edit `/etc/aws-kinesis/agent.json`. The default config is a starting point, but here are two production-ready configurations.

**Configuration 1: Kinesis Firehose with custom log parsing**

```json
{
  "awsAccessKeyId": "YOUR_ACCESS_KEY",
  "awsSecretAccessKey": "YOUR_SECRET_KEY",
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
          "customFieldNames": [
            "remote_addr", "datetime", "request_type", "request_url",
            "http_version", "response_status", "body_bytes_sent",
            "http_referer", "http_user_agent", "http_x_forwarded_for",
            "connection_serial_number", "upstream_addr",
            "upstream_response_time", "request_time"
          ]
        }
      ]
    }
  ]
}
```

**Configuration 2: Kinesis Data Streams with default parsing**

```json
{
  "awsAccessKeyId": "YOUR_ACCESS_KEY",
  "awsSecretAccessKey": "YOUR_SECRET_KEY",
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

### Key Configuration Notes

- **Endpoints are region-specific.** Find yours at the [AWS endpoint reference](https://docs.aws.amazon.com/general/latest/gr/rande.html).
- The default `COMMONAPACHELOG` format won't parse custom fields like `upstream_response_time`. You need a custom `matchPattern` regex with `customFieldNames`.
- **The Kinesis Agent is a Java application**, so the `matchPattern` must use Java regex syntax. This is an easy mistake to make.
- For detailed configuration options, see the [official documentation](https://docs.aws.amazon.com/streams/latest/dev/writing-with-agents.html).

### Debugging Your Regex

Since getting the regex right is critical, here is a useful approach. Use an [online Java code runner](https://tool.lu/coderunner) to test your pattern:

```java
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RegexMatches {
    public static void main(String args[]) {
        String line = "132.31.43.24 - - [12/Sep/2018:05:58:36 +0000] \"POST /v1/tracks/hello HTTP/1.1\" 200 79993 \"https://test.com/page\" \"Mozilla/5.0 ...\" \"17.47.23.134, 12.128.106.104\" 74518 \"127.0.0.1:9000\" upstream_response_time 20.186 request_time 0.186";

        String pattern = "^([\\d.]+) (\\S+) (\\S+) \\[([\\w:/]+\\s[+\\-]\\d{4})\\] \"([A-Z]+) (.+?) ([\\w./]+)\" (\\d{3}) (\\d+) \"(.+?)\" \"(.+?)\" \"(.+?)\" (\\d+) \"(.+?)\" upstream_response_time (\\d.+) request_time (\\d.+)";

        Pattern r = Pattern.compile(pattern);
        Matcher m = r.matcher(line);
        if (m.find()) {
            System.out.println("remote_addr: " + m.group(1));
            System.out.println("datetime: " + m.group(4));
            System.out.println("request_type: " + m.group(5));
            System.out.println("response_status: " + m.group(8));
            // ... test all groups
        } else {
            System.out.println("NO MATCH");
        }
    }
}
```

Remember to escape Java strings properly. Once your regex matches correctly, copy it into the `matchPattern` field in `agent.json`.

### Agent Service Commands

```bash
sudo service aws-kinesis-agent start     # Start
sudo service aws-kinesis-agent restart   # Restart (after config changes)
sudo service aws-kinesis-agent status    # Check status
```

## Configuring the ES Index Template

The data pipeline (Agent -> Firehose -> ES) works out of the box, but there is a field type problem: everything arrives as `text` type. For example, you probably want `datetime` as a `date` type and `body_bytes_sent` as `long`. The solution is an **index template**.

Create a template that automatically applies to matching index names:

```bash
curl -XPUT https://your-es-endpoint:9200/_template/nginx-access-log_template \
  -H 'Content-Type: application/json' -d '{
  "template": "*-nginx-access-log-*",
  "mappings": {
    "log": {
      "_all": { "enabled": false },
      "properties": {
        "remote_addr":              { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "request_type":             { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "request_url":              { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "http_version":             { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "response_status":          { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "body_bytes_sent":          { "type": "long" },
        "http_referer":             { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "http_user_agent":          { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "http_x_forwarded_for":     { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "connection_serial_number": { "type": "long" },
        "upstream_addr":            { "type": "text", "fields": { "keyword": { "type": "keyword" }}},
        "upstream_response_time":   { "type": "double" },
        "request_time":             { "type": "double" },
        "datetime":                 { "type": "date", "format": "dd/MMM/YYYY:HH:mm:ss" }
      }
    }
  }
}'
```

The template name is `nginx-access-log_template`, and the pattern `*-nginx-access-log-*` means any index matching that glob (e.g., `api-nginx-access-log-2018-08-02`) will automatically get these field mappings.

**Watch out for the datetime format.** Nginx uses `time_local` by default (e.g., `12/Sep/2018:03:59:12`), which requires the format `dd/MMM/YYYY:HH:mm:ss` -- not the more common ISO 8601 format. This is a subtle gotcha that can cost you hours of debugging.

## Result

Here is a screenshot of the logs flowing into Kibana:

![EKK Kibana Dashboard](/uploads/2018/kb.png)

### Known Limitations

- No geolocation data (country information is missing)
- Browser and device details are not parsed from the user agent string
- **Solution approach:** Add a Lambda function between Firehose and ES to enrich the data with GeoIP lookups and user agent parsing

---

## Related Articles

- [Elasticsearch Tutorial: Core Concepts of Indices, Documents, and Query APIs](/posts/elasticsearch/2018-09-12-elasticsearch/) - Deep dive into ES fundamentals and query syntax
- [ELK Stack Setup Guide: Elasticsearch + Logstash + Kibana + Kafka Full Architecture](/posts/elasticsearch/2018-09-11-log-elk/) - Complete enterprise logging platform deployment
