---
date: "2024-11-01T12:06:08+01:00"
draft: false
title: "Linux Manutenzione Dello Spazio Su Disco"
---

In questa sezione vengono illustrati i comandi per ottimizzare lo spazio su server Linux.

## Eliminare file con una certa estensione

Si può utilizzare il comando find specificando:

- directory in cui cercare (in maniera ricorsiva)
- il tag **-name** per filtrare l'estensione
- il tag **-delete** per lanciare la cancellazione dei file trovati

```bash
find /var/opt/docker -name *.bak -delete
```

## Trovare file con dimensione superiore a 1GB

Si può utilizzare il comando file specificando:

- directory in cui cercare (in maniera ricorsiva)
- il tag **-name** per filtrare l'estensione
- il tag **-size** per filtare solo i file con dimensione uguale o superiore a 1 GB
- il tag **-printf** per stampare nome del file e dimensione in KB

```bash
find /var/opt/docker -name '*.ldf' -size +1G -printf "%p %k KB\n"
```
