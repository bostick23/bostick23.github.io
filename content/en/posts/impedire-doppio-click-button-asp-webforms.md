---
date: "2024-11-01T11:59:00+01:00"
draft: false
title: "Prevent Double Click Button ASP WebForms"
---

To prevent inadvertent double-clicking of a Button in an ASP.NET WebForms project, you need to set the `UseSubmitBehavior="false"` tag:

```asp

<asp:Button runat="server" OnClick="Execute_Click" Text="Execute"
    UseSubmitBehavior="false" OnClientClick="CheckDouble(this)"/>

```

and invoke the following JavaScript:

```javascript
var submit = 0;
function CheckDouble(bt) {
  //alert(submit);
  if (submit > 0) {
    bt.disabled = true;
    alert(
      "You have already clicked the button. Wait for the operation to complete"
    );
    return false;
  }
  submit++;
  return true;
}
```
