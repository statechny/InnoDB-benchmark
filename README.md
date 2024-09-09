# Benchmark Report: MySQL InnoDB Indexing Performance

## 1. Introduction

The goal of this benchmark is to evaluate the performance impact of different indexing strategies on query execution times in MySQL. We tested three scenarios:
1. Query without an index.
2. Query with a `BTREE` index on the `date_of_birth` column.
3. Simulated query with a `HASH`-like index using the `MD5` hash of `date_of_birth`.

The benchmark helps us understand how indexing can improve data retrieval efficiency on large datasets.

---

## 2. Environment Setup

- **MySQL**: Version 8.0
- **Node.js**: Version 20.x
- **Python**: Version 3.12
- **Hardware**:
    - CPU: Apple M1
    - RAM: 16GB
    - Disk: SSD

### Database:

- `users` table with 4 000 000 rows.
- The `date_of_birth` column is a `DATE` field used in the benchmark tests.
- The `dob_hash` column (added for the `HASH` simulation) contains the `MD5` hash of the `date_of_birth`.

---

## 3. Test Cases

### 3.1. No Index:
A full table scan is performed to find users born on a specific date (`1990-01-01`).

```sql
SELECT * FROM users WHERE date_of_birth = '1990-01-01';
```

### 3.2. BTREE Index:
A BTREE index is created on the date_of_birth column to allow efficient searching of date ranges.

```sql
CREATE INDEX idx_dob_btree ON users(date_of_birth);
SELECT * FROM users WHERE date_of_birth = '1990-01-01';
```

### 3.3. HASH Index Simulation:
A new dob_hash column was added, which stores the MD5 hash of the date_of_birth. The query is performed against this hashed value.

```sql
SELECT * FROM users WHERE dob_hash = MD5('1990-01-01');
```

## 4. Results
The results of the tests are shown below:


| Test        | Execution Time (s) | Rows Returned |
|-------------|-------------------:|--------------:|
| No Index    | 4.126              | 175           |
| BTREE Index | 0.005              | 175           |
| Hash Index  | 1.589              | 175           |