# Meral Software LLC website

Static site served by GitHub Pages. Each app has `<app>/index.html` (support) and `<app>/privacy.html`.

Regenerate every page from `gen.py` (edit the `APPS` table, `EMAIL`, or the copy there) with:

    python3 gen.py

Custom domain: put the domain in a `CNAME` file at the root and point the domain's A records at GitHub Pages.
