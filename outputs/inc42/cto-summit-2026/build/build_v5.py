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
def rib_tile(k): return f'<figure class="rib-t" data-key="{k}"><img src="{img(k)}" alt="{esc(SPK[k][0])}"><figcaption><b>{esc(SPK[k][0])}</b><span>{esc(SPK[k][1])}, {esc(SPK[k][2])}</span></figcaption></figure>'
STAT_CARDS = [('30+', 'speakers'), ('10+', 'sessions'), ('175', 'tech leaders'), ('$320K+', 'in credits')]
def ribbon(icp, with_stats=False):
    order = SPK_ORDER[icp]; out = []
    for i, k in enumerate(order):
        out.append(rib_tile(k))
        if with_stats and i % 3 == 2:
            n, l = STAT_CARDS[(i // 3) % 4]
            out.append(f'<div class="rib-stat{" red" if n.startswith("$") else ""}"><b>{n}</b><span>{l}</span></div>')
    return ''.join(out)
ribbons_plain = ''.join(f'<div class="rib-belt" data-vf="{k}">{ribbon(k)}{ribbon(k)}</div>' for k in ICPS)
ribbons_stats = ''.join(f'<div class="rib-belt" data-vf="{k}">{ribbon(k, True)}{ribbon(k, True)}</div>' for k in ICPS)
spk_cards = ''.join(f'<article class="spk" data-key="{k}"><div class="spk-photo"><img src="{img(k)}" alt="{esc(SPK[k][0])}" loading="lazy"></div><div class="spk-info"><b>{esc(SPK[k][0])}</b><span>{esc(SPK[k][1])}</span><span class="co">{esc(SPK[k][2])}</span></div></article>' for k in SPK_ORDER['generic'])

# ---------- sessions (what you'll learn) ----------
SESS = [
 ('scale', '10:00', "The Architecture Of 10X: Engineering For India's Next Scale Curve", ['vikas','ish','vaibhav'], [
   'How to keep systems up during festive sales, IPL and UPI spikes',
   'What to slow down or switch off when traffic breaks your limits',
   'Which architecture choices to revisit for AI workloads']),
 ('ai', '10:30', 'Building AI Systems For Indian Scale', ['nitin'], [
   'What an AI feature really costs at millions of users',
   'When to use frontier, smaller or on-device models',
   'What to build and what to rent for AI']),
 ('code', '11:30', 'Why Verification Is Becoming The New Engineering Bottleneck', [], [
   'How to review code when AI writes a big share of it',
   'Which metrics show AI coding is actually working',
   'What teams changed after AI code caused incidents']),
 ('teams', '12:00', 'The Great Engineering Reset: Teams, Talent & Leadership After AI', ['kausal'], [
   'How to structure teams as AI takes over routine work',
   'What to test when hiring freshers now',
   'Which skills leaders should protect']),
 ('data', '13:00', 'Building The Data Foundation For AI At Scale', ['anil','thiya'], [
   'Why dashboard-era data stacks fail AI',
   'Which data problems to fix first',
   'Where real-time data is worth the cost']),
]
PICKS = {'tech': ['ai','teams','data'], 'engineering': ['scale','code','teams'], 'product': ['ai','data'], 'data': ['data','ai']}
PICK_LABEL = {'tech': 'For CTOs', 'engineering': 'For engineering leaders', 'product': 'For product leaders', 'data': 'For data &amp; AI leaders'}
sess_cards = ''
for key, time, title, spk, learn in SESS:
    tags = ''.join(f'<span class="pick" data-vi="{i}">{PICK_LABEL[i]}</span>' for i in PICKS if key in PICKS[i])
    if spk:
        who = '<div class="s-faces">' + ''.join(face(k, 'face md') for k in spk) + '</div><div class="s-names">' + ''.join(f'<span><b>{esc(SPK[k][0])}</b>{esc(SPK[k][2])}</span>' for k in spk) + '</div>'
    else:
        who = f'<div class="s-faces"><span class="ghost">{icon("user")}</span></div><div class="s-names"><span><b>Speakers</b>to be revealed</span></div>'
    sess_cards += f'''<article class="s-card" data-key="{key}">
  <div class="s-top"><span class="s-time">{time}</span><span class="s-fmt">30-min panel + live Q&amp;A</span>{tags}</div>
  <h3>{esc(title)}</h3>
  <p class="s-learn-l">You'll learn</p>
  <ul class="s-learn">{''.join(f'<li>{icon("check","ic sm")}<span>{esc(x)}</span></li>' for x in learn)}</ul>
  <div class="s-who">{who}</div>
</article>'''
sess_cards += f'''<article class="s-card s-tba" data-key="tba">
  <div class="s-top"><span class="s-time">11:00 · 12:30 · 15:00</span></div>
  <h3>Firesides and afternoon sessions</h3>
  <p class="s-tba-p">Speakers and topics to be revealed soon.</p>
  <div class="s-who"><div class="s-faces"><span class="ghost">{icon("user")}</span><span class="ghost">{icon("user")}</span><span class="ghost">{icon("user")}</span></div></div>
</article>'''
sess_css = []
for icp, keys in PICKS.items():
    order = keys + [k for k, *_ in SESS if k not in keys]
    for i, k in enumerate(order):
        sess_css.append(f'html[data-icp="{icp}"] .s-card[data-key="{k}"]{{order:{i}}}')
    sess_css.append(','.join(f'html[data-icp="{icp}"] .s-card[data-key="{k}"]' for k in keys) + '{border-color:var(--red);box-shadow:0 0 0 1px var(--red)}')

# ---------- day ----------
DAY = [
 ('10:00', 'Panels begin', 'Leaders share real systems, numbers and trade-offs, with live Q&amp;A.', 'row-2-1.jpg'),
 ('11:00', 'Fireside chats', 'One-on-one conversations with a speaker, revealed soon.', 'row-2-2.jpg'),
 ('13:30', 'Executive lunch', 'Seated roundtables with speakers and fellow leaders.', 'row-1-1.jpg'),
 ('15:00', 'Afternoon sessions and high tea', 'More panels, and time to meet people between them.', 'strip-b3.jpg'),
 ('18:00', 'Dinner and networking', 'An evening with the full room of 175 leaders.', 'row-2-3.jpg'),
]
day_stops = ''.join(f'<button type="button" class="stop" data-i="{i}"><span class="st-time">{t}</span><span class="st-dot"></span><span class="st-title">{h}</span></button>' for i, (t, h, p, im) in enumerate(DAY))
day_slides = ''.join(f'<figure class="slide{" on" if i == 0 else ""}" data-i="{i}"><img src="assets/img/{im}" alt="" loading="lazy"><figcaption><span class="sl-time">{t}</span><b>{h}</b><span>{p}</span></figcaption></figure>' for i, (t, h, p, im) in enumerate(DAY))

# ---------- bonus ----------
BARS = [('googlecloud','Google Cloud',350000,'up to $350K'),('cloudflare','Cloudflare',350000,'up to $350K'),('microsoftazure','Microsoft Azure',150000,'up to $150K'),
        ('alibabacloud','Alibaba Cloud',120000,'$120K'),('amazonwebservices','AWS Activate',100000,'up to $100K'),('posthog','PostHog',50000,'$50K'),
        ('databricks','Databricks',21000,'$21K'),('deepgram','Deepgram',15000,'$15K')]
bars = ''.join(f'<li><span class="b-name">{logo(s)}{esc(n)}</span><span class="b-track"><span class="b-fill" style="--w:{max(v/350000*100,3):.1f}%"></span></span><span class="b-val">{esc(l)}</span></li>' for s, n, v, l in BARS)
FREE = [('gitlab','GitLab','1 year free'),('datadog','Datadog','1 year free'),('retool','Retool','1 year free'),('mixpanel','Mixpanel','1 year free'),('auth0','Auth0','12 months free'),
        ('sentry','Sentry','6 months free'),('jetbrains','JetBrains','6 months free'),('notion','Notion','3 months free'),('openai','OpenAI','$1K credits'),('claude','Claude','$1K credits'),
        ('snowflake','Snowflake','$1,250 credits'),('intercom','Intercom Fin','$6.5K credits')]
free = ''.join(f'<span class="chip">{logo(s)}<b>{esc(n)}</b><em>{esc(v)}</em></span>' for s, n, v in FREE)
PICKED = {
 'generic': 'Most popular with tech teams: AWS, Google Cloud, Datadog, GitLab',
 'tech': 'Picked for CTOs: Google Cloud, AWS, Azure, OpenAI, Claude',
 'engineering': 'Picked for engineering teams: AWS, Cloudflare, Datadog, GitLab, Sentry',
 'product': 'Picked for product teams: PostHog $50K, Mixpanel, Intercom Fin, Notion',
 'data': 'Picked for data teams: Databricks $21K, Snowflake, PostHog, MongoDB',
}
picked = ''.join(f'<span data-v="{k}">{esc(v)}</span>' for k, v in PICKED.items())
picked = picked.replace('most popular', 'most popular')
rows = list(csv.DictReader(open(os.path.expanduser('~/Downloads/deals.csv'), encoding='utf-8-sig'), delimiter=';'))
N_DEALS = len(rows)
all_rows = ''.join('<li><b>' + esc(r['product_name'].strip()) + '</b><span>' + esc(r['title'].strip().replace(' // ', '; ')) + '</span></li>' for r in sorted(rows, key=lambda r: r['product_name'].strip().lower()))

# ---------- copy ----------
WORDS = [('tech', 'tech'), ('product', 'product'), ('engineering', 'engineering'), ('data', 'data &amp; AI')]
slot = '<span class="slot" id="slot">' + ''.join(f'<span class="w{" on" if i == 0 else ""}" data-k="{k}">{w}</span>' for i, (k, w) in enumerate(WORDS)) + '</span>'
VARS = {
 '{{SLOT}}': slot,
 '{{V_SUB}}': V(
   generic='One day of sessions and networking with 175 tech, product and data leaders.',
   tech='One day with CTOs from ShareChat, Cashfree and INDmoney on AI, costs and teams.',
   engineering='One day with engineering leaders from Meesho, Kuku and Shadowfax on scale and teams.',
   product='One day with leaders from Razorpay, Rapido and ShareChat on shipping AI to millions.',
   data='One day with data and AI leaders from Fibe, Eightfold and Meesho on data for AI.'),
 '{{V_SPK_LINE}}': V(generic='Rapido, Razorpay, ShareChat, Meesho', tech='ShareChat, Cashfree, INDmoney, Netradyne', engineering='Meesho, Eightfold, Kuku, Shadowfax', product='Razorpay, Rapido, IDfy, ShareChat', data='Fibe, Eightfold, Meesho, ShareChat'),
 '{{PICKED}}': picked,
}
FAQ_FIRST = {
 'generic': ('Who is this for?', 'Leaders at VP level and above in engineering, platform, product, data or AI.'),
 'tech': ("I'm a founder-CTO. Is this for me?", 'Yes. CTOs and founder-CTOs are a core part of the room.'),
 'engineering': ('I lead engineering, not the whole tech team. Is this for me?', 'Yes, at VP level or above. Engineering leaders are the largest group in the room.'),
 'product': ('I lead product. Is this for me?', 'Yes. The AI and data sessions are picked for product leaders.'),
 'data': ('I lead data or AI. Is this for me?', 'Yes. The data foundation and AI systems sessions are picked for you.'),
}
FAQ = [
 ("What if I'm not approved?", 'You get a full refund within 7 working days.'),
 ('What is the $320K+ bonus?', f'{N_DEALS} partner deals: credits and free plans on tools like AWS, Google Cloud, OpenAI and Datadog. Each provider sets its own eligibility.'),
 ('Will speakers pitch products?', 'No. Speakers run the systems they talk about.'),
 ('Can I transfer my pass?', "No. Confirmed passes can't be transferred."),
 ("Can I add my company's GST number?", 'Yes, at checkout.'),
]
def faq_item(q, a, attr=''): return f'<details{attr}><summary><span>{esc(q)}</span>{icon("plus","ic pm")}</summary><p>{esc(a)}</p></details>'
faq_html = ''.join(faq_item(q, a, f' data-vb="{k}"') for k, (q, a) in FAQ_FIRST.items()) + ''.join(faq_item(q, a) for q, a in FAQ)

css = ['html [data-v],html [data-vb],html [data-vf],html [data-vi]{display:none}']
for attr, disp in [('data-v', 'inline'), ('data-vb', 'block'), ('data-vf', 'flex'), ('data-vi', 'inline-flex')]:
    css.append(','.join(f'html[data-icp="{k}"] [{attr}="{k}"]' for k in ICPS) + '{display:' + disp + '}')
for k in ICPS:
    for i, s in enumerate(SPK_ORDER[k]):
        css.append(f'html[data-icp="{k}"] .spk[data-key="{s}"]{{order:{i}}}')
for k in ['tech', 'engineering', 'product', 'data']:
    css.append(f'html[data-icp="{k}"] .slot .w:not([data-k="{k}"]){{display:none}}')
    css.append(f'html[data-icp="{k}"] .slot .w[data-k="{k}"]{{opacity:1;transform:none}}')
AUD_CSS = '\n'.join(css + sess_css)

page = open(HERE + '/v5_template.html').read()
REPL = {'{{AUD_CSS}}': AUD_CSS, '{{INC42}}': INC42, '{{ORACLE}}': ORACLE, '{{BOOK}}': BOOK, '{{SPONSOR}}': SPONSOR,
        '{{RIB_PLAIN}}': ribbons_plain, '{{RIB_STATS}}': ribbons_stats, '{{SESS}}': sess_cards, '{{DAY_STOPS}}': day_stops, '{{DAY_SLIDES}}': day_slides,
        '{{BARS}}': bars, '{{FREE}}': free, '{{ALL_DEALS}}': all_rows, '{{SPEAKERS}}': spk_cards, '{{FAQ}}': faq_html}
REPL.update(VARS)
for k, v in REPL.items(): page = page.replace(k, v)
page = page.replace('{{N_DEALS}}', str(N_DEALS))
page = re.sub(r'\{\{icon:([a-z0-9-]+)(?:\|([a-z ]+))?\}\}', lambda m: icon(m.group(1), m.group(2) or 'ic'), page)
assert '{{' not in page, re.findall(r'\{\{[^}]+\}\}', page)[:5]
open(ROOT + '/index.html', 'w').write(page)

variants = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CTO Summit first-fold variants</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;600&display=swap">
<style>body{margin:0;background:#E6E7EA;font-family:Geist,system-ui,sans-serif;color:#15171C;padding:32px 20px 80px}.w{max-width:1440px;margin:0 auto;display:grid;gap:48px}
h1{margin:0 0 4px;font-size:24px}p{margin:0;color:#5A606B}.v{display:grid;gap:10px}.v h2{margin:0;font-size:18px}.v h2 span{color:#D11E2B}
iframe{width:100%;height:920px;border:1px solid #CFD2D8;border-radius:14px;background:#15171C}</style></head><body><div class="w">
<div><h1>First fold: 3 variations of C</h1><p>Same headline, price and CTA. Each frame is the live page at desktop width.</p></div>
<div class="v"><h2><span>C1</span> · Speaker ribbon + stats bar</h2><p>Labelled speaker row, stats bar above it, company logos below.</p><iframe src="index.html?hero=c1" scrolling="no" title="C1"></iframe></div>
<div class="v"><h2><span>C2</span> · Stats inside the ribbon</h2><p>Speaker photos and stat cards (30+ speakers, 10+ sessions, 175 leaders, $320K+) move together in one row.</p><iframe src="index.html?hero=c2" scrolling="no" title="C2"></iframe></div>
<div class="v"><h2><span>C3</span> · Two moving rows</h2><p>Speakers row and "Leaders joining from" logo row move in opposite directions, each with its own label.</p><iframe src="index.html?hero=c3" scrolling="no" title="C3"></iframe></div>
</div></body></html>'''
open(ROOT + '/first-fold-variants.html', 'w').write(variants)
print('written', len(page))
