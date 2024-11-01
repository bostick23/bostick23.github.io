---
date: "2024-11-01T12:08:10+01:00"
draft: true
title: "Sql Server Contare Tutte Le Righe Di Tutte Le Tabelle"
---

Questa query serve per contare tutte le righe di tutte le tabelle di un database

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
