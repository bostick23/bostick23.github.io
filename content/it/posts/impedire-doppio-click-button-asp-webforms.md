---
title: "ASP.NET WebForms: prevenire il doppio clic su un pulsante"
description: "Un esempio con UseSubmitBehavior e JavaScript per gestire i clic ripetuti su un pulsante ASP.NET WebForms durante un’operazione."
date: "2024-11-01T11:59:00+01:00"
draft: false
---

Per prevenire il doppio click involontario di un Button in un progetto Asp.Net WebForms è necessario impostare il tag `UseSubmitBehavior="false"`:

```asp

<asp:Button runat="server" OnClick="Execute_Click" Text="Esegui"
    UseSubmitBehavior="false" OnClientClick="CheckDouble(this)"/>

```

e richiamare il seguente script Javascript:

```javascript
var submit = 0;
function CheckDouble(bt) {
  //alert(submit);
  if (submit > 0) {
    bt.disabled = true;
    alert(
      "Hai già cliccato il bottone. Attendi il completamento dell'operazione"
    );
    return false;
  }
  submit++;
  return true;
}
```
