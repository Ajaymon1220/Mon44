"""Generate Work, case studies, Contact and 404 using the shared design system."""
from html import escape as e
from invoice_case import invoice_case
from taxos_case import taxos_case
from project_story import project_story
from portfolio_layout import PROFILE as p, render, write_page, contact_cta, project_card

cards = [project_card(project, i, 'h2', True) for i, project in enumerate(p['projects'])]
filters = ''.join(f'<button type="button" data-filter="{e(tag.lower())}" aria-pressed="{str(i==0).lower()}">{e(tag)}</button>' for i,tag in enumerate(['All', 'Fintech', 'AI products', 'Design systems', 'Research', 'Web design']))
content = f'''<div class="section-rule"><span>[selected]</span><span>[works / 01—{len(p['projects']):02d}]</span></div><header class="page-title work-title"><h1 class="sticker">Less friction.<br>More flow.</h1><p class="handwritten">A few problems I've enjoyed untangling.</p></header><div class="filter-bar"><div class="filters" role="group" aria-label="Filter projects">{filters}</div><p class="filter-count" aria-live="polite">{len(p['projects'])} projects</p></div><section class="projects work-projects" aria-label="Selected projects">{''.join(cards)}</section>{contact_cta()}'''
write_page('projects', render('Selected work', 'Fintech products, responsive websites and design systems by Ajaymon.', content, 'work', 'work-page'))

for i, project in enumerate(p['projects']):
    next_project = p['projects'][(i+1) % len(p['projects'])]
    if project.get('case_kind') == 'invoice':
        write_page('projects/'+project['slug'], invoice_case(project, next_project))
        continue
    if project.get('case_kind') == 'taxos':
        write_page('projects/'+project['slug'], taxos_case(project, next_project))
        continue
    write_page('projects/'+project['slug'], project_story(project, i, next_project))

content = f'''<div class="section-rule"><span>[say hello]</span><span>[let's make something]</span></div><section class="contact-layout"><header class="page-title"><h1 class="sticker">Good things<br>start here.</h1><p class="handwritten">An idea, a question,<br>or just a hello.</p><a class="contact-address" href="mailto:{e(p['email'])}">{e(p['email'])} ↗</a><button type="button" class="copy-email" data-email="{e(p['email'])}">copy email ⧉</button><p class="copy-status" aria-live="polite"></p><a class="contact-social" href="{e(p['linkedin'])}" target="_blank" rel="noopener">Find me on LinkedIn ↗</a><p class="location-note handwritten">↳ {e(p['location'])}</p></header><form class="contact-paper" data-contact-form data-recipient="{e(p['email'])}"><span class="photo-tape" aria-hidden="true"></span><h2 class="handwritten">A little note for Ajaymon</h2><label for="sender-name">Your name</label><input id="sender-name" name="name" autocomplete="name" required maxlength="100" placeholder="What should I call you?"><label for="sender-email">Email</label><input id="sender-email" name="email" type="email" autocomplete="email" required maxlength="254" placeholder="you@example.com"><label for="message">What's on your mind?</label><textarea id="message" name="message" rows="5" maxlength="4000" required placeholder="Tell me a little about it…"></textarea><button class="button button-yellow" type="submit">Open email draft ↗</button><p class="form-note">Opens your email app. Review and send from there.</p><p class="form-status" role="status"></p></form></section>'''
write_page('contact', render('Let’s talk', 'Start a conversation with Ajaymon about your next product or design project.', content, 'contact', 'contact-page'))

content = '''<div class="section-rule"><span>[a little detour]</span><span>[404]</span></div><section class="not-found inside-mat"><p class="handwritten">Looks like this page slipped off the desk.</p><h1 class="sticker">404</h1><p>The page you're looking for isn't here.</p><div><a class="button button-yellow" href="/">Back to the desk ↗</a><a class="button" href="/projects">Explore my work</a></div></section>'''
write_page('404', render('Page not found', 'This page could not be found. Return to Ajaymon’s portfolio.', content, page_class='not-found-page'))
print(f"Generated Work, {len(p['projects'])} case studies, Contact and 404.")
