import csv, re, html, os, json
ROOT = os.path.expanduser('~/ClaudeDocs/inc42/cto-summit-2026')
A = ROOT + '/assets'
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = 'https://events.inc42.com/cto-summit/checkout/?add-to-cart=12380'
SPONSOR = 'https://tally.so/r/44YONk?source=website'
ICPS = ['generic', 'tech', 'engineering', 'product', 'data']
esc = html.escape

def icon(name, cls='ic'):
    s = open(f'{A}/icons/{name}.svg').read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S).strip()
    s = re.sub(r'class="[^"]*"', f'class="{cls}" aria-hidden="true"', s, count=1)
    s = re.sub(r'\s(width|height)="24"', '', s)
    return re.sub(r'\s+', ' ', s)
def logo(slug, cls='lg'):
    s = re.sub(r'<title>.*?</title>', '', open(f'{A}/logos/tools/{slug}.svg').read())
    return s.replace('<svg ', f'<svg class="{cls}" fill="currentColor" aria-hidden="true" ', 1)
def inline_svg(path, cls):
    s = re.sub(r'<\?xml.*?\?>', '', open(path).read())
    return s.replace('<svg', f'<svg class="{cls}" aria-hidden="true"', 1)
INC42 = inline_svg(f'{A}/logos/inc42-logo-image.svg', 'inc42')
ORACLE = inline_svg(f'{A}/logos/logo01.svg', 'oracle').replace('viewBox="0 0 271 152"', 'viewBox="0 54 271 42"')
def V(**kw): return ''.join(f'<span data-v="{k}">{v}</span>' for k, v in kw.items())

# ---------------- speakers ----------------
SPK = {
 'rish': ('Rishikesh SR', 'Cofounder', 'Rapido', 'Rishikesh-SR'),
 'khilan': ('Khilan Haria', 'CPO', 'Razorpay', 'Khilan-Haria'),
 'nitin': ('Nitin Jain', 'CTO', 'ShareChat & Moj', 'Nitin-Jain'),
 'kiran': ('Kiran Kumar', 'Head, Platform Engineering & Agentic AI', 'Meesho', 'Kiran-Kumar'),
 'ram': ('Ramkumar Venkatesan', 'CTO', 'Cashfree Payments', 'Ramkumar-Venkatesan'),
 'kausal': ('Kausal Malladi', 'CTO, Investments', 'INDmoney', 'Kausal-Malladi'),
 'vaibhav': ('Vaibhav Khandelwal', 'Cofounder & CTO', 'Shadowfax', 'Vaibhav-Khandelwal'),
 'ish': ('Ish Babbar', 'Cofounder & CTO', 'InsuranceDekho', 'Ish-Babbar'),
 'vikas': ('Vikas Goyal', 'Cofounder & CTO', 'Kuku', 'Vikas-Goyal'),
 'anil': ('Anil Sinha', 'CTO', 'Fibe', 'Anil-Sinha'),
 'thiya': ('Thiyagaraj T', 'Director, Engineering', 'Eightfold', 'Thiyagaraj-T'),
 'ashok': ('Ashok Hariharan', 'CEO', 'IDfy', 'Ashok-Hariharan'),
 'vinay': ('Vinay Rai', 'Executive VP, Technology', 'Netradyne', 'Vinay-Rai'),
 'anuj': ('Anuj Srivastava', 'Cofounder & CEO', 'OnFinance AI', 'Anuj-Srivastava'),
}
SPK_ORDER = {
 'generic':     ['rish','khilan','nitin','kiran','ram','kausal','vaibhav','ish','vikas','anil','thiya','ashok','vinay','anuj'],
 'tech':        ['nitin','ram','kausal','vinay','anil','vikas','ish','vaibhav','kiran','thiya','khilan','rish','ashok','anuj'],
 'engineering': ['kiran','thiya','vikas','ish','vaibhav','nitin','kausal','ram','vinay','anil','khilan','rish','ashok','anuj'],
 'product':     ['khilan','rish','ashok','anuj','nitin','kiran','kausal','ram','vinay','anil','thiya','vikas','ish','vaibhav'],
 'data':        ['anil','thiya','kiran','nitin','anuj','kausal','ram','vinay','vikas','ish','vaibhav','khilan','rish','ashok'],
}
def img(k): return f'assets/img/speakers/{SPK[k][3]}.jpg'
def face(k, cls='face'): return f'<span class="{cls}" style="background-image:url({img(k)})" role="img" aria-label="{esc(SPK[k][0])}"></span>'
def spk_card(k, cls='spk'):
    return (f'<article class="{cls}" data-key="{k}"><div class="spk-photo"><img src="{img(k)}" alt="{esc(SPK[k][0])}" loading="lazy"></div>'
            f'<div class="spk-info"><b>{esc(SPK[k][0])}</b><span>{esc(SPK[k][1])}</span><span class="co">{esc(SPK[k][2])}</span></div></article>')
spk_cards = ''.join(spk_card(k) for k in SPK_ORDER['generic'])

# hero A: speaker wall (6 per audience)
WALL = {k: v[:6] for k, v in SPK_ORDER.items()}
hero_wall = ''.join(f'<div class="wall" data-vg="{icp}">' + ''.join(
    f'<figure class="wall-t"><img src="{img(k)}" alt="{esc(SPK[k][0])}"><figcaption><b>{esc(SPK[k][0])}</b><span>{esc(SPK[k][2])}</span></figcaption></figure>' for k in ks)
    + '</div>' for icp, ks in WALL.items())
# hero C: ribbon (all speakers)
ribbon = ''.join(f'<figure class="rib-t"><img src="{img(k)}" alt="{esc(SPK[k][0])}"><figcaption><b>{esc(SPK[k][0])}</b><span>{esc(SPK[k][2])}</span></figcaption></figure>' for k in SPK_ORDER['generic'])
FACES = {k: v[:5] for k, v in SPK_ORDER.items()}
hero_faces = ''.join(f'<span class="faces" data-vf="{k}">' + ''.join(face(s) for s in v) + '</span>' for k, v in FACES.items())

# ---------------- outcomes ----------------
TOPICS = [
 ('scale', 'Scale', "The Architecture Of 10X: Engineering For India's Next Scale Curve", '10:00', 'Panel', ['vikas','ish','vaibhav'], [
   'How do you keep systems up during festive sales, IPL and UPI spikes?',
   'How do you scale for patchy networks and low-end phones?',
   'What do you switch off first when traffic breaks your limits?',
   'Which old architecture decisions are teams now reversing for AI?']),
 ('ai', 'AI in production', 'Building AI Systems For Indian Scale', '10:30', 'Panel', ['nitin'], [
   'What does an AI feature cost once it reaches millions of users?',
   'When do you use a frontier, smaller or on-device model?',
   'How do you handle Hinglish and vernacular input?',
   'What should you build, and what should you rent?']),
 ('code', 'Coding with AI', 'Why Verification Is Becoming The New Engineering Bottleneck', '11:30', 'Panel', [], [
   'How do you review code when AI writes half of it?',
   'Which metrics show AI coding is actually working?',
   'What broke when AI-written code reached production?',
   'Which skills do engineers need now?']),
 ('teams', 'Teams & leadership', 'The Great Engineering Reset: Teams, Talent & Leadership After AI', '12:00', 'Panel', ['kausal'], [
   'How do you scale your team when AI does the routine work?',
   'Which roles will grow, shrink or change?',
   'What should you test when hiring freshers now?',
   'Which skills should leaders protect as AI takes over tasks?']),
 ('data', 'Data for AI', 'Building The Data Foundation For AI At Scale', '13:00', 'Panel', ['anil','thiya'], [
   "Why isn't a dashboard-era data stack ready for AI?",
   'Which data problems derail AI projects most often?',
   'Where is real-time data worth the cost?',
   'What should you fix first to be AI-ready?']),
]
DEFAULT_TOPIC = {'generic': 'scale', 'tech': 'ai', 'engineering': 'scale', 'product': 'ai', 'data': 'data'}
tabs = ''.join(f'<button type="button" class="tab" role="tab" data-topic="{t[0]}" aria-selected="false">{t[1]}</button>' for t in TOPICS)
panels = ''
for key, name, title, time, kind, spk, qs in TOPICS:
    who = (''.join(face(k, 'face md') for k in spk) + '<div class="who-n">' + ''.join(f'<span><b>{esc(SPK[k][0])}</b> {esc(SPK[k][2])}</span>' for k in spk) + '</div>') if spk else \
          '<span class="ghost">' + icon('user') + '</span><div class="who-n"><span>Speakers to be revealed</span></div>'
    panels += f'''<div class="panel" role="tabpanel" data-topic="{key}" hidden>
  <ul class="qs">{''.join(f'<li>{esc(q)}</li>' for q in qs)}</ul>
  <aside class="ans"><p class="ans-l">Answered at</p><p class="ans-t">{time} · {kind}</p><h3>{esc(title)}</h3><div class="who">{who}</div><p class="ans-qa">{icon("message-circle","ic sm")}Ask your own question in the Q&amp;A after the panel</p><a href="#agenda" class="ans-link">See the full agenda {icon("arrow-right","ic xs")}</a></aside>
</div>'''

# ---------------- experience ----------------
DAY = [
 ('10:00', 'Panels and firesides', 'Leaders walk through real systems, numbers and trade-offs. Q&amp;A after each.', 'row-2-1.jpg'),
 ('Breaks', 'Conversations over high tea', 'Short breaks built for meeting people between sessions.', 'strip-b3.jpg'),
 ('13:30', 'Executive lunch', 'Seated roundtables with speakers and fellow leaders.', 'row-1-1.jpg'),
 ('15:00', 'Afternoon sessions', 'More panels and firesides, with Q&amp;A.', 'row-2-2.jpg'),
 ('18:00', 'Dinner and networking', 'An evening with the full room of 175 leaders.', 'row-2-3.jpg'),
]
day_steps = ''.join(f'<button type="button" class="d-step" data-i="{i}" aria-pressed="{"true" if i==0 else "false"}"><span class="d-time">{t}</span><span class="d-txt"><b>{h}</b><span>{p}</span></span></button>' for i, (t, h, p, im) in enumerate(DAY))
day_imgs = ''.join(f'<img src="assets/img/{im}" alt="" data-i="{i}" class="{"on" if i==0 else ""}" loading="lazy">' for i, (t, h, p, im) in enumerate(DAY))

# ---------------- deals ----------------
DEALS = {  # slug: name, usd, label
 'googlecloud': ('Google Cloud', 350000, 'up to $350K'), 'cloudflare': ('Cloudflare', 350000, 'up to $350K'),
 'microsoftazure': ('Azure', 150000, 'up to $150K'), 'alibabacloud': ('Alibaba Cloud', 120000, '$120K'),
 'amazonwebservices': ('AWS', 100000, 'up to $100K'), 'posthog': ('PostHog', 50000, '$50K'),
 'databricks': ('Databricks', 21000, '$21K'), 'deepgram': ('Deepgram', 15000, '$15K'), 'algolia': ('Algolia', 10000, '$10K'),
 'intercom': ('Intercom Fin', 6500, '$6.5K'), 'qwen': ('Qwen AI', 5000, '$5K'), 'snowflake': ('Snowflake', 1250, '$1,250'),
 'openai': ('OpenAI', 1000, '$1K'), 'claude': ('Claude', 1000, '$1K'), 'mongodb': ('MongoDB', 500, '$500'),
 'gitlab': ('GitLab', 0, '1 year free'), 'datadog': ('Datadog', 0, '1 year free'), 'retool': ('Retool', 0, '1 year free'),
 'auth0': ('Auth0', 0, '12 months free'), 'mixpanel': ('Mixpanel', 0, '1 year free'), 'sentry': ('Sentry', 0, '6 months free'),
 'jetbrains': ('JetBrains', 0, '6 months free'), 'notion': ('Notion', 0, '3 months free'),
}
PRESET = {
 'generic': ['amazonwebservices','googlecloud','openai','databricks','datadog','gitlab'],
 'tech': ['amazonwebservices','googlecloud','openai','claude','datadog','databricks'],
 'engineering': ['amazonwebservices','cloudflare','datadog','gitlab','sentry','jetbrains'],
 'product': ['posthog','mixpanel','intercom','notion','openai','claude'],
 'data': ['databricks','snowflake','posthog','mongodb','algolia','googlecloud'],
}
calc_chips = ''.join(f'<button type="button" class="tool" data-slug="{s}" data-usd="{u}" aria-pressed="false">{logo(s)}<span class="t-n">{esc(n)}</span><span class="t-v">{esc(l)}</span></button>' for s, (n, u, l) in DEALS.items())
rows = list(csv.DictReader(open(os.path.expanduser('~/Downloads/deals.csv'), encoding='utf-8-sig'), delimiter=';'))
N_DEALS = len(rows)
all_rows = ''.join('<li><b>' + esc(r['product_name'].strip()) + '</b><span>' + esc(r['title'].strip().replace(' // ', '; ')) + '</span></li>' for r in sorted(rows, key=lambda r: r['product_name'].strip().lower()))

# ---------------- agenda ----------------
AG = [
 ('10:00', 'Panel', "The Architecture Of 10X: Engineering For India's Next Scale Curve", ['vikas','ish','vaibhav'], 'scale'),
 ('10:30', 'Panel', 'Building AI Systems For Indian Scale', ['nitin'], 'ai'),
 ('11:00', 'Fireside', None, [], None),
 ('11:30', 'Panel', 'Why Verification Is Becoming The New Engineering Bottleneck', [], 'code'),
 ('12:00', 'Panel', 'The Great Engineering Reset: Teams, Talent & Leadership After AI', ['kausal'], 'teams'),
 ('12:30', 'Fireside', None, [], None),
 ('13:00', 'Panel', 'Building The Data Foundation For AI At Scale', ['anil','thiya'], 'data'),
 ('13:30', 'Break', 'Executive lunch', [], 'break'),
 ('15:00', 'Panels & firesides', None, [], None),
 ('18:00', 'Evening', 'Dinner and networking', [], 'break'),
]
PICKS = {'tech': ['ai','teams','data'], 'engineering': ['scale','code','teams'], 'product': ['ai','data'], 'data': ['data','ai']}
PICK_LABEL = {'tech': 'For CTOs', 'engineering': 'For engineering leaders', 'product': 'For product leaders', 'data': 'For data &amp; AI leaders'}
agenda = ''
for time, kind, title, spk, key in AG:
    if title is None:
        agenda += f'<li class="ag tba"><span class="ag-time">{time}</span><span class="ag-kind">{kind}</span><span class="ag-title">To be revealed</span><span class="ag-who"><span class="ghost">{icon("user")}</span></span></li>'
    elif key == 'break':
        agenda += f'<li class="ag brk"><span class="ag-time">{time}</span><span class="ag-kind">{kind}</span><span class="ag-title">{esc(title)}</span><span class="ag-who"></span></li>'
    else:
        tags = ''.join(f'<span class="pick" data-vi="{i}">{PICK_LABEL[i]}</span>' for i in PICKS if key in PICKS[i])
        who = ''.join(face(k, 'face sm') for k in spk) if spk else f'<span class="ghost">{icon("user")}</span>'
        agenda += f'<li class="ag"><span class="ag-time">{time}</span><span class="ag-kind">{kind}</span><span class="ag-title">{esc(title)} {tags}</span><span class="ag-who">{who}</span></li>'

# ---------------- audience copy ----------------
VARS = {
 '{{V_WORD}}': V(generic='tech', tech='tech', engineering='engineering', product='product', data='data &amp; AI'),
 '{{V_SUB}}': V(
   generic='Learn how India\'s largest tech companies scale, ship AI and build teams. From the people who run them.',
   tech='Learn how CTOs at ShareChat, Cashfree and INDmoney run AI, costs and teams at scale.',
   engineering='Learn how engineering leaders at Meesho, Kuku and Shadowfax handle scale, reliability and teams.',
   product='Learn how Razorpay, Rapido and ShareChat ship AI features to millions of users.',
   data='Learn how Fibe, Eightfold and Meesho build data that AI can actually use.'),
 '{{V_SPEAKERS_LINE}}': V(generic='Rapido, Razorpay, ShareChat, Meesho', tech='ShareChat, Cashfree, INDmoney, Netradyne', engineering='Meesho, Eightfold, Kuku, InsuranceDekho', product='Razorpay, Rapido, IDfy, OnFinance AI', data='Fibe, Eightfold, Meesho, ShareChat'),
}
FAQ_FIRST = {
 'generic': ('Who is this for?', 'VP-level and above leaders in engineering, platform, product, data or AI at growth and late-stage tech companies.'),
 'tech': ("I'm a founder-CTO. Is this for me?", 'Yes. CTOs and founder-CTOs are a core part of the room.'),
 'engineering': ('I lead engineering, not the whole tech team. Is this for me?', 'Yes, at VP level or above. Engineering leaders are the largest group in the room.'),
 'product': ('I lead product. Is this for me?', 'Yes. Product leaders are part of the room, and the AI and data sessions are picked for you.'),
 'data': ('I lead data or AI. Is this for me?', 'Yes. The data foundation and AI systems sessions are picked for you.'),
}
FAQ = [
 ("What if I'm not approved?", 'Full refund within 7 working days.'),
 ('What is the $320K+ bonus?', f'{N_DEALS} partner deals: credits and free plans on tools like AWS, Google Cloud, OpenAI and Datadog. Each provider sets its own eligibility.'),
 ('Will speakers pitch products?', 'No. Speakers run the systems they talk about.'),
 ('Can I transfer my pass?', "No. Confirmed passes can't be transferred."),
 ("Can I add my company's GST number?", 'Yes, at checkout.'),
]
def faq_item(q, a, attr=''):
    return f'<details{attr}><summary><span>{esc(q)}</span>{icon("plus","ic pm")}</summary><p>{esc(a)}</p></details>'
faq_html = ''.join(faq_item(q, a, f' data-vb="{k}"') for k, (q, a) in FAQ_FIRST.items()) + ''.join(faq_item(q, a) for q, a in FAQ)

# hero B rotator questions (per audience: all questions, topic-first)
ROT = []
for key, name, title, time, kind, spk, qs in TOPICS:
    for q in qs[:2]:
        ROT.append({'q': q, 'topic': key, 'title': title, 'time': time, 'spk': [[SPK[k][0], SPK[k][2], img(k)] for k in spk]})

# ---------------- CSS for audiences ----------------
css = ['html [data-v],html [data-vb],html [data-vf],html [data-vi],html [data-vg]{display:none}']
for attr, disp in [('data-v', 'inline'), ('data-vb', 'block'), ('data-vf', 'flex'), ('data-vi', 'inline-flex'), ('data-vg', 'grid')]:
    css.append(','.join(f'html[data-icp="{k}"] [{attr}="{k}"]' for k in ICPS) + '{display:' + disp + '}')
for k in ICPS:
    for i, s in enumerate(SPK_ORDER[k]):
        css.append(f'html[data-icp="{k}"] .spk[data-key="{s}"]{{order:{i}}}')
AUD_CSS = '\n'.join(css)

CFG = json.dumps({'defaultTopic': DEFAULT_TOPIC, 'preset': PRESET, 'rot': ROT})

page = open(HERE + '/v4_template.html').read()
REPL = {'{{AUD_CSS}}': AUD_CSS, '{{CFG}}': CFG, '{{INC42}}': INC42, '{{ORACLE}}': ORACLE, '{{BOOK}}': BOOK, '{{SPONSOR}}': SPONSOR,
        '{{HERO_WALL}}': hero_wall, '{{RIBBON}}': ribbon, '{{HERO_FACES}}': hero_faces, '{{TABS}}': tabs, '{{PANELS}}': panels,
        '{{DAY_STEPS}}': day_steps, '{{DAY_IMGS}}': day_imgs, '{{CALC}}': calc_chips, '{{ALL_DEALS}}': all_rows,
        '{{AGENDA}}': agenda, '{{SPEAKERS}}': spk_cards, '{{FAQ}}': faq_html}
REPL.update(VARS)
for k, v in REPL.items(): page = page.replace(k, v)
page = page.replace('{{N_DEALS}}', str(N_DEALS))
page = re.sub(r'\{\{icon:([a-z0-9-]+)(?:\|([a-z ]+))?\}\}', lambda m: icon(m.group(1), m.group(2) or 'ic'), page)
assert '{{' not in page, re.findall(r'\{\{[^}]+\}\}', page)[:5]
open(ROOT + '/index.html', 'w').write(page)

variants = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CTO Summit first-fold variants</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600&display=swap">
<style>body{margin:0;background:#E9EBEF;font-family:Geist,system-ui,sans-serif;color:#0F1115;padding:32px 20px 80px}.w{max-width:1440px;margin:0 auto;display:grid;gap:48px}
h1{margin:0 0 4px;font-size:24px}p{margin:0;color:#5A606B}.v{display:grid;gap:12px}.v h2{margin:0;font-size:18px}.v h2 span{color:#D81E2B}
iframe{width:100%;height:900px;border:1px solid #D5D8DE;border-radius:14px;background:#fff}</style></head><body><div class="w">
<div><h1>First fold: 3 variations</h1><p>Same content and CTA, different structure. Each frame is the live page at desktop width.</p></div>
<div class="v"><h2><span>A</span> · Speaker wall (recommended)</h2><p>Trust first: six real speakers with companies next to the headline.</p><iframe src="index.html?hero=a" scrolling="no" title="Variant A"></iframe></div>
<div class="v"><h2><span>B</span> · Questions you'll get answered</h2><p>Outcome first: a rotating card shows a real question and the speaker who answers it.</p><iframe src="index.html?hero=b" scrolling="no" title="Variant B"></iframe></div>
<div class="v"><h2><span>C</span> · Centred with speaker ribbon</h2><p>Event-poster feel: centred headline and price, moving row of speaker photos below.</p><iframe src="index.html?hero=c" scrolling="no" title="Variant C"></iframe></div>
</div></body></html>'''
open(ROOT + '/first-fold-variants.html', 'w').write(variants)
print('written', len(page))
