+++
title = "MySQL SQL Complete Guide: From Beginner to Advanced (With Interview Questions)"
date = 2026-01-23T20:06:36+08:00
description = "Master MySQL SQL from basics to advanced topics: indexes, B+ trees, transactions, MVCC, locks, and query optimization. Includes real-world examples and common interview questions."
toc = true
tags = ["MySQL", "SQL", "Database", "Interview", "Index", "Transaction", "Performance"]
categories = ["MySQL"]
keywords = ["MySQL tutorial", "SQL guide", "MySQL interview questions", "index optimization", "transaction isolation levels", "MVCC", "B+ tree"]
+++
![MySQL SQL Complete Guide: From Beginner to Advanced](cover.webp)

**SQL (Structured Query Language)** is the universal language for communicating with databases. Whether you are a backend developer, data analyst, or DevOps engineer, SQL proficiency is a must-have skill. This guide uses MySQL as the reference implementation and walks you through everything from basic syntax to the internals that interviewers love to ask about.

> This is a long-form article (~15,000 words). Bookmark it and work through one section at a time. Use the table of contents to jump to the topics you need.

## 1. SQL Fundamentals

### 1.1 What Is SQL?

SQL stands for **Structured Query Language** and is used to manage relational databases. It lets you:

- **Query data** — retrieve information from one or more tables
- **Manipulate data** — insert, update, and delete rows
- **Define structure** — create and alter databases and tables
- **Control access** — manage user privileges and permissions

SQL statements fall into four categories:

| Category | Full Name | Common Statements | Purpose |
|----------|-----------|-------------------|---------|
| **DDL** | Data Definition Language | CREATE, ALTER, DROP | Define database structure |
| **DML** | Data Manipulation Language | SELECT, INSERT, UPDATE, DELETE | Manipulate data |
| **DCL** | Data Control Language | GRANT, REVOKE | Control access |
| **TCL** | Transaction Control Language | COMMIT, ROLLBACK | Manage transactions |

### 1.2 Database Operations

```sql
-- Create a database
CREATE DATABASE shop DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- List all databases
SHOW DATABASES;

-- Switch to a database
USE shop;

-- Show the current database
SELECT DATABASE();

-- Drop a database (use with caution!)
DROP DATABASE shop;
```

> **Best practice:** Always use the `utf8mb4` character set. It fully supports Unicode, including emoji.

### 1.3 Table Operations

```sql
-- Create a table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'User ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT 'Username',
    email VARCHAR(100) NOT NULL COMMENT 'Email address',
    password VARCHAR(255) NOT NULL COMMENT 'Hashed password',
    age TINYINT UNSIGNED DEFAULT 0 COMMENT 'Age',
    status TINYINT DEFAULT 1 COMMENT 'Status: 1=active, 0=disabled',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Created at',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Updated at'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Users table';

-- Inspect table structure
DESC users;
SHOW CREATE TABLE users;

-- Alter a table
ALTER TABLE users ADD COLUMN phone VARCHAR(20) COMMENT 'Phone number';   -- add column
ALTER TABLE users MODIFY COLUMN phone VARCHAR(15);                       -- change column type
ALTER TABLE users CHANGE phone mobile VARCHAR(15);                       -- rename column
ALTER TABLE users DROP COLUMN mobile;                                    -- drop column

-- Drop a table
DROP TABLE IF EXISTS users;
```

### 1.4 Choosing the Right Data Types

Picking the right data type is one of the most important decisions in schema design.

#### Integer Types

| Type | Bytes | Signed Range | Typical Use |
|------|-------|--------------|-------------|
| TINYINT | 1 | -128 to 127 | Status flags, age |
| SMALLINT | 2 | -32,768 to 32,767 | Small counters |
| INT | 4 | ~-2.1 billion to ~2.1 billion | Primary keys, counts |
| BIGINT | 8 | Very large | High-volume primary keys |

#### String Types

| Type | Length | Typical Use |
|------|--------|-------------|
| CHAR(n) | Fixed n bytes | Fixed-length strings (phone numbers, country codes) |
| VARCHAR(n) | Variable, max n | Variable-length strings (usernames, emails) |
| TEXT | Up to 64 KB | Long text (article bodies) |
| MEDIUMTEXT | Up to 16 MB | Very long text |

#### Date and Time Types

| Type | Format | Range | When to Use |
|------|--------|-------|-------------|
| DATE | YYYY-MM-DD | 1000-01-01 to 9999-12-31 | Date only |
| DATETIME | YYYY-MM-DD HH:MM:SS | 1000-01-01 to 9999-12-31 | Date and time |
| TIMESTAMP | YYYY-MM-DD HH:MM:SS | 1970 to 2038 | Auto-updating timestamps |

> **Interview tip:** What is the difference between DATETIME and TIMESTAMP?
> - DATETIME uses 8 bytes, has a wider range, and is timezone-agnostic.
> - TIMESTAMP uses 4 bytes, has a narrower range, and automatically converts between timezones.

---

## 2. CRUD Operations In Depth

### 2.1 INSERT — Adding Data

```sql
-- Single-row insert
INSERT INTO users (username, email, password, age)
VALUES ('alice', 'alice@example.com', 'hashed_password', 25);

-- Multi-row insert (recommended for efficiency)
INSERT INTO users (username, email, password, age) VALUES
('bob', 'bob@example.com', 'hashed_password', 30),
('charlie', 'charlie@example.com', 'hashed_password', 28),
('diana', 'diana@example.com', 'hashed_password', 35);

-- Upsert: insert or update on duplicate key
INSERT INTO users (id, username, email, password)
VALUES (1, 'alice', 'new_email@example.com', 'new_password')
ON DUPLICATE KEY UPDATE email = VALUES(email), password = VALUES(password);

-- Insert and silently skip duplicates
INSERT IGNORE INTO users (username, email, password)
VALUES ('alice', 'alice@example.com', 'password');
```

### 2.2 SELECT — Querying Data

SELECT is the most frequently used — and most complex — SQL statement.

#### Basic Queries

```sql
-- Select all columns (avoid in production — hurts performance)
SELECT * FROM users;

-- Select specific columns (recommended)
SELECT id, username, email FROM users;

-- Column aliases
SELECT id AS user_id, username AS name FROM users;

-- Remove duplicates
SELECT DISTINCT status FROM users;

-- Limit rows
SELECT * FROM users LIMIT 10;           -- first 10 rows
SELECT * FROM users LIMIT 10 OFFSET 20; -- skip 20, take 10
SELECT * FROM users LIMIT 20, 10;       -- shorthand for the above
```

#### WHERE Clauses

```sql
-- Comparison operators
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE status != 0;
SELECT * FROM users WHERE age <> 18;  -- alternative not-equal syntax

-- Logical operators
SELECT * FROM users WHERE age >= 18 AND status = 1;
SELECT * FROM users WHERE age < 18 OR age > 60;
SELECT * FROM users WHERE NOT status = 0;

-- Range queries
SELECT * FROM users WHERE age BETWEEN 18 AND 30;   -- inclusive
SELECT * FROM users WHERE age IN (18, 20, 25, 30);

-- NULL checks
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;

-- Pattern matching
SELECT * FROM users WHERE username LIKE 'alice%';  -- starts with "alice"
SELECT * FROM users WHERE username LIKE '%son';    -- ends with "son"
SELECT * FROM users WHERE username LIKE '%ob%';    -- contains "ob"
SELECT * FROM users WHERE username LIKE 'alic_';   -- _ matches a single character
```

> **Performance warning:** `LIKE '%value'` (leading wildcard) cannot use an index and triggers a full table scan!

#### ORDER BY

```sql
-- Ascending (default)
SELECT * FROM users ORDER BY age ASC;

-- Descending
SELECT * FROM users ORDER BY created_at DESC;

-- Multi-column sort
SELECT * FROM users ORDER BY status DESC, created_at DESC;

-- Handling NULLs (MySQL treats NULL as the smallest value)
SELECT * FROM users ORDER BY age IS NULL, age;  -- pushes NULLs to the end
```

#### GROUP BY

```sql
-- Basic grouping
SELECT status, COUNT(*) AS user_count
FROM users
GROUP BY status;

-- Multi-column grouping
SELECT status, age, COUNT(*) AS count
FROM users
GROUP BY status, age;

-- HAVING filters groups (WHERE filters rows before grouping; HAVING filters after)
SELECT status, COUNT(*) AS user_count
FROM users
GROUP BY status
HAVING user_count > 10;

-- WITH ROLLUP adds a summary row
SELECT status, COUNT(*) AS user_count
FROM users
GROUP BY status WITH ROLLUP;
```

### 2.3 UPDATE — Modifying Data

```sql
-- Update a single field
UPDATE users SET status = 0 WHERE id = 1;

-- Update multiple fields
UPDATE users SET status = 0, updated_at = NOW() WHERE id = 1;

-- Conditional update
UPDATE users SET status = 0 WHERE last_login < '2024-01-01';

-- Batch update with CASE WHEN
UPDATE users SET status = CASE
    WHEN age < 18 THEN 0
    WHEN age >= 60 THEN 2
    ELSE 1
END
WHERE id IN (1, 2, 3, 4, 5);

-- Limit the number of rows updated
UPDATE users SET status = 0 ORDER BY created_at LIMIT 100;
```

> **Safety tip:** Always include a WHERE clause with UPDATE and DELETE. Consider enabling `sql_safe_updates` mode to prevent accidental mass modifications.

### 2.4 DELETE — Removing Data

```sql
-- Delete with a condition
DELETE FROM users WHERE status = 0;

-- Delete a limited number of rows
DELETE FROM users WHERE status = 0 ORDER BY created_at LIMIT 100;

-- Truncate the entire table (faster, but cannot be rolled back)
TRUNCATE TABLE users;

-- DELETE vs TRUNCATE
-- DELETE:   row-by-row, can be rolled back, triggers fire, auto-increment continues
-- TRUNCATE: instant wipe, cannot be rolled back, triggers do not fire, auto-increment resets
```

---

## 3. Multi-Table Queries (JOIN)

### 3.1 Setting Up Sample Tables

```sql
-- Orders table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0
);

-- Order line items
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

### 3.2 JOIN Types Explained

```sql
-- INNER JOIN: returns only rows that match in both tables
SELECT u.username, o.id AS order_id, o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: returns all rows from the left table; NULLs where there is no match on the right
SELECT u.username, o.id AS order_id, o.total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- RIGHT JOIN: returns all rows from the right table; NULLs where there is no match on the left
SELECT u.username, o.id AS order_id, o.total_amount
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- Find users who have never placed an order
SELECT u.username
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- Self join: a table joined to itself
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### 3.3 Multi-Table Joins

```sql
-- Three-table join: fetch full order details
SELECT
    u.username,
    o.id AS order_id,
    p.name AS product_name,
    oi.quantity,
    oi.price
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.status = 1
ORDER BY o.created_at DESC;
```

> **Interview tip:** What is the difference between INNER JOIN and LEFT JOIN?
> - INNER JOIN returns only rows with matches in both tables.
> - LEFT JOIN returns every row from the left table, filling in NULLs for unmatched right-side columns.

---

## 4. Subqueries and Advanced Queries

### 4.1 Subqueries

```sql
-- Scalar subquery (returns a single value)
SELECT * FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- Row subquery (returns one row)
SELECT * FROM users
WHERE (age, status) = (SELECT MAX(age), 1 FROM users);

-- Column subquery (returns one column)
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total_amount > 1000);

-- EXISTS subquery (checks for existence)
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- NOT EXISTS (find users with no orders)
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

### 4.2 UNION

```sql
-- UNION (removes duplicates)
SELECT username, email FROM users WHERE status = 1
UNION
SELECT username, email FROM archived_users WHERE status = 1;

-- UNION ALL (keeps duplicates — better performance)
SELECT username, 'active' AS type FROM users WHERE status = 1
UNION ALL
SELECT username, 'inactive' AS type FROM users WHERE status = 0;
```

### 4.3 Window Functions (MySQL 8.0+)

Window functions let you perform calculations across a set of rows without collapsing them into groups.

```sql
-- ROW_NUMBER(): assigns a unique sequential number to each row
SELECT
    username,
    age,
    ROW_NUMBER() OVER (ORDER BY age DESC) AS rank
FROM users;

-- RANK(): same rank for ties, then skips numbers
SELECT
    username,
    age,
    RANK() OVER (ORDER BY age DESC) AS rank
FROM users;

-- DENSE_RANK(): same rank for ties, no gaps
SELECT
    username,
    age,
    DENSE_RANK() OVER (ORDER BY age DESC) AS rank
FROM users;

-- Ranking within groups (rank per status)
SELECT
    username,
    status,
    age,
    ROW_NUMBER() OVER (PARTITION BY status ORDER BY age DESC) AS rank_in_group
FROM users;

-- LAG / LEAD: access previous / next row values
SELECT
    username,
    created_at,
    LAG(created_at, 1) OVER (ORDER BY created_at) AS prev_created,
    LEAD(created_at, 1) OVER (ORDER BY created_at) AS next_created
FROM users;

-- Running total
SELECT
    username,
    total_amount,
    SUM(total_amount) OVER (ORDER BY created_at) AS running_total
FROM orders;
```

### 4.4 Common Table Expressions (CTEs)

```sql
-- Basic CTE
WITH active_users AS (
    SELECT * FROM users WHERE status = 1
)
SELECT * FROM active_users WHERE age >= 18;

-- Multiple CTEs
WITH
    active_users AS (
        SELECT * FROM users WHERE status = 1
    ),
    user_orders AS (
        SELECT user_id, COUNT(*) AS order_count
        FROM orders
        GROUP BY user_id
    )
SELECT u.username, COALESCE(o.order_count, 0) AS orders
FROM active_users u
LEFT JOIN user_orders o ON u.id = o.user_id;

-- Recursive CTE (e.g., organizational hierarchy)
WITH RECURSIVE org_tree AS (
    -- Base case: top-level nodes
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive step: child nodes
    SELECT e.id, e.name, e.manager_id, t.level + 1
    FROM employees e
    INNER JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;
```

---

## 5. Indexes Deep Dive (Interview Favorite)

Indexes are the backbone of database performance and one of the most common interview topics.

### 5.1 What Is an Index?

Think of an index as a book's table of contents. It lets the database engine jump directly to the rows it needs instead of scanning the entire table.

### 5.2 Index Types

```sql
-- Primary key index
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT
);

-- Unique index
CREATE UNIQUE INDEX idx_email ON users(email);
-- or
ALTER TABLE users ADD UNIQUE INDEX idx_email(email);

-- Regular index
CREATE INDEX idx_username ON users(username);

-- Composite (multi-column) index
CREATE INDEX idx_status_created ON users(status, created_at);

-- Prefix index (for long string columns)
CREATE INDEX idx_email_prefix ON users(email(10));

-- Full-text index
CREATE FULLTEXT INDEX idx_content ON articles(content);
```

### 5.3 B+ Tree Internals (Frequently Asked in Interviews)

MySQL InnoDB uses the **B+ tree** as its index data structure. Here is why it matters:

**B+ Tree vs. B Tree:**

| Property | B Tree | B+ Tree |
|----------|--------|---------|
| Data storage | All nodes | Leaf nodes only |
| Leaf node linking | None | Doubly linked list |
| Range query efficiency | Low | High |
| Keys per I/O page | Fewer | More |

**Why B+ tree wins:**

1. **Fewer disk I/O operations** — Internal nodes store only keys, so each page holds more entries.
2. **Efficient range scans** — Leaf nodes form a sorted linked list; scanning a range is just a sequential traversal.
3. **Consistent performance** — Every lookup reaches a leaf node, so time complexity is always O(log n).

> **Interview question:** Why does MySQL use a B+ tree instead of a red-black tree or a hash index?
>
> - **Red-black tree:** Much taller, which means more disk I/O per lookup.
> - **Hash index:** Cannot support range queries or ordered scans.
> - **B+ tree:** Short and wide structure minimizes I/O; the leaf linked list enables range queries natively.

### 5.4 Clustered vs. Secondary Indexes

**Clustered index** (primary key index):

- Leaf nodes store the full row data.
- A table can have only one clustered index.
- Selection order: primary key > first unique non-null index > hidden row_id.

**Secondary index** (non-primary key index):

- Leaf nodes store the primary key value.
- Queries require a **bookmark lookup** (also called a "table access by index rowid"): first look up the secondary index to get the primary key, then look up the clustered index to get the full row.

```sql
-- Assume users has a primary key on `id` and an index idx_username on `username`

-- This query requires a bookmark lookup
SELECT * FROM users WHERE username = 'alice';
-- Step 1: traverse idx_username to find the primary key for username='alice'
-- Step 2: traverse the clustered index using that primary key to get the full row

-- This query does NOT require a bookmark lookup (covering index)
SELECT id, username FROM users WHERE username = 'alice';
-- The secondary index already contains both id and username — done in one step
```

### 5.5 When Indexes Stop Working (Must-Know for Interviews)

All of the following situations cause the optimizer to skip your index:

```sql
-- 1. Using a function on an indexed column
SELECT * FROM users WHERE YEAR(created_at) = 2024;  -- index not used
SELECT * FROM users WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';  -- index used

-- 2. Implicit type conversion
-- Assume phone is VARCHAR
SELECT * FROM users WHERE phone = 13800138000;   -- numeric comparison, index skipped
SELECT * FROM users WHERE phone = '13800138000';  -- string comparison, index used

-- 3. Leading wildcard in LIKE
SELECT * FROM users WHERE username LIKE '%alice';  -- index not used
SELECT * FROM users WHERE username LIKE 'alice%';  -- index used

-- 4. OR with a non-indexed column
SELECT * FROM users WHERE username = 'alice' OR age = 25;  -- if age has no index, the whole query goes full scan

-- 5. Composite index violating the leftmost prefix rule
-- Assume index idx_a_b_c(a, b, c)
SELECT * FROM users WHERE a = 1 AND b = 2;  -- index used
SELECT * FROM users WHERE b = 2 AND c = 3;  -- leftmost prefix violated, index not used
SELECT * FROM users WHERE a = 1 AND c = 3;  -- only column a is used

-- 6. Not-equal conditions
SELECT * FROM users WHERE status != 1;  -- likely full table scan

-- 7. IS NOT NULL (depends on data distribution)
SELECT * FROM users WHERE email IS NOT NULL;  -- if most rows are non-NULL, a full scan may be cheaper
```

### 5.6 The Leftmost Prefix Rule

This is the governing principle for composite indexes and comes up in almost every database interview:

```sql
-- Composite index idx_a_b_c(a, b, c)

-- Index IS used
WHERE a = 1
WHERE a = 1 AND b = 2
WHERE a = 1 AND b = 2 AND c = 3
WHERE a = 1 AND c = 3  -- only column a participates

-- Index is NOT used
WHERE b = 2
WHERE c = 3
WHERE b = 2 AND c = 3
```

> **Pro tip:** Place the most selective column (highest cardinality) first in your composite index.

### 5.7 Covering Indexes

When every column in your query is present in the index, the engine never needs to look up the actual table row. This is the fastest possible access pattern:

```sql
-- Assume index idx_name_age(name, age)

-- Covering index: all queried columns are in the index
SELECT name, age FROM users WHERE name = 'alice';  -- EXPLAIN shows "Using index"

-- Needs a bookmark lookup: email is not in the index
SELECT name, age, email FROM users WHERE name = 'alice';  -- must access the clustered index for email
```

Check the `Extra` column in EXPLAIN output for `Using index` to confirm a covering index is being used.

---

## 6. Transactions and Locks (Interview Essentials)

### 6.1 ACID Properties

Every transaction must satisfy four properties:

| Property | Meaning | Implementation in InnoDB |
|----------|---------|--------------------------|
| **Atomicity** | All or nothing — a transaction either fully succeeds or fully rolls back | Undo log |
| **Consistency** | The database moves from one valid state to another | Guaranteed by the other three properties working together |
| **Isolation** | Concurrent transactions do not interfere with each other | MVCC + locks |
| **Durability** | Once committed, data survives crashes | Redo log |

### 6.2 Transaction Basics

```sql
-- Start a transaction
START TRANSACTION;
-- or
BEGIN;

-- Commit
COMMIT;

-- Roll back
ROLLBACK;

-- Savepoints
SAVEPOINT sp1;
ROLLBACK TO sp1;

-- Example: money transfer
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE user_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE user_id = 2;

-- Verify constraints
SELECT balance FROM accounts WHERE user_id = 1;
-- If balance is negative, roll back
-- ROLLBACK;

COMMIT;
```

### 6.3 Isolation Levels (High-Frequency Interview Topic)

The SQL standard defines four isolation levels:

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|----------------|------------|---------------------|--------------|
| READ UNCOMMITTED | Possible | Possible | Possible |
| READ COMMITTED | Prevented | Possible | Possible |
| REPEATABLE READ | Prevented | Prevented | Possible* |
| SERIALIZABLE | Prevented | Prevented | Prevented |

> **MySQL InnoDB default:** REPEATABLE READ. InnoDB largely prevents phantom reads at this level through MVCC and gap locks.

**What the three anomalies mean:**

1. **Dirty read** — Reading data written by an uncommitted transaction (data may vanish if that transaction rolls back).
2. **Non-repeatable read** — Reading the same row twice within a transaction and getting different values because another transaction modified it in between.
3. **Phantom read** — Running the same query twice within a transaction and getting a different set of rows because another transaction inserted or deleted rows.

```sql
-- Check the current isolation level
SELECT @@transaction_isolation;

-- Change the isolation level for the current session
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### 6.4 MVCC (Multi-Version Concurrency Control)

MVCC is how InnoDB achieves high concurrency without readers blocking writers (or vice versa).

**How it works:**

1. Every row has hidden columns: `DB_TRX_ID` (the transaction ID that last modified the row) and `DB_ROLL_PTR` (a pointer to the previous version in the undo log).
2. When a row is updated, the old version is preserved in the undo log, forming a version chain.
3. When a transaction reads a row, it consults a **Read View** to decide which version is visible.

**Read View contents:**

- **creator_trx_id** — The transaction ID that created this Read View.
- **m_ids** — The list of currently active (uncommitted) transaction IDs.
- **min_trx_id** — The smallest ID in m_ids.
- **max_trx_id** — The next transaction ID to be assigned.

**Visibility rules:**

1. If the row's trx_id equals creator_trx_id, it is visible (you modified it yourself).
2. If the row's trx_id is less than min_trx_id, it is visible (the transaction that wrote it has already committed).
3. If the row's trx_id is greater than or equal to max_trx_id, it is not visible (the transaction had not started when this Read View was created).
4. If the row's trx_id is in m_ids, it is not visible (the transaction is still in progress).

**Key difference between RC and RR:**

- **READ COMMITTED (RC):** A new Read View is created on every SELECT.
- **REPEATABLE READ (RR):** A single Read View is created at the start of the transaction and reused.

### 6.5 Lock Mechanisms

#### Lock Categories

| Dimension | Types | Notes |
|-----------|-------|-------|
| Granularity | Table lock, Row lock | Row locks offer higher concurrency but more overhead |
| Mode | Shared (S), Exclusive (X) | S locks allow concurrent reads; X locks provide exclusive write access |
| Algorithm | Record lock, Gap lock, Next-key lock | Used to prevent phantom reads |

#### Row Lock Types (InnoDB)

```sql
-- Shared lock (S): multiple transactions can read simultaneously
SELECT * FROM users WHERE id = 1 LOCK IN SHARE MODE;
-- MySQL 8.0+ syntax
SELECT * FROM users WHERE id = 1 FOR SHARE;

-- Exclusive lock (X): only one transaction can read or write
SELECT * FROM users WHERE id = 1 FOR UPDATE;

-- Gap lock: locks the space between index records
-- Activated under RR isolation level for range queries
SELECT * FROM users WHERE age > 20 FOR UPDATE;  -- locks gaps where age > 20

-- Next-key lock = record lock + gap lock
-- This is InnoDB's default row-locking algorithm
```

#### Deadlocks

A deadlock occurs when two transactions each hold a lock the other one needs:

```sql
-- Transaction A
START TRANSACTION;
UPDATE users SET status = 1 WHERE id = 1;  -- locks row id=1
UPDATE users SET status = 1 WHERE id = 2;  -- waits for row id=2...

-- Transaction B
START TRANSACTION;
UPDATE users SET status = 2 WHERE id = 2;  -- locks row id=2
UPDATE users SET status = 2 WHERE id = 1;  -- waits for row id=1...

-- Deadlock! InnoDB detects it and rolls back one of the transactions.
```

**How to avoid deadlocks:**

1. Always access resources in a consistent order.
2. Use indexed lookups so locks target specific rows, not entire tables.
3. Keep transactions short to minimize lock-holding time.
4. Consider a lower isolation level if your use case allows it.

```sql
-- View the latest deadlock information
SHOW ENGINE INNODB STATUS;

-- View current lock waits
SELECT * FROM performance_schema.data_lock_waits;
```

---

## 7. Query Optimization in Practice

### 7.1 EXPLAIN Execution Plans

The first step in diagnosing slow queries is to examine the execution plan. For a deeper dive, see [MySQL EXPLAIN Execution Plan Explained](/posts/mysql/2019-09-06-mysql-explain/).

```sql
EXPLAIN SELECT * FROM users WHERE username = 'alice';
```

Key fields to watch:

- **type** — Access method, ranked best to worst: `const > eq_ref > ref > range > index > ALL`
- **key** — The index actually used
- **rows** — Estimated number of rows scanned
- **Extra** — Additional info; watch out for `Using filesort` and `Using temporary`

### 7.2 Slow Query Log

```sql
-- Check slow query configuration
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';

-- Enable the slow query log
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;  -- log queries taking longer than 1 second

-- Analyze the slow query log with mysqldumpslow
-- mysqldumpslow -s t -t 10 /var/lib/mysql/slow.log
```

### 7.3 Common Optimization Techniques

#### Pagination Optimization

```sql
-- Problem: deep pagination is extremely slow
SELECT * FROM orders ORDER BY id LIMIT 1000000, 10;  -- scans 1 million rows

-- Solution 1: deferred join
SELECT * FROM orders o
INNER JOIN (SELECT id FROM orders ORDER BY id LIMIT 1000000, 10) t
ON o.id = t.id;

-- Solution 2: keyset (cursor-based) pagination
SELECT * FROM orders WHERE id > 1000000 ORDER BY id LIMIT 10;
```

#### Batch Updates for Large Tables

```sql
-- Problem: updating millions of rows at once causes severe lock contention
UPDATE orders SET status = 2 WHERE created_at < '2024-01-01';

-- Solution: process in batches
UPDATE orders SET status = 2
WHERE created_at < '2024-01-01' AND status != 2
LIMIT 1000;

-- Repeat until affected rows = 0
```

#### COUNT Optimization

```sql
-- COUNT(*) vs COUNT(1) vs COUNT(column)
-- MySQL treats COUNT(*) and COUNT(1) identically — both count all rows.
-- COUNT(column) counts only non-NULL values in that column.

-- For InnoDB, COUNT(*) always requires scanning rows.
-- Optimization strategies:
-- 1. Use an approximate count: SHOW TABLE STATUS LIKE 'orders';
-- 2. Maintain a counter in a cache (e.g., Redis)
-- 3. Use a summary table
```

#### Sort Optimization

```sql
-- Problem: filesort is slow
SELECT * FROM orders WHERE status = 1 ORDER BY created_at DESC LIMIT 10;

-- Solution: create a composite index
CREATE INDEX idx_status_created ON orders(status, created_at);
-- The index is already sorted, so no extra sorting is needed
```

### 7.4 SQL Optimization Checklist

| Area | What to Check |
|------|---------------|
| **SELECT** | Avoid `SELECT *`; list only the columns you need |
| **WHERE** | Index your filter columns; avoid functions and implicit type conversions |
| **JOIN** | Drive from the smaller table; index join columns |
| **ORDER BY** | Leverage index ordering whenever possible |
| **LIMIT** | Use keyset pagination or deferred joins for deep pages |
| **Subqueries** | Consider rewriting as JOINs |
| **UNION** | Use UNION ALL when deduplication is not needed |

---

## 8. Interview Questions You Should Know

### 8.1 Core Concepts

**Q1: What storage engines does MySQL offer? How do InnoDB and MyISAM differ?**

| Feature | InnoDB | MyISAM |
|---------|--------|--------|
| Transactions | Yes | No |
| Row-level locking | Yes | Table-level only |
| Foreign keys | Yes | No |
| Crash recovery | Yes | No |
| Full-text search | Since MySQL 5.6 | Yes |
| COUNT(*) speed | Requires scan | Stores row count |

**Q2: What are the three normal forms?**

- **1NF** — Every column holds atomic (indivisible) values.
- **2NF** — All non-key columns depend on the entire primary key (no partial dependencies).
- **3NF** — No non-key column depends on another non-key column (no transitive dependencies).

> In practice, controlled denormalization is common for performance.

**Q3: Does VARCHAR(100) use more space than VARCHAR(10)?**

- **Disk storage:** Identical for the same actual data length.
- **Memory allocation:** MySQL may allocate buffers based on the declared maximum.
- **Constraint:** Limits the maximum string length at the application level.

**Q4: Auto-increment ID or UUID for primary keys?**

| Aspect | Auto-Increment | UUID |
|--------|----------------|------|
| Write performance | Sequential inserts (fast) | Random inserts (page splits) |
| Storage | 4–8 bytes | 36 bytes |
| Predictability | Guessable | Not guessable |
| Distributed systems | Requires coordination | Naturally globally unique |

> Rule of thumb: use auto-increment for single-node setups; use Snowflake IDs for distributed systems.

### 8.2 Indexes

**Q5: Why B+ tree instead of B tree, hash, or red-black tree?**

- **vs. B tree:** B+ trees store data only in leaves, so each internal page holds more keys (fewer I/O reads). The leaf linked list is ideal for range scans.
- **vs. Hash:** Hash indexes cannot support range queries or ordering.
- **vs. Red-black tree:** Much deeper, leading to more disk I/O.

**Q6: Clustered vs. non-clustered index?**

- **Clustered:** Leaf nodes contain the full row. One per table.
- **Non-clustered:** Leaf nodes contain the primary key value. Queries may require a bookmark lookup.

**Q7: When does an index become useless?**

- Applying a function to the indexed column
- Implicit type conversion
- Leading-wildcard LIKE
- OR with a non-indexed column
- Violating the leftmost prefix rule on a composite index
- Not-equal comparisons (in many cases)

**Q8: Explain the leftmost prefix rule for a composite index (a, b, c).**

- `WHERE a = 1` — uses the index
- `WHERE a = 1 AND b = 2` — uses the index
- `WHERE b = 2` — does not use the index
- `WHERE a = 1 AND c = 3` — only column `a` is used

### 8.3 Transactions and Locks

**Q9: What is ACID, and how does MySQL guarantee each property?**

- **Atomicity:** Undo log enables rollback.
- **Consistency:** Ensured by the other three properties together.
- **Isolation:** MVCC + locking.
- **Durability:** Redo log survives crashes.

**Q10: What isolation levels does MySQL support? What is the default?**

Four levels: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, and SERIALIZABLE.

InnoDB defaults to REPEATABLE READ.

**Q11: How does MVCC work?**

Multi-Version Concurrency Control maintains a version chain (via undo logs) and uses a Read View to determine which row versions are visible. Under RC, a new Read View is created per SELECT. Under RR, the Read View is created once and reused.

**Q12: What is a deadlock, and how do you prevent one?**

A deadlock happens when two transactions each wait for a lock held by the other.

Prevention strategies:
- Access rows in a consistent order
- Keep transactions short
- Use indexed lookups to minimize lock scope
- Set a lock wait timeout

### 8.4 Performance

**Q13: How do you find slow queries?**

1. Enable the slow query log.
2. Run EXPLAIN on the offending query.
3. Examine the `type`, `key`, `rows`, and `Extra` fields.

**Q14: How do you optimize deep pagination?**

```sql
-- Deferred join
SELECT * FROM t
INNER JOIN (SELECT id FROM t ORDER BY id LIMIT 1000000, 10) t2
ON t.id = t2.id;

-- Keyset pagination
SELECT * FROM t WHERE id > last_id ORDER BY id LIMIT 10;
```

**Q15: A query is running slowly. What could be wrong?**

1. Missing index or index not being used
2. Lock contention (blocked by another transaction)
3. Table is too large for the current query plan
4. Server resources exhausted (CPU, memory, disk I/O)
5. Network latency

---

## 9. Hands-On Exercises

### 9.1 SQL Writing Practice

Sample schema:

```sql
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    class_id INT,
    score INT
);

CREATE TABLE classes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50)
);
```

**Exercises:**

```sql
-- 1. Average score per class, ordered descending
SELECT c.name AS class_name, AVG(s.score) AS avg_score
FROM classes c
LEFT JOIN students s ON c.id = s.class_id
GROUP BY c.id
ORDER BY avg_score DESC;

-- 2. Top scorer(s) in each class
SELECT s.*
FROM students s
INNER JOIN (
    SELECT class_id, MAX(score) AS max_score
    FROM students
    GROUP BY class_id
) t ON s.class_id = t.class_id AND s.score = t.max_score;

-- 3. Students scoring above the overall average
SELECT *
FROM students
WHERE score > (SELECT AVG(score) FROM students);

-- 4. Rank students within each class using window functions
SELECT
    name,
    class_id,
    score,
    RANK() OVER (PARTITION BY class_id ORDER BY score DESC) AS rank_in_class
FROM students;

-- 5. Find users who logged in for at least 3 consecutive days
WITH ranked_logins AS (
    SELECT
        user_id,
        login_date,
        DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) DAY) AS grp
    FROM login_logs
)
SELECT DISTINCT user_id
FROM ranked_logins
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;
```

### 9.2 Real-World Scenario: E-Commerce Analytics

```sql
-- 1. Daily order count and revenue
SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_sales
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY DATE(created_at)
ORDER BY order_date;

-- 2. Each user's first order date and lifetime spend
SELECT
    user_id,
    MIN(created_at) AS first_order_time,
    SUM(total_amount) AS total_spent,
    COUNT(*) AS order_count
FROM orders
GROUP BY user_id;

-- 3. Top 10 customers by total spend
SELECT
    u.id,
    u.username,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY total_spent DESC
LIMIT 10;

-- 4. Monthly product sales leaderboard
SELECT
    DATE_FORMAT(o.created_at, '%Y-%m') AS month,
    p.name AS product_name,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
GROUP BY month, p.id
ORDER BY month, total_quantity DESC;
```

---

## 10. Summary

This guide covered the full spectrum of MySQL SQL knowledge:

| Section | Key Topics |
|---------|------------|
| Fundamentals | Database and table operations, data type selection |
| CRUD | INSERT, SELECT, UPDATE, DELETE |
| Multi-table queries | JOIN types, subqueries |
| Advanced features | Window functions, CTEs |
| Indexes | B+ tree internals, index invalidation, covering indexes |
| Transactions | ACID, isolation levels, MVCC, locking |
| Optimization | EXPLAIN, slow query log, pagination strategies |

**Recommendations for continued learning:**

1. **Practice relentlessly** — Work through the [LeetCode SQL 50](https://leetcode.com/studyplan/top-sql-50/) problem set.
2. **Understand the internals** — Knowing how to write SQL is not enough; understanding how indexes and transactions work under the hood sets you apart.
3. **Make EXPLAIN a habit** — Run it on every non-trivial query before deploying to production.

## References

- [MySQL Official Documentation](https://dev.mysql.com/doc/refman/8.0/en/)
- [MySQL Index Guide — JavaGuide](https://javaguide.cn/database/mysql/mysql-index.html)
- [Transaction Isolation Levels — JavaGuide](https://javaguide.cn/database/mysql/transaction-isolation-level.html)
- [Top SQL 50 — LeetCode](https://leetcode.com/studyplan/top-sql-50/)
- [MySQL 45 Lectures — GeekTime](https://time.geekbang.org/column/intro/139)
