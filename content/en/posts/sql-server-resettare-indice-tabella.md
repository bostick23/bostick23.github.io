---
date: "2024-11-01T12:08:35+01:00"
draft: false
title: "SQL Server Reset Table Index"
---

In case a table has an auto-incremental ID column, it may sometimes be appropriate to reset its base value (for example, after a truncate table).

```sql
DBCC CHECKIDENT ('tableName', RESEED, 1)
```
