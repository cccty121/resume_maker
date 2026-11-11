# -*- coding: utf-8 -*-
import json, os, shutil
from PIL import Image

ROOT = r"D:\work\resume_maker"
PIG = r"C:\Users\50357\.dsh\attachments\v1\objects\81\811d3c554386cf131642359fefe100ee1c61a94e9d399d2abe612da45d733d31"
with open(os.path.join(ROOT, "tools", "personas.json"), "r", encoding="utf-8") as f:
    personas = json.load(f)["personas"]

src = Image.open(PIG).convert("RGB")
w, h = src.size
# 3:4 portrait crop, centered
tw = int(h * 0.75)
left = (w - tw) // 2
portrait = src.crop((left, 0, left + tw, h)).resize((520, 689), Image.LANCZOS)
icon180 = src.resize((180, 180), Image.LANCZOS)
icon32 = src.resize((32, 32), Image.LANCZOS)

targets = [os.path.join(ROOT, "assets", "img")] + [os.path.join(ROOT, p["slug"], "assets", "img") for p in personas]
for d in targets:
    os.makedirs(d, exist_ok=True)
    portrait.save(os.path.join(d, "avatar.jpg"), quality=90)
    icon180.save(os.path.join(d, "avatar-180.png"))
    icon32.save(os.path.join(d, "avatar-32.png"))

# shared css/js
css_src = r"D:\work\resume_create\templates\tokens.css"
js_src = r"D:\work\resume_create\templates\main.js"
for p in personas:
    d = os.path.join(ROOT, p["slug"], "assets")
    shutil.copyfile(css_src, os.path.join(d, "css", "style.css"))
    shutil.copyfile(js_src, os.path.join(d, "js", "main.js"))
os.makedirs(os.path.join(ROOT, "assets", "css"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "assets", "js"), exist_ok=True)
shutil.copyfile(css_src, os.path.join(ROOT, "assets", "css", "style.css"))
shutil.copyfile(js_src, os.path.join(ROOT, "assets", "js", "main.js"))

# plant the shared hero avatar for the gallery page
portrait.save(os.path.join(ROOT, "assets", "img", "avatar.jpg"), quality=90)
print("assets ready, portrait", portrait.size)
