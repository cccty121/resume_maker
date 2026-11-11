# resume_maker · 简历样例站（工科 / 理科 / 文科 / 社科）

一个仓库放四份样例，每份都是「在线简历站 + 一页 A4 PDF + 印在 PDF 上的二维码」，三种形态同源。

- 展厅：https://cccty121.github.io/resume_maker/
- 工科：https://cccty121.github.io/resume_maker/eng/ （林嘉禾 · 视觉算法）
- 理科：https://cccty121.github.io/resume_maker/sci/ （江牧 · 数据分析）
- 文科：https://cccty121.github.io/resume_maker/arts/ （温言 · 内容运营）
- 社科：https://cccty121.github.io/resume_maker/soc/ （许问 · 用户研究）

人物与经历全部虚构，头像是一张卡通猪。两样都是**样例标记**：防止有人把样例当真实简历投出去，也让作品一眼看出是演示件。

## 目录

```
index.html              展厅（四张卡片，点进去看各自完整版）
eng/ sci/ arts/ soc/    四份样例，每份自包含：
  index.html            在线站
  resume-print.html     一页 A4 打印页
  assets/resume.pdf     已经出好的 PDF
  assets/img/           头像与二维码
  assets/css|js/        共享样式与交互
tools/personas.json     四份样例的全部文案（改这里，重跑脚本）
tools/build_site.py     生成器：JSON → 四个站点
tools/prep_assets.py    头像裁切与共享资源分发
```

## 接单怎么用

**改文案不用碰 HTML。** 编辑 `tools/personas.json` 里对应那一段（学历、经历、项目、技能、荣誉），然后：

```powershell
cd D:\work\resume_maker\tools
python build_site.py
python prep_assets.py
```

会给四个站点重新生成 `index.html` 和 `resume-print.html`，头像与 CSS 自动分发。

**换头像**：直接覆盖各目录下的 `assets/img/avatar.jpg`（520×689）与两个 icon 即可。

**改二维码**：每个目录独立生成，指向自己的地址。

```powershell
cd D:\work\resume_maker\eng
python D:\work\resume_create\tools\make_qr.py --url https://cccty121.github.io/resume_maker/eng/ --out assets/img
```

**出 PDF**（带页数校验，超一页直接报错）：

```powershell
powershell -File D:\work\resume_create\tools\build_pdf.ps1 -Html .\resume-print.html -Out .\assets\resume.pdf -CheckPages 1
```

## 发布

先在 GitHub 建空仓库 `resume_maker`（不勾 README），然后：

```powershell
cd D:\work\resume_maker
git remote add origin https://github.com/cccty121/resume_maker.git
git -c http.proxy=http://127.0.0.1:7897 push -u origin main
```

仓库 Settings → Pages → Source 选 `main` / `/(root)`。首发生效 1-3 分钟。

**注意账号**：这台机器上之前存过另一个账号的凭据。push 时如果提示登录，走 cccty121 的 token，别用旧的。

发布后逐个验收：

```powershell
python D:\work\resume_create\tools\verify_site.py --base https://cccty121.github.io/resume_maker/eng/ --expect-qr https://cccty121.github.io/resume_maker/eng/
```

四个目录各跑一次，`--base` 与 `--expect-qr` 要对应同一个 slug，否则就是串味。

## 隐私三条

- 站点只放邮箱，不放手机号
- 每个页面头部带 `noindex, nofollow`，别删
- 客户单用带随机串的仓库名，不要 `resume_张三`

## 已验收

- 四个 PDF 均为 1 页（构建时校验通过）
- 四个二维码解码回验，各自指向自己的 slug
- 四份样例的网页与打印页事实一致（公司、时间、指标逐条对过）
