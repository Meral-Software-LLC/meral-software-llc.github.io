#!/usr/bin/env python3
"""Generates every page of meralsoftware.com. Edit APPS / copy below, then run `python3 gen.py`."""
import pathlib, shutil

ROOT = pathlib.Path(__file__).parent
COMPANY = "Meral Software"
LEGAL = "Meral Software LLC"
EMAIL = "support@meralsoftware.com"
DOMAIN = "https://meralsoftware.com"
DATE = "September 20, 2026"
STORE = "https://apps.apple.com/app/id{id}"

# Simple line icons, 24x24 viewBox, stroke = currentColor.
ICONS = {
 "store": '<path d="M3 10 5 4h14l2 6"/><path d="M3 10a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M5 12v8h14v-8M10 20v-5h4v5"/>',
 "building": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M11 21v-3h2v3"/>',
 "cube":  '<path d="M12 3 4 7v10l8 4 8-4V7l-8-4z"/><path d="M4 7l8 4 8-4M12 11v10"/>',
 "box":   '<path d="M3 8l9-5 9 5v8l-9 5-9-5z"/><path d="M3 8l9 5 9-5M12 13v8M7.5 5.5l9 5"/>',
 "frame": '<rect x="4" y="4" width="16" height="16" rx="1.5"/><rect x="8" y="8" width="8" height="8"/><path d="M12 2v2"/>',
 "cue":   '<circle cx="7" cy="17" r="3"/><path d="M9.5 14.5 21 3M17 3h4v4"/>',
 "book":  '<path d="M4 4h9a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M16 7a3 3 0 0 1 3-3h1v14h-1a2 2 0 0 0-2 2"/><path d="M7 9h5M7 12h5"/>',
 "glove": '<path d="M7 11V6a2 2 0 1 1 4 0v4M11 9V5a2 2 0 1 1 4 0v5"/><path d="M15 10V7a2 2 0 1 1 4 0v6a6 6 0 0 1-6 6h-1a5 5 0 0 1-5-5v-2a2 2 0 1 1 4 0"/>',
 "golf":  '<circle cx="12" cy="8" r="5"/><path d="M12 13v8M8 21h8"/><path d="M10 7h.01M13 6h.01M12 9.5h.01"/>',
}

APPS = [
 dict(slug="marketplace", name="Meral Property Marketplace", icon="store", live=True, url="https://meralproperty.com", privacy="https://meralproperty.com/privacy/",
      platform="Web", tag="Find your next rental, or list your own."),
 dict(slug="management", name="Meral Property Management", icon="building", live=True, url="https://pro.meralproperty.com", privacy="https://pro.meralproperty.com/privacy/",
      platform="Web · iOS · Android · Desktop", tag="Property management software for owners, tenants and vendors."),
 dict(slug="opencube", name="OpenCube", icon="cube", live=True, store_id="6814315632",
      platform="iPhone · iPad", price="Free", unlock="OpenCube Pro, $1.99 once",
      tag="Scan, solve and learn the cube.",
      blurb="Point the camera at your cube and OpenCube reads it, shows a short solution, and teaches Beginner, CFOP and Roux step by step. A solve timer with scrambles, inspection and per-method statistics rounds it out. Seven languages, no internet required.",
      features=["Reads all six faces through the camera","Short solutions from a two-phase solver","Beginner, CFOP and Roux lessons with 3D animations","Timer with scrambles, inspection and per-method stats"],
      perms=[("Camera","used only to read the colours on your cube while you scan. Frames are processed live and never stored or sent anywhere.")]),
]

def href(a, up=""):
    return a.get("url") or f'{up}{a["slug"]}/'

def icon(name, size=28):
    return f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def store_link(a, cls="btn primary"):
    if a.get("store_id"):
        return f'<a class="{cls}" href="{STORE.format(id=a["store_id"])}">{APPLE} Download on the App Store</a>'
    return f'<span class="{cls} disabled">Coming soon</span>'

APPLE = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.7c0-2.5 2-3.7 2.1-3.8-1.2-1.7-3-1.9-3.6-2-1.5-.2-3 .9-3.8.9-.8 0-2-.9-3.3-.8-1.7 0-3.2 1-4.1 2.5-1.8 3-.5 7.6 1.3 10.1.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8s2 .8 3.3.8c1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.9-1.1-2.9-4.1zM14 5.3c.7-.8 1.1-2 1-3.1-1 0-2.2.7-2.9 1.5-.6.7-1.2 1.9-1 3 1.1.1 2.2-.6 2.9-1.4z"/></svg>'

def shell(title, body, depth=0, desc="", active=""):
    up = "../"*depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="theme-color" content="#f7f6f2">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="{up or './'}"><img class="brand-logo" src="{up}logo-mark.svg" width="36" height="36" alt="">{COMPANY}</a>
  <nav aria-label="Main navigation">
    <a href="{up}#apps" class="{'active' if active=='apps' else ''}">Products</a>
    <a href="{up}#principles">Our approach</a>
    <a href="{up}support.html" class="{'active' if active=='support' else ''}">Support</a>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site">
  <div class="cols">
    <div>
      <a class="brand" href="{up or './'}"><img class="brand-logo" src="{up}logo-mark.svg" width="36" height="36" alt="">{COMPANY}</a>
      <p class="muted">Apps and software for property and for play, from Meral Software.</p>
    </div>
    <div>
      <h4>Apps</h4>
      {''.join(f'<a href="{href(a, up)}">{a["name"]}</a>' for a in APPS)}
    </div>
    <div>
      <h4>Company</h4>
      <a href="{up}support.html">Support</a>
      <a href="{up}privacy.html">Privacy</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
  <p class="legal">© 2026 {LEGAL}. Apple, the Apple logo, iPhone, iPad and Apple Watch are trademarks of Apple Inc.</p>
</footer>
</body>
</html>
"""

def privacy_body(app=None):
    perms = ""
    if app:
        perms = "<h2>Device permissions</h2><ul>" + "".join(f"<li><strong>{p}</strong> — {t}</li>" for p,t in app["perms"]) + "</ul>"
        paid = f"<h2>Purchases</h2><p>{app['name']} is free to download. A single one-time purchase ({app['unlock']}) unlocks the full app. Payment is handled entirely by Apple through the App Store. We never see your payment details and receive no personal information from a purchase.</p>"
    else:
        return f"""
<article class="doc">
<p class="eyebrow">Privacy</p>
<h1>Privacy policies</h1>
<p class="muted">Last updated {DATE}</p>
<p>Each Meral Software product has its own privacy policy describing what it collects and why.</p>
<ul class="linklist">{''.join(f'<li><a href="{a.get("privacy") or href(a)+"privacy.html"}">{a["name"]}</a> <span class="muted">— {a["tag"]}</span></li>' for a in APPS)}</ul>
<h2>Contact</h2>
<p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</article>
"""
    subject = app["name"]
    return f"""
<article class="doc">
<p class="eyebrow">Privacy policy{' · '+app['name'] if app else ''}</p>
<h1>{subject} collect{'s' if app else ''} no data.</h1>
<p class="muted">Last updated {DATE}</p>
<p>Not usage analytics, not crash reports, not an email address. The app works entirely on your device and works without an internet connection.</p>
<h2>What stays on your device</h2>
<p>Anything the app saves, such as your history, settings or scans, is stored only in the app's own storage on your device and in your device backups if you have those turned on. Delete the app and it is gone.</p>
{perms}
{paid}
<h2>Third parties</h2>
<p>The app contains no third-party code, advertising or tracking of any kind. It sends data to no one, including us.</p>
<h2>Children</h2>
<p>Because the app collects no data, it collects no data from children either.</p>
<h2>Changes</h2>
<p>If this policy ever changes, the new version will be posted on this page with a new date. The app itself cannot contact you, so it cannot notify you.</p>
<h2>Contact</h2>
<p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</article>
"""

def product_art(a):
    if a['slug'] == 'marketplace':
        return '<div class="house-scene" aria-hidden="true"><span class="sun"></span><div class="house"><div class="roof"></div><div class="house-wall"><i></i><i></i><b></b></div></div><div class="listing-label"><span class="status-dot"></span> A place to call home <span>↗</span></div></div>'
    if a['slug'] == 'management':
        return '<div class="dashboard-art" aria-hidden="true"><div class="dash-sidebar"><b>M</b><i></i><i></i><i></i></div><div class="dash-main"><span class="dash-heading">Your properties, connected.</span><div class="dash-stats"><div><small>Properties</small><b>12</b></div><div><small>Occupancy</small><b>94<span>%</span></b></div></div><div class="chart">'+''.join(f'<i style="--height:{h}%"></i>' for h in [30,46,39,60,51,72,64,85,76,96])+'</div><div class="dash-lines"><i></i><i></i></div></div></div>'
    return '<div class="cube-scene" aria-hidden="true"><div class="cube-art">'+''.join('<i></i>' for _ in range(9))+'</div><span class="cube-orbit orbit-one"></span><span class="cube-orbit orbit-two"></span><span class="cube-spark">✦</span><span class="cube-caption">Your next aha moment.</span></div>'

def app_card(a):
    category = {'marketplace':'FIND YOUR PLACE', 'management':'MANAGE WITH CLARITY', 'opencube':'MAKE YOUR NEXT MOVE'}.get(a['slug'], 'EXPLORE SOMETHING NEW')
    action = 'Explore the app' if not a.get('url') else 'Visit the platform'
    status = '' if a['live'] else '<span class="pill">Coming soon</span>'
    return f"""<a class="product-card {a['slug']}" href="{href(a)}">
      <div class="product-art">{product_art(a)}{status}</div>
      <div class="product-copy"><p class="product-category">{category}</p><h3>{a['name']}</h3><p>{a['tag']}</p><div class="product-bottom"><span class="meta">{a['platform']}</span><span class="product-arrow" aria-hidden="true">↗</span></div><span class="product-action">{action} <span aria-hidden="true">↗</span></span></div>
    </a>"""

# ---------- index ----------
live = [a for a in APPS if a["live"]]
hero_app = next(a for a in APPS if a["slug"] == "opencube")
index = f"""
<section class="hero studio-hero">
  <div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> Independent minds. Thoughtful software.</p>
  <h1>Big ideas.<br>Useful software.<br><span>A little more color.</span></h1>
  <p class="lead">From finding your next home to solving your next cube. We make software that brings a little clarity to your everyday.</p>
  <div class="actions"><a class="btn primary" href="#apps">Explore our products <span aria-hidden="true">↗</span></a><a class="text-link" href="#principles">Meet Meral <span aria-hidden="true">↓</span></a></div>
  <p class="hero-note">Built for real life. Made by Meral Software.</p></div>
  <div class="hero-art" aria-hidden="true"><div class="art-grid"></div><span class="art-caption">A small studio. A world of possibilities.</span><div class="art-tile tile-property">{icon('building',48)}<span>Spaces to thrive.</span></div><div class="art-tile tile-cube">{icon('cube',62)}<span>Room to play.</span></div><div class="art-tile tile-spark">✳</div><span class="art-label">IDEAS → EVERYDAY</span><span class="art-dot"></span></div>
</section>
<section id="apps" class="section products-section">
  <div class="section-head"><div><p class="eyebrow">THE MERAL COLLECTION</p><h2>Good tools. Great possibilities.</h2></div><p class="muted">For the practical.<br>And the playful.</p></div>
  <div class="product-grid">{''.join(app_card(a) for a in APPS)}</div>
  <div class="collection-note"><span class="mini-spark" aria-hidden="true">✳</span><p>A growing collection of thoughtful software.<br><span class="muted">More ideas are taking shape. Stay curious.</span></p><a href="mailto:{EMAIL}">Have an idea? Say hello <span aria-hidden="true">↗</span></a></div>
</section>
<section id="principles" class="section approach-section">
  <div class="section-head"><div><p class="eyebrow">OUR APPROACH</p><h2>Small studio.<br>High standards.</h2></div><p class="approach-intro">Different products. The same care.<br>We build things we’re proud to put our name on.</p></div>
  <div class="principles"><div><span class="principle-number">01 /</span><h3>Purpose comes first.</h3><p>Every product starts with a real need. We keep the experience focused, so you can get on with what matters.</p></div><div><span class="principle-number">02 /</span><h3>Clarity, always.</h3><p>Simple experiences and clear privacy policies. You should understand your software, and what happens to your data.</p></div><div><span class="principle-number">03 /</span><h3>At home on your device.</h3><p>Native Apple apps and fast web platforms. Thoughtful details that make every interaction feel right.</p></div></div>
</section>
<section class="contact-banner"><div><p class="eyebrow">LET’S TALK</p><h2>Good software starts<br>with a conversation.</h2></div><a class="btn" href="mailto:{EMAIL}">Say hello <span aria-hidden="true">↗</span></a></section>
"""
(ROOT/"index.html").write_text(shell(f"{COMPANY} · Property software and apps", index, 0,
    "Meral Software builds Meral Property, a property marketplace and management software, and focused apps such as OpenCube.", active="apps"), encoding="utf-8")

# ---------- support ----------
support = f"""
<article class="doc">
<p class="eyebrow">Support</p>
<h1>We answer every message.</h1>
<p class="lead">Email <a href="mailto:{EMAIL}">{EMAIL}</a>. Include the product, your device model and the OS version, and we can usually sort it out in one reply.</p>
<h2>Products</h2>
<ul class="linklist">{''.join(f'<li><a href="{href(a)}">{a["name"]}</a> <span class="muted">— {a["tag"]}</span></li>' for a in APPS)}</ul>
<h2>Purchases and refunds</h2>
<p>App Store purchases are handled by Apple. To restore a purchase on a new device, open the app's settings and tap Restore Purchases. For refunds, use <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>; Apple decides those, not us.</p>
</article>
"""
(ROOT/"support.html").write_text(shell(f"Support · {COMPANY}", support, 0, "Support for Meral Software apps.", active="support"), encoding="utf-8")
(ROOT/"privacy.html").write_text(shell(f"Privacy · {COMPANY}", privacy_body(), 0, "Privacy policies for Meral Software products."), encoding="utf-8")

# ---------- per app ----------
for a in APPS:
    if a.get("url"): continue
    d = ROOT/a["slug"]; d.mkdir(exist_ok=True)
    body = f"""
<section class="hero app-hero"><div class="app-intro">
  <span class="glyph large">{icon(a['icon'], 36)}</span>
  <p class="eyebrow">{a['platform']}</p>
  <h1>{a['name']}</h1>
  <p class="lead">{a['tag']}</p>
  <p class="actions">{store_link(a)} <a class="btn" href="#support">Support</a></p></div><div class="app-visual opencube">{product_art(a)}</div>
</section>
<section class="section two-col">
  <div>
    <h2>About</h2>
    <p>{a['blurb']}</p>
    <ul class="features">{''.join(f'<li>{f}</li>' for f in a['features'])}</ul>
  </div>
  <aside class="facts">
    <dl>
      <dt>Price</dt><dd>{a['price']}</dd>
      <dt>Unlock</dt><dd>{a['unlock']}</dd>
      <dt>Devices</dt><dd>{a['platform']}</dd>
      <dt>Internet</dt><dd>Not required</dd>
      <dt>Data collected</dt><dd>None</dd>
    </dl>
  </aside>
</section>
<section id="support" class="section">
  <h2>Support</h2>
  <p>Something not working, or an idea? Email <a href="mailto:{EMAIL}?subject={a['name']}">{EMAIL}</a> with your device model and OS version.</p>
  <h2>Privacy</h2>
  <p>{a['name']} collects no data and works entirely on your device. <a href="privacy.html">Read the {a['name']} privacy policy.</a></p>
  <h3>Permissions it asks for</h3>
  <ul>{''.join(f'<li><strong>{p}</strong> — {t}</li>' for p,t in a['perms'])}</ul>
</section>
"""
    (d/"index.html").write_text(shell(f"{a['name']} · {COMPANY}", body, 1, f"{a['name']}: {a['tag']} By {COMPANY}."), encoding="utf-8")
    (d/"privacy.html").write_text(shell(f"{a['name']} privacy policy · {COMPANY}", privacy_body(a), 1, f"Privacy policy for {a['name']}: no data collected."), encoding="utf-8")

# ---------- assets ----------
(ROOT/"favicon.svg").write_text((ROOT/"logo-mark.svg").read_text(encoding="utf-8"), encoding="utf-8")
(ROOT/".nojekyll").write_text("", encoding="utf-8")
print("generated", len(APPS), "apps")
