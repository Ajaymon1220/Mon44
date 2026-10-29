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

// Authored Home and About pages load outside the captured Framer router.
document.addEventListener('click', event => {
  const link = event.target.closest?.('a[href]');
  if (!link || link.hasAttribute('download')) return;
  if (link.matches('[data-framer-name="About Link"]')) link.setAttribute('href', '/about');
  const destination = new URL(link.href, location.href);
  if (destination.origin !== location.origin) return;
  if (destination.pathname !== '/' && !/^\/about\/?$/.test(destination.pathname)) return;
  event.stopImmediatePropagation();
  if (event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey && (!link.target || link.target === '_self')) {
    event.preventDefault();
    window.location.assign(destination.href);
  }
}, true);
