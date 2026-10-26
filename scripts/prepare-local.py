"""Small, reproducible adaptations to the preserved published runtime."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'public/reference/assets'
spinner = ASSETS / 'framerusercontent.com/images/pGiXYozQ3mE4cilNOItfe2L2fUA.svg'
spinner.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M17 10a7 7 0 1 1-7-7" fill="none" stroke="black" stroke-width="2" stroke-linecap="round"/></svg>')

for path in ASSETS.rglob('*.mjs'):
    text = path.read_text()
    for photo in [1060, 1036, 250, 452, 1015]:
        text = text.replace(f'https://picsum.photos/id/{photo}/900/1100', f'/reference/photos/{photo}.jpg')
    text = text.replace('https://framerusercontent.com/images/pGiXYozQ3mE4cilNOItfe2L2fUA.svg', '/reference/assets/framerusercontent.com/images/pGiXYozQ3mE4cilNOItfe2L2fUA.svg')
    text = re.sub(r'https://api\.framer\.com/forms/v1/forms/[^`"\s]+/submit', '/__contact-not-configured', text)
    text = text.replace('EditorBar:s===void 0?void 0:', 'EditorBar:true?void 0:')
    if path.name.startswith('shared-lib.'):
        # Framer's CDN implements a custom ?range= endpoint. Static hosts do not.
        # Fetch the complete local binary and extract the same byte ranges here.
        text = text.replace('a.searchParams.set(`range`,o);let s=await bn(a)', 'let s=await bn(a)')
        text = text.replace('let c=await s.arrayBuffer(),l=new Uint8Array(c);if(l.length!==i)', 'let c=await s.arrayBuffer(),fullBytes=new Uint8Array(c),l=new Uint8Array(i),sliceOffset=0;for(let part of n){if(part.to>fullBytes.length)throw Error(`Incomplete local CMS data`);l.set(fullBytes.subarray(part.from,part.to),sliceOffset);sliceOffset+=part.to-part.from}if(l.length!==i)')
    if path.name.startswith('shared-lib.'):
        text = text.replace('return e.textDecoder.decode(n)}', 'return e.textDecoder.decode(n).replaceAll(`https://framerusercontent.com/images/`,`/reference/assets/framerusercontent.com/images/`)}')
    path.write_text(text)

for path in (ROOT / 'src/reference').rglob('*.html'):
    text = path.read_text()
    if '/reference/local.js' not in text:
        text = text.replace('<head>', '<head><script src="/reference/local.js"></script>')
    path.write_text(text)
print('Prepared local CMS reads, carousel photos, spinner fallback, and preview form behavior.')
