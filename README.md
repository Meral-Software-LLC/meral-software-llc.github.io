# Meral Software LLC website

Static site served by GitHub Pages. Each app has `<app>/index.html` (support) and `<app>/privacy.html`.

Regenerate every page from `gen.py` (edit the `APPS` table, `EMAIL`, or the copy there). Shared visual styles live in `style.css` and are preserved when regenerating:

    python3 gen.py

Run a local preview with:

    python3 -m http.server 8000 --bind 127.0.0.1

Open http://127.0.0.1:8000 and refresh after changes. Product illustrations are decorative concepts, not screenshots of the apps.

Custom domain: put the domain in a `CNAME` file at the root and point the domain's A records at GitHub Pages.
