"""Shared long-form structure for the three supporting case studies."""
from html import escape as e
from portfolio_layout import render, contact_cta

def project_story(project, i, next_project):
    story = project['story']
    def steps(items):
        return '<ol>'+''.join(f'<li>{e(item)}</li>' for item in items)+'</ol>'
    def panels(items):
        return ''.join(f'<article><h3>{e(title)}</h3><p>{e(copy)}</p></article>' for title, copy in items)
    def figure(n):
        caption = story['captions'][n-1]
        return f'''<figure class="case-figure"><button class="case-image" type="button" data-image="/reference/profile/project-{project.get("image_index", i+1)}-{n}.png" data-title="{e(project['title'])}" aria-label="Enlarge {e(project['title'])} design"><img src="/reference/profile/project-{project.get("image_index", i+1)}-{n}.png" alt="{e(caption)}" loading="lazy"><span>take a closer look ↗</span></button><figcaption>{e(caption)}</figcaption></figure>'''
    decisions = project['decisions'] + [story['fourth_decision']]
    decisions_html = ''.join(f'<li><div><span>0{n+1}</span><h3>{e(title)}</h3></div><p>{e(reason)}</p></li>' for n,(title,reason) in enumerate(decisions))
    metrics = ''.join(f'<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for label,value in story['samples'])
    collaborators = f'<div><dt>Worked with</dt><dd>{e(project["collaborators"])}</dd></div>' if project.get('collaborators') else ''
    title = '<br>'.join(e(line) for line in story['headline'])
    content = f'''<div class="section-rule"><a href="/projects">← all work</a><span>[case study / 0{i+1}]</span></div>
<header class="case-header invoice-header"><p class="eyebrow">{e(project['tags'])}</p><h1 class="sticker">{title}</h1><p class="case-subtitle">{e(project['title'])}</p><p class="invoice-deck">{e(project['summary'])}.</p><dl class="case-facts"><div><dt>My focus</dt><dd>{e(project['role'])}</dd></div><div><dt>Timeline</dt><dd>{e(project['year'])}</dd></div>{collaborators}</dl></header>
<figure class="case-hero"><img src="/reference/profile/project-{project.get("image_index", i+1)}-0.png" alt="{e(project['title'])} design overview" fetchpriority="high"></figure>
<nav class="chapter-nav" aria-label="Case study chapters"><a href="#brief-title">At a glance</a><a href="#problem">The problem</a><a href="#research">Research</a><a href="#decisions">Design decisions</a><a href="#design">The design</a><a href="#iteration">Iteration plan</a><a href="#outcomes">Outcomes</a></nav>
<section class="case-brief" aria-labelledby="brief-title"><h2 id="brief-title">The project at a glance</h2><dl><div><dt>The problem</dt><dd>{e(project['problem'])}</dd></div><div><dt>My contribution</dt><dd>{e(project['contribution'])}</dd></div><div><dt>Design output</dt><dd>{e(project['output'])}</dd></div></dl><details class="evidence-note"><summary>Scope and evidence notes</summary><p>This narrative uses the existing portfolio description and project screenshots. It describes the design contribution, not sole ownership of research, engineering or business outcomes. Detailed research records, delivery status and measured results remain to be added. Sample results below are labelled as illustrative.</p></details></section>
<section class="invoice-chapter" id="problem"><p class="eyebrow">01 / THE PROBLEM</p><h2>{e(story['problem_heading'])}</h2><p class="chapter-copy">{e(story['context'])}</p><div class="workflow-comparison"><div><h3>Starting point</h3>{steps(story['before'])}</div><div><h3>Design direction</h3>{steps(story['after'])}</div></div></section>
<section class="invoice-chapter" id="research"><p class="eyebrow">02 / RESEARCH &amp; DISCOVERY</p><h2>The needs behind the interface.</h2><div class="user-needs">{panels(story['needs'])}</div><p class="chapter-copy">{e(story['research'])}</p><details class="evidence-note"><summary>Research documentation to add</summary><p>{e(story['research_evidence'])}</p></details></section>
<section class="invoice-chapter" id="decisions"><p class="eyebrow">03 / THE DESIGN REASONING</p><h2>Four decisions that shape the experience.</h2><ol class="invoice-decisions">{decisions_html}</ol></section>
<section class="invoice-chapter" id="design"><p class="eyebrow">04 / THE DESIGN</p><h2>From the approach to the interface.</h2><p class="chapter-copy">{e(project['output'])}</p>{figure(1)}{figure(2)}</section>
<section class="invoice-chapter" id="iteration"><p class="eyebrow">05 / FROM DESIGN TO EVIDENCE</p><h2>The next iteration to validate.</h2><p class="chapter-copy">The current material explains the approach, but does not document a complete tested iteration. This is a proposed test plan, not a claim that these sessions already happened.</p><div class="iteration-plan">{panels(story['iteration'])}</div><p class="evidence-pending">To complete this story: add an actual observation, the revision it prompted and what happened when it was tested again.</p></section>
<section class="invoice-chapter" id="outcomes"><p class="eyebrow">06 / OUTCOMES &amp; MEASUREMENT</p><h2>What to measure next.</h2><p class="chapter-copy">{e(story['measurement'])}</p><section class="sample-results" aria-labelledby="sample-title"><p class="sample-label">ILLUSTRATIVE DATA · NOT ACTUAL PROJECT RESULTS</p><h3 id="sample-title">Sample outcome snapshot</h3><dl class="sample-metrics">{metrics}</dl><p>Placeholder figures for this portfolio draft. Replace with verified findings, sample sizes, measurement sources and dates before publishing.</p></section></section>
<section class="next-project"><div><p class="eyebrow">[next story]</p><h2 class="handwritten">{e(next_project['title'])}</h2></div><a class="button button-yellow" href="/projects/{e(next_project['slug'])}">Next case study ↗</a></section>{contact_cta()}'''
    return render(project['title'], project['summary'], content, 'work', 'case-page invoice-case supporting-case')
