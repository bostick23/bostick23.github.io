---
date: '2026-05-13T13:59:42+02:00'
draft: true
title: 'Why a Proprietary Framework'
---
## Context
I work in a company which we realize product written in .NET framework. In 2022 our main products (LogicWay, MesWay and eWeb) was written with ASP.Net WebForms, a development environment that Microsoft claimed obsolete and has replaced it with ASP.Net Core. Despite similar name, these two frameworks haven't almost nothing in common. The WebForms language pattern is mutuated from 2000's .NET Form syntax in order to help desktop developers to start developing web pages. ASP.NET Core offers two different ways to create websites:
- Blazor pages: it use C# both from frontend than code behind development, translating C# into Javascript at runtime.
- Razor pages: frontend development is quite similar to WebForms structure with html markup mixed with ASP custom tags but it does large use of data binding.
The frameworks also introduce dependency injection and new version of entity framework: EF Core. In our WebForms project we dont'use EF for data access but direct sql queries with System.Data.SqlClient libray.
Then it's clear that it's impossibile to reuse our codebase: we need a fresh start.
## What market offers
My team is composed of fifteen people and all of them are .NET developers. So my first choice for a new framework was a .NET based Framework. 