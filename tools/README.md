# tools

Generators that patch the generated site in place (the HTML in the repo is the source of truth; see the root README).

- `dev/` — the Development section: `content_en.py` / `content_pt.py` (lessons), `demos_dev.py` (demo markup, EN/PT strings), `dev.css`, `dev.js`, `gen_dev.py` (builds `development.html` and `pt/development.html` from the AI pages' chrome, then patches nav, home cards and counts, the References eyebrow, `styles.css` and `app.js`). Idempotent: `python3 tools/dev/gen_dev.py`.
