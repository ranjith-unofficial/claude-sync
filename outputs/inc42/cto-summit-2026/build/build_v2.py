import csv, re, html, os
ROOT = os.path.expanduser('~/ClaudeDocs/inc42/cto-summit-2026')
A = ROOT + '/assets'
BOOK = 'https://events.inc42.com/cto-summit/checkout/?add-to-cart=12380'
SPONSOR = 'https://tally.so/r/44YONk?source=website'

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
    s = open(path).read()
    s = re.sub(r'<\?xml.*?\?>', '', s)
    return s.replace('<svg', f'<svg class="{cls}" aria-hidden="true"', 1)

INC42 = inline_svg(f'{A}/logos/inc42-logo-image.svg', 'inc42')
ORACLE = inline_svg(f'{A}/logos/logo01.svg', 'oracle').replace('viewBox="0 0 271 152"', 'viewBox="0 54 271 42"')

SPK = {
 'rish': ('Rishikesh SR', 'Cofounder', 'Rapido', 'Rishikesh-SR'),
 'khilan': ('Khilan Haria', 'CPO', 'Razorpay', 'Khilan-Haria'),
 'nitin': ('Nitin Jain', 'CTO', 'ShareChat & Moj', 'Nitin-Jain'),
 'kiran': ('Kiran Kumar', 'Head, Platform Eng & Agentic AI', 'Meesho', 'Kiran-Kumar'),
 'ram': ('Ramkumar Venkatesan', 'CTO', 'Cashfree Payments', 'Ramkumar-Venkatesan'),
 'kausal': ('Kausal Malladi', 'CTO, Investments', 'INDmoney', 'Kausal-Malladi'),
 'vaibhav': ('Vaibhav Khandelwal', 'Cofounder & CTO', 'Shadowfax', 'Vaibhav-Khandelwal'),
 'ish': ('Ish Babbar', 'Cofounder & CTO', 'InsuranceDekho', 'Ish-Babbar'),
 'vikas': ('Vikas Goyal', 'Cofounder & CTO', 'Kuku', 'Vikas-Goyal'),
 'anil': ('Anil Sinha', 'CTO', 'Fibe', 'Anil-Sinha'),
 'thiya': ('Thiyagaraj T', 'Director, Engineering', 'Eightfold', 'Thiyagaraj-T'),
 'ashok': ('Ashok Hariharan', 'CEO', 'IDfy', 'Ashok-Hariharan'),
 'vinay': ('Vinay Rai', 'EVP, Technology', 'Netradyne', 'Vinay-Rai'),
 'anuj': ('Anuj Srivastava', 'Cofounder & CEO', 'OnFinance AI', 'Anuj-Srivastava'),
}
def img(key): return f'assets/img/speakers/{SPK[key][3]}.jpg'
def face(key, cls='face'):
    n = html.escape(SPK[key][0])
    return f'<span class="{cls}" style="background-image:url({img(key)})" role="img" aria-label="{n}"></span>'

SESSIONS_ON = {'nitin': '10:30', 'kausal': '12:00', 'vaibhav': '10:00', 'ish': '10:00', 'vikas': '10:00', 'anil': '13:00', 'thiya': '13:00'}

# ---------- deals ----------
DEALS = [
 # slug, name, cat, prefix, value, sub, featured
 ('googlecloud', 'Google Cloud', 'cloud', 'up to', '$350K', 'cloud credits', True),
 ('cloudflare', 'Cloudflare', 'cloud', 'up to', '$350K', 'in credits', True),
 ('microsoftazure', 'Microsoft Azure', 'cloud', 'up to', '$150K', 'cloud credits', True),
 ('alibabacloud', 'Alibaba Cloud', 'cloud', '', '$120K', 'credits for 1 year', True),
 ('amazonwebservices', 'AWS Activate', 'cloud', 'up to', '$100K', 'in credits', True),
 ('posthog', 'PostHog', 'data', '', '$50K', 'credits for 1 year', True),
 ('databricks', 'Databricks', 'data', '', '$21K', 'credits, 1 year', False),
 ('deepgram', 'Deepgram', 'ai', '', '$15K', 'credits, 12 months', False),
 ('algolia', 'Algolia', 'data', '', '$10K', 'credits, 1 year', False),
 ('intercom', 'Fin by Intercom', 'ai', '', '$6.5K', 'AI agent credits', False),
 ('qwen', 'Qwen AI', 'ai', '', '$5K', 'credits, 1 year', False),
 ('snowflake', 'Snowflake', 'data', '', '$1,250', 'in credits', False),
 ('openai', 'OpenAI', 'ai', '', '$1K', 'model credits', False),
 ('claude', 'Claude', 'ai', '', '$1K', 'model credits', False),
 ('mongodb', 'MongoDB', 'data', '', '$500', 'credits, 1 year', False),
 ('gitlab', 'GitLab', 'dev', '', '1 year', 'Ultimate, free', False),
 ('datadog', 'Datadog', 'dev', '', '1 year', 'Pro plan, free', False),
 ('retool', 'Retool', 'dev', '', '1 year', 'Team plan, free', False),
 ('auth0', 'Auth0', 'dev', '', '12 mo', 'free', False),
 ('mixpanel', 'Mixpanel', 'data', '', '1 year', 'free', False),
 ('sentry', 'Sentry', 'dev', '', '6 mo', 'Teams plan, free', False),
 ('jetbrains', 'JetBrains', 'dev', '', '6 mo', 'free, then 50% off', False),
 ('notion', 'Notion', 'dev', '', '3 mo', 'Business + AI, free', False),
]
def deal_tile(d):
    slug, name, cat, pre, val, sub, feat = d
    pre_html = f'<small>{pre}</small>' if pre else ''
    return (f'<article class="deal{" feat" if feat else ""}" data-cat="{cat}" data-slug="{slug}">'
            f'<div class="deal-top">{logo(slug)}<span class="deal-name">{html.escape(name)}</span></div>'
            f'<div class="deal-val">{pre_html}<b>{html.escape(val)}</b><span>{html.escape(sub)}</span></div></article>')
deal_tiles = ''.join(deal_tile(d) for d in DEALS)

rows = list(csv.DictReader(open(os.path.expanduser('~/Downloads/deals.csv'), encoding='utf-8-sig'), delimiter=';'))
all_rows = ''.join('<li><b>' + html.escape(r['product_name'].strip()) + '</b><span>' + html.escape(r['title'].strip().replace(' // ', '; ')) + '</span></li>'
                   for r in sorted(rows, key=lambda r: r['product_name'].strip().lower()))
N_DEALS = len(rows)

# ---------- agenda ----------
TALK = {
 'x10': ["Engineering for Indian peaks: festive sales, 9:15 AM trading, IPL traffic, UPI spikes",
         "Scaling across patchy networks, low-end devices and tier-2/3 markets",
         "Where AI helped forecasting, capacity planning and incident response, and where it added complexity",
         "The graceful-degradation playbook: what to slow, switch off or simplify",
         "Architecture decisions scaled companies are now reversing for AI workloads"],
 'ai': ["From pilot to tens of millions of users: what changes in architecture and cost",
        "The inference bill as a design constraint: routing, caching, batching",
        "Latency on Indian networks and low-end Androids: on-device vs cloud",
        "Hinglish, vernacular and noisy input at scale",
        "Drift, regressions and fallback architecture in production",
        "Build vs rent for the AI serving layer"],
 'ver': ["What changes when 30–50% of production code is AI-assisted",
         "Code is faster; review, testing and security capacity isn't",
         "Measuring real gains: release frequency, rework, defects, rollbacks",
         "Incidents caused by AI-generated code and what teams changed",
         "The skills verification now demands"],
 'reset': ["The AI-era org chart: roles shrinking, growing, redesigned",
           "Where lean teams create speed and where they create fragility",
           "The missing middle: who trains the next generation",
           "Hiring in 2026: what the fresher bar tests now",
           "The new career ladder for senior, staff and EM",
           "The 2027 talent mix"],
 'data': ["Why dashboard-era data stacks fail production AI",
          "Fragmented IDs, messy catalogues, duplicates and unclear ownership",
          "Where real-time data actually pays off",
          "Data-access design for models and agents",
          "Multi-tenant AI and per-customer isolation",
          "The first fixes to become AI-ready"],
}
PICKS = {'tech': ('ai','reset','data'), 'engineering': ('x10','ver','reset'), 'product': ('ai','data')}
PICK_LABEL = {'tech': 'Top pick for CTOs', 'engineering': 'Top pick for engineering leaders', 'product': 'Top pick for product leaders'}
def session(time, kind, title, speakers, take, key):
    faces = ''.join(face(k, 'face sm') for k in speakers)
    names = ', '.join(f'{SPK[k][0]} <em>{html.escape(SPK[k][2])}</em>' for k in speakers) if speakers else '<em>Speakers announcing soon</em>'
    pts = ''.join(f'<li>{html.escape(p)}</li>' for p in TALK[key])
    picks = ''.join(f'<span class="pick" data-vi="{icp}">{icon("sparkles","ic xs")}{PICK_LABEL[icp]}</span>' for icp, ks in PICKS.items() if key in ks)
    return f'''<article class="sess">
  <div class="sess-time"><span>{time}</span></div>
  <div class="sess-card">
    <div class="sess-meta"><span class="tag">{kind}</span>{picks}</div>
    <h3>{html.escape(title)}</h3>
    <div class="sess-who">{('<span class="faces">'+faces+'</span>') if speakers else ''}<p>{names}</p></div>
    <p class="take">{icon("sparkles","ic sm")}<span>{take}</span></p>
    <details><summary>What's covered</summary><ul>{pts}</ul></details>
  </div>
</article>'''
def slim(time, ic, text, cls=''):
    return f'<article class="sess slim {cls}"><div class="sess-time"><span>{time}</span></div><div class="sess-slim">{icon(ic,"ic")}<span>{text}</span></div></article>'

agenda = ''.join([
 session('10:00', 'Panel', "The Architecture Of 10X: Engineering For India's Next Scale Curve", ['vikas','ish','vaibhav'], 'Take back a playbook for your peak day', 'x10'),
 session('10:30', 'Panel', 'Building AI Systems For Indian Scale', ['nitin'], 'Take back a cost model for AI in production', 'ai'),
 slim('11:00', 'mic', 'Fireside chat · announcing soon'),
 session('11:30', 'Panel', 'Why Verification Is Becoming The New Engineering Bottleneck', [], 'Take back the metrics that prove AI coding works', 'ver'),
 session('12:00', 'Panel', 'The Great Engineering Reset: Teams, Talent & Leadership After AI', ['kausal'], 'Take back a view of your 2027 team', 'reset'),
 slim('12:30', 'mic', 'Fireside chat · announcing soon'),
 session('13:00', 'Panel', 'Building The Data Foundation For AI At Scale', ['anil','thiya'], 'Take back your first data fixes for AI', 'data'),
 slim('13:30', 'utensils', 'Executive lunch', 'soft'),
 slim('15:00', 'mic', 'Afternoon panels &amp; firesides · announcing soon'),
 slim('18:00', 'wine', 'Dinner &amp; networking', 'soft'),
])

ORDER = ['rish','khilan','nitin','kiran','ram','kausal','vaibhav','ish','vikas','anil','thiya','ashok','vinay','anuj']
spk_cards = ''.join(f'''<article class="spk" data-key="{k}">
  <div class="spk-photo"><img src="{img(k)}" alt="{html.escape(SPK[k][0])}" loading="lazy"></div>
  <div class="spk-info"><b>{html.escape(SPK[k][0])}</b><span>{html.escape(SPK[k][1])}</span><span class="co">{html.escape(SPK[k][2])}</span>{('<span class="on">'+icon("mic","ic xs")+'On stage '+SESSIONS_ON[k]+'</span>') if k in SESSIONS_ON else ''}</div>
</article>''' for k in ORDER)

FACES = {
 'generic': (['rish','khilan','nitin','kiran','ram','kausal'], 'Speakers from <b>Rapido, Razorpay, ShareChat, Meesho</b> &amp; more'),
 'tech': (['nitin','kausal','ram','anil','vikas','ish'], 'CTOs from <b>ShareChat &amp; Moj, INDmoney, Cashfree, Fibe</b> &amp; more'),
 'engineering': (['vikas','ish','vaibhav','kiran','thiya','vinay'], 'Engineering leaders from <b>Kuku, Shadowfax, Meesho, Eightfold</b> &amp; more'),
 'product': (['khilan','rish','ashok','anuj','nitin','kiran'], 'Leaders from <b>Razorpay, Rapido, IDfy, ShareChat</b> &amp; more'),
}
hero_faces = ''.join(f'<div class="faces-row" data-vf="{icp}"><span class="faces">' + ''.join(face(k,'face') for k in ks) + f'</span><p>{txt}</p></div>' for icp,(ks,txt) in FACES.items())

def V(**kw):
    return ''.join(f'<span data-v="{k}">{v}</span>' for k, v in kw.items())
VARS = {
 '{{V_PILL}}': V(generic='AI leadership summit · Invite-only', tech='For CTOs &amp; tech leaders · Invite-only', engineering='For engineering &amp; platform leaders · Invite-only', product='For product leaders · Invite-only'),
 '{{V_WORD}}': V(generic='tech', tech='tech', engineering='engineering', product='product'),
 '{{V_SUB}}': V(generic="A day on building with AI at India's scale, with the people actually doing it.",
               tech="AI systems, inference costs and the org after AI, from the CTOs running India's biggest platforms.",
               engineering="Scaling for India's peaks, the new verification bottleneck and engineering teams after AI.",
               product="How AI features go from pilot to tens of millions of Indian users, from the leaders shipping them."),
 '{{V_ROOM_H2}}': V(generic='Everyone here runs tech at scale.', tech="Your peers run tech at India's scale.", engineering="Your peers run engineering at India's scale.", product='Sit with the tech leaders your roadmap depends on.'),
 '{{V_ROOM_LEDE}}': V(generic='Hand-picked by our editorial team. The conversations that never happen on stage happen here.',
                     tech='CTOs and founder-CTOs, hand-picked by our editorial team. The conversations that never happen on stage happen here.',
                     engineering='Heads of engineering and platform, hand-picked by our editorial team. The conversations that never happen on stage happen here.',
                     product='Product, data and AI leaders alongside the engineering leaders they build with. Hand-picked by our editorial team.'),
 '{{V_DEALS_LEDE}}': V(generic='Unlock credits and free plans on the cloud, AI and dev tools your teams already use.',
                      tech='Cloud, AI model and data credits for the stack you already run.',
                      engineering='Credits and free plans across cloud, observability and dev tooling.',
                      product='Analytics, AI and productivity tools for your product team, plus cloud credits.'),
 '{{V_DEALS_ORDER}}': '',
}

FAQ_FIRST = {
 'generic': ('Who is this summit for?', "Leaders, VP and above, who run engineering, platform, product, data or AI teams at India's growth and late-stage tech companies."),
 'tech': ("I'm a founder-CTO. Is this for me?", 'Yes. CTOs and founder-CTOs are at the core of the room, alongside the engineering, product, data and AI leaders who work with them.'),
 'engineering': ('I run engineering or platform, not the whole tech org. Is this for me?', 'Yes, if you lead at VP level or above. Engineering leaders are the largest group in the room.'),
 'product': ('I lead product, not engineering. Is this for me?', 'Yes. Product leaders are part of the room by design. The name says CTO; the room is five functions wide.'),
}
FAQ = [
 ("What if my application isn't approved?", 'You get a full refund within 7 working days.'),
 ('How do the $320K+ in deals work?', f"Your pass unlocks {N_DEALS} partner deals: credits and free plans on cloud, AI, data and dev tools. Values are each provider's listed maximum; eligibility varies by provider."),
 ('Will there be vendor pitches?', 'No. Every session is led by operators sharing real systems, numbers and trade-offs.'),
 ('Is this a CIO event?', "No. We don't cover IT governance or digital transformation. If you own a platform, product, data function or AI roadmap, this is your room."),
 ('Can I transfer my pass?', "No. Once confirmed, a pass can't be shared or transferred."),
 ("Can I add my company's GST number?", 'Yes, add it at checkout.'),
]
def faq_item(q, a, attr=''):
    return f'<details{attr}><summary><span>{html.escape(q)}</span>{icon("plus","ic pm")}</summary><p>{html.escape(a)}</p></details>'
faq_html = ''.join(faq_item(q, a, f' data-vb="{k}"') for k, (q, a) in FAQ_FIRST.items()) + ''.join(faq_item(q, a) for q, a in FAQ)

page = open(os.path.dirname(os.path.abspath(__file__)) + '/v2_template.html').read()
for k, v in {
 '{{INC42}}': INC42, '{{ORACLE}}': ORACLE, '{{BOOK}}': BOOK, '{{SPONSOR}}': SPONSOR,
 '{{HERO_FACES}}': hero_faces, '{{DEAL_TILES}}': deal_tiles, '{{ALL_DEALS}}': all_rows, '{{N_DEALS}}': str(N_DEALS),
 '{{N_MORE}}': str(N_DEALS - len(DEALS)), '{{AGENDA}}': agenda, '{{SPEAKERS}}': spk_cards, '{{FAQ}}': faq_html,
 **VARS}.items():
    page = page.replace(k, v)
page = re.sub(r'\{\{icon:([a-z0-9-]+)(?:\|([a-z ]+))?\}\}', lambda m: icon(m.group(1), m.group(2) or 'ic'), page)
assert '{{' not in page, re.findall(r'\{\{[^}]+\}\}', page)[:5]
open(ROOT + '/index.html', 'w').write(page)
print('written', len(page))
