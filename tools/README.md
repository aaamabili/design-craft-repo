# tools

Generators that patch the generated site in place (the HTML in the repo is the source of truth; see the root README).

- `dev/` — the Development section: `content_en.py` / `content_pt.py` (lessons), `demos_dev.py` (demo markup, EN/PT strings), `dev.css`, `dev.js`, `gen_dev.py` (builds `development.html` and `pt/development.html` from the AI pages' chrome, then patches nav, home cards and counts, the References eyebrow, `styles.css` and `app.js`). Idempotent: `python3 tools/dev/gen_dev.py`.
- `trilha/` — `add_dev_phase.py` patches the "Trilha Interface Craft" artifact (study plan): reads the live page HTML (saved by the Artifact tool), injects the Development lessons with their sources and extra references, adds phase 4 (weeks 17–24) and repairs the self-publish escaping so the page keeps parsing after it saves itself.
