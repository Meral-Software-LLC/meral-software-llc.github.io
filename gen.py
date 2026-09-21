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
 "cube":  '<path d="M12 3 4 7v10l8 4 8-4V7l-8-4z"/><path d="M4 7l8 4 8-4M12 11v10"/>',
 "box":   '<path d="M3 8l9-5 9 5v8l-9 5-9-5z"/><path d="M3 8l9 5 9-5M12 13v8M7.5 5.5l9 5"/>',
 "frame": '<rect x="4" y="4" width="16" height="16" rx="1.5"/><rect x="8" y="8" width="8" height="8"/><path d="M12 2v2"/>',
 "cue":   '<circle cx="7" cy="17" r="3"/><path d="M9.5 14.5 21 3M17 3h4v4"/>',
 "book":  '<path d="M4 4h9a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M16 7a3 3 0 0 1 3-3h1v14h-1a2 2 0 0 0-2 2"/><path d="M7 9h5M7 12h5"/>',
 "glove": '<path d="M7 11V6a2 2 0 1 1 4 0v4M11 9V5a2 2 0 1 1 4 0v5"/><path d="M15 10V7a2 2 0 1 1 4 0v6a6 6 0 0 1-6 6h-1a5 5 0 0 1-5-5v-2a2 2 0 1 1 4 0"/>',
 "golf":  '<circle cx="12" cy="8" r="5"/><path d="M12 13v8M8 21h8"/><path d="M10 7h.01M13 6h.01M12 9.5h.01"/>',
}

APPS = [
 dict(slug="opencube", name="OpenCube", icon="cube", live=True, store_id="6814315632",
      platform="iPhone · iPad", price="Free", unlock="OpenCube Pro, $1.99 once",
      tag="Scan, solve and learn the cube.",
      blurb="Point the camera at your cube and OpenCube reads it, shows a short solution, and teaches Beginner, CFOP and Roux step by step. A solve timer with scrambles, inspection and per-method statistics rounds it out. Seven languages, no internet required.",
      features=["Reads all six faces through the camera","Short solutions from a two-phase solver","Beginner, CFOP and Roux lessons with 3D animations","Timer with scrambles, inspection and per-method stats"],
      perms=[("Camera","used only to read the colours on your cube while you scan. Frames are processed live and never stored or sent anywhere.")]),
 dict(slug="openpack", name="OpenPack", icon="box", live=False, store_id=None,
      platform="iPhone with LiDAR", price="Free", unlock="$4.99 once",
      tag="Will it fit? Scan both and find out.",
      blurb="OpenPack measures an object and a space with the LiDAR scanner, then tells you whether one fits in the other, with a 3D preview you can turn.",
      features=["Scan any object into a measured 3D shape","Scan a trunk, bin, doorway or shelf","A clear yes or no, with the preview to prove it"],
      perms=[("Camera and LiDAR","used to measure objects and spaces on the device. Scans are stored only on your device.")]),
 dict(slug="hang", name="Hang", icon="frame", live=False, store_id=None,
      platform="iPhone with LiDAR", price="Free", unlock="$4.99 once",
      tag="Hang pictures straight, first time.",
      blurb="Scan a wall, arrange your frames to scale, and get exact nail positions with a live level guide while you hammer.",
      features=["Scan the wall and lay out frames to scale","Nail positions in centimetres or inches","Live level guide"],
      perms=[("Camera and LiDAR","used to measure your wall on the device."),("Motion sensors","used for the level guide.")]),
 dict(slug="pocketsight", name="PocketSight", icon="cue", live=False, store_id=None,
      platform="iPhone", price="Free", unlock="$4.99 once",
      tag="See the shot before you take it.",
      blurb="A live aiming overlay for pool, drawn over the real table through your camera: ghost ball, aiming line and predicted path.",
      features=["Ghost-ball aiming line over the real table","Predicted path for object and cue ball","Hide-the-line drill to train your eye"],
      perms=[("Camera","used to see the table and balls. Frames are processed live on the device and never stored or sent anywhere.")]),
 dict(slug="marginalia", name="Marginalia", icon="book", live=False, store_id=None,
      platform="iPad · Mac", price="Free", unlock="$9.99 once",
      tag="Ask the page a question, in your own handwriting.",
      blurb="A PDF reader for iPad. Handwrite a question in the margin and get an answer grounded only in that document, with page citations, entirely on the device.",
      features=["A proper PDF reader with Apple Pencil annotation","Handwritten questions, cited answers","Nothing leaves the iPad"],
      perms=[("Files","you choose which PDFs to open; they are indexed and stored only on your device.")]),
 dict(slug="punch", name="Punch", icon="glove", live=False, store_id=None,
      platform="Apple Watch", price="Free", unlock="$4.99 once",
      tag="Bag work, counted by your watch.",
      blurb="Counts and classifies punches from Apple Watch motion during bag work, with per-round fatigue trends. No straps, no trackers.",
      features=["Punch count from the watch alone","Jab, cross, hook and uppercut","Per-round fatigue drop-off"],
      perms=[("Motion sensors","read on the watch during a session."),("Health","Punch can record workouts to the Health app if you allow it. Health data is never read for any other purpose and never leaves your device.")]),
 dict(slug="tempomaster", name="TempoMaster", icon="golf", live=False, store_id=None,
      platform="Apple Watch · iPhone", price="Free", unlock="$3.99 once",
      tag="A steady putting stroke, from your wrist.",
      blurb="Measures putting tempo and face rotation from Apple Watch motion, with a haptic tempo trainer and a progress view on the phone.",
      features=["Back-to-forward tempo ratio for every stroke","Face rotation and consistency","Haptic tempo trainer on the wrist"],
      perms=[("Motion sensors","read on the watch during practice."),("Health","TempoMaster can record workouts to the Health app if you allow it. Health data never leaves your device.")]),
]

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
<meta name="theme-color" content="#0b0c10">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="site">
  <a class="brand" href="{up}"><span class="mark">{icon('cube',18)}</span>{COMPANY}</a>
  <nav>
    <a href="{up}#apps" class="{'active' if active=='apps' else ''}">Apps</a>
    <a href="{up}#principles">Principles</a>
    <a href="{up}support.html" class="{'active' if active=='support' else ''}">Support</a>
  </nav>
</header>
<main>
{body}
</main>
<footer class="site">
  <div class="cols">
    <div>
      <a class="brand" href="{up}"><span class="mark">{icon('cube',18)}</span>{COMPANY}</a>
      <p class="muted">Focused apps for iPhone, iPad and Apple Watch that work entirely on your device.</p>
    </div>
    <div>
      <h4>Apps</h4>
      {''.join(f'<a href="{up}{a["slug"]}/">{a["name"]}</a>' for a in APPS)}
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
        paid = "<h2>Purchases</h2><p>Our apps are free to download and each offers one single one-time purchase. Payment is handled entirely by Apple through the App Store. We never see your payment details and receive no personal information from a purchase.</p>"
    subject = app["name"] if app else "Our apps"
    return f"""
<article class="doc">
<p class="eyebrow">Privacy policy{' · '+app['name'] if app else ''}</p>
<h1>{subject} collect{'s' if app else ''} no data.</h1>
<p class="muted">Last updated {DATE}</p>
<p>Not usage analytics, not crash reports, not an email address. There are no accounts to create and no servers to talk to. Every one of our apps works entirely on your device and works without an internet connection.</p>
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

def app_card(a):
    status = '' if a["live"] else '<span class="pill">Coming soon</span>'
    return f"""<a class="card" href="{a['slug']}/">
  <div class="card-top"><span class="glyph">{icon(a['icon'])}</span>{status}</div>
  <h3>{a['name']}</h3>
  <p>{a['tag']}</p>
  <span class="meta">{a['platform']}</span>
</a>"""

# ---------- index ----------
live = [a for a in APPS if a["live"]]
hero_app = live[0] if live else APPS[0]
index = f"""
<section class="hero">
  <p class="eyebrow">Independent software studio</p>
  <h1>Apps that stay on your device.</h1>
  <p class="lead">We make small, focused apps for iPhone, iPad and Apple Watch. No accounts, no subscriptions, no data collection. Download for free, pay once if you want more.</p>
  <p class="actions"><a class="btn primary" href="#apps">See the apps</a> <a class="btn" href="{hero_app['slug']}/">{hero_app['name']}, our latest {'↗' if hero_app['live'] else ''}</a></p>
</section>

<section id="apps" class="section">
  <div class="section-head"><h2>The apps</h2><p class="muted">One job each, done properly.</p></div>
  <div class="grid">{''.join(app_card(a) for a in APPS)}</div>
</section>

<section id="principles" class="section">
  <div class="section-head"><h2>How we build</h2><p class="muted">The same four rules in every app.</p></div>
  <div class="principles">
    <div><h3>On device, always</h3><p>Camera, LiDAR and motion data are processed on the phone or watch and never uploaded. Every app works in airplane mode.</p></div>
    <div><h3>No accounts</h3><p>Nothing to sign up for, nothing to remember. Open the app and use it.</p></div>
    <div><h3>Pay once</h3><p>Each app is free to try and has one purchase that unlocks it forever. No subscriptions, no ads, no tip jars.</p></div>
    <div><h3>Native to Apple platforms</h3><p>Built with Swift and SwiftUI, using the sensors and frameworks each device already has. Fast, small and at home on your device.</p></div>
  </div>
</section>
"""
(ROOT/"index.html").write_text(shell(f"{COMPANY} · Apps that stay on your device", index, 0,
    "Meral Software makes focused iPhone, iPad and Apple Watch apps with no accounts, no subscriptions and no data collection.", active="apps"))

# ---------- support ----------
support = f"""
<article class="doc">
<p class="eyebrow">Support</p>
<h1>We answer every message.</h1>
<p class="lead">Email <a href="mailto:{EMAIL}">{EMAIL}</a>. Include the app, your device model and the iOS or watchOS version, and we can usually sort it out in one reply.</p>
<h2>Per-app support pages</h2>
<ul class="linklist">{''.join(f'<li><a href="{a["slug"]}/">{a["name"]}</a> <span class="muted">— {a["tag"]}</span></li>' for a in APPS)}</ul>
<h2>Purchases and refunds</h2>
<p>Purchases are handled by Apple. To restore a purchase on a new device, open the app's settings and tap Restore Purchases. For refunds, use <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>; Apple decides those, not us.</p>
</article>
"""
(ROOT/"support.html").write_text(shell(f"Support · {COMPANY}", support, 0, "Support for Meral Software apps.", active="support"))
(ROOT/"privacy.html").write_text(shell(f"Privacy · {COMPANY}", privacy_body(), 0, "Privacy policy for Meral Software apps: no data collected."))

# ---------- per app ----------
for a in APPS:
    d = ROOT/a["slug"]; d.mkdir(exist_ok=True)
    body = f"""
<section class="hero app-hero">
  <span class="glyph large">{icon(a['icon'], 36)}</span>
  <p class="eyebrow">{a['platform']}</p>
  <h1>{a['name']}</h1>
  <p class="lead">{a['tag']}</p>
  <p class="actions">{store_link(a)} <a class="btn" href="#support">Support</a></p>
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
    (d/"index.html").write_text(shell(f"{a['name']} · {COMPANY}", body, 1, f"{a['name']}: {a['tag']} By {COMPANY}."))
    (d/"privacy.html").write_text(shell(f"{a['name']} privacy policy · {COMPANY}", privacy_body(a), 1, f"Privacy policy for {a['name']}: no data collected."))

# ---------- assets ----------
(ROOT/"favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#0b0c10"/><g fill="none" stroke="#4cd964" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" transform="translate(2 2) scale(.84)">{ICONS["cube"]}</g></svg>')
(ROOT/"style.css").write_text("""
:root{
  --bg:#0b0c10;--bg2:#101218;--surface:#151821;--line:#232733;--fg:#f4f5f7;--fg2:#a6abb8;--muted:#7b8090;
  --accent:#4cd964;--accent-ink:#06210c;--radius:18px;--max:1080px;
}
@media(prefers-color-scheme:light){:root{--bg:#fbfbfc;--bg2:#f3f4f7;--surface:#fff;--line:#e6e8ee;--fg:#111318;--fg2:#4d5260;--muted:#767b89;--accent:#1f9d3d;--accent-ink:#fff}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Inter,-apple-system,BlinkMacSystemFont,"SF Pro Text",system-ui,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3,h4{letter-spacing:-.02em;line-height:1.15;margin:0}
p{margin:0 0 1em}
.muted{color:var(--muted)}
.eyebrow{font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:12px}

/* header */
header.site{max-width:var(--max);margin:0 auto;padding:22px 24px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.brand{display:inline-flex;align-items:center;gap:10px;font-weight:700;color:var(--fg);font-size:1.02rem}
.brand:hover{text-decoration:none}
.mark{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:9px;background:var(--accent);color:var(--accent-ink)}
header nav{display:flex;gap:26px}
header nav a{color:var(--fg2);font-weight:500;font-size:.95rem}
header nav a:hover,header nav a.active{color:var(--fg);text-decoration:none}

/* layout */
main{max-width:var(--max);margin:0 auto;padding:0 24px 40px}
.section{padding:56px 0}
.section-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.section-head h2,.section h2{font-size:1.75rem}
.section h2{margin:32px 0 10px}
.section h2:first-child{margin-top:0}
.section h3{font-size:1.05rem;margin:22px 0 6px}

/* hero */
.hero{padding:72px 0 40px;max-width:720px}
.hero h1{font-size:clamp(2.4rem,6vw,4rem);font-weight:700;margin-bottom:18px}
.lead{font-size:1.2rem;color:var(--fg2);max-width:640px}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 18px;border-radius:999px;font-weight:600;font-size:.95rem;border:1px solid var(--line);color:var(--fg);background:var(--surface)}
.btn:hover{text-decoration:none;border-color:var(--muted)}
.btn.primary{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.btn.disabled{color:var(--muted);cursor:default}

/* app grid */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.card{display:flex;flex-direction:column;gap:6px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px;color:var(--fg);transition:transform .15s ease,border-color .15s ease}
.card:hover{text-decoration:none;transform:translateY(-2px);border-color:var(--muted)}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px}
.glyph{display:inline-grid;place-items:center;width:52px;height:52px;border-radius:14px;background:var(--bg2);border:1px solid var(--line);color:var(--accent)}
.glyph.large{width:72px;height:72px;border-radius:20px;margin-bottom:22px}
.card h3{font-size:1.15rem}
.card p{color:var(--fg2);margin:0}
.card .meta{color:var(--muted);font-size:.85rem;margin-top:auto;padding-top:14px}
.pill{font-size:.72rem;font-weight:600;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:3px 9px;white-space:nowrap}

/* principles */
.principles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:28px 32px}
.principles h3{font-size:1.05rem;margin:0 0 6px}
.principles p{color:var(--fg2);margin:0}

/* app page */
.app-hero{padding-top:48px}
.two-col{display:grid;grid-template-columns:1fr 280px;gap:40px;align-items:start}
@media(max-width:760px){.two-col{grid-template-columns:1fr}}
.features{padding-left:20px;margin:12px 0 0;color:var(--fg2)}
.features li{margin:6px 0}
.facts{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px}
.facts dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:10px 16px;font-size:.95rem}
.facts dt{color:var(--muted)}
.facts dd{margin:0;font-weight:500}

/* docs */
.doc{max-width:720px;padding:48px 0}
.doc h1{font-size:clamp(2rem,5vw,2.75rem);margin-bottom:10px}
.doc h2{font-size:1.25rem;margin:36px 0 8px}
.doc ul{padding-left:20px}
.doc li{margin:6px 0}
.linklist{list-style:none;padding:0}
.linklist li{padding:10px 0;border-bottom:1px solid var(--line)}
.linklist a{font-weight:600;color:var(--fg)}

/* footer */
footer.site{max-width:var(--max);margin:0 auto;padding:40px 24px 48px;border-top:1px solid var(--line)}
footer .cols{display:grid;grid-template-columns:2fr 1fr 1fr;gap:32px}
@media(max-width:640px){footer .cols{grid-template-columns:1fr}}
footer h4{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:10px}
footer .cols a{display:block;color:var(--fg2);padding:3px 0;font-size:.95rem}
footer .cols a.brand{display:inline-flex;color:var(--fg);margin-bottom:12px}
footer .muted{max-width:320px;font-size:.95rem}
footer .legal{color:var(--muted);font-size:.8rem;margin:32px 0 0}
""")
(ROOT/".nojekyll").write_text("")
print("generated", len(APPS), "apps")
