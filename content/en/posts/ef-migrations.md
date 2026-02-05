---
date: "2024-11-01T12:05:12+01:00"
draft: false
title: "EF Migrations"
---

This section illustrates useful commands for managing migrations.

## Adding a migration
To add a migration, navigate to the folder where the solution file is located and use the following command:

```powershell

dotnet ef migrations add <<MigrationName>> --context LogicWayContext -p LogicWay.Core -s LogicWay

```

It is important to specify the -p flag to indicate the project where the context is located and where to create the migration file, and also the -s flag to specify the solution, from which the command can determine which startup project contains the database connection string.


## Removing a migration

To remove a migration, you need to use the following command specifying the migration you want to revert to. For example, if I have migrations m01 and m02 and wanted to cancel the latter, I should specify m01 in the following command:

```powershell

dotnet ef database update <<previous-migration>> --context contextName

```
