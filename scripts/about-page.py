"""Generate the standalone About page from the shared profile."""
from pathlib import Path
import json
from html import escape
from portfolio_layout import render, write_page, contact_cta

root = Path(__file__).resolve().parents[1]
p = json.loads((root / 'src/profile/profile.json').read_text())
e = escape
# Small inline illustrations keep the story crisp at every screen size.
scenes = [
    ('MBRDI (EX)', 'First, I connected the dots.', 'Data taught me to look for patterns.', 'data', '<path d="M48 162L102 113L157 140L222 65L280 91" stroke="#9181c9" stroke-width="2" stroke-dasharray="5 7"/><path d="M48 192H286" stroke="#d4cce5"/><rect x="68" y="145" width="26" height="47" rx="7" fill="#d9d1ed"/><rect x="119" y="124" width="26" height="68" rx="7" fill="#b6a6dc"/><rect x="170" y="96" width="26" height="96" rx="7" fill="#9181c9"/><rect x="221" y="62" width="26" height="130" rx="7" fill="#6657aa"/><g fill="#fff" stroke="#6657aa" stroke-width="2"><circle cx="48" cy="162" r="6"/><circle cx="102" cy="113" r="6"/><circle cx="157" cy="140" r="6"/><circle cx="222" cy="65" r="6"/><circle cx="280" cy="91" r="6"/></g><path d="M260 38v16m-8-8h16" stroke="#b3a2d4" stroke-width="2"/>'),
    ('Skillto', 'Then, I listened to people.', 'Research turned patterns into perspective.', 'people', '<rect x="48" y="48" width="110" height="72" rx="20" fill="#fff" stroke="#c7bbdf" stroke-width="2"/><path d="M76 120v16l19-16" fill="#fff" stroke="#c7bbdf" stroke-width="2"/><path d="M71 71h62M71 84h46M71 97h30" stroke="#b6a6dc" stroke-width="4" stroke-linecap="round"/><rect x="180" y="76" width="104" height="61" rx="18" fill="#6657aa"/><path d="M254 135v15l-19-15" fill="#6657aa"/><path d="M213 106l10 9 19-21" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="109" cy="165" r="19" fill="#c6b5e2"/><path d="M71 218c0-45 76-45 76 0" fill="#9181c9"/><circle cx="228" cy="177" r="17" fill="#d5c8e9"/><path d="M195 218c0-36 66-36 66 0" fill="#6657aa"/>'),
    ('Karbon Business', 'Now, I make things simpler.', 'Clearer fintech experiences, from idea to launch.', 'product', '<rect x="45" y="50" width="246" height="162" rx="14" fill="#fff" stroke="#b9afd4" stroke-width="2"/><path d="M45 78h246" stroke="#ded8ea"/><g fill="#b7a9d5"><circle cx="61" cy="64" r="3"/><circle cx="72" cy="64" r="3"/><circle cx="83" cy="64" r="3"/></g><rect x="60" y="93" width="46" height="103" rx="7" fill="#eeeaf5"/><path d="M72 108h21m-21 14h15m-15 14h21" stroke="#b7a9d5" stroke-width="3" stroke-linecap="round"/><rect x="121" y="94" width="73" height="40" rx="7" fill="#e7e0f3"/><rect x="205" y="94" width="69" height="40" rx="7" fill="#f2eff8"/><path d="M131 182l33-20 33 10 32-25 34 7" fill="none" stroke="#9181c9" stroke-width="3" stroke-linecap="round"/><circle cx="270" cy="57" r="27" fill="#6657aa"/><path d="M258 57l8 8 16-18" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'),
]
job_by_company = {job['company']: job for job in p['experience']}
cards = []
for i, (company, title, caption, kind, drawing) in enumerate(scenes):
    job = job_by_company[company]
    cards.append(f'''<li class="story-frame story-{kind}"><div class="story-scene"><span class="story-step">0{i+1}</span><svg viewBox="0 0 336 256" aria-hidden="true" focusable="false"><circle cx="168" cy="128" r="100" fill="#eee9f6"/>{drawing}</svg></div><p class="story-date">{e(job['date'])}</p><h3>{e(title)}</h3><p class="story-caption">{e(caption)}</p><p class="story-company">{e(company)}<span>{e(job['role'])}</span></p></li>''')
jobs = ''.join(cards)
# Recolor the chapter illustrations to the shared graphite / yellow palette.
for old, new in {'#6657aa':'#b78309', '#9181c9':'#d4a52e', '#b6a6dc':'#d7c693', '#eee9f6':'#e6e2d8', '#c6b5e2':'#d6c492', '#c7bbdf':'#bcb7a9', '#d5c8e9':'#e0d7bc', '#b9afd4':'#bcb7a9', '#b7a9d5':'#b9af94', '#e7e0f3':'#e1d5b0', '#eeeaf5':'#ece8dc', '#f2eff8':'#eeece5', '#ded8ea':'#d1cbbc', '#d9d1ed':'#dfd7c0', '#d4cce5':'#bdb7a8', '#b3a2d4':'#a99b76'}.items():
    jobs = jobs.replace(old, new)
content = f'''<div class="section-rule"><span>[the person]</span><span>[behind the pixels]</span></div>
<section class="inside-mat about-intro" aria-labelledby="about-title"><div><p class="mat-label">BANGALORE, INDIA / PRODUCT DESIGNER</p><h1 id="about-title" class="sticker">Curious mind.<br>Human touch.</h1><p class="mat-caption handwritten">I'm Ajaymon. I make complex things<br>feel a little more human.</p><a class="button button-yellow" href="/reference/profile/AjaymonCV.pdf" target="_blank" rel="noopener">My résumé ↗</a></div><figure class="about-photo tilt"><img src="/reference/profile/ajaymon-portrait.png" alt="Ajaymon, product designer"><figcaption class="handwritten">the human behind the work.</figcaption><span class="photo-tape" aria-hidden="true"></span></figure></section>
<section class="visual-story" aria-labelledby="experience-title"><div class="section-rule"><span>[the journey]</span><span>[three chapters]</span></div><header class="story-heading"><h2 id="experience-title" class="handwritten">Data. People. Possibilities.</h2><p>Same curiosity. A different perspective.</p></header><ol class="story-frames">{jobs}</ol><div class="story-ending"><a href="/projects">See where it led ↗</a><a href="/reference/profile/AjaymonCV.pdf" target="_blank" rel="noopener">The full story, on paper ↗</a></div></section>{contact_cta()}'''
write_page('about', render('About me', 'The story behind Ajaymon’s work: from data engineering to thoughtful product design.', content, 'about', 'about-page'))
print('Generated /about with the shared design system.')
