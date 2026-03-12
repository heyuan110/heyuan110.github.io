+++
date = '2025-03-11T14:40:02+08:00'
title = 'Vector Database Explained: From Core Concepts to Production'
description = 'Learn what vector databases actually solve, how ANN indexing works, when to use semantic search vs keyword search, and how to choose between Milvus, Pinecone, Qdrant, and pgvector.'
toc = true
tags = ['AI', 'Vector Database', 'RAG']
categories = ['AI Guides']
keywords = ['vector database', 'RAG retrieval augmented generation', 'embedding model', 'semantic search', 'ANN indexing', 'Milvus vs Pinecone', 'vector database comparison']
+++
![VectorDatabase](vector-db.webp)

## 1. Why Vector Databases Suddenly Took Off

Before 2023, vector databases were a niche technology that most engineers had never heard of.

Then ChatGPT happened. Large language models became mainstream overnight, and people quickly ran into a fundamental limitation: an LLM's knowledge is frozen at training time. It doesn't know your company's internal docs, yesterday's news, or your proprietary data.

The obvious fix? Feed it your private data at query time.

But you can't shove hundreds of pages into every prompt. Token costs aside, there are hard context length limits.

That's where RAG (Retrieval-Augmented Generation) comes in. The idea is simple: find the most relevant content from your knowledge base first, then pass it to the LLM so it can answer based on actual context.

The question then becomes: how do you "find relevant content"?

Traditional databases do keyword matching. Search for "Apple phone" and you'll only find documents containing those exact words — not documents that say "iPhone."

But humans know "Apple phone" and "iPhone" mean the same thing. How do you teach a machine that?

The answer: convert text into vectors and measure semantic similarity through vector distance.

This is the fundamental reason vector databases exploded — **the LLM era demands semantic retrieval, and vector databases are the most direct solution for it**.

## 2. What Are Vectors and What Does Embedding Actually Do

### What Is a Vector

A vector is simply an array of numbers.

Something like `[0.12, -0.34, 0.56, ..., 0.78]` — it might have 768 numbers, or 1536, depending on the model that generated it.

What do these numbers represent? They encode the "semantic features" of the content.

Think of it as coordinates in a high-dimensional space. In a 768-dimensional space, every piece of text occupies a position. Semantically similar texts sit close together; unrelated texts are far apart.

### What Embedding Models Do

An embedding model converts text into vectors.

Input: a piece of text. Output: an array of numbers. This process is called "embedding" or "vectorization."

For example:

```
Input:  "The weather is great today"
Output: [0.12, -0.34, 0.56, ..., 0.78]  (768-dimensional vector)
```

Different embedding models produce different dimensions and quality levels. Common choices include:

- OpenAI `text-embedding-3-small`: 1536 dimensions
- BGE series: 768 or 1024 dimensions
- GTE series: 768 or 1024 dimensions
- Cohere Embed v3: 1024 dimensions

For English-language use cases, OpenAI and Cohere models work well out of the box. For multilingual or specialized domains, open-source models like BGE and GTE are strong alternatives that you can self-host.

### How to Measure Whether Two Vectors Are Similar

The most common method is **cosine similarity**.

Mathematically, it's the cosine of the angle between two vectors. The smaller the angle, the closer the cosine value is to 1, meaning higher similarity.

There are other approaches — Euclidean distance, dot product — but cosine similarity is the most widely used because it's insensitive to vector magnitude and only considers direction.

## 3. Why Traditional Databases Can't Handle Vector Search

You might ask: vectors are just arrays of numbers, right? MySQL can store those. Why do we need a specialized database?

### Problem 1: Different Query Paradigm

Traditional databases do exact match or range queries:

```sql
SELECT * FROM users WHERE age = 25;
SELECT * FROM products WHERE price BETWEEN 100 AND 200;
```

Vector search is a similarity query:

```
Find the Top 10 vectors most similar to this query vector
```

This is a fundamentally different query pattern. B+ tree indexes are useless here.

### Problem 2: The Curse of Dimensionality

Vectors routinely have 768 or 1536 dimensions. In high-dimensional spaces, traditional index structures break down.

This is the "curse of dimensionality" — as dimensions increase, the distance between all data points converges, making everything appear roughly equidistant. Standard indexes degrade to brute-force full table scans.

### Problem 3: Performance Requirements

In production, vector search typically needs to return the Top K most similar results from **millions or tens of millions** of vectors in **single-digit milliseconds**.

Imagine storing 1 million 768-dimensional vectors in MySQL and computing cosine similarity for every query. Your server would melt.

That's why we need specialized **Approximate Nearest Neighbor (ANN)** algorithms and index structures.

## 4. Core Capabilities of a Vector Database

A vector database needs to solve several key problems:

### 4.1 Efficient ANN Indexing

ANN = Approximate Nearest Neighbor.

"Approximate" is the key word. For speed, we accept results that aren't the mathematically exact nearest neighbors — just "close enough."

Common ANN index algorithms:

**HNSW (Hierarchical Navigable Small World)**

The most popular algorithm today. It builds a multi-layer graph structure. During queries, it starts from the top layer and navigates downward, quickly converging on the target neighborhood.

Pros: fast queries, high recall
Cons: high memory usage, slow index construction

**IVF (Inverted File Index)**

Uses K-means to cluster vectors into groups. During queries, it first identifies the nearest clusters, then searches within them.

Pros: lower memory usage, works well with quantization
Cons: slightly lower recall than HNSW

**PQ (Product Quantization)**

Splits vectors into sub-segments and compresses each with a codebook. Queries use the compressed representations to compute distances.

Primarily used to **reduce memory footprint**. Usually combined with IVF (IVF-PQ).

### 4.2 Hybrid Queries: Vectors + Metadata Filtering

In practice, you rarely search by vector similarity alone. There are usually filter conditions:

```
Find the most relevant documents, but only those published in the last 7 days
Find the most similar products, but only those priced between $100 and $500
```

This requires **hybrid queries**: filter by metadata first, then run vector search on the filtered set.

Some databases use pre-filtering (filter then search), others use post-filtering (search then filter). The performance difference can be massive — this is a critical factor when choosing a database.

### 4.3 Real-Time CRUD Operations

Some use cases involve dynamic data — e-commerce product catalogs, news articles, support tickets.

The database needs to support:
- Inserting new vectors in real time
- Deleting expired vectors
- Updating existing vectors

This places demands on the index structure. Some indexes (like pure IVF) have high update costs.

### 4.4 Distributed Architecture and High Availability

As data grows, a single machine can't keep up. You need sharding, replicas, and failover.

Implementations vary widely here. Some databases are built distributed from the ground up; others bolt distribution onto a single-node core.

## 5. How Vector Databases Are Used in Real Systems

### Use Case 1: RAG Knowledge Base

The hottest use case by far.

The workflow:
1. Split documents into chunks
2. Convert each chunk into a vector using an embedding model
3. Store vectors in the vector database
4. When a user asks a question, convert the question into a vector
5. Search the vector database for the most similar chunks
6. Pass the retrieved chunks + question to the LLM

The vector database is one of the core components in this pipeline.

### Use Case 2: Semantic Search

Traditional search matches keywords. Semantic search understands intent.

A user searching "affordable and reliable phone" can find an article titled "Best Budget Smartphones of 2025" — even though not a single keyword matches.

Many products already use this. You may just not have noticed.

### Use Case 3: Recommendation Systems

Convert user behaviors and item features into vectors, then use vector similarity for candidate retrieval.

For example: average the vectors of products a user has viewed, then find the nearest products to that average vector for recommendations.

This use case actually predates RAG. Back then it wasn't called a "vector database" — it was Faiss, or an ANN service.

### Use Case 4: Deduplication and Similarity Detection

Determine whether two images are the same (plagiarism detection, copyright checks).

Convert images into vectors. When a new image arrives, search for similar ones.

Text deduplication works the same way.

## 6. Common Mistakes and Pitfalls in Production

### Mistake 1: Thinking Vector Search Solves Everything

Vector search is **semantic similarity** search. It's not a universal solution.

Some scenarios are better served by keyword matching. Searching for order numbers or SKU codes with vector search is like using a sledgehammer to hang a picture frame.

The right approach is usually **hybrid search**: keyword retrieval + vector retrieval, with result fusion and re-ranking.

### Mistake 2: Picking Any Embedding Model

Embedding model quality **directly determines** retrieval effectiveness.

If the model is weak, no vector database can save you.

Recommendations:
- Check the MTEB leaderboard for model scores
- Benchmark on your own data — generic leaderboards don't always translate
- For English, OpenAI, Cohere, and BGE models are solid starting points

### Mistake 3: Making Chunks Too Small or Too Large

Both are wrong.

Too small: context is lost, retrieved content is incomplete
Too large: too much noise, semantics get diluted

There's no universal chunking strategy. Tune it based on your content type. General guidelines:

- Structured documents (with heading hierarchy): chunk by section
- Plain text: 300-500 words per chunk, with overlap
- Code: chunk by function or class

### Mistake 4: Only Measuring Recall, Ignoring Ranking

Recall of 100 results means nothing if the most relevant one is ranked 50th.

Focus on **Top K precision**, not just "can it be recalled."

This depends on the embedding model, index parameters, and query strategy.

### Mistake 5: Ignoring Metadata Filtering Performance

As mentioned, hybrid queries (vector + filter) are extremely common.

But some databases implement filtering poorly — especially in post-filter mode. You retrieve 10,000 candidates, filter them, and end up with only 10 results. Terrible efficiency.

If your use case relies heavily on filtering, you must benchmark hybrid query performance during evaluation.

## 7. How to Choose a Vector Database (Engineering Perspective)

There are many options on the market, roughly categorized as follows:

### Purpose-Built Vector Databases

**Milvus**

- Open source, feature-rich, active community
- Built for distributed, large-scale workloads
- Downside: heavyweight deployment, depends on etcd and MinIO

Best for: teams serious about vector search at scale with strong feature and performance requirements

**Pinecone**

- Fully managed SaaS, zero ops
- No infrastructure to maintain
- Downside: expensive, and your data lives on their servers

Best for: teams that don't want to manage infrastructure, have budget, and aren't concerned about data residency

**Qdrant**

- Written in Rust, strong performance
- Rich filtering capabilities
- Simpler to deploy than Milvus

Best for: mid-scale deployments with significant filtering requirements

**Weaviate**

- Supports multimodal data (text, images)
- Built-in embedding model integrations
- GraphQL API

Best for: teams wanting an all-in-one solution

### Traditional Databases + Vector Extensions

**PostgreSQL + pgvector**

- If you're already running Postgres, just add an extension
- Performance is modest but sufficient for small scale
- Advantage: no new infrastructure to manage

Best for: datasets under a few hundred thousand vectors, quick prototyping

**Elasticsearch 8.x**

- Native vector search support starting from ES 8
- Seamlessly combines with full-text search
- Great for teams already running Elasticsearch

### Libraries (Build Your Own)

**Faiss**

- Built by Meta, industry benchmark
- A pure indexing library — not a database, no persistence, no API
- You have to wrap it yourself

Best for: teams with strong engineering capability who want full control

### Decision Matrix

| Scenario | Recommendation |
|----------|---------------|
| Quick prototyping, small data | pgvector / SQLite-VSS |
| Already running ES, want to add vector capability | Elasticsearch |
| Production use, medium scale | Qdrant / Weaviate |
| Large scale, high performance | Milvus |
| No-ops, sufficient budget | Pinecone |
| Deep customization, full control | Faiss |

Don't get swayed by marketing. Start by understanding your requirements:

- How much data do you have?
- What's your QPS target?
- Do you need hybrid queries (vector + metadata)?
- Do you need real-time updates?
- Does your team have the ops capability?

Then choose.

## 8. Final Thoughts: The Boundaries of Vector Databases

A vector database is not a silver bullet.

It solves one problem: **semantic similarity retrieval** — and it solves it approximately.

Don't expect it to:
- Replace traditional databases for exact queries
- Replace full-text search engines for keyword retrieval
- Automatically understand your business logic

It's one link in the chain. In a RAG system, the embedding model, chunking strategy, prompt design, and the LLM itself all affect the end result. The best vector database in the world won't save a pipeline where other components are weak.

This field is also evolving rapidly. Today's best practices may be obsolete in six months. Stay informed, but don't chase every new shiny thing.

Master the fundamentals first. Then experiment.
