(() => {
  const profile = globalThis.__ajayProfile;
  if (!profile) return;
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  function enhance() {
    const intro = document.querySelector('[data-framer-name="Intro"]');
    if (intro && !document.querySelector('.ajay-experience')) {
      const section = document.createElement('section');
      section.className = 'ajay-experience';
      section.setAttribute('aria-labelledby', 'experience-title');
      section.innerHTML = `<div class="ajay-section-head"><h2 id="experience-title">The experience behind the work.</h2><a href="/reference/profile/AjaymonCV.pdf" target="_blank" rel="noopener">View résumé ↗</a></div><div class="ajay-timeline">${profile.experience.map(job => `<article class="ajay-job"><time>${escape(job.date)}</time><h3>${escape(job.company)}</h3><p class="role">${escape(job.role)}</p><p>${escape(job.description)}</p></article>`).join('')}</div><div class="ajay-toolkit" aria-label="Tools and skills">${['Figma','Framer','Webflow','Miro','Jira','Photoshop','Illustrator','Spline','Design systems','Usability testing','AI-assisted exploration'].map(tool => `<span>${tool}</span>`).join('')}</div><p class="ajay-education">B.E. Computer Science Engineering · MAMCET, Trichy · 2016–2020<br>UI/UX & Product Design · Skillto · Google Fundamentals of Digital Marketing</p>`;
      intro.insertAdjacentElement('afterend', section);
    }
    const reel = document.querySelector('[data-framer-name="Showreel Body"]');
    if (reel && !reel.querySelector('.ajay-ai-banner')) {
      const image = document.createElement('img');
      image.className = 'ajay-ai-banner';
      image.src = '/reference/profile/ai-design-banner.png';
      image.alt = 'Designing smarter experiences with AI — product design, emerging technology, user research and problem solving';
      image.width = 2056; image.height = 765;
      reel.append(image);
    }
    for (const form of document.querySelectorAll('form')) {
      if (!form.querySelector('.ajay-form-help')) {
        const help = document.createElement('p'); help.className = 'ajay-form-help';
        help.textContent = 'Opens your email app. You can review and send your message there.';
        form.append(help);
        const email = document.createElement('a'); email.className = 'ajay-contact-email';
        email.href = `mailto:${profile.email}`; email.textContent = profile.email;
        form.append(email);
      }
    }
  }
  let scheduled = false;
  const observer = new MutationObserver(() => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { scheduled = false; enhance(); });
  });
  observer.observe(document.body, { childList: true, subtree: true });
  enhance();
})();
