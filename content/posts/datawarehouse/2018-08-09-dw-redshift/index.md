+++
title = 'Amazon Redshift Performance Tuning: VACUUM, ANALYZE, and Operations Best Practices'
date = '2018-08-09T16:03:05+08:00'
description = 'A complete guide to Amazon Redshift performance optimization covering all 6 VACUUM types (FULL, DELETE ONLY, SORT ONLY, REINDEX, RECLUSTER, BOOST), ANALYZE statistics, table design best practices, and essential operations commands.'
toc = true
tags = ['Redshift', 'AWS', 'Data Warehouse', 'Performance Tuning', 'VACUUM']
categories = ['Data Warehouse']
keywords = ['Amazon Redshift', 'Redshift VACUUM', 'Redshift performance tuning', 'data warehouse maintenance', 'AWS data warehouse']
+++
![Amazon Redshift performance tuning guide](cover.webp)

**Amazon Redshift** is AWS's fully managed cloud data warehouse built on columnar storage and massively parallel processing (MPP) architecture. It can deliver sub-second query performance on petabyte-scale datasets. However, as data is continuously inserted and deleted, table performance gradually degrades -- and that's where VACUUM and ANALYZE come in.

This article covers Redshift's performance optimization strategies in depth, including all six VACUUM types, ANALYZE statistics updates, and practical commands for day-to-day operations.

<!--more-->

## Why VACUUM Matters

Two characteristics of Redshift's storage engine cause performance to degrade over time:

### Deletes Don't Free Space Immediately

When you run `DELETE` or `UPDATE`, Redshift **does not physically remove the data**. Instead, it marks those rows as "deleted." These ghost rows still consume disk space and may be scanned during queries.

### New Data Lands in an Unsorted Region

Rows inserted via `COPY`, `INSERT`, or `UPDATE` are appended to the **unsorted region** at the end of the table. If the table has a sort key defined but a large portion of data remains unsorted, range-restricted scans and merge joins become significantly less efficient.

> **Analogy**: Think of a dictionary where new words are dumped at the back without alphabetical ordering. Looking anything up becomes painfully slow.

---

## VACUUM Command Reference

VACUUM reclaims space and re-sorts data. Redshift offers **6 VACUUM types**, each designed for different scenarios.

![Data center server architecture](architecture.webp)

### VACUUM Type Comparison

| Type | What It Does | When to Use | Duration |
|------|-------------|-------------|----------|
| `FULL` | Sort + reclaim space | General maintenance (default) | Medium |
| `DELETE ONLY` | Reclaim space only | After heavy deletes | Fast |
| `SORT ONLY` | Sort only | After heavy inserts | Medium |
| `REINDEX` | Rebuild interleaved sort index | Interleaved sort key tables | Slowest |
| `RECLUSTER` | Sort unsorted region only | Incremental maintenance on large tables | Fast |
| `BOOST` | Use extra resources to speed up | Maintenance windows | Fast (resource-heavy) |

### 1. VACUUM FULL (Default)

Sorts data and reclaims space from deleted rows. This is the most commonly used maintenance command.

```sql
-- VACUUM a single table
VACUUM sales;

-- VACUUM the entire database (use with caution)
VACUUM;
```

**Threshold behavior**: By default, Redshift skips the sort phase when more than 95% of rows are already sorted. You can adjust this with the `TO threshold PERCENT` parameter:

```sql
-- Force a complete sort (never skip)
VACUUM sales TO 100 PERCENT;

-- Skip sorting if 75%+ is already sorted
VACUUM sales TO 75 PERCENT;
```

### 2. VACUUM DELETE ONLY

Reclaims space occupied by rows marked for deletion **without re-sorting**. Ideal for quickly freeing disk after bulk deletes.

```sql
VACUUM DELETE ONLY sales;
```

> **Note**: Redshift runs automatic DELETE ONLY operations in the background, but running it manually gives you faster space reclamation.

### 3. VACUUM SORT ONLY

Sorts unsorted rows **without reclaiming space**. Useful after bulk inserts to restore query performance.

```sql
VACUUM SORT ONLY sales;
```

### 4. VACUUM REINDEX

Designed for tables with **interleaved sort keys**. It re-analyzes the distribution of values in sort key columns, then performs a full VACUUM.

```sql
VACUUM REINDEX listing;
```

**Key considerations**:
- Takes significantly longer than VACUUM FULL
- Only meaningful for interleaved sort key tables
- Required after initial loads done with `INSERT` instead of `COPY` to properly initialize the index

### 5. VACUUM RECLUSTER

Sorts only the table's **unsorted region**, leaving the already-sorted portion untouched. Best for incremental maintenance on large tables.

```sql
VACUUM RECLUSTER listing;
```

**Advantages**:
- Much faster than FULL
- Scales well for large tables
- AWS recommends this for write-heavy workloads that primarily query recent data

### 6. VACUUM BOOST

Allocates extra system resources to speed up the VACUUM operation, but **blocks concurrent DELETE and UPDATE** statements.

```sql
-- Boost a RECLUSTER operation
VACUUM RECLUSTER listing BOOST;

-- Boost a FULL VACUUM
VACUUM FULL sales BOOST;
```

**Best practice**: Only use BOOST during maintenance windows or off-peak hours.

---

## VACUUM Execution Strategy

### 1. Choosing the Right VACUUM Type

```
               ┌─────────────────────────────────────┐
               │       Table needs maintenance        │
               └──────────────┬──────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        After heavy      After heavy    Interleaved
         deletes          inserts       sort key table
              │               │               │
              ▼               ▼               ▼
        DELETE ONLY      SORT ONLY        REINDEX
              │               │               │
              └───────┬───────┘               │
                      ▼                       │
              Need both?                      │
                      │                       │
                      ▼                       │
                    FULL ◄────────────────────┘
```

### 2. Determining Whether VACUUM Is Needed

Query the `SVV_TABLE_INFO` view to check sort and space usage status:

```sql
SELECT
    "table",
    size AS size_mb,
    pct_used,
    tbl_rows,
    unsorted,
    vacuum_sort_benefit
FROM SVV_TABLE_INFO
WHERE unsorted > 5  -- More than 5% unsorted
ORDER BY size_mb DESC;
```

**Key metrics to watch**:
- `unsorted`: Percentage of unsorted rows
- `vacuum_sort_benefit`: Estimated performance gain from running VACUUM
- `pct_used`: Disk utilization

### 3. Monitoring VACUUM Progress

While VACUUM is running, check the estimated time remaining:

```sql
SELECT * FROM SVV_VACUUM_PROGRESS;
```

After VACUUM completes, review the results:

```sql
SELECT
    table_name,
    elapsed_time/1000000 AS elapsed_seconds,
    sort_partitions,
    row_delta,
    block_delta
FROM SVV_VACUUM_SUMMARY
ORDER BY xid DESC
LIMIT 10;
```

Check the space reclamation ratio:

```sql
SELECT * FROM SVL_VACUUM_PERCENTAGE ORDER BY xid DESC;
```

---

## ANALYZE: Keeping Statistics Up to Date

The ANALYZE command updates table statistics metadata so the query optimizer can generate more accurate execution plans.

### When to Run ANALYZE

- After heavy INSERT, UPDATE, or DELETE operations
- After completing a VACUUM
- When the `stats_off` metric exceeds 10%

```sql
-- Analyze a single table
ANALYZE sales;

-- Analyze the entire database
ANALYZE;

-- Only update statistics for predicate columns
ANALYZE PREDICATE COLUMNS sales;
```

### Checking for Stale Statistics

```sql
SELECT
    "table",
    stats_off
FROM SVV_TABLE_INFO
WHERE stats_off > 10
ORDER BY stats_off DESC;
```

> **Note**: The `COPY` command automatically runs ANALYZE after loading into an empty table, so no manual action is needed in that case.

---

## Table Design Best Practices

Good table design dramatically reduces both the frequency and duration of VACUUM operations.

### 1. Choosing the Right Sort Key

| Sort Key Type | Best For | VACUUM Strategy |
|--------------|----------|-----------------|
| Compound sort key | Range queries, time series | VACUUM FULL |
| Interleaved sort key | Multi-column equality filters | VACUUM REINDEX |
| No sort key | Full table scans | VACUUM DELETE ONLY |

**Recommendation**: Use a date/timestamp column as the leading sort key and load data in chronological order. This minimizes the need for re-sorting.

### 2. Loading Data in Sort Key Order

Redshift automatically places new data into the sorted region when using `COPY`, provided all of these conditions are met:

- The table uses a **compound sort key** with a single column
- The sort column is defined as `NOT NULL`
- The table is either empty or 100% sorted
- All new sort key values are greater than the existing maximum

### 3. Splitting Large Tables into Time-Series Tables

For very large tables, partitioning by time offers several benefits:
- Reduces per-table VACUUM duration
- Makes it easy to drop historical data (just `DROP TABLE` the old partition)
- Improves query pruning efficiency

```sql
-- Monthly partitioning example
CREATE TABLE sales_2024_01 (LIKE sales);
CREATE TABLE sales_2024_02 (LIKE sales);
-- ...
```

### 4. Deep Copy as a VACUUM Alternative

For large tables, a **deep copy** can be faster than VACUUM:

```sql
-- 1. Create a new empty table with the same structure
CREATE TABLE sales_new (LIKE sales);

-- 2. Insert all data (automatically sorted on load)
INSERT INTO sales_new SELECT * FROM sales;

-- 3. Swap the tables
ALTER TABLE sales RENAME TO sales_old;
ALTER TABLE sales_new RENAME TO sales;

-- 4. Drop the old table
DROP TABLE sales_old;
```

**Caveat**: No concurrent writes are allowed during a deep copy.

---

## Essential Operations Commands

### Table Information

```sql
-- View detailed info for all tables
SELECT
    "table",
    size AS size_mb,
    pct_used,
    tbl_rows,
    encoded,
    diststyle,
    sortkey_num,
    sortkey1,
    unsorted,
    stats_off
FROM SVV_TABLE_INFO
ORDER BY size_mb DESC;
```

### Compression Analysis

```sql
-- Analyze optimal compression encoding for a table
ANALYZE COMPRESSION sales;
```

### Error Troubleshooting

```sql
-- View COPY load errors
SELECT * FROM STL_LOAD_ERRORS ORDER BY starttime DESC LIMIT 20;

-- View query execution errors
SELECT * FROM STL_ERROR ORDER BY recordtime DESC LIMIT 20;
```

### Query Performance Analysis

```sql
-- Find recent slow queries
SELECT
    query,
    substring(querytxt, 1, 100) AS query_text,
    elapsed/1000000 AS elapsed_seconds,
    queue_time/1000000 AS queue_seconds
FROM STL_QUERY
WHERE elapsed > 60000000  -- Over 60 seconds
ORDER BY endtime DESC
LIMIT 20;
```

---

## Automated Maintenance with Analyze Vacuum Utility

AWS provides an open-source [Analyze Vacuum Utility](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/AnalyzeVacuumUtility) that automatically identifies tables needing maintenance and runs VACUUM and ANALYZE accordingly.

### Key Features

- Automatically decides based on `unsorted`, `stats_off`, and table size
- Supports per-schema or per-table execution
- Produces detailed execution logs

### Basic Usage

```bash
python analyze-vacuum-schema.py \
    --db mydb \
    --db-user admin \
    --db-host mycluster.xxx.redshift.amazonaws.com \
    --schema-name public \
    --vacuum-flag true \
    --analyze-flag true
```

---

## Summary

Effective Redshift performance tuning boils down to understanding how data is stored and establishing a sensible maintenance routine:

1. **Run VACUUM regularly** -- reclaim space, maintain sort order, and pick the right VACUUM type for each situation
2. **Run ANALYZE promptly** -- keep statistics fresh so the optimizer can build efficient execution plans
3. **Design tables thoughtfully** -- choose appropriate sort keys and distribution keys, and load data in sort order
4. **Monitor key metrics** -- track `unsorted`, `stats_off`, and `vacuum_sort_benefit`
5. **Automate with tooling** -- use the Analyze Vacuum Utility to take the manual work out of maintenance

With these practices in place, your Redshift cluster will consistently deliver the performance you expect.

---

## Related Reading

- [AWS CLI Complete Guide: Installation, Configuration, and Command Reference](/posts/linux/2020-07-04-aws-cli/) - AWS command-line tool tutorial

## References

- [Amazon Redshift VACUUM Command Documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_VACUUM_command.html)
- [Redshift Data Warehouse Architecture](https://docs.aws.amazon.com/redshift/latest/dg/c_high_level_system_architecture.html)
- [SVV_TABLE_INFO System View](https://docs.aws.amazon.com/redshift/latest/dg/r_SVV_TABLE_INFO.html)
- [Redshift Analyze Vacuum Utility - GitHub](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/AnalyzeVacuumUtility)
