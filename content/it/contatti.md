---
title: "Contatti"
description: "Scrivimi un messaggio"
hideMeta: true
disableShare: true
ShowBreadCrumbs: false
---

Hai una domanda, un suggerimento o vuoi semplicemente metterti in contatto? Compila il modulo qui sotto e ti risponderò il prima possibile.

{{< rawhtml >}}
<form id="contact-form" action="https://api.web3forms.com/submit" method="POST" class="contact-form">

  <!-- Web3Forms access key -->
  <input type="hidden" name="access_key" value="163b1ebc-9945-4623-8e19-ce903766d321">

  <!-- Honeypot anti-spam -->
  <input type="checkbox" name="botcheck" class="hidden" style="display: none;">

  <!-- Subject prefix per le email ricevute -->
  <input type="hidden" name="subject" value="Nuovo messaggio dal sito web">
  <input type="hidden" name="from_name" value="Sito Web - Contatti">

  <div class="contact-field">
    <label for="name">Nome *</label>
    <input type="text" id="name" name="name" placeholder="Il tuo nome" required minlength="2">
  </div>

  <div class="contact-field">
    <label for="email">Email *</label>
    <input type="email" id="email" name="email" placeholder="La tua email" required>
  </div>

  <div class="contact-field">
    <label for="user-subject">Oggetto</label>
    <input type="text" id="user-subject" name="Oggetto" placeholder="Oggetto del messaggio">
  </div>

  <div class="contact-field">
    <label for="message">Messaggio *</label>
    <textarea id="message" name="message" rows="6" placeholder="Scrivi il tuo messaggio..." required minlength="10"></textarea>
  </div>

  <!-- hCaptcha integrato con Web3Forms -->
  <div class="h-captcha" data-captcha="true"></div>

  <button type="submit" class="contact-submit-btn">
    <span class="btn-text">Invia messaggio</span>
    <span class="btn-loading" style="display:none;">Invio in corso...</span>
  </button>

  <div id="contact-result" class="contact-result"></div>
</form>

<script src="https://web3forms.com/client/script.js" async defer></script>

<script>
const form = document.getElementById('contact-form');
const result = document.getElementById('contact-result');

form.addEventListener('submit', function(e) {
  e.preventDefault();

  const btn = form.querySelector('.contact-submit-btn');
  const btnText = btn.querySelector('.btn-text');
  const btnLoading = btn.querySelector('.btn-loading');

  btnText.style.display = 'none';
  btnLoading.style.display = 'inline';
  btn.disabled = true;
  result.innerHTML = '';
  result.className = 'contact-result';

  const formData = new FormData(form);

  fetch('https://api.web3forms.com/submit', {
    method: 'POST',
    body: formData
  })
  .then(async (response) => {
    const json = await response.json();
    if (response.status === 200) {
      result.innerHTML = 'Messaggio inviato con successo! Ti risponderò il prima possibile.';
      result.className = 'contact-result success';
      form.reset();
    } else {
      result.innerHTML = 'Si è verificato un errore. Riprova più tardi.';
      result.className = 'contact-result error';
    }
  })
  .catch(() => {
    result.innerHTML = 'Si è verificato un errore di connessione. Riprova più tardi.';
    result.className = 'contact-result error';
  })
  .finally(() => {
    btnText.style.display = 'inline';
    btnLoading.style.display = 'none';
    btn.disabled = false;
  });
});
</script>
{{< /rawhtml >}}
