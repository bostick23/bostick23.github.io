---
date: "2024-11-01T12:08:10+01:00"
draft: false
title: "SQL Server Count All Rows in All Tables"
---

This query is used to count all rows in all tables of a database.

```sql
CREATE TABLE #counts
(
    table_name varchar(255),
    row_count int
)

EXEC sp_MSForEachTable @command1='INSERT #counts (table_name, row_count) SELECT ''?'', COUNT(*) FROM ?'
SELECT table_name, row_count FROM #counts ORDER BY row_count DESC
DROP TABLE #counts
```
