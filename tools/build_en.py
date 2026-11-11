# -*- coding: utf-8 -*-
"""Build English pages and link them from the Chinese pages."""
import io, json, os

ROOT = r"D:\work\resume_maker"
TPL = os.path.join(ROOT, "tools")

def load(name):
    with io.open(os.path.join(TPL, name), "r", encoding="utf-8") as f:
        return json.load(f)

PERSONAS = load("personas.json")["personas"]
EN = load("personas_en.json")

def build_en(p, e):
    facts = "".join('<div class="facts__row"><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in e["summary_facts"])
    exp = []
    for x in e["experience"]:
        bl = "".join("<li>%s</li>" % b for b in x["bullets"])
        exp.append('<li class="tl-item"><div class="tl-head"><div><h3 class="tl-title">%s</h3>'
                   '<div class="tl-org">%s</div></div><span class="tl-date">%s</span></div>'
                   '<div class="tl-body"><ul>%s</ul></div></li>' % (x["title"], x["org"], x["date"], bl))
    exp = "".join(exp)
    edu = "".join('<li class="tl-item"><div class="tl-head"><div><h3 class="tl-title">%s</h3>'
                  '<div class="tl-org">%s</div></div><span class="tl-date">%s</span></div></li>'
                  % (s, m, d) for s, m, d in e["education"])
    skills = "".join("<p><strong>%s.</strong> %s</p>" % (k, v) for k, v in e["skills"])
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(name)s · %(title)s</title>
<meta name="description" content="%(role)s">
<meta name="author" content="%(name)s">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/img/avatar-32.png">
<link rel="stylesheet" href="../assets/css/style.css"></head><body>
<nav class="nav"><div class="nav__inner"><a class="nav__brand" href="#top">%(name)s</a>
<div class="nav__links"><a href="#about">Summary</a><a href="#experience">Experience</a>
<a href="#education">Education</a><a href="#skills">Skills</a><a href="../">中文</a></div></div></nav>
<main id="top">
<section class="hero"><div class="wrap hero__inner"><div>
<p class="hero__eyebrow">%(eyebrow)s</p>
<h1 class="hero__name">%(name)s</h1>
<p class="hero__role">%(role)s</p>
<div class="hero__cta"><a class="btn btn--primary" href="../assets/resume.pdf" target="_blank" rel="noopener">Download PDF</a>
<a class="btn btn--ghost" href="mailto:%(email)s">%(email)s</a></div>
</div><div class="hero__avatar"><img src="../assets/img/avatar.jpg" alt="%(name)s" width="520" height="689"></div>
</div></section>

<section class="section section--alt" id="about"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Summary</span><h2 class="section__title">At a glance</h2></div>
<aside class="facts reveal"><dl>%(facts)s</dl></aside>
</div></section>

<section class="section" id="experience"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Experience</span><h2 class="section__title">Experience</h2></div>
<ol class="timeline reveal">%(exp)s</ol>
</div></section>

<section class="section section--alt" id="education"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Education</span><h2 class="section__title">Education</h2></div>
<ol class="timeline reveal">%(edu)s</ol>
</div></section>

<section class="section" id="skills"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Skills</span><h2 class="section__title">Skills</h2></div>
<div class="about__text reveal">%(skills)s</div>
</div></section>
</main>
<footer class="footer"><div class="wrap">© 2026 %(name)s · sample layout · <a href="../">中文</a></div></footer>
<script src="../assets/js/main.js"></script>
</body></html>
""" % dict(name=p["name"], title=e["title"], role=e["role"], eyebrow=e["eyebrow"], email=p["email"],
           facts=facts, exp=exp, edu=edu, skills=skills)

for p in PERSONAS:
    slug = p["slug"]
    d = os.path.join(ROOT, slug, "en")
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_en(p, EN[slug]))

    # link the English page from the Chinese footer
    cn = os.path.join(ROOT, slug, "index.html")
    with io.open(cn, "r", encoding="utf-8") as f:
        html = f.read()
    if 'href="en/"' not in html:
        html = html.replace("· 样例版式</div></footer>", '· 样例版式 · <a href="en/">English</a></div></footer>')
        with io.open(cn, "w", encoding="utf-8") as f:
            f.write(html)

print("english pages built:", [p["slug"] for p in PERSONAS])
