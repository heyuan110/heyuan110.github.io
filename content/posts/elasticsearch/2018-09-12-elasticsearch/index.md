+++
date = '2018-09-12T18:52:59+08:00'
title = 'Elasticsearch Tutorial: Core Concepts of Indices, Documents, and Query APIs'
description = 'A beginner-friendly Elasticsearch tutorial covering core concepts like indices, types, and documents (with RDBMS analogies), plus hands-on examples of _cat, _search, CRUD operations, and DSL queries'
toc = true
tags = ['Elasticsearch', '搜索引擎', '全文检索', 'API']
categories = ['Elasticsearch']
keywords = ['Elasticsearch tutorial', 'Elasticsearch REST API', 'Elasticsearch CRUD', 'Elasticsearch DSL query', 'Elasticsearch index document']
+++

![](https://raw.githubusercontent.com/heyuan110/static-source/master/cover/es.jpg)

Elasticsearch (ES) is an open-source search engine built on Apache Lucene. It is the go-to solution for full-text search, capable of storing, searching, and analyzing massive volumes of data in near real-time. Companies like GitHub and Stack Overflow use it at scale.

## Core Concepts: ES vs. Relational Databases

If you come from a relational database background, the following mapping will help you understand ES terminology quickly:

| Elasticsearch | Relational DB |
| ------------- | ------------- |
| Index         | Database      |
| Type          | Table         |
| Document      | Row           |
| Field         | Column        |

An ES cluster can contain multiple **indices** (analogous to databases). Each index can hold multiple **types** (tables), each type contains multiple **documents** (rows), and each document consists of multiple **fields** (columns).

> Note: In ES 7.x+, the concept of "type" has been deprecated. Each index effectively has a single type.

## Common Query Commands

### 1. The `_cat` API

The `_cat` API provides human-readable cluster information. List all available endpoints:

```
GET /_cat/
```

```
➜  ~ curl -XGET http://192.168.11.119:9200/_cat/
>=^.^=
/_cat/allocation
/_cat/shards
/_cat/shards/{index}
/_cat/master
/_cat/nodes
/_cat/indices
/_cat/indices/{index}
/_cat/count
/_cat/count/{index}
/_cat/health
/_cat/pending_tasks
/_cat/aliases
/_cat/thread_pool
/_cat/plugins
/_cat/fielddata
/_cat/nodeattrs
/_cat/repositories
/_cat/snapshots/{repository}
/_cat/templates
```

### 2. Check Cluster Health

```
GET /_cat/health?v
```

```
epoch      timestamp cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
1533717572 08:39:32  elasticsearch yellow          1         1    315 315    0    0      315             0                  -                 50.0%
```

Health status meanings:

- **green** -- All primary and replica shards are active
- **yellow** -- All primary shards are active, but some replicas are unassigned
- **red** -- Some primary shards are missing, meaning data loss has occurred

A single-node cluster will always show **yellow** because replica shards cannot be allocated to the same node as their primary shard (that would defeat the purpose of replication for fault tolerance).

### 3. List All Indices

```
GET /_cat/indices?v
```

```
health status index                    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   es_es_category_products  u2TdPYcXS5yyFF8P3a3jYQ   5   1      95311         7103      156mb          156mb
yellow open   web_product_ar_new       8qhhh9C7QvuwEEu-YYrIgA   5   1      37610           77     55.6mb         55.6mb
```

### 4. Create an Index

```
PUT /test_index?pretty
```

```json
{
  "acknowledged": true,
  "shards_acknowledged": true
}
```

### 5. Delete an Index

```
DELETE /test_index?pretty
```

### 6. Index a Document (Create)

The syntax follows the pattern `PUT /index/type/id`:

```bash
curl -XPUT http://192.168.11.119:9200/test_index/user/1 -H 'Content-Type: application/json' -d '{
    "name": "John",
    "email": "john@test.com",
    "tags": ["basketball", "swimming"]
}'
```

Response:

```json
{
  "_index": "test_index",
  "_type": "user",
  "_id": "1",
  "_version": 1,
  "result": "created",
  "_shards": {"total": 2, "successful": 1, "failed": 0},
  "created": true
}
```

### 6.1 Retrieve a Document

```
GET /test_index/user/1?pretty
```

```json
{
  "_index": "test_index",
  "_type": "user",
  "_id": "1",
  "_version": 1,
  "found": true,
  "_source": {
    "name": "John",
    "email": "john@test.com",
    "tags": ["basketball", "swimming"]
  }
}
```

### 7. Update a Document

**Full replacement** (PUT) -- you must include all fields:

```bash
curl -XPUT http://192.168.11.119:9200/test_index/user/1 -H 'Content-Type: application/json' -d '{
    "name": "John",
    "email": "john@test.com",
    "tags": ["basketball", "swimming", "football"]
}'
```

**Partial update** (POST) -- only update specific fields using the `doc` wrapper:

```bash
curl -XPOST http://192.168.11.119:9200/test_index/user/1/_update -H 'Content-Type: application/json' -d '{
    "doc": {
        "email": "john@demo.com"
    }
}'
```

### 8. Delete a Document

```
DELETE /test_index/user/1
```

### 9. Query String Search

Search all documents in a type:

```
GET /test_index/user/_search?pretty
```

Response fields explained:

| Field             | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| `took`            | Time in milliseconds                                           |
| `timed_out`       | Whether the request timed out                                  |
| `_shards`         | Number of shards searched                                      |
| `hits.total`      | Total matching documents                                       |
| `hits.max_score`  | Highest relevance score among results                          |
| `hits.hits`       | Array of matching documents with full details                  |

Search for a specific name with sorting:

```bash
curl -XGET 'http://192.168.11.119:9200/test_index/user/_search?pretty&q=name:bruce&sort=email:desc'
```

Note: Query string search is case-insensitive. It is useful for quick ad-hoc queries via curl, but for complex queries, use the DSL approach described below.

### 10. View Index Mappings

```bash
# All mappings across all indices
GET /_mapping

# Mappings for a specific index
GET /test_index/_mapping

# Mappings for a specific type
GET /test_index/user/_mapping
```

Example response showing field types and keyword sub-fields:

```json
{
  "test_index": {
    "mappings": {
      "user": {
        "properties": {
          "email": {
            "type": "text",
            "fields": {
              "keyword": { "type": "keyword", "ignore_above": 256 }
            }
          },
          "name": {
            "type": "text",
            "fields": {
              "keyword": { "type": "keyword", "ignore_above": 256 }
            }
          },
          "tags": {
            "type": "text",
            "fields": {
              "keyword": { "type": "keyword", "ignore_above": 256 }
            }
          }
        }
      }
    }
  }
}
```

### 11. Query DSL (Domain Specific Language)

DSL queries use a JSON request body, which is far more powerful and readable than query strings for complex searches.

#### 11.1 Match All Documents

```bash
curl -XGET 'http://192.168.11.119:9200/test_index/user/_search?pretty' \
  -H 'Content-Type: application/json' -d '{
  "query": {
    "match_all": {}
  }
}'
```

Note that `match_all` is nested inside the `query` object, which sits at the root level of the request body.

#### 11.2 Match Query with Sorting and Pagination

```bash
curl -XGET 'http://192.168.11.119:9200/test_index/user/_search?pretty' \
  -H 'Content-Type: application/json' -d '{
  "query": {
    "match": { "name": "bruce" }
  },
  "sort": [{ "email": "desc" }]
}'
```

**Fielddata gotcha:** If you get the error `Fielddata is disabled on text fields by default`, you need to enable fielddata for sorting/aggregation on text fields:

```bash
curl -XPUT 'http://192.168.11.119:9200/test_index/_mapping/user?pretty' \
  -H 'Content-Type: application/json' -d '{
  "properties": {
    "email": { "type": "text", "fielddata": true }
  }
}'
```

See the [official fielddata documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html) for details. A better approach for sorting is to use the `.keyword` sub-field instead.

**Pagination** uses `from` and `size` at the root level:

```json
{
  "query": { "match_all": {} },
  "from": 0,
  "size": 10,
  "_source": ["email"],
  "sort": [{ "email": "asc" }]
}
```

#### 11.3 Bool Query with Filters

This example searches for products with "Rhinestone" in the name, priced between 1 (inclusive) and 3 (exclusive), sorted by price ascending:

```json
{
  "query": {
    "bool": {
      "must": {
        "match": { "product_name": "Rhinestone" }
      },
      "filter": {
        "range": {
          "store_price": {
            "gte": 1,
            "lt": 3
          }
        }
      }
    }
  },
  "_source": ["product_id", "product_name", "store_price", "icon"],
  "sort": [{ "store_price": "asc" }]
}
```

Range operators:

| Operator | Meaning              |
| -------- | -------------------- |
| `gt`     | Greater than         |
| `gte`    | Greater than or equal|
| `lt`     | Less than            |
| `lte`    | Less than or equal   |

Pay attention to the nesting structure: `query`, `_source`, and `sort` are all at the root level. Inside `query`, `bool` contains `must` and `filter` as siblings.

---

## Related Articles

- [ELK Stack Setup Guide: Elasticsearch + Logstash + Kibana + Kafka Full Architecture](/posts/elasticsearch/2018-09-11-log-elk/) - Complete enterprise logging platform deployment
- [AWS EKK Log System Setup: Elasticsearch + Kinesis + Kibana Hands-On Guide](/posts/elasticsearch/2018-09-12-log-ekk/) - AWS managed services approach to centralized logging
