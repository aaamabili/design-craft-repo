# Builds the Development section (development.html, pt/development.html) from the AI pages' chrome and patches the rest of the site.
# Run from anywhere: python3 tools/dev/gen_dev.py   (idempotent)
import re, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import content_en, content_pt, demos_dev
SITE = os.path.abspath(os.path.join(HERE, '..', '..'))
KEY = 'dev'; NAME = 'Development'; PAGE = 'development.html'
ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
UI = dict(en=dict(details='Details that make the difference', sources='Sources:', other='Other sections', refs=('references.html', 'References'), lessons='lessons', contents='Section contents'),
          pt=dict(details='Detalhes que fazem a diferença', sources='Fontes:', other='Outras seções', refs=('referencias.html', 'Referências'), lessons='aulas', contents='Conteúdo da seção'))
SECTIONS = [('craft.html', 'Craft'), ('typography.html', 'Typography'), ('color.html', 'Color'), ('layout.html', 'Layout'), ('motion.html', 'Motion'), ('ux.html', 'UX'), ('primitives.html', 'Primitives'), ('practice.html', 'Practice'), ('ai.html', 'AI')]
PAGE_OF = dict(craft='craft.html', type='typography.html', color='color.html', layout='layout.html', motion='motion.html', ux='ux.html', primitives='primitives.html', practice='practice.html', ai='ai.html', dev=PAGE)

def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

def section_html(L):
    C = content_en if L == 'en' else content_pt; lessons = C.EN if L == 'en' else C.PT
    D = demos_dev.build(L); u = UI[L]
    out = ['<section class="section" data-section="%s">' % KEY, '        <div class="section-head" id="%s">' % KEY, '          <span class="eyebrow">%s</span>' % C.HEAD['eyebrow'], '          <h2>%s</h2>' % C.HEAD['title'], '          <p>%s</p>' % C.HEAD['desc'], '        </div>', '']
    for i, l in enumerate(lessons, 1):
        out += ['        <article class="lesson" id="%s">' % l['id'], '          <span class="eyebrow">%s · %02d</span>' % (NAME, i), '          <h2>%s</h2>' % l['title'], '          <p class="lede">%s</p>' % l['lede'], '', '          ' + D[l['id']], '', '          ' + l['body'], '          <h3>%s</h3>' % u['details'], '          <ul class="details">']
        out += ['            <li>%s</li>' % d for d in l['details']]
        out += ['          </ul>', '          <footer class="sources"><span>%s</span> %s</footer>' % (u['sources'], l['sources']), '        </article>', '']
    out.append('      </section>')
    return '\n'.join(out), lessons

def build_page(L):
    u = UI[L]; C = content_en if L == 'en' else content_pt
    tpl = rd(os.path.join(SITE, 'ai.html' if L == 'en' else 'pt/ai.html'))
    sec, lessons = section_html(L)
    tpl = re.sub(r'<title>.*?</title>', '<title>%s — Interface Craft</title>' % NAME, tpl)
    tpl = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="%s">' % C.HEAD['desc'].replace('"', '&quot;'), tpl)
    tpl = tpl.replace('href="pt/ai.html"', 'href="pt/%s"' % PAGE).replace('href="../ai.html"', 'href="../%s"' % PAGE)
    links = ''.join('<li><a class="nav-link" href="#%s">%s</a></li>' % (l['id'], l['title']) for l in lessons)
    others = ''.join('<li><a class="nav-link" href="%s">%s</a></li>' % s for s in SECTIONS) + '<li><a class="nav-link" href="%s">%s</a></li>' % u['refs']
    nav = ('<nav class="nav-groups" aria-label="%s">\n      <div class="nav-group" data-section="%s" style="margin-top:0">\n        <div class="nav-title">%s%s</div>\n        <ul class="nav-list">%s</ul>\n      </div>\n      <div class="nav-group nav-other" data-section="%s">\n        <div class="nav-title">%s</div>\n        <ul class="nav-list">%s</ul>\n      </div>\n    </nav>' % (u['contents'], KEY, ICON, NAME, links, KEY, u['other'], others))
    tpl = re.sub(r'<nav class="nav-groups".*?</nav>', lambda m: nav, tpl, flags=re.S)
    i = tpl.index('<section class="section" data-section="ai">'); j = tpl.rindex('</section>') + len('</section>')
    tpl = tpl[:i] + sec + tpl[j:]
    wr(os.path.join(SITE, PAGE if L == 'en' else 'pt/' + PAGE), tpl)
    return len(lessons)

def patch_nav():
    for L in ('en', 'pt'):
        u = UI[L]; d = SITE if L == 'en' else os.path.join(SITE, 'pt')
        for f in sorted(os.listdir(d)):
            if not f.endswith('.html') or f in ('index.html', PAGE): continue
            p = os.path.join(d, f); s = rd(p)
            if 'href="%s">%s<' % (PAGE, NAME) in s: continue
            ai = '<li><a class="nav-link" href="ai.html">AI</a></li>'
            s2 = s.replace(ai, ai + '<li><a class="nav-link" href="%s">%s</a></li>' % (PAGE, NAME))
            if s2 == s:
                ref = '<li><a class="nav-link" href="%s">%s</a></li>' % u['refs']
                s2 = s.replace(ref, '<li><a class="nav-link" href="%s">%s</a></li>' % (PAGE, NAME) + ref)
            if s2 == s: print('WARN no nav insert', p)
            wr(p, s2)

def section_counts():
    return dict((k, rd(os.path.join(SITE, f)).count('<article class="lesson"')) for k, f in PAGE_OF.items())

def patch_home(n):
    for L in ('en', 'pt'):
        C = content_en if L == 'en' else content_pt; u = UI[L]
        p = os.path.join(SITE, 'index.html' if L == 'en' else 'pt/index.html'); s = rd(p)
        if 'data-section="%s"' % KEY not in s:
            card = ('        <a class="home-card" data-section="%s" href="%s">\n          <div class="home-card-head">%s<span class="home-card-count">%d %s%s</span></div>\n          <h2>%s</h2>\n          <p>%s</p>\n        </a>\n' % (KEY, PAGE, ICON, n, u['lessons'], ARROW, NAME, C.HEAD['desc']))
            k = s.index('        <a class="home-card" data-section="resources"'); s = s[:k] + card + s[k:]
        s = re.sub(r'(<a class="home-card" data-section="%s" href="[^"]+">.*?<p>).*?(</p>)' % KEY, lambda m: m.group(1) + C.HEAD['desc'] + m.group(2), s, count=1, flags=re.S)
        for key, cnt in section_counts().items():
            s = re.sub(r'(data-section="%s" href="[^"]+">\s*<div class="home-card-head">.*?<span class="home-card-count">)\d+' % key, lambda m: m.group(1) + str(cnt), s, flags=re.S)
        total = sum(section_counts().values())
        s = re.sub(r'<strong>\d+</strong> (lessons|aulas)', lambda m: '<strong>%d</strong> %s' % (total, m.group(1)), s)
        s = re.sub(r'<strong>\d+</strong> (sections|seções)', lambda m: '<strong>%d</strong> %s' % (len(PAGE_OF), m.group(1)), s)
        wr(p, s)

def patch_refs():
    for f, a, b in (('references.html', 'Section 10', 'Section 11'), ('pt/referencias.html', 'Seção 10', 'Seção 11')):
        p = os.path.join(SITE, f); wr(p, rd(p).replace(a, b))

def patch_css():
    p = os.path.join(SITE, 'styles.css'); s = rd(p)
    if '--accent-dev' not in s:
        s = s.replace('  --accent-ai: oklch(58% 0.17 275);\n', '  --accent-ai: oklch(58% 0.17 275);\n  --accent-dev: oklch(58% 0.15 230);\n', 1)
        s = s.replace('    --accent-ai: oklch(76% 0.13 275);\n', '    --accent-ai: oklch(76% 0.13 275);\n    --accent-dev: oklch(74% 0.12 230);\n')
        s = s.replace('  --accent-ai: oklch(76% 0.13 275);\n', '  --accent-ai: oklch(76% 0.13 275);\n  --accent-dev: oklch(74% 0.12 230);\n')
        for sel in ('.nav-group', '.section', '.home-card'):
            s = s.replace('%s[data-section="ai"] { --accent: var(--accent-ai); }' % sel, '%s[data-section="ai"] { --accent: var(--accent-ai); }\n%s[data-section="dev"] { --accent: var(--accent-dev); }' % (sel, sel))
    css = rd(os.path.join(HERE, 'dev.css'))
    if '/* ---- Development:' in s: s = s[:s.index('\n/* ---- Development:')] + '\n' + css.lstrip('\n')
    else: s = s.rstrip('\n') + '\n' + css
    wr(p, s)

def patch_js():
    p = os.path.join(SITE, 'app.js'); s = rd(p)
    js = rd(os.path.join(HERE, 'dev.js')).rstrip('\n') + '\n'
    if '    // Development demos' in s:
        i = s.index('    // Development demos'); j = s.index('    // Practice demos'); s = s[:i] + js + s[j:]
    else:
        s = s.replace('    // Practice demos', js + '    // Practice demos', 1)
    wr(p, s)

def patch_readme(n):
    p = os.path.join(SITE, 'README.md'); s = rd(p)
    total = sum(section_counts().values())
    s = re.sub(r'\d+ lessons across Craft, Typography, Color, Layout, Motion, UX, Primitives, Practice(?:, AI and Development| and AI)', '%d lessons across Craft, Typography, Color, Layout, Motion, UX, Primitives, Practice, AI and Development' % total, s)
    s = s.replace('`ai.html`, `references.html`', '`ai.html`, `development.html`, `references.html`') if '`development.html`' not in s else s
    wr(p, s)

if __name__ == '__main__':
    n = build_page('en'); m = build_page('pt'); assert n == m
    patch_nav(); patch_home(n); patch_refs(); patch_css(); patch_js(); patch_readme(n)
    print('built %s with %d lessons; totals %s' % (PAGE, n, json.dumps(section_counts())))
