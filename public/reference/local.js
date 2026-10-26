// Compose an email locally; the visitor reviews and sends it in their email app.
document.addEventListener('submit', event => {
  if (!(event.target instanceof HTMLFormElement)) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  const values = [...new FormData(event.target).entries()].map(([key, value]) => `${key}: ${value}`).join('\n\n');
  const recipient = globalThis.__ajayProfile?.email;
  if (recipient) window.location.href = `mailto:${recipient}?subject=${encodeURIComponent('Portfolio enquiry for Ajaymon')}&body=${encodeURIComponent(values)}`;
  let notice = event.target.querySelector('[data-local-form-notice]');
  if (!notice) {
    notice = document.createElement('p');
    notice.dataset.localFormNotice = '';
    notice.setAttribute('role', 'status');
    notice.style.cssText = 'font:14px/1.5 sans-serif;color:#34463c;margin:16px 0 0;';
    event.target.append(notice);
  }
  notice.textContent = recipient ? 'Continue in your email app to review and send. If it did not open, email aj.design.mon@gmail.com directly.' : 'Email is not configured yet. Your message has not been sent.';
}, true);
