import os, pathlib
ROOT = pathlib.Path(__file__).parent
EMAIL = "support@meralsoftware.example"  # replaced once the owner confirms
COMPANY = "Meral Software LLC"
DATE = "September 20, 2026"

STORE = "https://apps.apple.com/app/id{id}"
APPS = [
 dict(slug="opencube", name="OpenCube", live=True, store_id="6814315632", platform="iPhone · iPad", price="Free · OpenCube Pro $1.99 once",
      features=["Scan your cube with the camera, one face at a time","Short solutions from a two-phase solver","Beginner, CFOP and Roux lessons with 3D animations","Solve timer with scrambles, inspection and per-method stats","Seven languages, works fully offline"],
      tag="Scan, solve and learn the 3×3 cube.",
      blurb="Point the camera at your cube and OpenCube reads it, shows a short solution, and teaches you Beginner, CFOP and Roux step by step. A solve timer with scrambles and per-method statistics rounds it out. Everything runs on the phone.",
      perms=[("Camera","used only to read the colours on your cube while you scan. Frames are processed live and never stored or sent anywhere.")],
      paid="A one-time purchase, OpenCube Pro, unlocks the advanced methods, case scrambles, statistics and colour schemes."),
 dict(slug="openpack", name="OpenPack", live=False, store_id=None, platform="iPhone (LiDAR)", price="Free · $4.99 once",
      features=["Scan any object into a measured 3D shape","Scan a trunk, bin, doorway or shelf","Yes/no fit verdict with a 3D preview"],
      tag="Will it fit? Scan the object and the space and find out.",
      blurb="OpenPack uses the LiDAR scanner to measure an object and a space, then tells you whether one fits in the other with a 3D preview.",
      perms=[("Camera and LiDAR","used to measure objects and spaces on the device. Scans are stored only on your device.")],
      paid="A one-time purchase unlocks the full app."),
 dict(slug="hang", name="Hang", live=False, store_id=None, platform="iPhone (LiDAR)", price="Free · $4.99 once",
      features=["Scan the wall and lay out frames to scale","Nail positions in centimetres","Live level guide while you hammer"],
      tag="Hang pictures straight, first time.",
      blurb="Scan a wall, arrange your frames to scale, and get exact nail positions with a live level guide.",
      perms=[("Camera and LiDAR","used to measure your wall on the device."),("Motion sensors","used for the level guide.")],
      paid="A one-time purchase unlocks the full app."),
 dict(slug="pocketsight", name="PocketSight", live=False, store_id=None, platform="iPhone", price="Free · $4.99 once",
      features=["Ghost-ball aiming line over the real table","Predicted path for object and cue ball","Hide-the-line test to train your eye"],
      tag="See the shot before you take it.",
      blurb="A live aiming overlay for pool, shown over the real table through your camera.",
      perms=[("Camera","used to see the table and balls. Frames are processed live on the device and never stored or sent anywhere.")],
      paid="A one-time purchase unlocks the full app."),
 dict(slug="marginalia", name="Marginalia", live=False, store_id=None, platform="iPad · Mac", price="Free · $9.99 once",
      features=["A proper PDF reader with Apple Pencil annotation","Handwrite a question in the margin, get a cited answer","Answers come only from that document, on the device"],
      tag="Write a question in the margin, get an answer from the page.",
      blurb="A PDF reader for iPad. Handwrite a question in the margin and get an answer grounded only in that document, entirely on the device.",
      perms=[("Files","you choose which PDFs to open; they are indexed and stored only on your device.")],
      paid="A one-time purchase unlocks the full app."),
 dict(slug="punch", name="Punch", live=False, store_id=None, platform="Apple Watch", price="Free · $4.99 once",
      features=["Punch count from the watch alone, no straps","Jab, cross, hook and uppercut","Per-round fatigue drop-off"],
      tag="Bag work, counted by your watch.",
      blurb="Counts and classifies punches from Apple Watch motion during bag work, with per-round fatigue trends.",
      perms=[("Motion sensors","read on the watch during a session."),("Health","Punch can record workouts to the Health app on your device if you allow it. Health data is never read for any other purpose and never leaves your device.")],
      paid="A one-time purchase unlocks the full app."),
 dict(slug="tempomaster", name="TempoMaster", live=False, store_id=None, platform="Apple Watch · iPhone", price="Free · $3.99 once",
      features=["Back:forward tempo ratio for every stroke","Face rotation and consistency","Haptic tempo trainer on the wrist"],
      tag="A steady putting stroke, from your wrist.",
      blurb="Measures putting tempo and face rotation from Apple Watch motion, with a haptic tempo trainer.",
      perms=[("Motion sensors","read on the watch during practice."),("Health","TempoMaster can record workouts to the Health app on your device if you allow it. Health data never leaves your device.")],
      paid="A one-time purchase unlocks the full app."),
]

def store_button(a, cls="btn"):
    if a.get("store_id"):
        return f'<a class="{cls}" href="{STORE.format(id=a["store_id"])}">Download on the App Store</a>'
    return f'<span class="{cls} disabled">Coming soon to the App Store</span>'

def page(title, body, depth=0, desc=""):
    up = "../"*depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header><a class="brand" href="{up}">{COMPANY}</a></header>
<main>
{body}
</main>
<footer>© 2026 {COMPANY} · <a href="{up}privacy.html">Privacy</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></footer>
</body>
</html>
"""

def privacy_body(app=None):
    name = app["name"] if app else "our apps"
    perms = ""
    if app:
        perms = "<h2>Device permissions</h2><ul>" + "".join(f"<li><strong>{p}</strong> — {t}</li>" for p,t in app["perms"]) + "</ul>"
        paid = f"<h2>Purchases</h2><p>{app['paid']} Payment is handled entirely by Apple through the App Store. We never see your payment details, and we receive no personal information about you from a purchase.</p>"
    else:
        paid = "<h2>Purchases</h2><p>Where an app offers a one-time purchase, payment is handled entirely by Apple through the App Store. We never see your payment details, and we receive no personal information about you from a purchase.</p>"
    return f"""
<h1>Privacy Policy{' for '+app['name'] if app else ''}</h1>
<p class="muted">Last updated {DATE}</p>
<p><strong>{name.capitalize() if not app else name} collects no data.</strong> Not usage analytics, not crash reports, not an email address, nothing. There are no accounts to create and no servers to talk to. The app works entirely on your device and works without an internet connection.</p>
<h2>What stays on your device</h2>
<p>Anything the app saves, such as your history, settings or scans, is stored only in the app's own storage on your device and in your device backups if you have those turned on. You can delete it at any time by deleting the app.</p>
{perms}
{paid}
<h2>Third parties</h2>
<p>The app contains no third-party code, advertising, or tracking of any kind. It does not send data to anyone, including us.</p>
<h2>Children</h2>
<p>Because the app collects no data, it collects no data from children either.</p>
<h2>Changes</h2>
<p>If this policy ever changes, the new version will be posted on this page with a new date. Since the app cannot contact us, the app itself cannot notify you.</p>
<h2>Contact</h2>
<p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
"""

# root
sections = "".join(f"""<section class="app" id="{a['slug']}">
<div class="app-head"><h2><a href="{a['slug']}/">{a['name']}</a></h2><span class="meta">{a['platform']}</span></div>
<p class="tag">{a['tag']}</p>
<p>{a['blurb']}</p>
<ul class="features">{''.join(f'<li>{f}</li>' for f in a['features'])}</ul>
<p class="price">{a['price']}</p>
<p class="actions">{store_button(a)} <a class="btn ghost" href="{a['slug']}/">Support &amp; privacy</a></p>
</section>""" for a in APPS)
nav = " · ".join(f'<a href="#{a["slug"]}">{a["name"]}</a>' for a in APPS)
(ROOT/"index.html").write_text(page(COMPANY, f"""
<h1>Apps that stay on your device.</h1>
<p class="lead">Small, focused iPhone, iPad and Apple Watch apps. No accounts, no subscriptions, no data collection. Pay once if you want more.</p>
<p class="nav">{nav}</p>
{sections}
""", 0, "Meral Software LLC makes offline iPhone, iPad and Apple Watch apps."))
(ROOT/"privacy.html").write_text(page(f"Privacy · {COMPANY}", privacy_body(), 0, "Privacy policy for Meral Software LLC apps."))

for a in APPS:
    d = ROOT/a["slug"]; d.mkdir(exist_ok=True)
    perms = "".join(f"<li><strong>{p}</strong> — {t}</li>" for p,t in a["perms"])
    (d/"index.html").write_text(page(f"{a['name']} · Support", f"""
<h1>{a['name']}</h1>
<p class="lead">{a['tag']}</p>
<p>{a['blurb']}</p>
<ul class="features">{''.join(f'<li>{f}</li>' for f in a['features'])}</ul>
<p class="price">{a['price']} · {a['platform']}</p>
<p class="actions">{store_button(a)}</p>
<h2>Support</h2>
<p>Something not working, or an idea for the app? Email <a href="mailto:{EMAIL}?subject={a['name']}">{EMAIL}</a> and include your device model and iOS version. We answer every message.</p>
<h2>Privacy</h2>
<p>{a['name']} collects no data and works entirely on your device. <a href="privacy.html">Read the full privacy policy.</a></p>
<h2>Permissions</h2>
<ul>{perms}</ul>
""", 1, f"Support and privacy for {a['name']} by {COMPANY}."))
    (d/"privacy.html").write_text(page(f"{a['name']} · Privacy Policy", privacy_body(a), 1, f"Privacy policy for {a['name']}: no data collected."))

(ROOT/"style.css").write_text("""
:root{--bg:#1c1d21;--fg:#f2f2f4;--muted:#9a9ba3;--card:#26272d;--accent:#4cd964;--line:#33343b}
@media(prefers-color-scheme:light){:root{--bg:#fafafa;--fg:#16171b;--muted:#6b6c75;--card:#fff;--accent:#1f9d3d;--line:#e4e4e8}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 -apple-system,BlinkMacSystemFont,"SF Pro Text",Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
header,main,footer{max-width:760px;margin:0 auto;padding:0 20px}
header{padding-top:28px}
.brand{font-weight:700;color:var(--fg);text-decoration:none;letter-spacing:-.01em}
main{padding:36px 20px 60px}
h1{font-size:2rem;line-height:1.15;letter-spacing:-.02em;margin:0 0 12px}
h2{font-size:1.15rem;margin:36px 0 8px}
.lead{font-size:1.2rem;color:var(--muted);margin-top:0}
.muted{color:var(--muted)}
a{color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin-top:28px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;color:var(--fg);text-decoration:none;position:relative}
.card h2{margin:0 0 6px;font-size:1.1rem}
.card p{margin:0;color:var(--muted);font-size:.95rem}
.soon{display:inline-block;margin-top:10px;font-size:.75rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:2px 9px}
p.soon{display:inline-block}
ul{padding-left:20px}
li{margin:6px 0}
.nav{color:var(--muted);font-size:.95rem}
.app{border-top:1px solid var(--line);padding:32px 0 8px;margin-top:24px}
.app-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.app-head h2{margin:0;font-size:1.5rem}
.app-head h2 a{color:var(--fg);text-decoration:none}
.meta{color:var(--muted);font-size:.9rem}
.tag{font-size:1.1rem;color:var(--muted);margin:4px 0 10px}
.features{padding-left:20px;margin:8px 0}
.price{color:var(--muted);font-size:.95rem}
.actions{display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-block;background:var(--accent);color:#0b1a0e;font-weight:600;padding:10px 16px;border-radius:12px;text-decoration:none}
.btn.ghost{background:transparent;color:var(--accent);border:1px solid var(--line)}
.btn.disabled{background:var(--card);color:var(--muted);border:1px solid var(--line)}
footer{padding:24px 20px 48px;color:var(--muted);font-size:.9rem;border-top:1px solid var(--line)}
footer a{color:var(--muted)}
""")
(ROOT/".nojekyll").write_text("")
(ROOT/"README.md").write_text(f"""# {COMPANY} website

Static site served by GitHub Pages. Each app has `<app>/index.html` (support) and `<app>/privacy.html`.

Regenerate every page from `gen.py` (edit the `APPS` table, `EMAIL`, or the copy there) with:

    python3 gen.py

Custom domain: put the domain in a `CNAME` file at the root and point the domain's A records at GitHub Pages.
""")
print("ok")
