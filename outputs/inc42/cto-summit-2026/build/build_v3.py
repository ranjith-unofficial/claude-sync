import csv, re, html, os
ROOT = os.path.expanduser('~/ClaudeDocs/inc42/cto-summit-2026')
A = ROOT + '/assets'
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = 'https://events.inc42.com/cto-summit/checkout/?add-to-cart=12380'
SPONSOR = 'https://tally.so/r/44YONk?source=website'
ICPS = ['generic', 'tech', 'engineering', 'product', 'data']

def icon(name, cls='ic'):
    s = open(f'{A}/icons/{name}.svg').read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S).strip()
    s = re.sub(r'class="[^"]*"', f'class="{cls}" aria-hidden="true"', s, count=1)
    s = re.sub(r'\s(width|height)="24"', '', s)
    return re.sub(r'\s+', ' ', s)

def logo(slug, cls='lg'):
    s = open(f'{A}/logos/tools/{slug}.svg').read()
    s = re.sub(r'<title>.*?</title>', '', s)
    return s.replace('<svg ', f'<svg class="{cls}" fill="currentColor" aria-hidden="true" ', 1)

def inline_svg(path, cls):
    s = re.sub(r'<\?xml.*?\?>', '', open(path).read())
    return s.replace('<svg', f'<svg class="{cls}" aria-hidden="true"', 1)

INC42 = inline_svg(f'{A}/logos/inc42-logo-image.svg', 'inc42')
ORACLE = inline_svg(f'{A}/logos/logo01.svg', 'oracle').replace('viewBox="0 0 271 152"', 'viewBox="0 54 271 42"')

def V(tag='span', **kw):
    attr = {'span': 'data-v', 'div': 'data-vb'}[tag]
    return ''.join(f'<{tag} {attr}="{k}">{v}</{tag}>' for k, v in kw.items())

# ---------- speakers ----------
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
def face(k, cls='face'):
    return f'<span class="{cls}" style="background-image:url({img(k)})" role="img" aria-label="{html.escape(SPK[k][0])}"></span>'
spk_cards = ''.join(f'<article class="spk" data-key="{k}"><div class="spk-photo"><img src="{img(k)}" alt="{html.escape(SPK[k][0])}" loading="lazy"></div>'
                    f'<div class="spk-info"><b>{html.escape(SPK[k][0])}</b><span>{html.escape(SPK[k][1])}</span><span class="co">{html.escape(SPK[k][2])}</span></div></article>'
                    for k in SPK_ORDER['generic'])

# ---------- deals ----------
DEALS = {
 'googlecloud': ('Google Cloud', 'up to', '$350K', 'cloud credits'),
 'cloudflare': ('Cloudflare', 'up to', '$350K', 'in credits'),
 'microsoftazure': ('Microsoft Azure', 'up to', '$150K', 'cloud credits'),
 'alibabacloud': ('Alibaba Cloud', '', '$120K', 'credits for 1 year'),
 'amazonwebservices': ('AWS Activate', 'up to', '$100K', 'in credits'),
 'posthog': ('PostHog', '', '$50K', 'credits for 1 year'),
 'databricks': ('Databricks', '', '$21K', 'credits for 1 year'),
 'deepgram': ('Deepgram', '', '$15K', 'credits over 12 months'),
 'algolia': ('Algolia', '', '$10K', 'credits for 1 year'),
 'intercom': ('Fin by Intercom', '', '$6.5K', 'AI agent credits'),
 'qwen': ('Qwen AI', '', '$5K', 'credits for 1 year'),
 'snowflake': ('Snowflake', '', '$1,250', 'in credits'),
 'openai': ('OpenAI', '', '$1K', 'model credits'),
 'claude': ('Claude', '', '$1K', 'model credits'),
 'mongodb': ('MongoDB', '', '$500', 'credits for 1 year'),
 'gitlab': ('GitLab', '', '1 year', 'Ultimate plan, free'),
 'datadog': ('Datadog', '', '1 year', 'Pro plan, free'),
 'retool': ('Retool', '', '1 year', 'Team plan, free'),
 'auth0': ('Auth0', '', '12 months', 'free'),
 'mixpanel': ('Mixpanel', '', '1 year', 'free'),
 'sentry': ('Sentry', '', '6 months', 'Teams plan, free'),
 'jetbrains': ('JetBrains', '', '6 months', 'free, then 50% off'),
 'notion': ('Notion', '', '3 months', 'Business plan with AI, free'),
}
FEAT = {
 'generic':     ['googlecloud','amazonwebservices','microsoftazure','cloudflare','alibabacloud','posthog'],
 'tech':        ['googlecloud','amazonwebservices','microsoftazure','cloudflare','openai','claude'],
 'engineering': ['amazonwebservices','googlecloud','cloudflare','datadog','gitlab','sentry'],
 'product':     ['posthog','intercom','mixpanel','notion','openai','claude'],
 'data':        ['databricks','posthog','snowflake','mongodb','algolia','qwen'],
}
REST = {
 'generic':     ['databricks','openai','claude','deepgram','datadog','gitlab','algolia','intercom','qwen','snowflake','mongodb','retool','auth0','mixpanel','sentry','jetbrains','notion'],
 'tech':        ['alibabacloud','posthog','databricks','datadog','deepgram','gitlab','sentry','snowflake','retool','qwen','intercom','auth0','algolia','mongodb','mixpanel','jetbrains','notion'],
 'engineering': ['microsoftazure','alibabacloud','retool','jetbrains','auth0','databricks','mongodb','posthog','openai','claude','deepgram','snowflake','algolia','qwen','intercom','mixpanel','notion'],
 'product':     ['googlecloud','amazonwebservices','microsoftazure','cloudflare','alibabacloud','deepgram','algolia','databricks','retool','auth0','snowflake','mongodb','qwen','datadog','gitlab','sentry','jetbrains'],
 'data':        ['googlecloud','amazonwebservices','microsoftazure','cloudflare','alibabacloud','mixpanel','openai','claude','deepgram','intercom','retool','datadog','gitlab','sentry','auth0','jetbrains','notion'],
}
for k in ICPS:
    assert sorted(FEAT[k] + REST[k]) == sorted(DEALS), k
deal_tiles = ''.join(
    f'<article class="deal" data-slug="{s}"><div class="deal-top">{logo(s)}<span class="deal-name">{html.escape(n)}</span></div>'
    f'<div class="deal-val">{("<small>"+p+"</small>") if p else ""}<b>{html.escape(v)}</b><span>{html.escape(sub)}</span></div></article>'
    for s, (n, p, v, sub) in DEALS.items())
voucher_logos = ''.join(f'<div class="v-logos" data-vg="{k}">' + ''.join(f'<span>{logo(s)}<em>{html.escape(DEALS[s][0])}</em></span>' for s in FEAT[k]) + '</div>' for k in ICPS)

rows = list(csv.DictReader(open(os.path.expanduser('~/Downloads/deals.csv'), encoding='utf-8-sig'), delimiter=';'))
N_DEALS = len(rows)
all_rows = ''.join('<li><b>' + html.escape(r['product_name'].strip()) + '</b><span>' + html.escape(r['title'].strip().replace(' // ', '; ')) + '</span></li>'
                   for r in sorted(rows, key=lambda r: r['product_name'].strip().lower()))

# ---------- agenda ----------
TALK = {
 'x10': ["Engineering for Indian peaks: festive sales, 9:15 AM trading, IPL traffic, UPI spikes",
         "Scaling across patchy networks, low-end devices and tier-2/3 markets",
         "Where AI helped forecasting, capacity planning and incident response, and where it added complexity",
         "What to slow down, switch off or simplify when everything can't stay live",
         "Architecture decisions scaled companies are now reversing for AI workloads"],
 'ai': ["From pilot to tens of millions of users: what changes in architecture and cost",
        "Cost per query as a design constraint: model routing, caching and batching",
        "Latency on Indian networks and low-end Android phones: on-device vs cloud",
        "Handling Hinglish, vernacular and noisy input at scale",
        "Drift, regressions and fallback plans in production",
        "What to build and what to rent in the AI serving layer"],
 'ver': ["What changes when 30 to 50% of production code is AI-assisted",
         "Code ships faster than review, testing and security can keep up",
         "Measuring real gains: release frequency, rework, defects, rollbacks",
         "Incidents caused by AI-generated code and what teams changed after",
         "The skills engineers need to check AI-written code"],
 'reset': ["Which roles are shrinking, growing or being redesigned",
           "Where small teams move faster and where they become fragile",
           "Who mentors and reviews as the mid-senior layer thins",
           "What hiring for freshers tests in 2026",
           "How senior, staff and EM roles now differ",
           "Where CTOs would add headcount in 2027"],
 'data': ["Why data stacks built for dashboards fall short for production AI",
          "Fragmented customer IDs, messy catalogues, duplicates and unclear ownership",
          "Where real-time data pays off in payments, commerce, logistics and fraud",
          "Which datasets models and agents should be allowed to read",
          "Keeping each customer's data separate in multi-tenant AI",
          "The first fixes to make your data AI-ready"],
}
PICKS = {'tech': ['ai', 'reset', 'data'], 'engineering': ['x10', 'ver', 'reset'], 'product': ['ai', 'data'], 'data': ['data', 'ai']}
PICK_LABEL = {'tech': 'Picked for CTOs', 'engineering': 'Picked for engineering leaders', 'product': 'Picked for product leaders', 'data': 'Picked for data &amp; AI leaders'}

def session(time, kind, title, speakers, key):
    picks = ' '.join(k for k, v in PICKS.items() if key in v)
    faces = ''.join(face(k, 'face sm') for k in speakers)
    names = ''.join(f'<span><b>{html.escape(SPK[k][0])}</b> {html.escape(SPK[k][2])}</span>' for k in speakers)
    tags = ''.join(f'<span class="pick" data-vi="{k}">{PICK_LABEL[k]}</span>' for k in PICKS if key in PICKS[k])
    pts = ''.join(f'<li>{html.escape(p)}</li>' for p in TALK[key])
    return f'''<article class="sess" data-pick="{picks}">
  <div class="sess-time">{time}</div>
  <div class="sess-card">
    <div class="sess-meta"><span class="kind">{kind}</span>{tags}</div>
    <h3>{html.escape(title)}</h3>
    <div class="sess-who"><span class="faces">{faces}</span><div class="names">{names}</div></div>
    <details><summary>Topics</summary><ul>{pts}</ul></details>
  </div>
</article>'''
def tba(time, kind, text):
    return f'''<article class="sess tba">
  <div class="sess-time">{time}</div>
  <div class="sess-card"><span class="ghosts"><span class="ghost">{icon("user")}</span><span class="ghost">{icon("user")}</span></span><div><span class="kind">{kind}</span><p>{text}</p></div></div>
</article>'''
def brk(time, ic, text):
    return f'<article class="sess brk"><div class="sess-time">{time}</div><div class="sess-card">{icon(ic)}<span>{text}</span></div></article>'

agenda = ''.join([
 session('10:00', 'Panel · 30 min', "The Architecture Of 10X: Engineering For India's Next Scale Curve", ['vikas','ish','vaibhav'], 'x10'),
 session('10:30', 'Panel · 30 min', 'Building AI Systems For Indian Scale', ['nitin'], 'ai'),
 tba('11:00', 'Fireside · 25 min', 'Speaker to be revealed'),
 session('11:30', 'Panel · 30 min', 'Why Verification Is Becoming The New Engineering Bottleneck', [], 'ver'),
 session('12:00', 'Panel · 30 min', 'The Great Engineering Reset: Teams, Talent &amp; Leadership After AI'.replace('&amp;', '&'), ['kausal'], 'reset'),
 tba('12:30', 'Fireside · 25 min', 'Speaker to be revealed'),
 session('13:00', 'Panel · 30 min', 'Building The Data Foundation For AI At Scale', ['anil','thiya'], 'data'),
 brk('13:30', 'utensils', 'Executive lunch'),
 tba('15:00', 'Panels &amp; firesides', 'Afternoon sessions to be revealed'),
 brk('18:00', 'wine', 'Dinner and networking'),
])
agenda = agenda.replace('<div class="names"></div>', '<div class="names"><span>Speakers to be revealed</span></div>').replace('<span class="faces"></span>', '<span class="ghosts"><span class="ghost">' + icon("user") + '</span><span class="ghost">' + icon("user") + '</span></span>')

# ---------- per-audience copy ----------
FACES = {
 'generic': ['rish','khilan','nitin','kiran','ram'],
 'tech': ['nitin','ram','kausal','vinay','anil'],
 'engineering': ['kiran','thiya','vikas','ish','vaibhav'],
 'product': ['khilan','rish','ashok','anuj','nitin'],
 'data': ['anil','thiya','kiran','nitin','anuj'],
}
hero_faces = ''.join(f'<span class="faces" data-vf="{k}">' + ''.join(face(s) for s in v) + '</span>' for k, v in FACES.items())

VARS = {
 '{{V_WORD}}': V(generic='tech', tech='tech', engineering='engineering', product='product', data='data &amp; AI'),
 '{{V_SUB}}': V(
   generic="One day of sessions and networking with 175 tech, product and data leaders.",
   tech="One day with CTOs from ShareChat, Cashfree, INDmoney and more on AI systems, costs and teams.",
   engineering="One day with engineering leaders from Meesho, Eightfold, Kuku and more on scale, reliability and teams.",
   product="One day with product and tech leaders from Razorpay, Rapido, ShareChat and more on shipping AI to millions.",
   data="One day with data and AI leaders from Fibe, Eightfold, Meesho and more on building data for AI."),
 '{{V_SPEAKERS_LINE}}': V(
   generic='Rapido, Razorpay, ShareChat, Meesho, Cashfree',
   tech='ShareChat, Cashfree, INDmoney, Netradyne, Fibe',
   engineering='Meesho, Eightfold, Kuku, InsuranceDekho, Shadowfax',
   product='Razorpay, Rapido, IDfy, OnFinance AI, ShareChat',
   data='Fibe, Eightfold, Meesho, ShareChat, OnFinance AI'),
 '{{V_NET_H2}}': V(
   generic="Meet 175 leaders from India's top tech companies",
   tech='Meet 175 tech leaders, from CTOs to heads of platform',
   engineering='Meet 175 engineering and tech leaders',
   product='Meet 175 product, tech and data leaders',
   data='Meet 175 data, AI and tech leaders'),
 '{{V_BONUS_SUB}}': V(
   generic='Credits and free plans on cloud, AI, data and developer tools. {{N_DEALS}} deals in total.',
   tech='Cloud and AI model credits first, plus {{N_DEALS}} deals across data and developer tools.',
   engineering='Cloud, observability and developer tool credits first, plus {{N_DEALS}} deals in total.',
   product='Analytics, AI and product tools first, plus cloud credits. {{N_DEALS}} deals in total.',
   data='Data platform and analytics credits first, plus cloud and AI. {{N_DEALS}} deals in total.'),
 '{{V_AGENDA_SUB}}': V(
   generic='Wednesday, 30 September. Sessions from 10:00, dinner and networking from 18:00.',
   tech='Sessions picked for CTOs are expanded. Wednesday, 30 September, from 10:00.',
   engineering='Sessions picked for engineering leaders are expanded. Wednesday, 30 September, from 10:00.',
   product='Sessions picked for product leaders are expanded. Wednesday, 30 September, from 10:00.',
   data='Sessions picked for data and AI leaders are expanded. Wednesday, 30 September, from 10:00.'),
 '{{V_SPK_SUB}}': V(
   generic='CTOs, founders and product leaders from companies running at India scale.',
   tech='CTOs first, followed by engineering, product and founders.',
   engineering='Engineering and platform leaders first, followed by CTOs.',
   product='Product leaders and founders first, followed by CTOs.',
   data='Data and AI leaders first, followed by CTOs.'),
}

FAQ_FIRST = {
 'generic': ('Who is this summit for?', "Leaders at VP level and above who run engineering, platform, product, data or AI at India's growth and late-stage tech companies."),
 'tech': ("I'm a founder-CTO. Is this for me?", 'Yes. CTOs and founder-CTOs make up a large part of the room, alongside the engineering, product and data leaders they work with.'),
 'engineering': ('I run engineering or platform, not the whole tech team. Is this for me?', 'Yes, if you lead at VP level or above. Engineering leaders are the largest group in the room.'),
 'product': ('I lead product, not engineering. Is this for me?', 'Yes. Product leaders are part of the room by design, and two sessions are picked for you on the agenda.'),
 'data': ('I lead data or AI. Is this for me?', 'Yes. Data and AI leaders are part of the room by design, and the data foundation session is built around your work.'),
}
FAQ = [
 ("What if my application isn't approved?", 'You get a full refund within 7 working days.'),
 ('What is the $320K+ bonus?', f"Your pass unlocks {N_DEALS} partner deals: credits and free plans on tools like Google Cloud, AWS, OpenAI and Datadog. Values are each provider's listed maximum, and each provider sets its own eligibility."),
 ('Will speakers pitch products?', 'No. Sessions are led by people who run the systems they talk about.'),
 ('Is this a CIO event?', "No. It doesn't cover IT governance or digital transformation. It's for people who own a platform, product, data function or AI roadmap."),
 ('Can I transfer my pass?', "No. Once confirmed, a pass can't be transferred."),
 ("Can I add my company's GST number?", 'Yes, at checkout.'),
]
def faq_item(q, a, attr=''):
    return f'<details{attr}><summary><span>{html.escape(q)}</span>{icon("plus","ic pm")}</summary><p>{html.escape(a)}</p></details>'
faq_html = ''.join(faq_item(q, a, f' data-vb="{k}"') for k, (q, a) in FAQ_FIRST.items()) + ''.join(faq_item(q, a) for q, a in FAQ)

# ---------- audience CSS ----------
css = ['html [data-v],html [data-vb],html [data-vf],html [data-vi],html [data-vg]{display:none}']
for attr, disp in [('data-v', 'inline'), ('data-vb', 'block'), ('data-vf', 'flex'), ('data-vi', 'inline-flex'), ('data-vg', 'grid')]:
    css.append(','.join(f'html[data-icp="{k}"] [{attr}="{k}"]' for k in ICPS) + '{display:' + disp + '}')
for k in ICPS:
    for i, s in enumerate(FEAT[k]):
        css.append(f'html[data-icp="{k}"] .deal[data-slug="{s}"]{{order:{i};grid-column:span 2}}')
    css.append(','.join(f'html[data-icp="{k}"] .deal[data-slug="{s}"] .deal-val b' for s in FEAT[k]) + '{font-size:40px}')
    css.append(','.join(f'html[data-icp="{k}"] .deal[data-slug="{s}"] .lg' for s in FEAT[k]) + '{width:26px;height:26px}')
    for i, s in enumerate(REST[k]):
        css.append(f'html[data-icp="{k}"] .deal[data-slug="{s}"]{{order:{10+i}}}')
    for i, s in enumerate(SPK_ORDER[k]):
        css.append(f'html[data-icp="{k}"] .spk[data-key="{s}"]{{order:{i}}}')
for k in PICKS:
    css.append(f'html[data-icp="{k}"] .sess:not([data-pick~="{k}"]):not(.tba):not(.brk) .sess-card{{padding:16px 22px}}')
    css.append(f'html[data-icp="{k}"] .sess:not([data-pick~="{k}"]):not(.tba):not(.brk) h3{{font-size:17px;margin:6px 0 0;color:var(--muted);font-family:var(--sans);font-weight:500;letter-spacing:0}}')
    css.append(f'html[data-icp="{k}"] .sess:not([data-pick~="{k}"]):not(.tba):not(.brk) :is(.sess-who,details){{display:none}}')
    css.append(f'html[data-icp="{k}"] .sess[data-pick~="{k}"] .sess-card{{border-color:rgba(238,39,56,.5)}}')
AUD_CSS = '\n'.join(css)

page = open(HERE + '/v3_template.html').read()
REPL = {
 '{{AUD_CSS}}': AUD_CSS, '{{INC42}}': INC42, '{{ORACLE}}': ORACLE, '{{BOOK}}': BOOK, '{{SPONSOR}}': SPONSOR,
 '{{HERO_FACES}}': hero_faces, '{{VOUCHER_LOGOS}}': voucher_logos, '{{DEAL_TILES}}': deal_tiles, '{{ALL_DEALS}}': all_rows,
 '{{N_MORE}}': str(N_DEALS - len(DEALS)), '{{AGENDA}}': agenda, '{{SPEAKERS}}': spk_cards, '{{FAQ}}': faq_html,
}
REPL.update(VARS)
for k, v in REPL.items():
    page = page.replace(k, v)
page = page.replace('{{N_DEALS}}', str(N_DEALS))
page = re.sub(r'\{\{icon:([a-z0-9-]+)(?:\|([a-z ]+))?\}\}', lambda m: icon(m.group(1), m.group(2) or 'ic'), page)
assert '{{' not in page, re.findall(r'\{\{[^}]+\}\}', page)[:5]
open(ROOT + '/index.html', 'w').write(page)
print('written', len(page))
