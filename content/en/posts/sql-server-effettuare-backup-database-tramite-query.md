---
title: "SQL Server: back up a database with a SQL query"
description: "An example of BACKUP DATABASE in SQL Server to save a database to a .bak file at a specified destination path."
date: "2024-11-01T12:06:50+01:00"
draft: false
---

To backup a SQL Server database using a SQL query, you need to use the following command:

```sql
BACKUP DATABASE DatabaseName TO DISK ='C:\DBSQLBACKUP\DatabaseName.bak'
```
