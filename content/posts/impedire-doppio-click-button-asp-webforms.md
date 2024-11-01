---
date: "2024-11-01T11:59:00+01:00"
draft: false
title: "Impedire Doppio Click Button Asp Webforms"
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
