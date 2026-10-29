"""Shared page frame for the authored portfolio."""
from html import escape as e
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / 'src/profile/profile.json').read_text())

def navigation(active=''):
    links = ''.join(f'<a href="{url}"'+(' aria-current="page"' if active == key else '')+f'>{label}</a>' for key, url, label in [('work','/projects','Work'),('about','/about','About')])
    return f'''<header class="navigation"><a class="signature sticker" href="/" aria-label="Ajaymon home">ajaymon</a><nav aria-label="Main navigation">{links}<a class="nav-cv" href="/reference/profile/AjaymonCV.pdf" target="_blank" rel="noopener">CV ↗</a><a class="button button-yellow" href="/contact"{' aria-current="page"' if active == 'contact' else ''}>Let's talk ↗</a></nav></header>'''

def footer():
    return f'''<footer><a href="#top">back to top ↑</a><a href="{e(PROFILE['linkedin'])}" target="_blank" rel="noopener">LinkedIn ↗</a><span>© {e(PROFILE['name'])} / <span id="year">2026</span></span></footer>'''

def dialog():
    return '<dialog class="image-dialog" aria-labelledby="image-title"><div class="dialog-bar"><h2 id="image-title">Design detail</h2><button type="button" class="close-dialog" aria-label="Close image">Close ×</button></div><img alt=""></dialog>'

def render(title, description, content, active='', page_class=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#19191b"><title>{e(title)} — Ajaymon</title><meta name="description" content="{e(description)}"><meta property="og:title" content="{e(title)} — Ajaymon"><meta property="og:description" content="{e(description)}"><meta property="og:image" content="/reference/profile/ai-design-banner.png"><link rel="preload" href="/reference/profile/fonts/geist.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/reference/profile/fonts/caveat.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/reference/profile/home.css"><link rel="stylesheet" href="/reference/profile/pages.css"><script src="/reference/profile/home.js" defer></script><script src="/reference/profile/pages.js" defer></script></head><body id="top" class="inner-page {e(page_class)}"><a class="skip-link" href="#main">Skip to content</a><div class="reading-progress" aria-hidden="true"></div>{navigation(active)}<main id="main" class="page">{content}{footer()}</main>{dialog()}</body></html>'''

def write_page(route, html):
    path = ROOT / 'src/reference' / route / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)

def contact_cta():
    return '''<section class="page-cta"><p class="eyebrow">[your next chapter]</p><h2 class="handwritten">Have something in mind?</h2><a class="button button-yellow" href="/contact">Let's talk ↗</a></section>'''

def project_card(project, i, heading='h3', filtering=False):
    cover = project.get('cover', f'/reference/profile/project-{project.get("image_index", i+1)}-0.png')
    attrs = f' data-tags="{e(project["tags"].lower())}"' if filtering else ''
    return f'''<article class="project evidence-card"{attrs}><a class="project-cover" href="/projects/{e(project['slug'])}" aria-label="Read {e(project['title'])}"><div class="project-paper"><img src="{e(cover)}" alt="{e(project['title'])} product interface" loading="lazy"></div><span class="open-project" aria-hidden="true">view case ↗</span></a><div class="project-description"><p class="project-index">0{i+1} / {e(project['tags'].split(' · ')[0])}</p><{heading}><a href="/projects/{e(project['slug'])}">{e(project['title'])}</a></{heading}><p class="project-problem">{e(project['problem'])}</p><p class="project-contribution"><span>My contribution</span>{e(project['contribution'])}</p><a class="case-link" href="/projects/{e(project['slug'])}">See the design decisions ↗</a></div></article>'''
