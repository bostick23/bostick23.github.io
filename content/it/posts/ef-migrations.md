---
date: "2024-11-01T12:05:12+01:00"
draft: false
title: "Ef Migrations"
---

In questa sezione sono illustrati comandi utili per gestire le migrations.

## Aggiungere una migration
Per aggiungere una migrations posizionarsi nella cartella dove è presente il file di solution e utilizzare il comando sottostante:

```powershell

dotnet ef migrations add <<MigrationName>> --context LogicWayContext -p LogicWay.Core -s LogicWay

```

E' importante specificare il flag -p per indicare il progetto in cui è presente il context e in cui creare il file di migration e anche il flag -s per speficare la solution, da cui il comando può capire quale sia il progetto di avvio contenente la connection string del database.


## Rimuovere una migration

Per rimuovere una migration bisogna utilizzare il comando sottostante specificando la migration alla quale si vuole tornare. Ad esempio se ho la migration m01 e m02 e volessi annullare quest'ultima, dovrei specificare m01 nel seguente comando:

```powershell

dotnet ef database update <<previous-migration>> --context contextName

```
