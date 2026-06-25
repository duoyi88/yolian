#!/usr/bin/env python3
"""Build a self-contained, password-gated static site for Yolian Music.

This is an INDEPENDENT deployment, separate from the fitness Yolian site
(build_site.py → docs/index.html). It outputs to docs/music/index.html so it
can be served as its own page under GitHub Pages, with its own branding
(violet theme), its own gate, and its own sessionStorage key.

Re-run after editing any source markdown:
    python3 build_music_site.py
"""
import os
import html
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "music")            # source markdown lives here
SITE = os.path.join(BASE, "docs", "music")   # independent sub-deployment
PASSWORD = "555"

# ---- source documents (id, title, path) ----
DOCS = [
    ("assessment", "適配評估", os.path.join(SRC, "assessment.md")),
    ("product", "Yolian Music 產品架構", os.path.join(SRC, "product-architecture.md")),
]


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


os.makedirs(SITE, exist_ok=True)
# self-contained: ship our own marked.min.js copy
shutil.copy2(os.path.join(BASE, "docs", "marked.min.js"),
            os.path.join(SITE, "marked.min.js"))

# nav buttons
nav_items = ['<button class="nav-btn active" data-target="overview">總覽</button>']
for did, title, _ in DOCS:
    nav_items.append(f'<button class="nav-btn" data-target="{did}">{html.escape(title)}</button>')
nav_items.append('<a class="nav-btn nav-ext" href="../index.html">健身版 Yolian ↗</a>')
nav_html = "\n".join(nav_items)

# markdown script blocks + sections
md_blocks = []
sections = []
for did, title, path in DOCS:
    md = read(path)
    md = md.replace("</script>", "<\\/script>")  # guard premature close
    md_blocks.append(f'<script type="text/markdown" id="md-{did}">\n{md}\n</script>')
    sections.append(f'<section class="doc-section" id="sec-{did}" hidden><article class="md" id="art-{did}"></article></section>')

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Yolian Music — 音樂教學營運平台（評估與系統說明）</title>
<style>
:root{
  --accent:#7c3aed; --accent-d:#6d28d9; --ink:#1e1b2e; --muted:#6b6480;
  --bg:#f7f5fb; --card:#ffffff; --line:#e7e3f0; --sidebar:#1e1b2e;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Microsoft JhengHei","Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;-webkit-font-smoothing:antialiased}

/* password gate */
#gate{position:fixed;inset:0;z-index:1000;background:linear-gradient(135deg,#1e1b2e,#4c1d95);display:flex;align-items:center;justify-content:center;padding:24px}
#gate .card{background:var(--card);border-radius:18px;padding:40px 34px;max-width:380px;width:100%;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.35)}
#gate .logo{font-size:30px;font-weight:800;letter-spacing:.5px}
#gate .logo span{color:var(--accent)}
#gate .logo small{display:block;font-size:13px;font-weight:600;color:var(--muted);letter-spacing:.18em;margin-top:4px}
#gate p{color:var(--muted);margin:.4em 0 1.4em;font-size:14px}
#gate input{width:100%;padding:13px 15px;font-size:18px;text-align:center;letter-spacing:.3em;border:1.5px solid var(--line);border-radius:11px;outline:none}
#gate input:focus{border-color:var(--accent)}
#gate button{margin-top:14px;width:100%;padding:13px;font-size:16px;font-weight:700;color:#fff;background:var(--accent);border:none;border-radius:11px;cursor:pointer}
#gate button:hover{background:var(--accent-d)}
#gate .err{color:#e11d48;font-size:13px;height:18px;margin-top:10px}

/* layout */
#app{display:none;min-height:100vh}
.sidebar{position:fixed;top:0;left:0;bottom:0;width:248px;background:var(--sidebar);color:#cbc5dc;padding:22px 16px;overflow-y:auto}
.brand{font-size:22px;font-weight:800;color:#fff;padding:6px 10px 0}
.brand span{color:var(--accent)}
.brand small{display:block;font-size:12px;font-weight:600;color:#a99fd0;letter-spacing:.16em;margin-top:2px}
.tag{font-size:12px;color:#9b93b8;padding:8px 10px 18px;border-bottom:1px solid #322c47;margin-bottom:14px}
.nav-btn{display:block;width:100%;text-align:left;background:none;border:none;color:#cbc5dc;font-size:14.5px;padding:11px 12px;border-radius:9px;cursor:pointer;margin-bottom:3px;font-family:inherit}
.nav-btn:hover{background:#322c47;color:#fff}
.nav-btn.active{background:var(--accent);color:#fff;font-weight:700}
a.nav-btn{text-decoration:none}
a.nav-ext{color:#c4b5fd;font-weight:600}
a.nav-ext:hover{background:#322c47;color:#fff}
.side-foot{font-size:11px;color:#6b6488;padding:16px 12px 0;margin-top:10px;border-top:1px solid #322c47}
.main{margin-left:248px;padding:38px 46px 80px;max-width:1180px}

/* overview */
.hero{background:linear-gradient(135deg,#1e1b2e,#4c1d95);color:#fff;border-radius:18px;padding:40px 38px;margin-bottom:30px}
.hero h1{margin:.1em 0 .3em;font-size:30px}
.hero .lead{font-size:17px;color:#ddd0f7;max-width:760px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:26px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px}
.kpi b{display:block;font-size:26px;color:var(--accent-d)}
.kpi span{font-size:13px;color:var(--muted)}
.callout{background:#f5f0ff;border:1px solid #ddd0f7;border-left:4px solid var(--accent);border-radius:10px;padding:16px 18px;margin:18px 0}
.ov-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:22px}
.ov-links button,.ov-links .ov-card-link{display:block;text-align:left;background:var(--card);border:1px solid var(--line);border-radius:13px;padding:18px;cursor:pointer;font-family:inherit;text-decoration:none;color:inherit}
.ov-links button:hover,.ov-links .ov-card-link:hover{border-color:var(--accent);box-shadow:0 6px 18px rgba(124,58,237,.14)}
.ov-links b{display:block;font-size:16px;margin-bottom:4px}
.ov-links span{font-size:13px;color:var(--muted)}
.ov-card-link{border-color:#ddd0f7;background:#faf7ff}

/* markdown */
.md{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:34px 40px}
.md h1{font-size:27px;border-bottom:2px solid var(--line);padding-bottom:.3em;margin-top:0}
.md h2{font-size:21px;margin-top:1.7em;border-bottom:1px solid var(--line);padding-bottom:.25em}
.md h3{font-size:17px;margin-top:1.4em}
.md h4{font-size:15px;color:var(--muted)}
.md p,.md li{font-size:14.5px}
.md a{color:var(--accent-d)}
.md code{background:#f1ecfb;padding:.15em .4em;border-radius:5px;font-size:.88em}
.md pre{background:#1e1b2e;color:#e7e3f0;padding:16px;border-radius:10px;overflow:auto;font-size:12.5px;line-height:1.5}
.md pre code{background:none;color:inherit;padding:0}
.md blockquote{margin:1em 0;padding:.6em 1.1em;background:#f5f0ff;border-left:4px solid var(--accent);border-radius:6px;color:#1e1b2e}
.md table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:13px;display:block;overflow-x:auto}
.md th,.md td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
.md th{background:#f1ecfb;font-weight:700;white-space:nowrap}
.md tr:nth-child(even){background:#faf8fe}
.md hr{border:none;border-top:1px solid var(--line);margin:2em 0}

.menu-btn{display:none}
@media(max-width:860px){
  .sidebar{transform:translateX(-100%);transition:.25s;z-index:500;width:230px}
  .sidebar.open{transform:none}
  .main{margin-left:0;padding:64px 18px 60px}
  .md{padding:22px 16px}
  .menu-btn{display:flex;position:fixed;top:12px;left:12px;z-index:600;background:var(--sidebar);color:#fff;border:none;border-radius:9px;width:42px;height:42px;font-size:20px;cursor:pointer;align-items:center;justify-content:center}
  .hero{padding:28px 22px}
}
</style>
</head>
<body>

<div id="gate">
  <form class="card" id="gate-form">
    <div class="logo">Yo<span>lian</span> <small>MUSIC · 有練 音樂版</small></div>
    <p>音樂教學營運平台 · 評估與系統說明 · 請輸入存取密碼</p>
    <input id="pw" type="password" inputmode="numeric" autocomplete="off" placeholder="••••" autofocus>
    <button type="submit">進入</button>
    <div class="err" id="err"></div>
  </form>
</div>

<button class="menu-btn" id="menuBtn" aria-label="menu">☰</button>

<div id="app">
  <aside class="sidebar" id="sidebar">
    <div class="brand">Yo<span>lian</span> <small>MUSIC</small></div>
    <div class="tag">音樂老師 / 音樂教室營運平台</div>
    __NAV__
    <div class="side-foot">適配評估 · 系統說明<br>2026 · 內部文件 · 獨立部署</div>
  </aside>

  <main class="main">
    <section class="doc-section" id="sec-overview">
      <div class="hero">
        <h1>用「對話」就能跑的音樂教學營運系統</h1>
        <p class="lead">把「老師行政效率」「家長看得見孩子的進步」「課與課之間的家庭練習閉環」第一次縫進同一個產品。</p>
      </div>
      <div class="cards">
        <div class="kpi"><b>~80%</b><span>商業模式可從健身版移植</span></div>
        <div class="kpi"><b>4 面</b><span>後台 / Agent / 家長端 / 學生端</span></div>
        <div class="kpi"><b>+1 層</b><span>家長代理帳號（最根本差異）</span></div>
        <div class="kpi"><b>0 家</b><span>同時做到完整營運+練習閉環+AI 副駕</span></div>
      </div>
      <div class="callout"><b>核心判斷：</b>商業模式照搬、<b>引擎重造</b>、<b>加一層家長</b>。OS 層（CRM/排課/合約/訊息/權限/Agent）100% 沿用健身版；重做的只有「曲目精熟引擎」與「家庭練習閉環」，並新增家長代理層——學員多是小孩，無法自行操作。</div>
      <h3>文件導覽</h3>
      <div class="ov-links" id="ovLinks">
        <button data-target="assessment"><b>適配評估</b><span>同一商業模式搬到音樂教學成不成立：可移植性逐層對照、三大結構差異、市場與風險、要不要做的判斷</span></button>
        <button data-target="product"><b>Yolian Music 產品架構</b><span>完全獨立系統說明：定位、含家長層的用戶、產品四面、音樂原生資料模型、Agent、MVP、LINE、與健身版差異</span></button>
        <a class="ov-card-link" href="../index.html"><b>健身版 Yolian ↗</b><span>同源母體平台的完整研究與藍圖（OS 層與 Action 層的來源）</span></a>
      </div>
    </section>

    __SECTIONS__
  </main>
</div>

<script src="marked.min.js"></script>
__MDBLOCKS__
<script>
(function(){
  var PW="__PASSWORD__";
  var gate=document.getElementById('gate'), app=document.getElementById('app');
  if(sessionStorage.getItem('yolian_music_ok')==='1'){gate.style.display='none';app.style.display='block';}
  document.getElementById('gate-form').addEventListener('submit',function(e){
    e.preventDefault();
    var v=document.getElementById('pw').value.trim();
    if(v===PW){sessionStorage.setItem('yolian_music_ok','1');gate.style.display='none';app.style.display='block';render();}
    else{document.getElementById('err').textContent='密碼錯誤，請再試一次';document.getElementById('pw').value='';}
  });

  var rendered={};
  function renderDoc(id){
    if(rendered[id])return;
    var src=document.getElementById('md-'+id);
    var art=document.getElementById('art-'+id);
    if(src&&art){art.innerHTML=marked.parse(src.textContent);rendered[id]=true;}
  }
  function render(){}

  function show(target){
    document.querySelectorAll('.doc-section').forEach(function(s){s.hidden=true;});
    var sec=document.getElementById('sec-'+target);
    if(sec){sec.hidden=false;}
    if(target!=='overview')renderDoc(target);
    document.querySelectorAll('.nav-btn').forEach(function(b){b.classList.toggle('active',b.dataset.target===target);});
    window.scrollTo(0,0);
    document.getElementById('sidebar').classList.remove('open');
  }
  document.querySelectorAll('.nav-btn').forEach(function(b){if(!b.dataset.target)return;b.addEventListener('click',function(){show(b.dataset.target);});});
  document.getElementById('ovLinks').querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.target);});});
  document.getElementById('menuBtn').addEventListener('click',function(){document.getElementById('sidebar').classList.toggle('open');});
})();
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__NAV__", nav_html)
       .replace("__SECTIONS__", "\n".join(sections))
       .replace("__MDBLOCKS__", "\n".join(md_blocks))
       .replace("__PASSWORD__", PASSWORD))

with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(out)

print("Built docs/music/index.html  (%d docs)" % len(DOCS))
