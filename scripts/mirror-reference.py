"""Capture the public Visualfolio pages and their published visual runtime."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse, urljoin
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://visualfolio.framer.website'
PAGES = ['/', '/projects', '/contact', '/404', '/projects/voxera-ai', '/projects/socialo', '/projects/arconai', '/projects/creston-vale-law']
ASSETS = ROOT / 'public/reference/assets'
SOURCE = ROOT / 'src/reference'
ALLOWED = {'framerusercontent.com', 'fonts.gstatic.com'}
URLS = re.compile(r'https://(?:framerusercontent\.com|fonts\.gstatic\.com)/[^\s<>"\x27`\\)]+')
MODULES = re.compile(r'["\x27`]((?:\./|\.\./)[^"\x27`\s]+\.mjs)["\x27`]')
seen, failures, texts = set(), {}, {}

def normalized(url):
    return html.unescape(url).split('?')[0].split('#')[0]

def asset_path(url):
    p = urlparse(url)
    return ASSETS / p.netloc / p.path.lstrip('/')

def fetch(url):
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=50) as response:
            return response.read()
    except HTTPError as error:
        if error.code == 404 and url == ORIGIN + '/404':
            return error.read()
        raise

def collect(text, base):
    urls = {normalized(m) for m in URLS.findall(text)}
    urls.update(urljoin(base, m) for m in MODULES.findall(text))
    for relative, origin in re.findall(r'new URL\([`"\x27]([^`"\x27]+\.framercms)[`"\x27],[`"\x27](https://[^`"\x27]+)[`"\x27]\)', text):
        urls.add(urljoin(origin, relative).replace('/modules/', '/cms/'))
    return {u for u in urls if urlparse(u).netloc in ALLOWED and Path(urlparse(u).path).suffix.lower() in {'.mjs', '.js', '.css', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.svg', '.woff2', '.woff', '.ttf', '.mp4', '.webm', '.json', '.gif', '.framercms'}}

pending = set()
for route in PAGES:
    content = fetch(ORIGIN + route).decode()
    destination = SOURCE / ('index.html' if route == '/' else route.lstrip('/') + '/index.html')
    destination.parent.mkdir(parents=True, exist_ok=True)
    texts[destination] = content
    pending.update(collect(content, ORIGIN + route))
    print('Page:', route, flush=True)

while pending:
    batch, pending = pending - seen, set()
    seen.update(batch)
    with ThreadPoolExecutor(max_workers=10) as pool:
        jobs = {pool.submit(fetch, url): url for url in batch}
        for job in as_completed(jobs):
            url = jobs[job]
            try:
                data = job.result()
                destination = asset_path(url)
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.suffix in {'.mjs', '.js', '.css', '.svg', '.json'}:
                    content = data.decode()
                    texts[destination] = content
                    pending.update(collect(content, url) - seen)
                else:
                    destination.write_bytes(data)
            except Exception as error:
                failures[url] = str(error)
    print('Assets processed:', len(seen), 'Next:', len(pending), 'Failures:', len(failures), flush=True)

successful = seen - failures.keys()
for destination, content in texts.items():
    for url in sorted(successful, key=len, reverse=True):
        p = urlparse(url)
        content = content.replace(url, '/reference/assets/' + p.netloc + p.path)
    if destination.suffix == '.html':
        # Analytics and editor bootstrap are unrelated to the reproduced experience.
        content = re.sub(r'<script[^>]*src="https://events\.framer\.com/[^>]*></script>', '', content)
        content = re.sub(r'<script>try\{if\(localStorage\.getItem\("__framer_force_showing_editorbar_since"\).*?</script>', '', content, flags=re.S)
        content = content.replace('https://visualfolio.framer.website', '')
    if destination.suffix in {'.mjs', '.js'}:
        # CMS URL constructors require an absolute base, even on a local origin.
        content = re.sub(r'(new URL\(`[^`]+`,)`(/reference/[^`]+)`', r'\1`${location.origin}\2`', content)
    destination.write_text(content)

(SOURCE / 'manifest.json').write_text(json.dumps({'origin': ORIGIN, 'pages': PAGES, 'assets': len(successful), 'failed': failures}, indent=2))
print('Finished:', len(successful), 'assets.', flush=True)
if failures:
    print(json.dumps(failures, indent=2))
