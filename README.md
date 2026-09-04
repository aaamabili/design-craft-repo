# Interface Craft

A study library on interface craft: 112 lessons across Craft, Typography, Color, Layout, Motion and UX, plus a References section. Every lesson has a live, hands-on demo (sliders and switches, no play buttons), "details that make the difference", and sources.

Static site: HTML + CSS + a small amount of vanilla JS. English at the root, Portuguese under `pt/`. Light and dark themes, Inter everywhere, exactly five font sizes (11, 13, 16, 24 and 32px).

## Run locally

Any static server works:

```bash
npx -y serve .
```

Then open `http://localhost:3000`.

## Structure

- `index.html` — home with one card per section
- `craft.html`, `typography.html`, `color.html`, `layout.html`, `motion.html`, `ux.html`, `references.html` — sections (EN)
- `pt/` — the same pages in Portuguese
- `styles.css` — tokens, layout and every demo's styles
- `app.js` — theme, language, sidebar and demo interactions

Content is synthesized from the sources listed at the end of each lesson (Making Software, Interface Craft, animations.dev, the craft community and the handbooks on motion, craft, UX, color and typography). Course and author names belong to their respective owners.
