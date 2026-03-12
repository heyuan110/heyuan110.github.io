+++
title = "MySQL SQL 完全指南：从小白到高手的进阶之路（含面试宝典）"
date = 2026-01-23T20:06:36+08:00
description = "全面掌握 MySQL SQL 核心知识：从基础语法到高级特性，涵盖索引原理、事务隔离、锁机制、查询优化。包含大量实战案例和高频面试题，助你快速从 SQL 小白进阶为数据库高手。"
toc = true
tags = ["MySQL", "SQL", "Database", "Interview", "Index", "Transaction", "Performance"]
categories = ["MySQL"]
keywords = ["MySQL教程", "SQL入门", "MySQL面试题", "索引优化", "事务隔离级别", "MVCC", "B+树"]
+++
![MySQL SQL 完全指南：从基础到精通](cover.webp)

**SQL（Structured Query Language）** 是与数据库交流的通用语言。无论你是后端开发、数据分析还是运维工程师，掌握 SQL 都是必备技能。本文以 MySQL 为例，从零基础带你系统学习 SQL，并深入讲解面试高频考点，助你快速进阶。

> 本文约 15000 字，建议收藏后分章节阅读。文章结构清晰，可根据目录跳转到感兴趣的部分。

## 一、SQL 基础入门

### 1.1 什么是 SQL

SQL 是 **结构化查询语言**（Structured Query Language）的缩写，用于管理关系型数据库。它可以：

- **查询数据**：从数据库中检索信息
- **操作数据**：插入、更新、删除数据
- **定义结构**：创建、修改数据库和表
- **控制访问**：管理用户权限

SQL 语句分为以下几类：

| 类型 | 全称 | 常用语句 | 作用 |
|------|------|----------|------|
| **DDL** | Data Definition Language | CREATE、ALTER、DROP | 定义数据库结构 |
| **DML** | Data Manipulation Language | SELECT、INSERT、UPDATE、DELETE | 操作数据 |
| **DCL** | Data Control Language | GRANT、REVOKE | 控制访问权限 |
| **TCL** | Transaction Control Language | COMMIT、ROLLBACK | 管理事务 |

### 1.2 数据库基本操作

```sql
-- 创建数据库
CREATE DATABASE shop DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 查看所有数据库
SHOW DATABASES;

-- 使用数据库
USE shop;

-- 查看当前数据库
SELECT DATABASE();

-- 删除数据库（谨慎操作！）
DROP DATABASE shop;
```

> **最佳实践**：建议使用 `utf8mb4` 字符集，它完整支持 Unicode，包括 emoji 表情。

### 1.3 表的基本操作

```sql
-- 创建表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL COMMENT '邮箱',
    password VARCHAR(255) NOT NULL COMMENT '密码',
    age TINYINT UNSIGNED DEFAULT 0 COMMENT '年龄',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常 0禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 查看表结构
DESC users;
SHOW CREATE TABLE users;

-- 修改表
ALTER TABLE users ADD COLUMN phone VARCHAR(20) COMMENT '手机号';  -- 添加列
ALTER TABLE users MODIFY COLUMN phone VARCHAR(15);                -- 修改列类型
ALTER TABLE users CHANGE phone mobile VARCHAR(15);                -- 重命名列
ALTER TABLE users DROP COLUMN mobile;                             -- 删除列

-- 删除表
DROP TABLE IF EXISTS users;
```

### 1.4 数据类型选择指南

选择合适的数据类型是数据库设计的关键：

#### 整数类型

| 类型 | 字节 | 范围（有符号） | 适用场景 |
|------|------|----------------|----------|
| TINYINT | 1 | -128 ~ 127 | 状态标识、年龄 |
| SMALLINT | 2 | -32768 ~ 32767 | 小范围数值 |
| INT | 4 | -21亿 ~ 21亿 | 主键、计数 |
| BIGINT | 8 | 很大 | 大数据量主键 |

#### 字符串类型

| 类型 | 长度 | 适用场景 |
|------|------|----------|
| CHAR(n) | 固定 n 字节 | 定长字符串，如手机号、身份证 |
| VARCHAR(n) | 可变，最大 n | 变长字符串，如用户名、邮箱 |
| TEXT | 最大 64KB | 长文本，如文章内容 |
| MEDIUMTEXT | 最大 16MB | 更长的文本 |

#### 时间类型

| 类型 | 格式 | 范围 | 建议 |
|------|------|------|------|
| DATE | YYYY-MM-DD | 1000-01-01 ~ 9999-12-31 | 仅需日期 |
| DATETIME | YYYY-MM-DD HH:MM:SS | 1000-01-01 ~ 9999-12-31 | 需要日期和时间 |
| TIMESTAMP | YYYY-MM-DD HH:MM:SS | 1970-2038 | 自动更新时间戳 |

> **面试考点**：DATETIME 和 TIMESTAMP 的区别？
> - DATETIME 占 8 字节，存储范围大，不受时区影响
> - TIMESTAMP 占 4 字节，存储范围小，会自动转换时区

---

## 二、CRUD 操作详解

### 2.1 INSERT - 插入数据

```sql
-- 单行插入
INSERT INTO users (username, email, password, age)
VALUES ('zhangsan', 'zhangsan@example.com', 'hashed_password', 25);

-- 多行插入（推荐，效率更高）
INSERT INTO users (username, email, password, age) VALUES
('lisi', 'lisi@example.com', 'hashed_password', 30),
('wangwu', 'wangwu@example.com', 'hashed_password', 28),
('zhaoliu', 'zhaoliu@example.com', 'hashed_password', 35);

-- 插入或更新（存在则更新）
INSERT INTO users (id, username, email, password)
VALUES (1, 'zhangsan', 'new_email@example.com', 'new_password')
ON DUPLICATE KEY UPDATE email = VALUES(email), password = VALUES(password);

-- 插入忽略重复（存在则跳过）
INSERT IGNORE INTO users (username, email, password)
VALUES ('zhangsan', 'zhangsan@example.com', 'password');
```

### 2.2 SELECT - 查询数据

这是 SQL 中最常用、也是最复杂的语句。

#### 基础查询

```sql
-- 查询所有列（不推荐，影响性能）
SELECT * FROM users;

-- 查询指定列（推荐）
SELECT id, username, email FROM users;

-- 使用别名
SELECT id AS user_id, username AS name FROM users;

-- 去重
SELECT DISTINCT status FROM users;

-- 限制行数
SELECT * FROM users LIMIT 10;          -- 前 10 行
SELECT * FROM users LIMIT 10 OFFSET 20; -- 跳过 20 行取 10 行
SELECT * FROM users LIMIT 20, 10;       -- 同上，简写形式
```

#### WHERE 条件查询

```sql
-- 比较运算符
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE status != 0;
SELECT * FROM users WHERE age <> 18;  -- 不等于的另一种写法

-- 逻辑运算符
SELECT * FROM users WHERE age >= 18 AND status = 1;
SELECT * FROM users WHERE age < 18 OR age > 60;
SELECT * FROM users WHERE NOT status = 0;

-- 范围查询
SELECT * FROM users WHERE age BETWEEN 18 AND 30;   -- 包含边界
SELECT * FROM users WHERE age IN (18, 20, 25, 30);

-- 空值判断
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;

-- 模糊查询
SELECT * FROM users WHERE username LIKE 'zhang%';  -- 以 zhang 开头
SELECT * FROM users WHERE username LIKE '%san';    -- 以 san 结尾
SELECT * FROM users WHERE username LIKE '%ang%';   -- 包含 ang
SELECT * FROM users WHERE username LIKE 'zhang_';  -- _ 匹配单个字符
```

> **性能警告**：`LIKE '%xxx'` 左模糊查询无法使用索引，会导致全表扫描！

#### ORDER BY 排序

```sql
-- 升序（默认）
SELECT * FROM users ORDER BY age ASC;

-- 降序
SELECT * FROM users ORDER BY created_at DESC;

-- 多字段排序
SELECT * FROM users ORDER BY status DESC, created_at DESC;

-- NULL 值排序（MySQL 中 NULL 被视为最小值）
SELECT * FROM users ORDER BY age IS NULL, age;  -- NULL 排最后
```

#### GROUP BY 分组

```sql
-- 基本分组
SELECT status, COUNT(*) AS user_count
FROM users
GROUP BY status;

-- 多字段分组
SELECT status, age, COUNT(*) AS count
FROM users
GROUP BY status, age;

-- HAVING 过滤分组（WHERE 在分组前过滤，HAVING 在分组后过滤）
SELECT status, COUNT(*) AS user_count
FROM users
GROUP BY status
HAVING user_count > 10;

-- WITH ROLLUP 添加汇总行
SELECT status, COUNT(*) AS user_count
FROM users
GROUP BY status WITH ROLLUP;
```

### 2.3 UPDATE - 更新数据

```sql
-- 更新单个字段
UPDATE users SET status = 0 WHERE id = 1;

-- 更新多个字段
UPDATE users SET status = 0, updated_at = NOW() WHERE id = 1;

-- 条件更新
UPDATE users SET status = 0 WHERE last_login < '2024-01-01';

-- 使用 CASE WHEN 批量更新
UPDATE users SET status = CASE
    WHEN age < 18 THEN 0
    WHEN age >= 60 THEN 2
    ELSE 1
END
WHERE id IN (1, 2, 3, 4, 5);

-- 限制更新行数
UPDATE users SET status = 0 ORDER BY created_at LIMIT 100;
```

> **安全警告**：UPDATE 和 DELETE 操作一定要带 WHERE 条件！建议开启 `sql_safe_updates` 模式。

### 2.4 DELETE - 删除数据

```sql
-- 条件删除
DELETE FROM users WHERE status = 0;

-- 限制删除行数
DELETE FROM users WHERE status = 0 ORDER BY created_at LIMIT 100;

-- 清空表（TRUNCATE 更快，但不可回滚）
TRUNCATE TABLE users;

-- DELETE vs TRUNCATE
-- DELETE: 逐行删除，可回滚，触发器会执行，自增 ID 继续
-- TRUNCATE: 直接清空，不可回滚，触发器不执行，自增 ID 重置
```

---

## 三、多表查询（JOIN）

### 3.1 表关系与准备数据

先创建示例表：

```sql
-- 订单表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 商品表
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0
);

-- 订单详情表
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

### 3.2 JOIN 类型详解

```sql
-- INNER JOIN（内连接）：只返回两表都匹配的行
SELECT u.username, o.id AS order_id, o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN（左连接）：返回左表所有行，右表无匹配则为 NULL
SELECT u.username, o.id AS order_id, o.total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- RIGHT JOIN（右连接）：返回右表所有行，左表无匹配则为 NULL
SELECT u.username, o.id AS order_id, o.total_amount
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- 查找没有订单的用户
SELECT u.username
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- 自连接：表与自身连接
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### 3.3 多表关联查询

```sql
-- 三表关联：查询订单详情
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

> **面试考点**：INNER JOIN 和 LEFT JOIN 的区别？
> - INNER JOIN 只返回两表都有匹配的行
> - LEFT JOIN 返回左表所有行，右表无匹配则为 NULL

---

## 四、子查询与高级查询

### 4.1 子查询

```sql
-- 标量子查询（返回单个值）
SELECT * FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- 行子查询（返回一行）
SELECT * FROM users
WHERE (age, status) = (SELECT MAX(age), 1 FROM users);

-- 列子查询（返回一列）
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total_amount > 1000);

-- EXISTS 子查询（判断是否存在）
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- NOT EXISTS（找出没有订单的用户）
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

### 4.2 UNION 合并结果

```sql
-- UNION（去重）
SELECT username, email FROM users WHERE status = 1
UNION
SELECT username, email FROM archived_users WHERE status = 1;

-- UNION ALL（不去重，性能更好）
SELECT username, 'active' AS type FROM users WHERE status = 1
UNION ALL
SELECT username, 'inactive' AS type FROM users WHERE status = 0;
```

### 4.3 窗口函数（MySQL 8.0+）

窗口函数是 MySQL 8.0 引入的强大特性，可以在不改变行数的情况下进行聚合计算。

```sql
-- ROW_NUMBER()：为每行分配唯一序号
SELECT
    username,
    age,
    ROW_NUMBER() OVER (ORDER BY age DESC) AS rank
FROM users;

-- RANK()：相同值同排名，后续跳过
SELECT
    username,
    age,
    RANK() OVER (ORDER BY age DESC) AS rank
FROM users;

-- DENSE_RANK()：相同值同排名，后续不跳过
SELECT
    username,
    age,
    DENSE_RANK() OVER (ORDER BY age DESC) AS rank
FROM users;

-- 分组排名（每个 status 内排名）
SELECT
    username,
    status,
    age,
    ROW_NUMBER() OVER (PARTITION BY status ORDER BY age DESC) AS rank_in_group
FROM users;

-- LAG/LEAD：获取前/后行的值
SELECT
    username,
    created_at,
    LAG(created_at, 1) OVER (ORDER BY created_at) AS prev_created,
    LEAD(created_at, 1) OVER (ORDER BY created_at) AS next_created
FROM users;

-- 累计求和
SELECT
    username,
    total_amount,
    SUM(total_amount) OVER (ORDER BY created_at) AS running_total
FROM orders;
```

### 4.4 CTE（通用表表达式）

```sql
-- 基本 CTE
WITH active_users AS (
    SELECT * FROM users WHERE status = 1
)
SELECT * FROM active_users WHERE age >= 18;

-- 多个 CTE
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

-- 递归 CTE（如组织架构）
WITH RECURSIVE org_tree AS (
    -- 基础查询：顶级节点
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 递归查询：子节点
    SELECT e.id, e.name, e.manager_id, t.level + 1
    FROM employees e
    INNER JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;
```

---

## 五、索引详解（面试重点）

索引是数据库性能优化的核心，也是面试必考内容。

### 5.1 索引是什么

索引就像书的目录，帮助数据库快速定位数据。没有索引，数据库只能全表扫描。

### 5.2 索引类型

```sql
-- 主键索引（PRIMARY KEY）
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT
);

-- 唯一索引（UNIQUE）
CREATE UNIQUE INDEX idx_email ON users(email);
-- 或
ALTER TABLE users ADD UNIQUE INDEX idx_email(email);

-- 普通索引（INDEX）
CREATE INDEX idx_username ON users(username);

-- 复合索引（多列索引）
CREATE INDEX idx_status_created ON users(status, created_at);

-- 前缀索引（长字符串字段）
CREATE INDEX idx_email_prefix ON users(email(10));

-- 全文索引（FULLTEXT）
CREATE FULLTEXT INDEX idx_content ON articles(content);
```

### 5.3 B+ 树原理（面试高频）

MySQL InnoDB 使用 **B+ 树** 作为索引数据结构，核心特点：

**B+ 树 vs B 树**：

| 特性 | B 树 | B+ 树 |
|------|------|-------|
| 数据存储位置 | 所有节点 | 仅叶子节点 |
| 叶子节点连接 | 无 | 双向链表 |
| 范围查询效率 | 低 | 高 |
| 单次 IO 索引数 | 少 | 多 |

**为什么选择 B+ 树**：

1. **减少磁盘 IO**：非叶子节点只存储键值，一页可存储更多索引
2. **范围查询高效**：叶子节点形成有序链表，范围扫描只需遍历链表
3. **查询稳定**：所有查询都要到叶子节点，时间复杂度稳定为 O(log n)

> **面试题**：为什么 MySQL 选择 B+ 树而不是红黑树、Hash 索引？
>
> - 红黑树：树高较大，磁盘 IO 次数多
> - Hash 索引：不支持范围查询，不支持排序
> - B+ 树：矮胖结构减少 IO，叶子链表支持范围查询

### 5.4 聚簇索引与二级索引

**聚簇索引**（主键索引）：

- 叶子节点存储完整的行数据
- 一个表只能有一个聚簇索引
- 规则：主键 > 第一个唯一非空索引 > 隐藏的 row_id

**二级索引**（非主键索引）：

- 叶子节点存储主键值
- 查询需要 **回表**：先查二级索引获取主键，再查聚簇索引获取数据

```sql
-- 示例：假设 users 表有主键 id 和索引 idx_username

-- 这个查询需要回表
SELECT * FROM users WHERE username = 'zhangsan';
-- 1. 通过 idx_username 找到 username='zhangsan' 的主键 id
-- 2. 再通过主键 id 查询聚簇索引获取完整数据

-- 这个查询不需要回表（覆盖索引）
SELECT id, username FROM users WHERE username = 'zhangsan';
-- 二级索引已包含 id 和 username，直接返回
```

### 5.5 索引失效场景（面试必考）

以下情况会导致索引失效：

```sql
-- 1. 对索引列使用函数
SELECT * FROM users WHERE YEAR(created_at) = 2024;  -- ❌ 索引失效
SELECT * FROM users WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';  -- ✅ 可以用索引

-- 2. 隐式类型转换
-- 假设 phone 是 VARCHAR 类型
SELECT * FROM users WHERE phone = 13800138000;  -- ❌ 数字比较，索引失效
SELECT * FROM users WHERE phone = '13800138000';  -- ✅ 字符串比较

-- 3. LIKE 左模糊
SELECT * FROM users WHERE username LIKE '%zhang';  -- ❌ 索引失效
SELECT * FROM users WHERE username LIKE 'zhang%';  -- ✅ 可以用索引

-- 4. OR 连接非索引列
SELECT * FROM users WHERE username = 'zhang' OR age = 25;  -- 如果 age 没有索引，整个查询不走索引

-- 5. 联合索引不满足最左前缀
-- 假设有索引 idx_a_b_c(a, b, c)
SELECT * FROM users WHERE a = 1 AND b = 2;  -- ✅ 使用索引
SELECT * FROM users WHERE b = 2 AND c = 3;  -- ❌ 不满足最左前缀，索引失效
SELECT * FROM users WHERE a = 1 AND c = 3;  -- ⚠️ 只能使用 a 列索引

-- 6. 使用不等于
SELECT * FROM users WHERE status != 1;  -- ❌ 大概率全表扫描

-- 7. IS NOT NULL（视情况）
SELECT * FROM users WHERE email IS NOT NULL;  -- 如果大部分都不为 NULL，可能全表扫描更快
```

### 5.6 最左前缀原则

复合索引的核心原则，面试必问：

```sql
-- 复合索引 idx_a_b_c(a, b, c)

-- ✅ 可以使用索引
WHERE a = 1
WHERE a = 1 AND b = 2
WHERE a = 1 AND b = 2 AND c = 3
WHERE a = 1 AND c = 3  -- 只能用到 a

-- ❌ 无法使用索引
WHERE b = 2
WHERE c = 3
WHERE b = 2 AND c = 3
```

> **技巧**：把选择性最高（区分度大）的列放在索引最前面。

### 5.7 覆盖索引

当查询的列都包含在索引中时，无需回表，性能最佳：

```sql
-- 假设有索引 idx_name_age(name, age)

-- 覆盖索引：查询列都在索引中
SELECT name, age FROM users WHERE name = 'zhang';  -- ✅ Using index

-- 需要回表：查询列不全在索引中
SELECT name, age, email FROM users WHERE name = 'zhang';  -- 需要回表查 email
```

通过 EXPLAIN 查看 `Extra` 列是否显示 `Using index` 判断是否为覆盖索引。

---

## 六、事务与锁（面试重点）

### 6.1 ACID 特性

事务必须满足四个特性：

| 特性 | 英文 | 含义 | 实现机制 |
|------|------|------|----------|
| **原子性** | Atomicity | 事务要么全成功，要么全失败 | undo log |
| **一致性** | Consistency | 事务前后数据保持一致 | 其他三个特性共同保证 |
| **隔离性** | Isolation | 事务之间互不干扰 | MVCC + 锁 |
| **持久性** | Durability | 提交后数据永久保存 | redo log |

### 6.2 事务基本操作

```sql
-- 开始事务
START TRANSACTION;
-- 或
BEGIN;

-- 提交事务
COMMIT;

-- 回滚事务
ROLLBACK;

-- 设置保存点
SAVEPOINT sp1;
ROLLBACK TO sp1;

-- 示例：转账事务
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE user_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE user_id = 2;

-- 检查约束
SELECT balance FROM accounts WHERE user_id = 1;
-- 如果余额为负，回滚
-- ROLLBACK;

COMMIT;
```

### 6.3 隔离级别（面试高频）

SQL 标准定义了四种隔离级别：

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|----------|------|------------|------|
| READ UNCOMMITTED（读未提交） | ✅ 可能 | ✅ 可能 | ✅ 可能 |
| READ COMMITTED（读已提交） | ❌ 解决 | ✅ 可能 | ✅ 可能 |
| REPEATABLE READ（可重复读） | ❌ 解决 | ❌ 解决 | ✅ 可能* |
| SERIALIZABLE（串行化） | ❌ 解决 | ❌ 解决 | ❌ 解决 |

> **MySQL InnoDB 默认**：REPEATABLE READ，且通过 MVCC + 间隙锁在很大程度上解决了幻读。

**三种问题解释**：

1. **脏读**：读到其他事务未提交的数据（事务回滚后数据消失）
2. **不可重复读**：同一事务内，两次读取同一数据结果不同（被其他事务修改）
3. **幻读**：同一事务内，两次查询结果集行数不同（被其他事务插入/删除）

```sql
-- 查看当前隔离级别
SELECT @@transaction_isolation;

-- 设置隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### 6.4 MVCC 机制

**MVCC**（Multi-Version Concurrency Control，多版本并发控制）是 InnoDB 实现高并发的核心：

**原理**：
1. 每行数据有隐藏列：`DB_TRX_ID`（事务 ID）、`DB_ROLL_PTR`（回滚指针）
2. 修改数据时，旧版本保存在 undo log，形成版本链
3. 读取时，根据 **Read View** 判断可见性

**Read View**：
- **creator_trx_id**：创建该 Read View 的事务 ID
- **m_ids**：活跃事务 ID 列表
- **min_trx_id**：m_ids 中最小的事务 ID
- **max_trx_id**：下一个将分配的事务 ID

**可见性判断规则**：
1. 数据的 trx_id == creator_trx_id → 可见（自己修改的）
2. 数据的 trx_id < min_trx_id → 可见（事务已提交）
3. 数据的 trx_id >= max_trx_id → 不可见（事务还未开始）
4. 数据的 trx_id 在 m_ids 中 → 不可见（事务未提交）

**RC 与 RR 的区别**：
- **RC**：每次 SELECT 都创建新的 Read View
- **RR**：事务开始时创建一次 Read View，后续复用

### 6.5 锁机制

#### 锁的分类

| 维度 | 类型 | 说明 |
|------|------|------|
| 粒度 | 表锁、行锁 | 行锁并发高但开销大 |
| 模式 | 共享锁(S)、排他锁(X) | S 锁共享读，X 锁独占写 |
| 算法 | 记录锁、间隙锁、临键锁 | 用于防止幻读 |

#### 行锁类型（InnoDB）

```sql
-- 共享锁（S Lock）：允许多个事务同时读
SELECT * FROM users WHERE id = 1 LOCK IN SHARE MODE;
-- MySQL 8.0+ 新语法
SELECT * FROM users WHERE id = 1 FOR SHARE;

-- 排他锁（X Lock）：只允许一个事务读写
SELECT * FROM users WHERE id = 1 FOR UPDATE;

-- 间隙锁（Gap Lock）：锁定索引记录之间的间隙
-- 在 RR 隔离级别下，范围查询会产生间隙锁
SELECT * FROM users WHERE age > 20 FOR UPDATE;  -- 锁定 age > 20 的间隙

-- 临键锁（Next-Key Lock）= 记录锁 + 间隙锁
-- InnoDB 默认的行锁算法
```

#### 死锁

当两个事务互相等待对方持有的锁时，就会发生死锁：

```sql
-- 事务 A
START TRANSACTION;
UPDATE users SET status = 1 WHERE id = 1;  -- 锁定 id=1
UPDATE users SET status = 1 WHERE id = 2;  -- 等待 id=2 的锁...

-- 事务 B
START TRANSACTION;
UPDATE users SET status = 2 WHERE id = 2;  -- 锁定 id=2
UPDATE users SET status = 2 WHERE id = 1;  -- 等待 id=1 的锁...

-- 死锁！InnoDB 会检测到并回滚其中一个事务
```

**避免死锁的方法**：

1. 按固定顺序访问资源
2. 尽量使用索引访问数据
3. 减少事务持锁时间
4. 使用较低的隔离级别

```sql
-- 查看死锁日志
SHOW ENGINE INNODB STATUS;

-- 查看当前锁等待
SELECT * FROM performance_schema.data_lock_waits;
```

---

## 七、查询优化实战

### 7.1 EXPLAIN 执行计划

分析 SQL 性能的第一步是查看执行计划，详细内容请参考 [MySQL EXPLAIN 执行计划详解](/posts/mysql/2019-09-06-mysql-explain/)。

```sql
EXPLAIN SELECT * FROM users WHERE username = 'zhangsan';
```

关键指标：
- **type**：访问类型，从好到差：`const > eq_ref > ref > range > index > ALL`
- **key**：实际使用的索引
- **rows**：预估扫描行数
- **Extra**：额外信息，注意 `Using filesort`、`Using temporary`

### 7.2 慢查询日志

```sql
-- 查看慢查询配置
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';

-- 开启慢查询日志
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;  -- 超过 1 秒记录

-- 分析慢查询日志
-- 使用 mysqldumpslow 工具
-- mysqldumpslow -s t -t 10 /var/lib/mysql/slow.log
```

### 7.3 常见优化技巧

#### 分页优化

```sql
-- 问题：深分页性能很差
SELECT * FROM orders ORDER BY id LIMIT 1000000, 10;  -- 需要扫描 100 万行

-- 优化方案1：延迟关联
SELECT * FROM orders o
INNER JOIN (SELECT id FROM orders ORDER BY id LIMIT 1000000, 10) t
ON o.id = t.id;

-- 优化方案2：游标分页（需要知道上一页最后一条的 id）
SELECT * FROM orders WHERE id > 1000000 ORDER BY id LIMIT 10;
```

#### 大数据量 UPDATE

```sql
-- 问题：一次更新太多行，锁等待严重
UPDATE orders SET status = 2 WHERE created_at < '2024-01-01';

-- 优化：分批更新
UPDATE orders SET status = 2
WHERE created_at < '2024-01-01' AND status != 2
LIMIT 1000;

-- 循环执行直到影响行数为 0
```

#### COUNT 优化

```sql
-- COUNT(*) vs COUNT(1) vs COUNT(列名)
-- MySQL 官方优化：COUNT(*) 和 COUNT(1) 效率相同，都统计所有行
-- COUNT(列名) 只统计该列非 NULL 的行

-- 对于 InnoDB，COUNT(*) 需要全表扫描
-- 优化方案：
-- 1. 使用近似值：SHOW TABLE STATUS LIKE 'orders';
-- 2. 使用缓存（Redis）维护计数
-- 3. 使用汇总表
```

#### 排序优化

```sql
-- 问题：filesort 性能差
SELECT * FROM orders WHERE status = 1 ORDER BY created_at DESC LIMIT 10;

-- 优化：创建复合索引
CREATE INDEX idx_status_created ON orders(status, created_at);
-- 索引已经有序，无需额外排序
```

### 7.4 SQL 优化清单

| 优化项 | 检查点 |
|--------|--------|
| **SELECT** | 避免 `SELECT *`，只查需要的列 |
| **WHERE** | 条件字段加索引，避免函数和隐式转换 |
| **JOIN** | 小表驱动大表，关联字段加索引 |
| **ORDER BY** | 尽量利用索引排序 |
| **LIMIT** | 深分页使用游标或延迟关联 |
| **子查询** | 考虑用 JOIN 替代 |
| **UNION** | 无需去重时用 UNION ALL |

---

## 八、高频面试题精选

### 8.1 基础概念类

**Q1：MySQL 有哪些存储引擎？InnoDB 和 MyISAM 的区别？**

| 特性 | InnoDB | MyISAM |
|------|--------|--------|
| 事务支持 | ✅ 支持 | ❌ 不支持 |
| 行级锁 | ✅ 支持 | ❌ 只有表锁 |
| 外键 | ✅ 支持 | ❌ 不支持 |
| 崩溃恢复 | ✅ 支持 | ❌ 不支持 |
| 全文索引 | MySQL 5.6+ 支持 | ✅ 支持 |
| COUNT(*) | 需要扫描 | 保存行数 |

**Q2：什么是三大范式？**

- **第一范式（1NF）**：字段不可再分（原子性）
- **第二范式（2NF）**：在 1NF 基础上，非主键字段完全依赖主键
- **第三范式（3NF）**：在 2NF 基础上，非主键字段不传递依赖

> 实际开发中，为了性能可以适当反范式（冗余字段）。

**Q3：VARCHAR(100) 和 VARCHAR(10) 有什么区别？**

- 存储空间：实际存储相同长度时占用空间一样
- 内存消耗：MySQL 分配内存时按最大长度分配
- 约束作用：限制最大输入长度

**Q4：MySQL 主键用自增 ID 还是 UUID？**

| 方面 | 自增 ID | UUID |
|------|---------|------|
| 写入性能 | ✅ 顺序写入 | ❌ 随机写入（页分裂） |
| 存储空间 | 4-8 字节 | 36 字节 |
| 安全性 | ❌ 可猜测 | ✅ 不可猜测 |
| 分布式 | ❌ 需要协调 | ✅ 天然全局唯一 |

> 推荐：单机用自增 ID，分布式用雪花算法。

### 8.2 索引类

**Q5：为什么 MySQL 使用 B+ 树而不是 B 树、Hash、红黑树？**

- **vs B 树**：B+ 树数据只在叶子节点，一页存更多索引，减少 IO；叶子节点链表适合范围查询
- **vs Hash**：Hash 不支持范围查询和排序
- **vs 红黑树**：红黑树层高大，磁盘 IO 多

**Q6：什么是聚簇索引和非聚簇索引？**

- **聚簇索引**：叶子节点存储整行数据，一表只有一个
- **非聚簇索引**：叶子节点存储主键值，查询需要回表

**Q7：什么情况下索引会失效？**

- 对索引列使用函数
- 隐式类型转换
- LIKE 左模糊查询
- OR 连接非索引列
- 联合索引不满足最左前缀
- 使用不等于条件

**Q8：联合索引 (a, b, c) 的最左前缀原则？**

- `WHERE a = 1` ✅
- `WHERE a = 1 AND b = 2` ✅
- `WHERE b = 2` ❌
- `WHERE a = 1 AND c = 3` 只用到 a

### 8.3 事务与锁类

**Q9：事务的 ACID 特性是什么？MySQL 如何保证？**

- **原子性**：undo log 回滚
- **一致性**：其他三个特性保证
- **隔离性**：MVCC + 锁
- **持久性**：redo log 恢复

**Q10：MySQL 的隔离级别有哪些？默认是什么？**

四种隔离级别：READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ、SERIALIZABLE

MySQL InnoDB 默认 REPEATABLE READ。

**Q11：MVCC 是什么？如何实现？**

多版本并发控制。通过版本链 + Read View 实现非锁定读取。

RC 每次读创建 Read View，RR 事务开始创建一次。

**Q12：什么是死锁？如何避免？**

两个事务互相等待对方的锁。

避免方法：
- 按固定顺序访问资源
- 减少事务持锁时间
- 使用索引避免锁表
- 设置锁等待超时

### 8.4 优化类

**Q13：如何定位慢查询？**

1. 开启慢查询日志
2. 使用 EXPLAIN 分析执行计划
3. 查看 type、key、rows、Extra 字段

**Q14：如何优化深分页？**

```sql
-- 延迟关联
SELECT * FROM t
INNER JOIN (SELECT id FROM t ORDER BY id LIMIT 1000000, 10) t2
ON t.id = t2.id;

-- 游标分页
SELECT * FROM t WHERE id > last_id ORDER BY id LIMIT 10;
```

**Q15：一条 SQL 执行很慢，可能是什么原因？**

1. 没有使用索引或索引失效
2. 锁等待（被其他事务阻塞）
3. 表数据量太大
4. 服务器资源不足（CPU、内存、IO）
5. 网络延迟

---

## 九、实战练习题

### 9.1 SQL 写法练习

准备数据：

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

**练习题**：

```sql
-- 1. 查询每个班级的平均分，并按平均分降序排列
SELECT c.name AS class_name, AVG(s.score) AS avg_score
FROM classes c
LEFT JOIN students s ON c.id = s.class_id
GROUP BY c.id
ORDER BY avg_score DESC;

-- 2. 查询每个班级中分数最高的学生
SELECT s.*
FROM students s
INNER JOIN (
    SELECT class_id, MAX(score) AS max_score
    FROM students
    GROUP BY class_id
) t ON s.class_id = t.class_id AND s.score = t.max_score;

-- 3. 查询分数高于平均分的学生
SELECT *
FROM students
WHERE score > (SELECT AVG(score) FROM students);

-- 4. 使用窗口函数查询每个班级的学生排名
SELECT
    name,
    class_id,
    score,
    RANK() OVER (PARTITION BY class_id ORDER BY score DESC) AS rank_in_class
FROM students;

-- 5. 查询连续三天都有登录记录的用户
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

### 9.2 实战场景

**场景：电商订单统计**

```sql
-- 1. 统计每天的订单数和销售额
SELECT
    DATE(created_at) AS order_date,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_sales
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY DATE(created_at)
ORDER BY order_date;

-- 2. 统计每个用户的首单时间和总消费
SELECT
    user_id,
    MIN(created_at) AS first_order_time,
    SUM(total_amount) AS total_spent,
    COUNT(*) AS order_count
FROM orders
GROUP BY user_id;

-- 3. 查询消费金额排名前 10 的用户
SELECT
    u.id,
    u.username,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY total_spent DESC
LIMIT 10;

-- 4. 统计商品销量排行（带月份维度）
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

## 十、总结

本文从 SQL 基础语法讲起，覆盖了以下核心知识点：

| 章节 | 核心内容 |
|------|----------|
| 基础入门 | 数据库/表操作、数据类型选择 |
| CRUD | INSERT、SELECT、UPDATE、DELETE |
| 多表查询 | JOIN 类型、子查询 |
| 高级特性 | 窗口函数、CTE |
| 索引 | B+ 树原理、索引失效、覆盖索引 |
| 事务 | ACID、隔离级别、MVCC、锁 |
| 优化 | EXPLAIN、慢查询、分页优化 |

**学习建议**：

1. **多写多练**：理论结合实践，在 [LeetCode SQL 题库](https://leetcode.cn/studyplan/sql-free-50/) 刷题
2. **理解原理**：不只会写 SQL，更要理解索引和事务原理
3. **关注性能**：养成用 EXPLAIN 分析的习惯

## 参考资料

- [MySQL 官方文档](https://dev.mysql.com/doc/refman/8.0/en/)
- [MySQL 索引详解 | JavaGuide](https://javaguide.cn/database/mysql/mysql-index.html)
- [MySQL 事务隔离级别详解 | JavaGuide](https://javaguide.cn/database/mysql/transaction-isolation-level.html)
- [高频 SQL 50 题 | LeetCode](https://leetcode.cn/studyplan/sql-free-50/)
- [MySQL 45 讲 | 极客时间](https://time.geekbang.org/column/intro/139)
