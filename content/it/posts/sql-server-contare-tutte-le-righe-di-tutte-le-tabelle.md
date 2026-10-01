---
title: "SQL Server: contare le righe di tutte le tabelle"
description: "Una query SQL Server con COUNT(*) e una tabella temporanea per elencare le tabelle del database ordinate per numero di righe."
date: "2024-11-01T12:08:10+01:00"
draft: false
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
