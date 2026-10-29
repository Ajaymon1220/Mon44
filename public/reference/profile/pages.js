(() => {
  const filters = document.querySelector('.filters');
  if (filters) {
    const cards = [...document.querySelectorAll('.work-projects [data-tags]')];
    filters.addEventListener('click', event => {
      const button = event.target.closest('[data-filter]');
      if (!button) return;
      const filter = button.dataset.filter;
      let count = 0;
      for (const card of cards) {
        card.hidden = filter !== 'all' && !card.dataset.tags.includes(filter);
        if (!card.hidden) count++;
      }
      for (const item of filters.querySelectorAll('button')) item.setAttribute('aria-pressed', String(item === button));
      document.querySelector('.filter-count').textContent = `${count} ${count === 1 ? 'project' : 'projects'}`;
    });
  }
  const form = document.querySelector('[data-contact-form]');
  if (form) form.addEventListener('submit', event => {
    event.preventDefault();
    const values = new FormData(form);
    const body = `${values.get('message')}\n\nFrom: ${values.get('name')}\nEmail: ${values.get('email')}`;
    const subject = `Portfolio enquiry from ${values.get('name')}`;
    window.location.href = `mailto:${form.dataset.recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    form.querySelector('.form-status').textContent = 'Your email draft is ready to open. If your email app did not launch, use the email address on this page. Your message has not been sent.';
  });
})();

// A labelled portfolio exploration, independent of the real payment product.
(() => {
  const demo = document.querySelector('[data-invoice-demo]');
  if (!demo) return;
  const customer = demo.querySelector('#demo-customer');
  const title = demo.querySelector('[data-preview-title]');
  const description = demo.querySelector('[data-preview-copy]');
  const status = demo.querySelector('[data-preview-status]');
  function update() {
    const kind = demo.querySelector('input[name="request-type"]:checked').value;
    demo.querySelector('[data-preview-customer]').textContent = customer.value.trim() || 'Customer name';
    demo.querySelector('[data-invoice-only]').hidden = kind === 'link';
    demo.querySelector('[data-schedule]').hidden = kind !== 'recurring';
    title.textContent = kind === 'link' ? 'Payment request' : kind === 'recurring' ? 'Recurring invoice' : 'Invoice';
    description.textContent = kind === 'link' ? 'Request payment for design services. No invoice document is included.' : kind === 'recurring' ? 'Design services, invoiced on a monthly schedule.' : 'One-time invoice for design services.';
    status.textContent = kind === 'link' ? 'Showing a payment request without invoice fields.' : kind === 'recurring' ? 'Showing a recurring invoice with a monthly schedule.' : 'Showing a one-time invoice preview.';
  }
  demo.addEventListener('change', update);
  customer.addEventListener('input', () => { demo.querySelector('[data-preview-customer]').textContent = customer.value.trim() || 'Customer name'; });
  update();
})();

// Optional, progressively enhanced guidance for the TaxOS visual story.
(() => {
  if (!document.body.classList.contains('taxos-case')) return;
  const chapters = [
    ['problem', 'The problem', 'Meet the people'],
    ['research', 'Meet the people', 'Explore the decisions'],
    ['decisions', 'Design decisions', 'See the prototype story'],
    ['prototype', 'The prototype', 'Follow the iteration'],
    ['iteration', 'The iteration', 'Explore the outcomes'],
    ['outcomes', 'The outcomes', 'Back to the beginning']
  ];
  const sections = chapters.map(([id]) => document.getElementById(id));
  const guide = document.querySelector('.story-guide');
  const next = guide.querySelector('[data-guide-next]');
  const previous = guide.querySelector('[data-guide-prev]');
  const start = document.querySelector('[data-guide-start]');
  let current = 0;
  let scheduled = false;
  function update() {
    scheduled = false;
    current = 0;
    sections.forEach((section, i) => {
      if (section.getBoundingClientRect().top <= window.innerHeight * .38) current = i;
    });
    guide.querySelector('[data-guide-count]').textContent = `0${current + 1} / 06`;
    guide.querySelector('[data-guide-title]').textContent = chapters[current][1];
    guide.querySelector('progress').value = current + 1;
    guide.querySelector('progress').textContent = `${current + 1} of 6`;
    previous.href = current ? `#${chapters[current - 1][0]}` : '#top';
    previous.setAttribute('aria-label', current ? `Previous: ${chapters[current - 1][1]}` : 'Back to the introduction');
    next.href = current === chapters.length - 1 ? '#top' : `#${chapters[current + 1][0]}`;
    next.textContent = `${chapters[current][2]} ${current === 5 ? '↑' : '→'}`;
    document.querySelectorAll('.chapter-nav a').forEach(link => {
      if (link.hash === `#${chapters[current][0]}`) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    });
  }
  function go(event) {
    const target = document.querySelector(event.currentTarget.hash);
    if (!target) return;
    event.preventDefault();
    const focusTarget = target.querySelector('h2') || target;
    focusTarget.setAttribute('tabindex', '-1');
    focusTarget.focus({preventScroll: true});
    target.scrollIntoView({behavior: 'instant', block: 'start'});
    history.replaceState(null, '', event.currentTarget.hash);
    update();
  }
  start.addEventListener('click', event => {
    guide.hidden = false;
    document.body.classList.add('story-guide-open');
    go(event);
  });
  [next, previous].forEach(link => link.addEventListener('click', go));
  document.querySelectorAll('.taxos-case .chapter-nav a').forEach(link => link.addEventListener('click', go));
  guide.querySelector('[data-guide-close]').addEventListener('click', () => {
    guide.hidden = true;
    document.body.classList.remove('story-guide-open');
    const heading = sections[current].querySelector('h2');
    heading.setAttribute('tabindex', '-1');
    heading.focus({preventScroll: true});
    start.textContent = 'Restart the story →';
  });
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  }, {passive: true});
  window.addEventListener('resize', update);
  update();

  const perspectives = {
    cpa: ['CPA perspective: focus on the dedicated workspace and assisted preparation.', ['01', '03']],
    client: ['Client perspective: focus on a simpler portal and relevant intake questions.', ['01', '02']],
    lead: ['Firm lead perspective: focus on a connected workflow and testing it with CPAs.', ['03', '04']]
  };
  document.querySelectorAll('[data-persona]').forEach(link => link.addEventListener('click', event => {
    const [copy, selected] = perspectives[link.dataset.persona];
    document.querySelectorAll('.persona-card').forEach(card => card.classList.toggle('persona-selected', card.contains(link)));
    document.querySelectorAll('[data-decision]').forEach(card => {
      const highlighted = selected.includes(card.dataset.decision);
      card.classList.toggle('decision-highlight', highlighted);
      const existing = card.querySelector('.perspective-tag');
      if (existing) existing.remove();
      if (highlighted) {
        const badge = document.createElement('span');
        badge.className = 'perspective-tag';
        badge.textContent = 'Relevant to this perspective';
        card.append(badge);
      }
    });
    const reading = document.querySelector('[data-persona-reading]');
    reading.hidden = false;
    reading.textContent = copy;
    go(event);
  }));
  const explorer = document.querySelector('.flow-explorer');
  if (!explorer) return;
  explorer.hidden = false;
  const stageNames = ['Collect', 'Organize', 'Prepare'];
  const lab = document.querySelector('.workflow-lab');
  const panels = [...document.querySelectorAll('[data-flow-panel]')];
  const play = explorer.querySelector('[data-flow-play]');
  const label = explorer.querySelector('[data-flow-play-label]');
  const timerBar = explorer.querySelector('[data-flow-timer]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const duration = 8000;
  let currentStep = 0;
  let elapsed = 0;
  let paused = reducedMotion.matches;
  let visible = false;
  let lastTick = performance.now();
  function playbackLabel() {
    play.textContent = paused ? 'Play ▶' : 'Pause ⏸';
    play.setAttribute('aria-label', paused ? 'Play animated walkthrough' : 'Pause animated walkthrough');
    label.textContent = paused ? 'Paused · explore each scene at your pace' : 'Auto-playing · next scene in ' + Math.max(1, Math.ceil((duration - elapsed) / 1000)) + 's';
  }
  function selectStep(step, announce = false) {
    currentStep = Number(step);
    elapsed = 0;
    timerBar.style.transform = 'scaleX(0)';
    explorer.querySelectorAll('[data-flow-step]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.flowStep) === currentStep)));
    panels.forEach(panel => { panel.hidden = Number(panel.dataset.flowPanel) !== currentStep; });
    // Automatic playback stays quiet for screen readers; manual choices are announced.
    if (announce) explorer.querySelector('[data-flow-copy]').textContent = `Step ${currentStep + 1} of 3: ${stageNames[currentStep]}. Showing the previous workflow and the TaxOS design.`;
    playbackLabel();
  }
  explorer.querySelectorAll('[data-flow-step]').forEach(button => button.addEventListener('click', () => {
    paused = true;
    selectStep(button.dataset.flowStep, true);
  }));
  play.addEventListener('click', () => {
    paused = !paused;
    lastTick = performance.now();
    playbackLabel();
  });
  reducedMotion.addEventListener('change', event => {
    if (event.matches) { paused = true; playbackLabel(); }
  });
  // Keep the first scene until the reader actually reaches the illustration.
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    lastTick = performance.now();
  }, {threshold: 0.15}).observe(lab);
  document.addEventListener('visibilitychange', () => { lastTick = performance.now(); });
  window.setInterval(() => {
    const now = performance.now();
    const delta = now - lastTick;
    lastTick = now;
    if (paused || !visible || document.hidden) return;
    elapsed += Math.min(delta, 250);
    if (elapsed >= duration) selectStep((currentStep + 1) % stageNames.length);
    timerBar.style.transform = `scaleX(${elapsed / duration})`;
    playbackLabel();
  }, 100);
  selectStep(0);
})();
