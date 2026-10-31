"""Builds the area and service pages in public/ from the content below.

Run from the repo root:  python3 tools/build_pages.py
The output is plain HTML that gets committed, so Cloudflare needs no build step.
"""
import json
from html import escape
from pathlib import Path

SITE = "https://rapidemergencyresponse.co.uk"
PHONE, PHONE_TEL = "07543 599184", "+447543599184"
WA = "https://wa.me/447543599184?text=Hi%20Ryan%2C%20I%20need%20a%20plumber.%20"
GBP = "https://www.google.com/maps?cid=15060057663350423494"
OUT = Path(__file__).resolve().parent.parent / "public"

REVIEWS = [
    ("The definition of a Real Tradesman. I called Ryan at short notice after my original plumber let me down… He came out and did a great job. Would highly recommend. Local, professional and reasonable.", "Shaun S.", "Kitchen sink, tap & radiator"),
    ("Ryan was reliable and very honest. Turned up when he said he would and traced our leak quickly and fixed it, which filled us with confidence. Very reasonable rate too!", "Chris G.", "Leak repair"),
    ("Excellent job!! Love my new bathroom, completed to a very high standard. The team are professional, polite, respectful and hardworking. I would highly recommend.", "Joanne C.", "Bathroom"),
]

AREAS = [
    dict(slug="plumber-leeds", name="Leeds", pc="LS1 to LS28", review=1,
         pc_table=[("LS11", "Beeston, Holbeck"), ("LS12", "Armley, Farnley, Wortley"), ("LS13", "Bramley, Rodley"),
                   ("LS10", "Hunslet, Middleton, Belle Isle"), ("LS27", "Morley, Gildersome, Churwell"), ("LS28", "Pudsey, Farsley, Calverley, Stanningley"),
                   ("LS5", "Kirkstall"), ("LS6", "Headingley, Hyde Park"), ("LS8", "Roundhay, Harehills"), ("LS18", "Horsforth"),
                   ("LS26", "Rothwell"), ("LS1, LS2", "City centre")],
         faq_extra=[("Is there a plumber near me in Leeds right now?", "If you're anywhere in LS1 to LS28, yes. Ryan takes emergency call-outs across Leeds 24/7. Call 07543 599184 and he'll tell you honestly how soon he can be there."),
                    ("Do you cover the city centre and flats?", "Yes, including flats and rented properties. Landlords and letting agents can call too.")],
         places=["Beeston", "Holbeck", "Hunslet", "Armley", "Bramley", "Farnley", "Wortley", "Kirkstall", "Headingley", "Roundhay", "Horsforth", "Rothwell"],
         intro="Ryan covers all of Leeds, LS1 to LS28, day and night. South and west Leeds are the quickest to reach from his base in Batley, but a leak in Headingley or a blocked toilet in Roundhay gets the same call-out. One call gets you a qualified local plumber, not a national call centre.",
         extra="Big firms often send whoever's free. With Rapid Emergency Response you get Ryan every time: City & Guilds qualified since 2002, DBS checked, with five-star Google reviews and the price agreed before any work starts. Leeds has a lot of older terraces and back-to-backs where pipework has been added to over the years, and Ryan traces the real cause rather than patching the symptom."),
    dict(slug="plumber-batley", name="Batley", pc="WF17", review=0,
         places=["Batley town centre", "Birstall", "Staincliffe", "Carlinghow", "Hanging Heaton", "Soothill", "Healey"],
         intro="Batley is home. Ryan is based on South Bank Road, so a call-out anywhere in WF17 is usually the quickest job of his day. If water is coming through a ceiling in Birstall or a toilet won't stop running in Staincliffe, you're talking to a plumber who lives just round the corner.",
         extra="Being local also means no inflated travel charges and no waiting for someone driving in from the other side of Leeds. Ryan agrees the price with you before he starts, and you deal with him directly from the first call to the finished job."),
    dict(slug="plumber-morley", name="Morley", pc="LS27", review=1,
         places=["Morley town centre", "Gildersome", "Churwell", "Bruntcliffe"],
         intro="Morley sits just up the road from Ryan's base in Batley, so LS27 is one of the areas he covers most. Whether it's a burst pipe in Gildersome, a dripping tap in Churwell or a leak you can't find, one call gets a City & Guilds qualified plumber to your door.",
         extra="Many homes in Morley are older stone terraces and semis with pipework that's been added to over the years. Ryan traces leaks properly, fixes the cause rather than the symptom, and tells you plainly if anything else needs looking at."),
    dict(slug="plumber-drighlington", name="Drighlington", pc="BD11", review=0,
         places=["Drighlington village", "Adwalton", "Birkenshaw"],
         intro="Drighlington and Adwalton are a short drive from Ryan's base in Batley, which makes BD11 easy to reach when something goes wrong. Leaks, blocked toilets, broken taps and new appliances plumbed in: one local plumber for all of it.",
         extra="Smaller villages often get overlooked by the bigger Leeds firms. Ryan covers Drighlington, Adwalton and Birkenshaw as standard, agrees the price before starting, and leaves the place tidy."),
    dict(slug="plumber-pudsey", name="Pudsey", pc="LS28", review=1,
         places=["Pudsey town centre", "Farsley", "Stanningley", "Fulneck"],
         intro="Ryan covers Pudsey and the rest of LS28, from Farsley to Stanningley. If you've got water where it shouldn't be, a toilet that won't flush or a tap that won't stop dripping, call or send a photo on WhatsApp and he'll tell you what it is and whether it's urgent.",
         extra="You deal with Ryan directly, not a call centre. He's held his City & Guilds plumbing NVQ since 2002, is DBS checked, and agrees the price with you before any work starts."),
    dict(slug="plumber-calverley", name="Calverley", pc="LS28", review=2,
         places=["Calverley village", "Farsley"],
         intro="Ryan covers Calverley and the surrounding LS28 area for emergency call-outs and everyday plumbing repairs. Leaks traced and fixed, toilets and taps repaired or replaced, sinks and appliances plumbed in neatly.",
         extra="Calverley has a lot of older stone properties where pipework can be tucked away in awkward places. Ryan takes the time to find the real cause, explains it in plain English and agrees the price before starting."),
]

SERVICES = [
    dict(slug="emergency-plumber", name="Emergency plumber", h1="Emergency plumber", img="van.webp",
         img_alt="Rapid Emergency Response Plumbing van",
         title="24/7 Emergency Plumber Leeds & Batley | Rapid Emergency Response",
         desc="24/7 emergency plumber for Leeds, Batley, Morley, Pudsey, Drighlington and Calverley. Leaks, burst pipes and overflowing toilets. Call Ryan on 07543 599184.",
         intro="Water coming through the ceiling, a burst pipe, or a toilet overflowing? Call Ryan on 07543 599184, day or night, weekends included. He's a City & Guilds qualified plumber based in Batley, covering Leeds, Morley, Drighlington, Pudsey and Calverley.",
         now=["Turn off your stopcock. It's usually under the kitchen sink, where the mains pipe comes in. Turn it clockwise until it stops.",
              "If water is near lights or sockets, switch off the electrics at the consumer unit and don't touch wet switches.",
              "Open your cold taps to drain the system and catch drips with buckets and towels.",
              "Take a photo or short video and send it on WhatsApp, so Ryan knows what he's walking into."],
         fixes=["Burst and frozen pipes", "Water leaking through ceilings", "Overflowing or blocked toilets", "Leaking tanks, cisterns and valves", "Stopcocks that won't turn off"],
         faqs=[("Do you come out at night and at weekends?", "Yes. Ryan takes emergency call-outs 24 hours a day, 7 days a week, including bank holidays. Call 07543 599184."),
               ("What counts as a plumbing emergency?", "Anything where water is escaping and you can't stop it, water near electrics, a toilet that's blocked or overflowing when it's the only one in the house, or no water at all. If you're not sure, send a photo on WhatsApp and Ryan will tell you whether it's urgent."),
               ("How much does an emergency call-out cost?", "Ryan agrees the price with you before any work starts, so there are no surprises. Call and describe the problem, or send a photo, and he'll give you a clear price."),
               ("Do you do boiler or gas work?", "No. Ryan is a plumber, not a Gas Safe engineer, so boilers and gas appliances need a Gas Safe registered engineer.")]),
    dict(slug="leak-repair", name="Leak & burst pipe repair", h1="Leak & burst pipe repair", img="tap-fitting.webp",
         img_alt="Plumber tightening the fitting under a chrome tap",
         title="Leak & Burst Pipe Repair Leeds | Rapid Emergency Response",
         desc="Leaks traced and fixed, burst pipes repaired. Local plumber covering Leeds, Batley, Morley, Pudsey, Drighlington and Calverley. Price agreed first.",
         intro="A leak that's left gets worse, and water damage costs far more than the repair. Ryan traces where the water is really coming from, stops it, and puts in a proper permanent fix.",
         now=["Turn off the stopcock if water is escaping and you can't stop it at an isolation valve.",
              "Look for an isolation valve on the pipe feeding the leaking tap, toilet or appliance. A quarter turn with a flat screwdriver shuts it off.",
              "Put a bucket under the drip and move anything valuable out of the way.",
              "Note when it started and what was running at the time. It helps track the leak down faster."],
         fixes=["Burst and frozen pipes", "Leaks traced and fixed", "Water through ceilings", "Leaking joints, valves and fittings", "Leaking waste pipes and traps"],
         faqs=[("Can you find a leak I can't see?", "Usually, yes. Ryan works back from where the water shows up, checks the likely joints, valves and pipe runs, and explains what he's found before fixing it."),
               ("Will you need to lift floorboards?", "Only if the leak is under the floor. Ryan will tell you before doing anything and agree the price first."),
               ("Can you deal with a frozen pipe?", "Yes. Don't use a blowtorch or boiling water on it. Turn off the stopcock and call. Frozen pipes often split, and the leak only shows once they thaw.")]),
    dict(slug="toilet-repair", name="Toilet repair & replacement", h1="Toilet repair & replacement", img="toilet.webp",
         img_alt="Newly fitted close-coupled toilet in a modern bathroom",
         title="Toilet Repair Leeds & Batley | Rapid Emergency Response",
         desc="Blocked, running or leaking toilets fixed, and new toilets fitted. Local plumber covering Leeds, Batley, Morley, Pudsey and nearby. Call 07543 599184.",
         intro="A toilet that won't stop running wastes water and money. One that's blocked or leaking can't wait. Ryan repairs flush and fill valves, clears blockages and swaps out old toilets for new ones.",
         now=["If it's overflowing, lift the cistern lid and push the float up, or turn the isolation valve on the feed pipe a quarter turn.",
              "Don't keep flushing a blocked toilet.",
              "If water is leaking round the base, stop using it and put towels down. It can rot the floor underneath."],
         fixes=["Blocked toilets cleared", "Constant running, slow fill and weak flush", "Flush and fill valve repairs", "Leaks from the cistern or around the base", "Full toilet replacement"],
         faqs=[("Why does my toilet keep running?", "Usually a worn flush valve seal or a fill valve that isn't shutting off. Both are quick repairs that don't need a new toilet."),
               ("Can you supply the new toilet?", "Yes. Ryan can supply and fit one, or fit one you've already bought. Either way the price is agreed first.")]),
    dict(slug="tap-repair", name="Tap repair & replacement", h1="Tap repair & replacement", img="tap-rapid.webp",
         img_alt="Plumber fitting a new kitchen mixer tap",
         title="Tap Repair & Replacement Leeds | Rapid Emergency Response",
         desc="Dripping, stiff or broken taps fixed, or a new kitchen or bathroom tap supplied and fitted. Local plumber for Leeds, Batley, Morley and Pudsey.",
         intro="Dripping, stiff or broken taps fixed, or a new tap supplied and fitted in your kitchen or bathroom. Ryan replaces washers, cartridges and valves, and fits kitchen mixers, basin taps, bath taps and outdoor taps.",
         now=["A dripping tap isn't an emergency, but don't overtighten it. That damages the washer or cartridge further.",
              "If it won't turn off, shut the isolation valve under the sink with a flat screwdriver, or turn off the stopcock.",
              "Send a photo of the tap on WhatsApp so Ryan can bring the right parts."],
         fixes=["Dripping and leaking taps", "Washers, cartridges and valves", "Kitchen mixer taps", "Basin and bath taps", "Outdoor taps"],
         faqs=[("Repair or replace?", "If the tap body is sound, a new washer or cartridge usually fixes it for a fraction of the cost. If it's corroded or parts aren't available, Ryan will tell you and price a replacement."),
               ("Can you fit a tap I've bought?", "Yes. Send a photo or the product link and Ryan will confirm it suits your sink and pipework.")]),
    dict(slug="sink-plumbing", name="Sinks, wastes & appliances", h1="Sinks, wastes & appliances", img="kitchen.webp",
         img_alt="Kitchen sink cabinet with new waste trap and isolation valves",
         title="Sink, Waste & Appliance Plumbing Leeds | Rapid Emergency",
         desc="Leaking waste traps, blocked sinks and washing machine or dishwasher hook-ups. Local plumber covering Leeds, Batley, Morley and Pudsey.",
         intro="Leaking sink pipework put right and new appliances plumbed in neatly. Ryan fixes leaking waste traps, sorts slow or blocked sinks, and connects washing machines and dishwashers properly.",
         now=["If a waste pipe is leaking, stop using the sink and put a bowl under the trap.",
              "Avoid chemical drain cleaners on a fully blocked sink. They can damage plastic traps and are dangerous if the pipe has to be opened.",
              "For a new appliance, check there's a cold feed and a waste connection under the sink, and send Ryan a photo."],
         fixes=["Leaking waste traps and pipework", "Slow and blocked sinks", "Washing machine and dishwasher hook-ups", "New sinks plumbed in", "Isolation valves fitted"],
         faqs=[("Can you plumb in my washing machine?", "Yes, including adding a new cold feed, valve and waste connection if there isn't one already."),
               ("My sink smells. Is that a plumbing problem?", "Often it's a dried-out or poorly fitted trap letting drain smells back up. It's a quick fix.")]),
]


def head(title, desc, path, extra_ld):
    url = SITE + "/" + path if path else SITE + "/"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n' for ld in extra_ld)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0e2a47">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="Rapid Emergency Response Plumbing">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@1,700;1,800&family=Public+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="styles.css">
{lds}</head>
<body>
"""


PHONE_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'

def _nav():
    svc = "".join(f'<a href="{s['slug']}">{s['name']}</a>' for s in SERVICES)
    ar = "".join(f'<a href="{a['slug']}">{a['name']}</a>' for a in AREAS)
    return (f'<div class="dd"><a href="/#services">Services</a><div class="dd-menu">{svc}</div></div>'
            f'<div class="dd"><a href="/#areas">Areas</a><div class="dd-menu">{ar}</div></div>'
            '<a href="/#about">About Ryan</a><a href="/#reviews">Reviews</a><a href="/#contact">Contact</a>')


NAV = _nav()

HEADER = f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="/">
      <img src="img/logo.webp" alt="Rapid Emergency Response Plumbing logo" width="58" height="58">
      <div><b>Rapid</b><small>Emergency Response Plumbing</small></div>
    </a>
    <nav class="nav" aria-label="Main">
      {NAV}
    </nav>
    <a class="btn btn-red" href="tel:{PHONE_TEL}" aria-label="Call {PHONE}">{PHONE_SVG}<span>{PHONE}</span></a>
  </div>
</header>
"""


def footer_links():
    areas = "".join(f'<a href="{a["slug"]}">Plumber in {a["name"]}</a>' for a in AREAS)
    svcs = "".join(f'<a href="{s["slug"]}">{s["name"]}</a>' for s in SERVICES)
    return f"""<nav class="foot-links" aria-label="Areas and services"><div><b>Areas</b>{areas}</div><div><b>Services</b>{svcs}</div></nav>"""


def footer():
    return f"""<footer>
  <div class="wrap">
    {footer_links()}
    <div><img src="img/logo.webp" alt="" width="40" height="40" style="border-radius:6px;margin-bottom:8px"><b>Rapid Emergency Response Plumbing</b><br>Ryan Aubrey · South Bank Road, Batley<br>{PHONE} · Plumber247@mail.com</div>
    <div><nav aria-label="Footer" style="display:flex;gap:16px"><a href="/#services">Services</a><a href="/#reviews">Reviews</a><a href="/#areas">Areas</a><a href="privacy">Privacy</a></nav><br>© 2026 Rapid Emergency Response</div>
  </div>
</footer>

<div class="callbar">
  <a class="btn btn-red" href="tel:{PHONE_TEL}">Call now · 24/7</a>
  <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
</div>
</body>
</html>
"""


def cta_card(heading):
    return f"""<div class="side-card">
          <h3>{heading}</h3>
          <p>Call Ryan or send a photo on WhatsApp. Price agreed before any work starts.</p>
          <a class="btn btn-red" href="tel:{PHONE_TEL}">{PHONE_SVG}Call {PHONE}</a>
          <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp a photo</a>
        </div>"""


def review_block(i):
    q, who, job = REVIEWS[i]
    return f"""<figure class="quote"><blockquote>{escape(q)}</blockquote><cite>{who} <span>· Google review · {escape(job)}</span></cite></figure>
        <p><a href="{GBP}" target="_blank" rel="noopener">5.0 from 5 Google reviews. Read them all →</a></p>"""


def faq_html(faqs):
    return "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faqs)


def business_ld(area_names, page_url):
    return {"@context": "https://schema.org", "@type": "Plumber", "@id": SITE + "/#business",
            "name": "Rapid Emergency Response Plumbing", "url": SITE + "/", "telephone": PHONE_TEL,
            "image": SITE + "/img/og.jpg",
            "address": {"@type": "PostalAddress", "streetAddress": "South Bank Road", "addressLocality": "Batley",
                        "addressRegion": "West Yorkshire", "postalCode": "WF17", "addressCountry": "GB"},
            "areaServed": [{"@type": "Place", "name": n} for n in area_names],
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}],
            "mainEntityOfPage": page_url}


def crumbs_ld(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + "/" + path}]}


def pc_table_html(a):
    if "pc_table" not in a:
        return ""
    rows = "".join(f"<tr><th scope=\"row\">{pc}</th><td>{escape(places)}</td></tr>" for pc, places in a["pc_table"])
    return f"""<h2>Leeds postcodes Ryan covers</h2>
        <table class="pc-table"><thead><tr><th>Postcode</th><th>Areas</th></tr></thead><tbody>{rows}</tbody></table>
        <p class="note">Plus every other LS postcode from LS1 to LS28. Not listed? <a href="tel:{PHONE_TEL}">Call and ask.</a></p>"""


def area_page(a):
    path, name = a["slug"], a["name"]
    title = f"Plumber in {name} {a['pc'] if name != 'Leeds' else ''} | Rapid Emergency Response".replace("  ", " ")
    desc = f"24/7 local plumber in {name}, {a['pc']}. Ryan Aubrey, City & Guilds qualified and DBS checked, fixes leaks, burst pipes, toilets and taps. Price agreed first. Call {PHONE}."
    common = [("Do you cover " + p + "?", f"Yes. {p} is part of the {name} area Ryan covers as standard.") for p in a["places"][1:2]]
    faqs = a.get("faq_extra", []) + common + [
        (f"How quickly can you get to {name}?", f"It depends on what Ryan is already working on, so call and he'll give you an honest time. {name} is a short drive from his base in Batley."),
        ("Do you come out at night and at weekends?", f"Yes. Ryan takes emergency call-outs in {name} 24 hours a day, 7 days a week."),
        ("Is the price agreed before you start?", "Yes, always. Ryan explains what's wrong and agrees the price with you before any work starts."),
        ("Do you do boiler or gas work?", "No. Boilers and gas appliances need a Gas Safe registered engineer."),
    ]
    svc_links = "".join(f'<li><a href="{s["slug"]}">{s["name"]}<small>in {name}</small></a></li>' for s in SERVICES)
    other = "".join(f'<li><a href="{o["slug"]}">Plumber in {o["name"]}<small>{o["pc"]}</small></a></li>' for o in AREAS if o is not a)
    places = "".join(f"<li>{escape(p)}</li>" for p in a["places"])
    lds = [business_ld([name], SITE + "/" + path), crumbs_ld(f"Plumber in {name}", path)]
    return head(title, desc, path, lds) + HEADER + f"""
<main>
  <section class="page-hero">
    <div class="wrap two-col">
      <div class="prose">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/#areas">Areas</a> › {name}</nav>
        <span class="status">Taking emergency call-outs now, 24/7</span>
        <h1>Plumber in <em>{name}</em></h1>
        <p class="lede">{escape(a['intro'])}</p>
        <p>{escape(a['extra'])}</p>
        <h2>Areas around {name} we cover</h2>
        <ul class="chips">{places}</ul>
        <p class="note">Postcode {a['pc']}. Just outside? <a href="tel:{PHONE_TEL}">Call anyway and ask.</a></p>

        {pc_table_html(a)}
        <h2>What Ryan fixes in {name}</h2>
        <ul class="link-grid">{svc_links}</ul>

        <h2>Why {name} customers call Ryan</h2>
        <ul>
          <li>City &amp; Guilds NVQ Level 2 in plumbing, held since 2002 (certificate Q1027228)</li>
          <li>Emergency call-outs 24/7, nights and weekends included</li>
          <li>DBS checked, August 2026</li>
          <li>Price agreed before any work starts</li>
          <li>You deal with Ryan directly, from the first call to the finished job</li>
        </ul>

        <h2>Questions from {name} customers</h2>
        <div class="faq">{faq_html(faqs)}</div>
      </div>
      <aside class="side">
        {cta_card(f"Need a plumber in {name}?")}
        {review_block(a['review'])}
      </aside>
    </div>
  </section>
  <section class="contact" style="padding-block:48px">
    <div class="wrap">
      <h2 style="font-size:2rem;margin-bottom:16px">Other areas Ryan covers</h2>
      <ul class="link-grid">{other}</ul>
    </div>
  </section>
</main>
""" + footer()


def service_page(s):
    path = s["slug"]
    area_links = "".join(f'<li><a href="{a["slug"]}">{a["name"]}<small>{a["pc"]}</small></a></li>' for a in AREAS)
    other = "".join(f'<li><a href="{o["slug"]}">{o["name"]}</a></li>' for o in SERVICES if o is not s)
    now = "".join(f"<li>{escape(x)}</li>" for x in s["now"])
    fixes = "".join(f"<li>{escape(x)}</li>" for x in s["fixes"])
    lds = [business_ld([a["name"] for a in AREAS], SITE + "/" + path), crumbs_ld(s["name"], path)]
    review = 1 if path == "leak-repair" else 0
    return head(s["title"], s["desc"], path, lds) + HEADER + f"""
<main>
  <section class="page-hero">
    <div class="wrap two-col">
      <div class="prose">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/#services">Services</a> › {escape(s['name'])}</nav>
        <span class="eyebrow">Leeds · Batley · Morley · Pudsey</span>
        <h1>{escape(s['h1'])}</h1>
        <p class="lede">{escape(s['intro'])}</p>

        <h2>What to do right now</h2>
        <ol style="margin:0;padding-left:1.2em;display:grid;gap:6px">{now}</ol>

        <h2>What Ryan fixes</h2>
        <ul>{fixes}</ul>

        <h2>Areas covered</h2>
        <ul class="link-grid">{area_links}</ul>

        <h2>Common questions</h2>
        <div class="faq">{faq_html(s['faqs'])}</div>
      </div>
      <aside class="side">
        <img class="side-img" src="img/{s['img']}" alt="{escape(s['img_alt'])}" width="1400" height="933">
        {cta_card("Call Ryan now")}
        {review_block(review)}
      </aside>
    </div>
  </section>
  <section class="contact" style="padding-block:48px">
    <div class="wrap">
      <h2 style="font-size:2rem;margin-bottom:16px">Other services</h2>
      <ul class="link-grid">{other}</ul>
    </div>
  </section>
</main>
""" + footer()


def sitemap():
    urls = [""] + [a["slug"] for a in AREAS] + [s["slug"] for s in SERVICES] + ["privacy"]
    body = "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-10-27</lastmod></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


if __name__ == "__main__":
    for a in AREAS:
        (OUT / f"{a['slug']}.html").write_text(area_page(a), encoding="utf-8")
    for s in SERVICES:
        (OUT / f"{s['slug']}.html").write_text(service_page(s), encoding="utf-8")
    (OUT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    # Same list under a fresh name, so Search Console fetches it anew instead of reusing a stale error.
    (OUT / "sitemap-pages.xml").write_text(sitemap(), encoding="utf-8")
    print(f"Built {len(AREAS)} area pages, {len(SERVICES)} service pages and sitemap.xml")
