"""Apply the editable Ajaymon profile to the preserved animated template."""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
import json, re, shutil, html
ROOT=Path(__file__).resolve().parents[1]
PROFILE=json.loads((ROOT/'src/profile/profile.json').read_text())
BASE=ROOT/'scripts/profile-baseline'
FILES=list((ROOT/'src/reference').rglob('*.html'))+list((ROOT/'public/reference/assets').rglob('*.mjs'))
if not (BASE/'files.json').exists():
    files={str(p.relative_to(ROOT)):p.read_text() for p in FILES}
    (BASE/'files.json').write_text(json.dumps(files))
files=json.loads((BASE/'files.json').read_text())
records=json.loads((BASE/'records.json').read_text())
M={
'Fawaz Ahamed':'Ajaymon','Fawaz ahamed':'Ajaymon','Fawaz':'Ajaymon','Visualfolio':'Ajaymon',
'Product Designer Portfolio Template':'AI Product Designer',
'I design products & brands that solve billion-dollar problems.':PROFILE['headline'],
'Fawaz Ahamed, product designer for SaaS and AI teams.':PROFILE['intro'],
'A note from Fawaz':'A note from Ajaymon','Product designer':'AI Product Designer',
'Product designer for SaaS and AI teams.':'AI Product Designer · Bangalore, India',
'Available for new projects':'Based in Bangalore, India','Open for new projects':'Let’s start a conversation',
'Availability':'Let’s connect',
"I'm a product designer working with SaaS and AI teams. I turn complex products into flows, interfaces and sites that people understand at a glance. Tools now make it easy to produce a screen. They don't make it easy to know which screen is right, or why someone should care. That judgement is the part I care about most.":PROFILE['about'][0],
'I start with positioning and content structure, then design the interface, then build it. I design in Figma, add motion in Jitter and ship in Framer, so nothing gets lost between the idea and the live product. I also publish my own Framer templates, which keeps my systems sharp and my builds easy for other teams to own.':PROFILE['about'][1],
'Turn a complex product into an experience that feels easy to understand, credible and actionable.':'Make complex products feel intuitive, accessible and effortless to use.',
'Product work for SaaS and AI teams.':'Thoughtful design for complex products.',
'Landing pages, product sites and Framer templates, each designed in Figma and shipped in Framer.':'Selected work across fintech products, banking tools, responsive websites and design systems.',
'Design · Framer build':'Research · Design · Delivery',
'End-to-end flows and high-fidelity interfaces for SaaS and AI products, designed around how people actually use them.':'End-to-end experiences for web and mobile, from customer dashboards to complex fintech workflows.',
'Information architecture, user flows and interactive prototypes that make complex features feel simple.':'User research, usability testing and interactive prototypes that turn real feedback into clearer product decisions.',
'Components, type scales and layout rules that keep a product consistent as it grows, built in Figma and mirrored in Framer.':'Scalable Figma components, tokens and interface patterns that keep design and development aligned as a product grows.',
'Design to build':'Design to delivery',
'Product sites and prototypes built in Framer, so the product story ships exactly as designed and stays easy for your team to edit.':'Developer handoff, design QA and close collaboration with product and engineering to carry the design through to implementation.',
'Showreel':'Designing with AI','Selected motion and product work':'Curiosity, craft and emerging technology',
'Things I love besides design':'A little more of me',
'Kind words from clients':'Kind words from collaborators',
'Hire me on Contra ↗':'Connect on LinkedIn ↗','Hire me on Contra':'Connect on LinkedIn','View Contra ↗':'View LinkedIn ↗','Prefer Contra?':'Prefer LinkedIn?',
'Contra':'LinkedIn','Framer templates':'Download résumé','X (formerly Twitter)':'Email me',
'https://contra.com/fawaz_ahamed':PROFILE['linkedin'],'https://www.framer.com/@fawaz-ahamed/':'/reference/profile/AjaymonCV.pdf','https://x.com/buildwithjoe97':'mailto:'+PROFILE['email'],
'Tell me about your product, where it is today and what you need. I\'ll get back to you by email.':'Tell me about your product, the problem you’re solving and how we could work together. You can also email me at '+PROFILE['email']+'.',
'Landing pages, product sites and Framer builds for SaaS and AI teams':'Product design, fintech workflows, design systems and AI-assisted exploration',
'Goals, Timeline, Budger, Links to anything that i should see':'Your goals, timeline and links you would like me to see',
'Send message':'Open email draft'
}
# Genuine recommendations from Ajaymon's existing public portfolio.
quote1='I had the pleasure of working with Ajay for a good amount of time and found him to be a highly skilled designer with a strong grasp of tech requirements. He’s passionate about his work and consistently brings multiple thoughtful solutions to the table.'
quote2='I’ve worked closely with Ajaymon during my time at Karbon, and it’s been impressive to see how quickly and effectively he’s embedded user experience thinking into complex financial workflows.'
for suffix in ['', ' Copy']:
 M['“The Framer build was spotless. Every section was a reusable component, so our team shipped new pages the same week.”'+suffix]=quote1
 M['“He asks the right questions during every call. The positioning work alone was worth it. Fast, Effiicient and Absolute life saver”'+suffix]=quote2
M['“Fawaz took a product we struggled to explain and turned it into a page our sales team now sends to every lead.']=quote1
M.update({'Stephen Hawking':'Deepak Manjunath','John Doe':'Shubhasheesh Bagchi','Richard C':'Deepak Manjunath','Head of Marketing, B2B platform':'Senior Software Engineer · Karbon','Co-founder, creative agency':'Customer Operations · Forex','Founder, AI SaaS startup':'Senior Software Engineer · Karbon'})
IM={}
for old in ['KwulRJphLTHCSkeWH9eiq7WIw.png']:
 IM['/reference/assets/framerusercontent.com/images/'+old]='/reference/profile/ajaymon-portrait.png'
for old in ['cptjyfr3e6APqnHgO9OADsePk.jpg','B53jgAnIs81Rz2tXlHIkWuPVHcM.jpg','efVPE71NTOgsM4JqwkTOISUlKUk.jpg']:
 IM['/reference/assets/framerusercontent.com/images/'+old]='/reference/profile/deepak.svg'
IM['/reference/assets/framerusercontent.com/images/cZbdTJjygQ8Uj4pEgv5D4Z0t5Y.jpg']='/reference/profile/shubhasheesh.svg'
richtexts={}
project_by_old={}
for i,(record,project) in enumerate(zip(records,PROFILE['projects'])):
 d=record['data']; oldslug=d['giP_V1vHZ']['value'];project_by_old[oldslug]=project
 for field,new in [('B_ZiumyUX',project['title']),('yTZUyf0Wl',project['summary']),('giP_V1vHZ',project['slug'])]:M[d[field]['value']]=new
 for field,new in [('Cm8FKdxFe','Karbon Business'),('ban_8MH1u',project['tags']),('zXdzzUen0',project['role'])]:
  if d[field]['value'] not in M:M[d[field]['value']]=new
 nodes=[1]
 for heading,paragraph in project['sections']:
  nodes.extend([[4,'h2',{'dir':'auto'},[5,heading]],[4,'p',{'dir':'auto'},[5,paragraph]]])
 nodes.append([4,'p',{'dir':'auto'},[4,'a',{'href':project['source'],'target':'_blank','rel':'noopener noreferrer'},[5,'View original case study ↗']]])
 richtexts[d['Ovls3s13b']['value']]=json.dumps(nodes,separators=(',',':'),ensure_ascii=False)
 for j,field in enumerate(['nRrO4aIen','HeiafU8cr','V7_W36oeM']):
  IM[d[field]['value']['src'].split('?')[0]]=f'/reference/profile/project-{i+1}-{j}.png'
M.update(IM)
# Slug lookups use the retained record IDs, so new public URLs do not depend on old sorted indexes.
ids={p['slug']:r['data']['id']['value'] for r,p in zip(records,PROFILE['projects'])}
reverse={v:k for k,v in ids.items()}
record_updates={r['data']['id']['value']:{'BwFJwfjzq':p['year'],'Cm8FKdxFe':'Karbon Business','zXdzzUen0':p['role'],'ban_8MH1u':p['tags']} for r,p in zip(records,PROFILE['projects'])}
allmap={**M,**richtexts}
# Apply a single replacement pass to avoid cascades between project/client names.
pattern=re.compile('|'.join(re.escape(k) for k in sorted(M,key=len,reverse=True)))
def transform(s):
 if s in richtexts:return richtexts[s]
 return pattern.sub(lambda m:M[m.group()],s)
def recursive(v):
 if isinstance(v,str):return transform(v)
 if isinstance(v,list):return [recursive(x) for x in v]
 if isinstance(v,dict):return {k:recursive(x) for k,x in v.items()}
 return v
# Data decoding also runs for CMS records requested during client-side navigation.
js='globalThis.__ajayProfile='+json.dumps(PROFILE,ensure_ascii=False)+';\n'
js+='const ajayExact='+json.dumps(allmap,ensure_ascii=False)+';\n'
js+='const ajayPairs='+json.dumps(sorted(M.items(),key=lambda x:len(x[0]),reverse=True),ensure_ascii=False)+';\n'
js+='globalThis.__ajayText=value=>{if(typeof value!=="string")return value;value=value.replaceAll("https://framerusercontent.com/images/","/reference/assets/framerusercontent.com/images/");if(Object.hasOwn(ajayExact,value))return ajayExact[value];let result=value;for(const [from,to] of ajayPairs)if(from.startsWith("/reference/")||from.startsWith("https://"))result=result.split(from).join(to);return result;};\n'
js+='const ajayRecords='+json.dumps(record_updates,ensure_ascii=False)+';globalThis.__ajayRecord=r=>{const updates=ajayRecords[r.id?.value];if(updates)for(const [key,value] of Object.entries(updates))r[key]={type:"string",value};return r;};\n'
(ROOT/'public/reference/profile/data.js').write_text(js)
photos=[{'caption':'Off the clock','id':'ajay-photo','image':{'src':'/reference/profile/ajaymon-outdoors.jpg'},'note':'A moment away from the screen'}, {'caption':'Designing with AI','id':'ajay-ai','image':{'src':'/reference/profile/ai-design-banner.png'},'note':'Product design · Research · Emerging technology'}, {'caption':'Hello, I’m Ajaymon','id':'ajay-portrait','image':{'src':'/reference/profile/ajaymon-portrait.png'},'note':'AI Product Designer · Bangalore'}]
for rel,source in files.items():
 path=ROOT/rel
 if path.suffix=='.mjs':
  source=transform(source)
  # Wrap every binary string decoder, including the homepage testimonial collection.
  source=source.replace('return e.textDecoder.decode(n)', 'return (globalThis.__ajayText||((v)=>v))(e.textDecoder.decode(n))')
  source=source.replace('t[n]=R.read(e)}return t}', 't[n]=R.read(e)}return (globalThis.__ajayRecord||((v)=>v))(t)}')
  if path.name.startswith('24AsTp'):
   source+='\ne.getRecordIdBySlug=async slug=>('+json.dumps(ids)+')[slug];e.getSlugByRecordId=async id=>('+json.dumps(reverse)+')[id];\n'
  if path.name.startswith('et4l'):
   source=re.sub(r'photos:\[\{caption:`Nature Person`.*?\],style:', 'photos:'+json.dumps(photos,ensure_ascii=False)+',style:', source)
   source=source.replace('mono:!0,photos:', 'mono:!1,photos:')
   source=source.replace('/reference/assets/framerusercontent.com/assets/MLWPbW1dUQawJLhhun3dBwpgJak.mp4','').replace('/reference/assets/framerusercontent.com/assets/UnQb7t89BXXziV7zafN22nBJD0.mp4','')
  path.write_text(source)
  continue
 soup=BeautifulSoup(source,'html.parser')
 # Profile sections differ from the published hydration snapshot. Mount the
 # preserved React runtime cleanly instead of reconciling incompatible SSR nodes.
 main=soup.find(id='main')
 if main:main.attrs.pop('data-framer-hydrate-v2',None)
 # Change complete headings before split animation spans obscure their text.
 for el in soup.select('h1,h2,h3,h4,h5,p'):
  full=el.get_text('',strip=False)
  if full in M and len(el.contents)>1:
   el.clear();el.append(M[full])
 for node in list(soup.find_all(string=True)):
  if isinstance(node,(Comment,Doctype)):continue
  if node.parent.name in ['script','style']:continue
  node.replace_with(transform(str(node)))
 for tag in soup.find_all(True):
  for key,value in list(tag.attrs.items()):
   if isinstance(value,str):tag[key]=transform(value)
 for script in soup.find_all('script'):
  if script.get('type')=='framer/handover' and script.string:
   flat=recursive(json.loads(script.string))
   if isinstance(flat,list):
    for record in list(flat):
     if isinstance(record,dict) and 'id' in record and isinstance(record['id'],int):
      try:
       ident=flat[flat[record['id']]['value']]
       for key,value in record_updates.get(ident,{}).items():
        if key in record:
         value_index=len(flat);flat.append(value)
         type_index=next(i for i,v in enumerate(flat) if v=='string')
         record[key]=len(flat);flat.append({'type':type_index,'value':value_index})
      except (TypeError,KeyError,IndexError,StopIteration):pass
   script.string=json.dumps(flat,ensure_ascii=False,separators=(',',':'))
 # Case-study copy and metadata from Ajaymon's actual work.
 oldslug=next((slug for slug in project_by_old if '/'+slug+'/' in rel),None)
 if oldslug:
  project=project_by_old[oldslug]
  body=soup.find(attrs={'data-framer-name':'Case Study'})
  if body:
   body.clear()
   for heading,paragraph in project['sections']:
    for tag,text in [('h2',heading),('p',paragraph)]:
     element=soup.new_tag(tag);element['class']='framer-text';element.string=text;body.append(element)
   link=soup.new_tag('a',href=project['source']);link.string='View original case study ↗';body.append(link)
  for h in soup.find_all('h5'):
   if h.get_text()=='2026':h.string=project['year']
  path=ROOT/rel.replace('/'+oldslug+'/', '/'+project['slug']+'/')
 # Retain the animated photo stack with just the three supplied images.
 for gallery in soup.select('[aria-roledescription="carousel"]'):
  imgs=gallery.select('[role="img"]')
  for i,img in enumerate(imgs):
   if i<3:
    img['style']=re.sub(r'background-image:url\([^)]*\)', 'background-image:url('+photos[i]['image']['src']+')', img.get('style','')).replace('grayscale(1)','grayscale(0)')
    img['aria-label']=photos[i]['caption']
   else:img.parent.decompose()
  for node in list(gallery.find_all(string=True)):
   if isinstance(node,Comment):continue
   if str(node)=='05':node.replace_with('03')
   elif str(node)=='Nature Person':node.replace_with(photos[0]['caption'])
   elif str(node)=='Laugavegur Trail, Iceland':node.replace_with(photos[0]['note'])
 for name in ['Headshot']:
  for headshot in soup.find_all(attrs={'data-framer-name':name}):
   for img in headshot.find_all('img'):img['alt']='Ajaymon, AI Product Designer'
 # Local profile scripts load before the preserved runtime hydrates the page.
 for tag in [soup.new_tag('script',src='/reference/profile/data.js'),soup.new_tag('link',rel='stylesheet',href='/reference/profile/profile.css'),soup.new_tag('script',src='/reference/profile/enhancements.js',defer=True)]:soup.head.append(tag)
 if soup.title:
  soup.title.string=project_by_old[oldslug]['title']+' — Ajaymon' if oldslug else ('Ajaymon — AI Product Designer' if rel.endswith('reference/index.html') else transform(soup.title.get_text()))
 for meta in soup.select('meta[name="description"],meta[property="og:description"],meta[name="twitter:description"]'):meta['content']='Ajaymon is an AI Product Designer based in Bangalore, designing intuitive fintech products, scalable design systems and accessible web and mobile experiences.'
 for meta in soup.select('meta[property="og:image"],meta[name="twitter:image"]'):meta['content']='/reference/profile/ai-design-banner.png'
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(str(soup))
# Remove obsolete template case-study page files; their source stays in the private build baseline.
for oldslug in project_by_old:
 old=ROOT/'src/reference/projects'/oldslug
 if old.exists():shutil.rmtree(old)
for name,initials in [('deepak','DM'),('shubhasheesh','SB')]:
 (ROOT/f'public/reference/profile/{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80"><rect width="80" height="80" rx="40" fill="#e6e0ff"/><text x="40" y="48" text-anchor="middle" font-family="sans-serif" font-size="24" fill="#49416d">{initials}</text></svg>')
print('Personalized all pages, runtime text, project routes, CMS content and images for Ajaymon.')
