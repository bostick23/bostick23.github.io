---
title: "SQL Server: backup di un database con una query SQL"
description: "Esempio di BACKUP DATABASE in SQL Server per salvare un database in un file .bak, specificando il percorso di destinazione."
date: "2024-11-01T12:06:50+01:00"
draft: false
---

Per effettuare il backup di un database SQL Server utilizzando una query SQL bisogna utilizzare il seguente comando:

```sql
BACKUP DATABASE NomeDB TO DISK ='C:\DBSQLBACKUP\NomeDB.bak'
```
