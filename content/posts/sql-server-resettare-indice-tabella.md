---
date: "2024-11-01T12:08:35+01:00"
draft: true
title: "Sql Server Resettare Indice Tabella"
---

Nel caso in cui una tabella abbia una colonna ID autoincrementale talvolta può essere opportuno resettare il suo valore di base (ad esempio in seguito ad una truncate table)

```sql
DBCC CHECKIDENT ('tableName', RESEED, 1)
```
