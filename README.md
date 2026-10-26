# Ajaymon portfolio

Personalized portfolio using the Visualfolio layout and its published Framer/React motion runtime. This is a local static website, not a Framer editor project.

## Run

```sh
npm run dev
```

Open http://127.0.0.1:5173. Node.js 22.12+ is required; the static server needs no package installation.

```sh
npm run check
npm run build
npm run preview
```

Build produces `dist/`. Stop the development server before previewing on the same port, or use `PORT=5174 npm run preview`.

## Update your profile

Edit `src/profile/profile.json` for your biography, experience, links, and four case studies. Supplied portraits, banner, résumé, and project images live in `public/reference/profile/`. CSS adjustments and career-section rendering live in `profile.css` and `enhancements.js` in that directory.

Regenerate personalized pages and runtime data after editing the JSON:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-profile.txt
.venv/bin/python scripts/personalize.py
npm run check
npm run build
```

Python is only required to regenerate content; the generated website runs without it. `scripts/profile-baseline/` preserves the original inputs for deterministic regeneration. Do not overwrite this baseline with personalized output.

## Pages and behavior

- `/`: introduction, experience, selected work, services, recommendations, and photo carousel.
- `/projects`: project listing.
- `/projects/karbon-forex`, `/projects/swift-code-finder`, `/projects/karbon-design-system`, `/projects/karbon-business`: case studies based on your existing portfolio.
- `/contact`: opens a draft in the visitor’s email application. No backend sends or stores submissions.
- `/404`: not-found page.

Your CV supplies career details; your existing portfolio supplies project material and recommendations. The supplied AI banner replaces the template designer’s showreel. Original motion, SVG illustrations, navigation, and responsive variants remain in the compiled runtime. The live React app mounts the personalized page; static HTML supplies an initial document.

## Implementation

`src/reference/` holds page HTML and responsive styles. `public/reference/assets/` holds local Framer modules, fonts, imagery, and binary CMS data. The personalizer adapts both static markup and decoded CMS records. `public/reference/local.js` handles the email draft. `scripts/serve.mjs` supports media byte ranges and development error diagnostics.

The earlier hand-authored starter remains in `src/` and is accessible with `npm run dev:starter`; it is not the current portfolio. Compiled Framer modules preserve fidelity but are less convenient for structural edits than authored components.

The original capture tools (`mirror-reference.py` and `prepare-local.py`) are archival maintenance tools. Running them overwrites captured files; use `personalize.py` for normal content updates. The website has not been published.
