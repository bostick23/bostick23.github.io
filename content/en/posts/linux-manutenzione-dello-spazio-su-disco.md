---
date: "2024-11-01T12:06:08+01:00"
draft: false
title: "Linux Disk Space Maintenance"
---

This section illustrates commands for optimizing space on Linux servers.

## Delete files with a certain extension

You can use the find command specifying:

- directory to search (recursively)
- the **-name** tag to filter by extension
- the **-delete** tag to launch deletion of found files

```bash
find /var/opt/docker -name *.bak -delete
```

## Find files larger than 1GB

You can use the find command specifying:

- directory to search (recursively)
- the **-name** tag to filter by extension
- the **-size** tag to filter only files with size equal to or greater than 1 GB
- the **-printf** tag to print filename and size in KB

```bash
find /var/opt/docker -name '*.ldf' -size +1G -printf "%p %k KB\n"
```
