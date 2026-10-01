---
title: "SQL Server: reimpostare IDENTITY con DBCC CHECKIDENT"
description: "Esempio di DBCC CHECKIDENT con RESEED per reimpostare il valore del contatore di una colonna IDENTITY in una tabella SQL Server."
date: "2024-11-01T12:08:35+01:00"
draft: false
---

Nel caso in cui una tabella abbia una colonna ID autoincrementale talvolta può essere opportuno resettare il suo valore di base (ad esempio in seguito ad una truncate table)

```sql
DBCC CHECKIDENT ('tableName', RESEED, 1)
```
