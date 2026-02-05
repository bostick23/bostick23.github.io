---
date: "2024-11-01T12:06:50+01:00"
draft: false
title: "SQL Server effettuare backup database tramite query"
---

Per effettuare il backup di un database SQL Server utilizzando una query SQL bisogna utilizzare il seguente comando:

```sql
BACKUP DATABASE NomeDB TO DISK ='C:\DBSQLBACKUP\NomeDB.bak'
```
