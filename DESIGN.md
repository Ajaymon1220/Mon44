# Portfolio design system

The visual reference is [Paperline](https://paperline.framer.website/). Match its **dark textured canvas, cutting-mat collage, bold white-outlined sticker typography, layered paper objects, yellow pill controls, and large project imagery**. The homepage is the visual baseline for all routes. Keep Ajaymon’s identity, biography, work and images.

The earlier light page with script headings was an incorrect interpretation. Do not return to the cream-and-purple theme, generic card grids, or handwritten primary titles.

## Source of truth

| Responsibility | File |
| --- | --- |
| Colors, fonts, spacing, shadows, motion variables | `public/reference/profile/design-tokens.css` |
| Shared foundation, navigation, buttons, footer, image dialog, homepage | `public/reference/profile/home.css` |
| About, Work, case study, Contact and 404 components | `public/reference/profile/pages.css` |
| Shared page frame and navigation | `scripts/portfolio_layout.py` |
| Profile, project narrative and destinations | `src/profile/profile.json` |
| Homepage generator | `scripts/home-page.py` |
| Illustrated About generator | `scripts/about-page.py` |
| Work, case studies, Contact and 404 generator | `scripts/portfolio-pages.py` |
| Shared interactions and homepage collage | `public/reference/profile/home.js` |
| Work filters and local email draft | `public/reference/profile/pages.js` |

Generated HTML lives in `src/reference/`. Make persistent edits in the generators and styles, then regenerate. All active routes use the authored shared frame; captured Framer assets and legacy enhancement styles remain archival and are not loaded by these pages.

## Design tokens

| Token | Value | Use |
| --- | --- | --- |
| `--paper` | `#19191b` | Charcoal page background |
| `--sheet` | `#fdfcfd` | White paper, photo frames |
| `--ink` | `#d0cdd7` | Main text on charcoal |
| `--muted` | `#aaa7b1` | Supporting copy |
| `--faint` | `#85818d` | Small annotations and metadata |
| `--line` | `#ffffff12` | Quiet grid and section rules |
| `--wash` | `#242426` | Raised dark surfaces |
| `--yellow` | `#ffba18` | Primary actions, focus, highlights |
| `--content` | `1160px` | Maximum page width |
| `--radius` | `16px` | Cutting mat and large image surfaces |
| `--paper-shadow` | `2px 3px 5px #0003, 8px 20px 30px #0003` | Layered physical objects |
| `--ease` | `cubic-bezier(.2,.7,.2,1)` | Gentle settling motion |
| `--fast` / `--slow` | `180ms` / `600ms` | Controls / object tilt |

Spacing scale: **8, 16, 24, 32, 40, 64, 80px**. Paper surfaces use dark graphite text. Yellow controls also use dark text. Reserve saturated accent colors in the homepage company names for that illustration, rather than expanding the interface palette.

## Typography

Fonts are hosted locally in `public/reference/profile/fonts/`.

- **Geist 800:** primary titles and name stickers. Graphite fill, white outline, tight tracking, approximately 1.0–1.08 line height. Use `paint-order: stroke fill` to preserve letter interiors. Slight rotation gives the sticker character.
- **Geist Mono:** navigation, buttons, brackets, project names and metadata. Small labels sit around 9–12px; project titles around 17–20px. Do not use tiny metadata for essential explanations.
- **Caveat:** handwritten captions, chapter headings, personal notes and annotations. This supports the composition; it does not replace the bold sticker heading.
- **Geist regular:** forms and longer case study paragraphs, 15–16px with 1.75–1.8 line height.

Keep primary headings short enough to retain their silhouette on narrow screens. Give outlined text extra breathing room so its white edge does not collide with other objects.

## Shared shell

Use the shared navigation and footer generators on every route. The tilted name sticker links home. Work and About links sit in a rounded navigation group; CV opens the local résumé; the yellow “Let’s talk” control goes to `/contact`. Inner pages mark the relevant link with `aria-current="page"`.

Use a charcoal backdrop with subtle grain, faint vertical guides and bracketed section labels. Grain is decorative, ignores pointer input and must not obstruct controls. Keep the page width at 1160px, with 40px outer margins on smaller desktops, then 24px and 16px on mobile.

## Page compositions

| Page | Composition |
| --- | --- |
| Home | Large neutral cutting mat. Bold name sticker with a plain-language fintech headline and current role on the left; a smaller portrait and readable process note on the right. Yellow selected-work action and white résumé link. Compact introduction followed immediately by selected work: a compact interactive project showcase with one large screenshot stage and a five-project selector, plus an All projects link. Full problem and contribution narratives live on the Work page and case studies. Career background follows the projects. |
| About | Smaller cutting-mat introduction and tilted portrait. Preserve the three illustrated chapters: data → people → product. One short caption per chapter; put the full employment history in the résumé. |
| Work | Sticker title, short handwritten introduction, pill filters, and paired large project images. Filtered cards must disappear from both layout and keyboard navigation. |
| Case studies | Sticker project title, short summary and role/timeline. Readable screenshots, a problem/contribution/output brief, three grounded design decisions, chapter links and narrative sections. Image enlargement and a next-project link. Retain the supplied project facts. |
| Contact | Bold sticker introduction beside a tilted graph-paper note. Properly labelled fields. A clear action to open an email draft, plus direct email, copy email and LinkedIn links. |
| 404 | A large 404 sticker on the cutting mat with a brief caption and routes back to Home and Work. The server returns HTTP 404 for unknown paths. |

Project screenshots must remain legible. Do not substitute invented client work or outcomes. Illustration and stationery can supply texture and depth; avoid decorative UI that implies unsupported functionality.

## Interactions

- **Navigation and buttons:** subtle lift or rotation on hover, visible keyboard focus.
- **Image surfaces:** small pointer tilt on devices with a fine pointer. Direct case-study links remain ordinary links.
- **Field note:** pointer drag via its handle; arrow keys move it, Home/Escape reset it. The reset-desk button provides an explicit reset action. It rises above nearby collage objects when focused or dragged.
- **Scroll reveals:** progressive enhancement. Content remains readable without JavaScript. Reduced-motion preference disables decorative transitions.
- **Image dialogs:** native modal dialogs, labelled title, Close button, Escape support and backdrop dismissal. No custom keyboard trap.
- **Work filters:** native buttons with `aria-pressed`, visible count in an `aria-live` region, and `hidden` on nonmatching cards.
- **Email copy:** report success only after the clipboard write succeeds; show the selectable address on failure.
- **Contact form:** browser validation, then a `mailto:` draft with encoded fields. Do not claim the message was sent. No backend stores or sends it.
- **Audio:** the shared script retains optional audio support, but the review-focused homepage does not show an audio widget.

## Responsive and accessibility rules

At 809px and below, stack large compositions and case-study columns. About’s chapters become a vertical illustrated story. Keep Work filters wrapping and case-study chapter links accessible. At 420px and below, reduce spacing and heading size; the optional CV navigation item can be hidden because the résumé remains available on Home and About.

Use one `h1`, meaningful heading order, a skip link, image alternative text, labelled inputs and descriptive link names. Decorative assets use empty alternative text. Native buttons and links are preferable to clickable containers. Respect `prefers-reduced-motion` and avoid autoplay.

## Assets

Ajaymon’s portrait, résumé and project captures are in `public/reference/profile/`. The neutral mat, paper, pencil, hello decoration and earbuds in `public/reference/profile/paperline/` were downloaded from the user-provided Paperline reference. They are decorative; the source attribution does not imply ownership of those assets or the original template.

## Regeneration and checks

```sh
python3 scripts/home-page.py
python3 scripts/about-page.py
python3 scripts/portfolio-pages.py
node --check public/reference/profile/home.js
node --check public/reference/profile/pages.js
npm run build
```

`personalize.py` also regenerates all authored pages after its archival personalization steps. Check generated routes, local asset paths, heading structure and anchor destinations after changes. Per the user’s preference, do not perform browser validation unless requested. Do not claim visual or interaction validation from a successful build alone.

## Hiring-review refinements

Lead with the specific fintech positioning and current Junior Product Designer role at Karbon Business. Keep the name sticker as a visual signature; supporting copy uses readable, unoutlined type. The smaller homepage hero links directly to selected work. Move career background below projects.

Each project card exposes its problem and Ajaymon’s contribution. Use flat, contained screenshots instead of perspective distortion. Case-study briefs distinguish problem, contribution and design output; collaborators are listed only where supported by the existing source material. Design decisions explain the documented approach without inventing alternative explorations or test findings.

At the user’s request, the three supporting case studies include **illustrative placeholder results**. Every sample section must retain its visible “NOT ACTUAL PROJECT RESULTS” label. These numbers are layout examples, not evidence of impact. Replace them with verified findings and context before publication; never propagate them into homepage claims.

## Invoice case study

`/projects/karbon-forex` now contains the focused invoice case study adapted from the user's older portfolio at `https://mon44.framer.website/work/case-study-1`. Its authored narrative lives in `scripts/invoice_case.py`; card content and image paths live in `src/profile/profile.json`. Preserve the existing route so links continue to work.

Use the specific workflow problem instead of the undefined “80% improvement” headline. Keep four design decisions, a before/redesigned workflow comparison and original project screenshots. The interactive preview is explicitly a proposed refinement with sample data; it is not evidence of a shipped implementation. The iteration section is a test plan awaiting actual observations, not a fabricated research story.

The invoice page no longer uses the generic dummy-result snapshot. Prior portfolio metrics are retained in an expandable evidence section, marked as previously reported and awaiting measurement context. Do not turn them into headline claims until definitions, sample sizes, sources and time windows are supplied. Other case studies still contain visibly labelled sample figures.

## Supporting case-study structure

SWIFT Code Finder, Karbon Design System and Karbon Business use `scripts/project_story.py`, with project-specific story content in each `src/profile/profile.json` project's `story` field. Match the invoice page's narrative rhythm: scope, problem comparison, user needs and research, four design decisions, original images, proposed iteration and outcome measurement. Keep proposed tests and sample metrics explicitly distinguished from completed research and actual results. The original screenshot galleries remain inspectable through the shared image dialog.

## TaxOS case study

`/projects/taxos` uses `scripts/taxos_case.py` and the original screenshots in `public/reference/profile/taxos/`. Follow the invoice narrative structure: a specific workflow problem, two user audiences, four decisions, functional prototyping, documented iteration stages and reported outcomes. Keep the 50% manual-work reduction goal distinct from collection-cycle results. Checklist generation time does not establish end-to-end preparation or review speed. Do not present commercial traction as sole design attribution.

Home and Work show five projects, with TaxOS second and an AI products filter. Preserve `image_index` for original assets when reordering projects. The archival personalization pass maps only the four original records; authored generators add TaxOS afterward.

### TaxOS visual storytelling

Use `scripts/taxos_visuals.py` for the three-step overview, illustrative role personas, before/after workflow and four concept diagrams. These are code-native SVG/HTML illustrations, not product screenshots or research evidence. Preserve the visible persona and concept-diagram labels. Keep original screenshots inspectable and supporting evidence in native disclosures. Scope visual styles to the TaxOS components, stack boards on mobile, and keep decorative illustrations hidden from assistive technology when adjacent text carries the meaning.

### Guided reading interactions

TaxOS offers an optional six-chapter walkthrough with previous/next links, scroll-synced chapter progress and a close control. Persona links highlight related decisions without hiding other content. The three workflow controls explain collection, organization and preparation. Controls work by keyboard, explicit navigation moves focus to the chapter heading, and navigation introduces no animation. Keep links functional without JavaScript and hide JS-only controls until initialized. Progress denotes the current chapter, not proof of reading.

The workflow comparison now uses a single `.workflow-lab` with integrated Collect / Organize / Prepare controls. Each stage pairs a concrete previous-workflow illustration with a simplified TaxOS interface and one takeaway. JavaScript shows one paired scene at a time; without JavaScript all scenes remain readable. Preserve pressed states, panel relationships and the live stage announcement. Stack before/after scenes vertically below 650px.

The workflow lab auto-plays as a live-text loop, eight seconds per scene, once in view. Show a countdown, progress line and Play/Pause control. Pause on manual stage selection and while out of view or in a background tab. Reduced-motion preference starts paused. Announce manual changes only; automatic cycling must not repeatedly interrupt screen readers.

### Homepage project showcase

Selected Work uses a colored preview stage beside a compact project selector. Selecting a project updates the screenshot, title, summary and case-study links. Use accessible vertical tabs on desktop with arrow-key, Home and End navigation; the selector becomes a two-column grid on mobile. Keep all five project panels visible with working links when JavaScript is unavailable. No autoplay. Reduced motion disables preview transforms.
