# -*- coding: utf-8 -*-
"""Generate the four-discipline sample sites."""
import json, os, shutil

ROOT = r"D:\work\resume_maker"
TPL = os.path.join(ROOT, "tools")
SITE = "https://cccty121.github.io/resume_maker"

with open(os.path.join(TPL, "personas.json"), "r", encoding="utf-8") as f:
    PERSONAS = json.load(f)["personas"]

PRINT_CSS = """
  @page { size: A4; margin: 9.5mm 13mm 6mm; }
  *{box-sizing:border-box}
  body{margin:0;color:#1a1d23;font-family:"Source Han Sans SC","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;
    font-size:9.3pt;line-height:1.4;-webkit-font-smoothing:antialiased}
  h1{font-size:20.5pt;margin:0;letter-spacing:.01em}
  h2{font-size:10.8pt;margin:10.5pt 0 4.5pt;padding-bottom:2.4pt;border-bottom:1.3px solid #1b4b8f;color:#14356a}
  ul{margin:2.4pt 0 0;padding-left:11.5pt}
  li{margin:1.6pt 0}
  strong{font-weight:700;color:#14356a}
  header{border-bottom:2px solid #1b4b8f;padding-bottom:6pt;margin-bottom:1pt}
  .hdr{display:flex;justify-content:space-between;align-items:flex-start;gap:10pt}
  .hdr__text{flex:1;min-width:0}
  .tagline{margin:3.5pt 0 4pt;color:#334;font-size:9.5pt}
  .contact{display:flex;flex-wrap:wrap;gap:9pt;font-size:8pt;color:#444}
  .hdr__side{display:flex;align-items:flex-start;gap:7pt;flex:none}
  .hdr__qr{margin:0;display:flex;flex-direction:column;align-items:center;gap:2pt}
  .hdr__qr img{width:15mm;height:15mm;display:block}
  .hdr__qr figcaption{font-size:5.6pt;color:#6b7280;white-space:nowrap}
  .hdr__photo{width:15.5mm;height:20.5mm;object-fit:cover;object-position:50% 30%;
    border-radius:2pt;border:1px solid #e2e6ee;flex:none;margin-top:1pt}
  .item{margin-bottom:5.5pt}
  .row{display:flex;justify-content:space-between;align-items:baseline;gap:8pt}
  .org{font-weight:700;font-size:9.7pt}
  .role{color:#415;font-size:8.7pt;margin-left:6pt}
  .date{color:#6b7280;font-size:8pt;white-space:nowrap}
  .meta{margin:1.5pt 0 0;color:#333}
  .skills{list-style:none;padding:0;margin:0}
  .skills li{margin:1.6pt 0}
  .skills b{color:#14356a}
"""

def esc(s):
    return s

def section_heading(text, kicker=""):
    if kicker:
        return '<div class="section__head reveal"><span class="section__kicker">%s</span><h2 class="section__title">%s</h2></div>' % (kicker, text)
    return '<div class="section__head reveal"><h2 class="section__title">%s</h2></div>' % text

def build_index(p):
    slug, name, en = p["slug"], p["name"], p["en_name"]
    facts = "".join('<div class="facts__row"><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in p["facts"])
    stats = "".join('<div class="stat"><span class="stat__num">%s</span><span class="stat__label">%s</span></div>' % (n, l) for n, l in p["stats"])
    about = "".join("<p>%s</p>" % t for t in p["about"])

    exp_html = []
    for e in p["experience"]:
        bullets = "".join("<li>%s</li>" % b for b in e["bullets"])
        sub = ""
        if e.get("sub"):
            s = e["sub"]
            sb = "".join("<li>%s</li>" % b for b in s["bullets"])
            sub = ('<div class="tl-sub"><div class="tl-sub__head"><span class="tl-sub__role">%s</span>'
                   '<span class="tl-date">%s</span></div><div class="tl-body"><ul>%s</ul></div></div>'
                   % (s["role"], s["date"], sb))
        exp_html.append('<li class="tl-item"><div class="tl-head"><div><h3 class="tl-title">%s</h3>'
                        '<div class="tl-org">%s</div></div><span class="tl-date">%s</span></div>'
                        '<div class="tl-body"><ul>%s</ul></div>%s</li>' % (e["title"], e["org"], e["date"], bullets, sub))
    exp_html = "".join(exp_html)

    proj_html = []
    for i, pr in enumerate(p["projects"]):
        wide = " card--wide" if i == 0 else ""
        chips = "".join('<span class="chip">%s</span>' % c for c in pr["stack"])
        link = '<div class="card__links"><a href="#honors">%s</a></div>' % pr["link"] if pr.get("link") else ""
        proj_html.append('<article class="card%s reveal"><div class="card__top"><span class="tag">%s</span>'
                         '<span class="card__date">%s</span></div><h3 class="card__title">%s</h3>'
                         '<p class="card__desc">%s</p><div class="card__stack">%s</div>%s</article>'
                         % (wide, pr["tag"], pr["date"], pr["title"], pr["desc"], chips, link))
    proj_html = "".join(proj_html)

    edu_html = []
    for e in p["education"]:
        bl = "".join("<li>%s</li>" % b for b in e["bullets"])
        edu_html.append('<li class="tl-item"><div class="tl-head"><div><h3 class="tl-title">%s</h3>'
                        '<div class="tl-org">%s</div></div><span class="tl-date">%s</span></div>'
                        '<div class="tl-body"><ul>%s</ul></div></li>' % (e["school"], e["major"], e["date"], bl))
    edu_html = "".join(edu_html)

    skills = "".join("<p><strong>%s：</strong>%s</p>" % (k, v) for k, v in p["skills"])

    works = []
    for w in p["works"]:
        chips = "".join('<span class="chip">%s</span>' % c for c in w["stack"])
        works.append('<article class="card reveal"><div class="card__top"><span class="tag">%s</span>'
                     '<span class="card__date">%s</span></div><h3 class="card__title">%s</h3>'
                     '<p class="card__desc">%s</p><div class="card__stack">%s</div></article>'
                     % (w["tag"], w["date"], w["title"], w["desc"], chips))
    works = "".join(works)

    honors = "".join('<li class="tl-item"><div class="tl-head"><div><h3 class="tl-title">%s</h3></div>'
                     '<span class="tl-date">%s</span></div></li>' % (t, d) for t, d in p["honors"])

    meta_li = "".join("<li>%s</li>" % m for m in p["meta"])
    contacts = "".join('<div class="contact-card"><a href="mailto:%s">%s</a></div>' % (p["email"], p["email"]) for _ in [0])
    contacts += '<div class="contact-card">%s</div>' % p["meta"][0]

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(name)s · %(title)s</title>
<meta name="description" content="%(seo)s">
<meta name="author" content="%(name)s">
<meta name="robots" content="noindex, nofollow">
<meta property="og:title" content="%(name)s · %(title)s">
<meta property="og:type" content="profile">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/avatar-32.png">
<link rel="apple-touch-icon" href="assets/img/avatar-180.png">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<nav class="nav"><div class="nav__inner"><a class="nav__brand" href="#top">%(name)s</a>
<div class="nav__links">
<a href="#about">关于</a><a href="#experience">经历</a><a href="#projects">项目</a>
<a href="#education">教育</a><a href="#skills">技能</a><a href="#works">%(works_nav)s</a><a href="#contact">联系</a>
</div></div></nav>
<main id="top">
<section class="hero"><div class="wrap hero__inner"><div>
<p class="hero__eyebrow">%(eyebrow)s</p>
<h1 class="hero__name">%(name)s<small>%(en)s</small></h1>
<p class="hero__role">%(role)s</p>
<ul class="hero__meta">%(meta)s</ul>
<div class="hero__cta"><a class="btn btn--primary" href="assets/resume.pdf" target="_blank" rel="noopener">下载 PDF 简历</a>
<a class="btn btn--ghost" href="mailto:%(email)s">%(email)s</a></div>
</div><div class="hero__avatar"><img src="assets/img/avatar.jpg" alt="%(name)s" width="520" height="689"></div>
</div></section>

<section class="section section--alt" id="about"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">About</span><h2 class="section__title">关于我</h2></div>
<div class="about"><div class="about__text reveal">%(about)s</div>
<aside class="facts reveal"><dl>%(facts)s</dl></aside></div>
<div class="stats reveal">%(stats)s</div>
</div></section>

<section class="section" id="experience"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Experience</span><h2 class="section__title">工作经历</h2></div>
<ol class="timeline reveal">%(exp)s</ol>
</div></section>

<section class="section section--alt" id="projects"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Projects</span><h2 class="section__title">项目经历</h2></div>
<div class="projects">%(proj)s</div>
</div></section>

<section class="section" id="education"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Education</span><h2 class="section__title">教育背景</h2></div>
<ol class="timeline reveal">%(edu)s</ol>
</div></section>

<section class="section section--alt" id="skills"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Skills</span><h2 class="section__title">专业能力</h2></div>
<div class="about__text reveal">%(skills)s</div>
</div></section>

<section class="section" id="works"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Works</span><h2 class="section__title">%(works_title)s</h2>
<p class="section__desc">%(works_desc)s</p></div>
<div class="projects">%(works)s</div>
<div class="section__head reveal"><span class="section__kicker">Honors</span><h2 class="section__title">荣誉与成果</h2></div>
<ol class="timeline reveal">%(honors)s</ol>
</div></section>

<section class="section section--alt" id="contact"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Contact</span><h2 class="section__title">联系</h2></div>
<div class="contact-grid reveal">%(contacts)s</div>
</div></section>
</main>
<footer class="footer"><div class="wrap">© 2026 %(name)s · 样例版式</div></footer>
<script src="assets/js/main.js"></script>
</body>
</html>
""" % dict(name=name, title=p["title"], seo=p["seo"], eyebrow=p["eyebrow"], en=en, role=p["role"],
           meta=meta_li, email=p["email"], about=about, facts=facts, stats=stats, exp=exp_html,
           proj=proj_html, edu=edu_html, skills=skills, works_title=p["works_title"],
           works_desc=p["works_desc"], works=works, honors=honors, contacts=contacts,
           works_nav=p["works_title"][-2:])

def build_print(p):
    name = p["name"]
    edu = []
    for e in p["education"]:
        edu.append('<div class="item"><div class="row"><div><span class="org">%s</span>'
                   '<span class="role">%s</span></div><span class="date">%s</span></div>'
                   '<p class="meta">%s</p></div>' % (e["school"], e["major"].split("（")[0], e["date"], " ".join(e["bullets"])))
    edu = "".join(edu)
    skills = "".join("<li><b>%s：</b>%s</li>" % (k, v) for k, v in p["skills"])
    exp = []
    for e in p["experience"]:
        bl = "".join("<li>%s</li>" % b for b in e["bullets"])
        exp.append('<div class="item"><div class="row"><div><span class="org">%s</span>'
                   '<span class="role">%s</span></div><span class="date">%s</span></div><ul>%s</ul></div>'
                   % (e["org"].split("（")[0], e["title"], e["date"], bl))
    exp = "".join(exp)
    proj = "".join('<div class="item"><div class="row"><div><span class="org">%s</span>'
                   '<span class="role">%s</span></div><span class="date">%s</span></div>'
                   '<ul><li>%s</li></ul></div>' % (pr["title"].split("：")[0], "", pr["date"], pr["desc"])
                   for pr in p["projects"][:2])
    honors = "".join("<li>%s（%s）</li>" % (t, d) for t, d in p["honors"])
    wk = "".join('<div class="item"><div class="row"><div><span class="org">%s</span>'
                 '<span class="role">%s</span></div></div><ul><li>%s</li></ul></div>'
                 % (w["title"], w["tag"], w["desc"]) for w in p["works"])
    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="robots" content="noindex, nofollow">
<title>%(name)s · 简历</title><style>%(css)s</style></head><body>
<header><div class="hdr"><div class="hdr__text">
<h1>%(name)s</h1>
<p class="tagline">%(tagline)s</p>
<p class="contact">%(contact)s</p>
</div><div class="hdr__side">
<figure class="hdr__qr"><img src="assets/img/qr-site.png" alt="扫码查看在线简历"><figcaption>在线简历</figcaption></figure>
<img class="hdr__photo" src="assets/img/avatar.jpg" alt="%(name)s">
</div></div></header>

<h2>求职意向</h2>
<div class="item" style="margin-bottom:2pt"><p class="meta" style="margin:0">%(intent)s</p></div>

<h2>教育背景</h2>%(edu)s

<h2>核心技能</h2>
<ul class="skills">%(skills)s</ul>

<h2>工作经历</h2>%(exp)s

<h2>项目经历</h2>%(proj)s

<h2>%(works_title)s</h2>%(wk)s

<h2>荣誉与成果</h2>
<ul>%(honors)s</ul>
</body></html>
""" % dict(name=name, css=PRINT_CSS, tagline=p["tagline"], contact=p["meta"][0] + " · " + p["meta"][2] + " · " + p["email"],
           intent=p["intent"], edu=edu, skills=skills, exp=exp, proj=proj, honors=honors,
           wk=wk, works_title=p["works_title"])

def build_gallery(ps):
    cards = []
    for p in ps:
        cards.append('<a class="card reveal" href="%(slug)s/" style="text-decoration:none;color:inherit">'
                     '<div class="card__top"><span class="tag">%(disc)s</span><span class="card__date">%(title)s</span></div>'
                     '<h3 class="card__title">%(name)s</h3>'
                     '<p class="card__desc">%(tagline)s</p>'
                     '<div class="card__stack"><span class="chip">在线简历站</span><span class="chip">一页 PDF</span>'
                     '<span class="chip">扫码入口</span></div></a>'
                     % dict(slug=p["slug"], disc=p["discipline"], title=p["title"], name=p["name"], tagline=p["tagline"]))
    cards = "".join(cards)
    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>简历样例 · 工科 / 理科 / 文科 / 社科</title>
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="assets/css/style.css"></head><body>
<nav class="nav"><div class="nav__inner"><a class="nav__brand" href="#top">简历样例</a>
<div class="nav__links"><a href="#list">四份样例</a><a href="#how">怎么做的</a></div></div></nav>
<main id="top">
<section class="hero"><div class="wrap"><p class="hero__eyebrow">样例 · 不是真实求职者</p>
<h1 class="hero__name">同一套做法，四种学科</h1>
<p class="hero__role">每份都是「在线简历站 + 一页 A4 的 PDF + 印在 PDF 上的二维码」，三种形态同源。点进去可以看完整版，右上角二维码扫出来的就是它自己。</p>
</div></section>
<section class="section section--alt" id="list"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">Samples</span><h2 class="section__title">四份样例</h2></div>
<div class="projects">%s</div>
</div></section>
<section class="section" id="how"><div class="wrap">
<div class="section__head reveal"><span class="section__kicker">How</span><h2 class="section__title">同一套流程</h2></div>
<div class="about__text reveal">
<p>人物与经历均为虚构，用于展示版式与写法，不代表真实求职者。</p>
<p>四份样例用同一个版式，区别在留下什么：工科留指标，理科留方法和口径，文科留作品和数据，社科留研究过程和结论。</p>
</div></div></section>
</main>
<footer class="footer"><div class="wrap">© 2026 简历样例 · 仅供展示</div></footer>
<script src="assets/js/main.js"></script></body></html>
""" % cards

for p in PERSONAS:
    d = os.path.join(ROOT, p["slug"])
    os.makedirs(os.path.join(d, "assets", "img"), exist_ok=True)
    os.makedirs(os.path.join(d, "assets", "css"), exist_ok=True)
    os.makedirs(os.path.join(d, "assets", "js"), exist_ok=True)
    os.makedirs(os.path.join(d, "assets"), exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index(p))
    with open(os.path.join(d, "resume-print.html"), "w", encoding="utf-8") as f:
        f.write(build_print(p))
    open(os.path.join(d, ".nojekyll"), "a").close()

os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(build_gallery(PERSONAS))

print("sites built:", [p["slug"] for p in PERSONAS])
