(() => {
  const profile = globalThis.__ajayProfile;
  if (!profile) return;
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const filters = ['All', 'Fintech', 'Design systems', 'Research', 'Web design'];
  function workPage(content) {
    const projects = profile.projects;
    const work = document.createElement('section');
    work.className = 'ajay-work';
    work.setAttribute('aria-labelledby', 'work-title');
    work.innerHTML = `<header class="ajay-work-head"><p class="ajay-eyebrow">Selected work · 2023–2026</p><h1 id="work-title">Thoughtful design for complex products.</h1><div class="ajay-work-intro"><p>Case studies from fintech dashboards, banking operations tools, responsive websites and the design system that ties them together.</p><dl class="ajay-stats"><div><dt>Case studies</dt><dd>${projects.length}</dd></div><div><dt>Focus</dt><dd>Fintech</dd></div><div><dt>Based in</dt><dd>${escape(profile.location.split(',')[0])}</dd></div></dl></div></header><div class="ajay-work-bar"><div class="ajay-filters" role="group" aria-label="Filter projects">${filters.map((name, i) => `<button type="button" data-filter="${name}" aria-pressed="${i === 0}">${name}</button>`).join('')}</div><p class="ajay-work-count" aria-live="polite"></p></div><ol class="ajay-work-list">${projects.map((project, i) => `<li class="ajay-case" data-tags="${escape(project.tags)}"><a href="./projects/${escape(project.slug)}"><figure class="ajay-case-cover"><img src="/reference/profile/project-${i + 1}-0.png" alt="${escape(project.title)} interface" loading="${i ? 'lazy' : 'eager'}" decoding="async"></figure><div class="ajay-case-body"><p class="ajay-case-meta"><span>${String(i + 1).padStart(2, '0')}</span><span>${escape(project.year)}</span></p><h2>${escape(project.title)}</h2><p class="ajay-case-summary">${escape(project.summary)}</p><dl class="ajay-case-facts"><div><dt>Role</dt><dd>${escape(project.role)}</dd></div></dl><ul class="ajay-case-tags">${project.tags.split(' · ').map(tag => `<li>${escape(tag)}</li>`).join('')}</ul><span class="ajay-case-link">Read case study <span aria-hidden="true">→</span></span></div></a></li>`).join('')}</ol><aside class="ajay-work-cta"><p>Want the full picture of how I work?</p><div><a href="/reference/profile/AjaymonCV.pdf" target="_blank" rel="noopener">Download résumé ↗</a><a href="./contact">Start a conversation</a></div></aside>`;
    const count = work.querySelector('.ajay-work-count');
    const cases = [...work.querySelectorAll('.ajay-case')];
    function apply(filter) {
      let shown = 0;
      for (const item of cases) {
        const match = filter === 'All' || item.dataset.tags.toLowerCase().includes(filter.toLowerCase());
        item.hidden = !match;
        if (match) shown++;
      }
      count.textContent = `${shown} of ${cases.length} projects`;
      for (const button of work.querySelectorAll('[data-filter]')) button.setAttribute('aria-pressed', button.dataset.filter === filter);
    }
    work.querySelector('.ajay-filters').addEventListener('click', event => {
      const button = event.target.closest('[data-filter]');
      if (button) apply(button.dataset.filter);
    });
    apply('All');
    content.prepend(work);
    document.documentElement.classList.add('ajay-work-page');
  }
  function enhance() {
    for (const link of document.querySelectorAll('[data-framer-name="About Link"]')) {
      if (link.getAttribute("href") !== "/about") link.setAttribute("href", "/about");
    }
    const projectsBar = document.querySelector('[data-framer-name="Projects Bar"]');
    if (projectsBar && !document.querySelector('.ajay-work')) workPage(projectsBar.parentElement);
    const services = document.getElementById('services');
    if (services && !document.querySelector('.ajay-experience')) {
      const section = document.createElement('section');
      section.className = 'ajay-experience';
      section.id = 'experience';
      section.setAttribute('aria-labelledby', 'experience-title');
      const tools = ['Figma', 'Framer', 'Webflow', 'Miro', 'Jira', 'Photoshop', 'Illustrator', 'Spline'];
      const practice = ['Design systems', 'Usability testing', 'Prototyping', 'Design QA', 'AI-assisted exploration'];
      const education = [['B.E. Computer Science Engineering', 'MAMCET, Trichy', '2016–2020'], ['UI/UX & Product Design', 'Skillto', 'Course'], ['Fundamentals of Digital Marketing', 'Google', 'Certificate']];
      const chips = list => `<ul class="ajay-chips">${list.map(item => `<li>${escape(item)}</li>`).join('')}</ul>`;
      section.innerHTML = `<div class="ajay-xp-bar"><p>Experience</p><a href="/reference/profile/AjaymonCV.pdf" target="_blank" rel="noopener">View résumé <span aria-hidden="true">↗</span></a></div><header class="ajay-xp-head"><h2 id="experience-title">The experience behind the work.</h2><div><p>From data engineering to fintech product design: an analytical foundation, applied to making complex workflows feel simple.</p><dl class="ajay-stats"><div><dt>Roles</dt><dd>${profile.experience.length}</dd></div><div><dt>Industry</dt><dd>Fintech</dd></div><div><dt>Background</dt><dd>Data</dd></div></dl></div></header><ol class="ajay-timeline">${profile.experience.map(job => `<li class="ajay-job${/present/i.test(job.date) ? ' is-current' : ''}"><div class="ajay-job-when"><time>${escape(job.date)}</time>${/present/i.test(job.date) ? '<span class="ajay-now">Now</span>' : ''}</div><div class="ajay-job-who"><h3>${escape(job.company)}</h3><p class="role">${escape(job.role)}</p></div><p class="ajay-job-what">${escape(job.description)}</p></li>`).join('')}</ol><div class="ajay-xp-foot"><section aria-labelledby="toolkit-title"><h3 id="toolkit-title">Toolkit</h3><p class="ajay-xp-label">Tools</p>${chips(tools)}<p class="ajay-xp-label">Practice</p>${chips(practice)}</section><section aria-labelledby="education-title"><h3 id="education-title">Education</h3><ul class="ajay-edu">${education.map(([what, where, when]) => `<li><div><p>${escape(what)}</p><p>${escape(where)}</p></div><span>${escape(when)}</span></li>`).join('')}</ul></section></div>`;
      services.insertAdjacentElement('afterend', section);
    }
    const reel = document.querySelector('[data-framer-name="Designing with AI Body"]');
    if (reel && !reel.querySelector('.ajay-ai-banner')) {
      const image = document.createElement('img');
      image.className = 'ajay-ai-banner';
      image.src = '/reference/profile/ai-design-banner.png';
      image.alt = 'Designing smarter experiences with AI — product design, emerging technology, user research and problem solving';
      image.width = 2056; image.height = 765;
      reel.append(image);
    }
    for (const card of document.querySelectorAll('#work [data-framer-name="Project Card"]')) {
      const text = card.querySelector('[data-framer-name="Text"]');
      const project = profile.projects.find(item => card.getAttribute('href')?.endsWith(`/${item.slug}`));
      if (!text || !project || text.querySelector('.ajay-card-meta')) continue;
      const meta = document.createElement('p');
      meta.className = 'ajay-card-meta';
      meta.textContent = `${project.year} · ${project.tags.split(' · ').slice(0, 2).join(' · ')}`;
      text.prepend(meta);
    }
    if (services && !services.querySelector('.ajay-services')) {
      const icons = {
        product: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 9v11"/>',
        ux: '<path d="M5 3l14 7-6 2-2 6z"/>',
        systems: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M17.5 14v7M14 17.5h7"/>',
        delivery: '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>'
      };
      const items = [
        ['product', 'Product design', 'End-to-end experiences for web and mobile, from customer dashboards to complex fintech workflows.'],
        ['ux', 'UX & interaction', 'User research, usability testing and interactive prototypes that turn real feedback into clearer product decisions.'],
        ['systems', 'Design systems', 'Scalable Figma components, tokens and interface patterns that keep design and development aligned as a product grows.'],
        ['delivery', 'Design to delivery', 'Developer handoff, design QA and close collaboration with product and engineering to carry the design through to implementation.']
      ];
      const block = document.createElement('section');
      block.className = 'ajay-services';
      block.setAttribute('aria-labelledby', 'services-title');
      block.innerHTML = `<header class="ajay-svc-head"><p class="ajay-svc-eyebrow">What I do</p><h2 id="services-title">From first research to <em>shipped product.</em></h2><p class="ajay-svc-intro">I stay with a feature from discovery through design QA, so what ships matches what was designed.</p></header><ol class="ajay-svc-grid">${items.map(([icon, title, body], i) => `<li class="ajay-svc"><div class="ajay-svc-top"><span class="ajay-svc-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${icons[icon]}</svg></span><span class="ajay-svc-num">${String(i + 1).padStart(2, '0')}</span></div><h3>${escape(title)}</h3><p>${escape(body)}</p></li>`).join('')}</ol>`;
      services.append(block);
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
