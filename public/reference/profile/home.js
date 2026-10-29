(() => {
  'use strict';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  document.querySelector('#year').textContent = new Date().getFullYear();

  const workExplorer = document.querySelector('.work-explorer');
  if (workExplorer) {
    const tabs = [...workExplorer.querySelectorAll('[data-work-tab]')];
    const panels = [...workExplorer.querySelectorAll('.work-panel')];
    const tablist = workExplorer.querySelector('.work-tabs');
    const compactWork = window.matchMedia('(max-width: 700px)');
    tablist.setAttribute('role', 'tablist');
    const setOrientation = () => tablist.setAttribute('aria-orientation', compactWork.matches ? 'horizontal' : 'vertical');
    setOrientation();
    compactWork.addEventListener('change', setOrientation);
    function selectWork(index, moveFocus = false) {
      tabs.forEach((tab, i) => {
        const selected = i === index;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        panels[i].hidden = !selected;
      });
      workExplorer.querySelector('.work-position').textContent = `${String(index + 1).padStart(2, '0')} / ${String(tabs.length).padStart(2, '0')}`;
      if (moveFocus) tabs[index].focus();
    }
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[index].id);
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
      tab.addEventListener('click', () => selectWork(index));
      tab.addEventListener('keydown', event => {
        const nextKey = compactWork.matches ? 'ArrowRight' : 'ArrowDown';
        const previousKey = compactWork.matches ? 'ArrowLeft' : 'ArrowUp';
        let next;
        if (event.key === nextKey) next = (index + 1) % tabs.length;
        if (event.key === previousKey) next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); selectWork(next, true); }
      });
    });
    selectWork(0);
    workExplorer.querySelector('.work-picker').hidden = false;
    workExplorer.classList.add('is-ready');
  }

  // The page remains readable without JavaScript or IntersectionObserver.
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }, { threshold: 0.08 });
    for (const element of document.querySelectorAll('.reveal')) {
      element.classList.add('motion-ready');
      observer.observe(element);
    }
  }
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
  });

  const progress = document.querySelector('.reading-progress');
  let scrollFrame = 0;
  function updateProgress() {
    const range = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${range > 0 ? Math.min(1, Math.max(0, scrollY / range)) : 0})`;
    scrollFrame = 0;
  }
  addEventListener('scroll', () => { if (!scrollFrame) scrollFrame = requestAnimationFrame(updateProgress); }, { passive: true });
  addEventListener('resize', updateProgress);
  updateProgress();

  for (const card of document.querySelectorAll('.tilt')) {
    let frame = 0;
    card.addEventListener('pointermove', event => {
      if (!finePointer.matches || reducedMotion.matches || frame) return;
      const { clientX, clientY } = event;
      frame = requestAnimationFrame(() => {
        const box = card.getBoundingClientRect();
        card.style.setProperty('--tilt-x', `${-((clientY - box.top) / box.height - .5) * 5}deg`);
        card.style.setProperty('--tilt-y', `${((clientX - box.left) / box.width - .5) * 5}deg`);
        frame = 0;
      });
    });
    card.addEventListener('pointerleave', () => {
      cancelAnimationFrame(frame); frame = 0;
      card.style.setProperty('--tilt-x', '0deg'); card.style.setProperty('--tilt-y', '0deg');
    });
  }

  // The note's handle supports dragging and keyboard movement; reset is always available.
  const note = document.querySelector('.field-note');
  if (note) {
  const handle = note.querySelector('.note-handle');
  let noteX = 0, noteY = 0, drag = null;
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  function moveNote(x, y) {
    const box = note.getBoundingClientRect();
    const originLeft = box.left - noteX;
    const originRight = box.right - noteX;
    noteX = clamp(x, Math.max(-100, 12 - originLeft), Math.min(100, innerWidth - 12 - originRight));
    noteY = clamp(y, -90, 65);
    note.style.setProperty('--note-x', `${noteX}px`);
    note.style.setProperty('--note-y', `${noteY}px`);
  }
  handle.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    drag = { id: event.pointerId, x: event.clientX, y: event.clientY, startX: noteX, startY: noteY };
    note.classList.add('is-dragging');
    handle.setPointerCapture(event.pointerId);
  });
  handle.addEventListener('pointermove', event => {
    if (!drag || drag.id !== event.pointerId) return;
    moveNote(drag.startX + event.clientX - drag.x, drag.startY + event.clientY - drag.y);
  });
  for (const type of ['pointerup', 'pointercancel', 'lostpointercapture']) handle.addEventListener(type, () => { drag = null; note.classList.remove('is-dragging'); });
  function resetNote() { noteX = noteY = 0; note.style.setProperty('--note-x', '0px'); note.style.setProperty('--note-y', '0px'); }
  handle.addEventListener('keydown', event => {
    const directions = { ArrowLeft: [-10, 0], ArrowRight: [10, 0], ArrowUp: [0, -10], ArrowDown: [0, 10] };
    if (directions[event.key]) { event.preventDefault(); const [x, y] = directions[event.key]; moveNote(noteX + x, noteY + y); }
    if (event.key === 'Escape' || event.key === 'Home') { event.preventDefault(); resetNote(); }
  });
  document.querySelector('#reset-note').addEventListener('click', resetNote);
  addEventListener('resize', resetNote);
  }

  const dialog = document.querySelector('.image-dialog');
  for (const button of document.querySelectorAll('[data-image]')) button.addEventListener('click', () => {
    const img = dialog.querySelector('img');
    img.src = button.dataset.image; img.alt = `${button.dataset.title} — enlarged design detail`;
    document.querySelector('#image-title').textContent = button.dataset.title;
    dialog.showModal();
  });
  dialog.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const box = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
  });

  const copy = document.querySelector('.copy-email');
  copy?.addEventListener('click', async () => {
    const status = document.querySelector('.copy-status');
    try { await navigator.clipboard.writeText(copy.dataset.email); status.textContent = 'Email copied. Say hello whenever you like.'; }
    catch { status.textContent = `You can copy it here: ${copy.dataset.email}`; }
  });

  // Quiet synthesized ambience: opt-in only, no autoplay or external audio request.
  const sound = document.querySelector('#sound-toggle');
  if (sound) {
  const widget = document.querySelector('.sound-widget');
  let audio = null, playing = false;
  function soundState(next) {
    playing = next;
    sound.setAttribute('aria-pressed', String(next));
    sound.setAttribute('aria-label', next ? 'Pause ambient sound' : 'Play ambient sound');
    sound.textContent = next ? 'Ⅱ' : '▶';
    widget.classList.toggle('is-playing', next);
  }
  sound.addEventListener('click', async () => {
    sound.disabled = true;
    try {
      if (!audio) {
        const AudioEngine = window.AudioContext || window.webkitAudioContext;
        if (!AudioEngine) throw new Error('Audio unavailable');
        audio = new AudioEngine();
        const master = audio.createGain(); master.gain.value = .018; master.connect(audio.destination);
        for (const frequency of [130.81, 196, 261.63]) {
          const oscillator = audio.createOscillator(); oscillator.type = 'sine'; oscillator.frequency.value = frequency;
          oscillator.connect(master); oscillator.start();
        }
      }
      if (playing) { await audio.suspend(); soundState(false); }
      else { await audio.resume(); soundState(true); }
    } catch { widget.querySelector('.sound-caption').textContent = 'audio unavailable'; soundState(false); }
    finally { sound.disabled = false; }
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && audio && playing) { audio.suspend().catch(() => {}); soundState(false); }
  });
  addEventListener('pagehide', () => { if (audio) audio.suspend().catch(() => {}); soundState(false); });
  }
})();
