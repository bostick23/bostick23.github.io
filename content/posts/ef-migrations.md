---
date: "2024-11-01T12:05:12+01:00"
draft: true
title: "Ef Migrations"
---

In questa sezione sono illustrati comandi utili per gestire le migrations.

## Rimuovere una migration

Per rimuovere una migration bisogna utilizzare il comando sottostante specificando la migration alla quale si vuole tornare. Ad esempio se ho la migration m01 e m02 e volessi annullare quest'ultima, dovrei specificare m01 nel seguente comando:

```powershell

dotnet ef database update <<previous-migration>> --context contextName

```
