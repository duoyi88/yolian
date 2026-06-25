#!/usr/bin/env python3
"""Build a self-contained, password-gated static site from the Yolian research docs.

Re-run after editing any of the source markdown files:
    python3 build_site.py
Outputs site/index.html (screenshots + marked.min.js already in site/).
"""
import os
import glob
import html
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "docs")  # GitHub Pages serves from /docs
SHOTS_SRC = os.path.join(BASE, "research", "screenshots")
SHOTS_DST = os.path.join(SITE, "screenshots")
PASSWORD = "555"

# ---- source documents (id, title, path) ----
DOCS = [
    ("research", "競品研究（台/外/中）", os.path.join(BASE, "research", "competitor-research.md")),
    ("deepdive", "競品深度拆解", os.path.join(BASE, "research", "deep-dive-competitors.md")),
    ("product", "Yolian 產品架構", os.path.join(BASE, "product", "product-architecture.md")),
    ("modalities", "工作室項目類型分析", os.path.join(BASE, "research", "studio-modalities.md")),
    ("style", "UI 風格系統", os.path.join(BASE, "research", "ui-style-system.md")),
    ("opensource", "開源整併與授權", os.path.join(BASE, "research", "open-source-strategy.md")),
    ("journeys", "使用者歷程", os.path.join(BASE, "product", "user-journeys.md")),
    ("ossstack", "開源採用與缺口", os.path.join(BASE, "research", "oss-stack-and-gaps.md")),
    ("backlog", "開發項目", os.path.join(BASE, "product", "dev-backlog.md")),
]

# ---- screenshot captions ----
CAPTIONS = {
    "onefloors-home.png": "OneFloors 首頁（功能/雙角色/FAQ）",
    "onefloors-pricing.png": "OneFloors 三方案定價",
    "onefloors-coach-templates.png": "OneFloors 7 種教練網站版型",
    "onefloors-coach-ironclad.png": "OneFloors 教練網站實例 Ironclad",
    "onefloors-coach-atelier.png": "OneFloors 版型 Atelier（瑜伽）",
    "onefloors-coach-concrete.png": "OneFloors 版型 Concrete（極簡）",
    "onefloors-appstore.png": "OneFloors App Store 頁",
    "onefloors-app-screens.png": "OneFloors App 實機畫面 1-3",
    "onefloors-app-screens2.png": "OneFloors App 實機畫面 2-4（InBody）",
    "simpletraining-home.png": "SimpleTraining 首頁（7 模組）",
    "simpletraining-signup.png": "SimpleTraining 註冊（Google OAuth）",
    "simpletraining-guide.png": "SimpleTraining 使用指南/後台流程",
    "trainerize-features.png": "Trainerize 功能總頁",
    "trainerize-pricing.png": "Trainerize 定價與功能比較",
    "mohot-home.png": "MoHot 全產品線",
    "17fit-home.png": "17FIT 首頁（雙入口）",
    "17fit-business.png": "17FIT 商家端 11 模組",
    "17fit-booking.png": "17FIT 預約模組",
    "17fit-report.png": "17FIT 報表模組（20+）",
    "17fit-customer.png": "17FIT 客戶管理",
    "17fit-pos.png": "17FIT POS",
    "17fit-iot.png": "17FIT 入出場 IoT",
    "mindbody-home.png": "Mindbody 首頁（7 模組）",
    "mindbody-pricing.png": "Mindbody 定價 + Messenger[ai]",
    "mindbody-scheduling.png": "Mindbody 排程功能",
    "mindbody-messenger-ai.png": "Mindbody Messenger[ai] AI 前台",
    "pushpress-pricing.png": "PushPress 定價 + AI Assistant",
    "glofox-pricing.png": "Glofox 詢價頁",
    "styd-home.png": "三体云动首頁（SaaS+AIoT）",
    "styd-ai-assistant.png": "三体 AI 小助理 實測對話",
    "qingcheng-home.png": "青橙科技首頁（AI 賦能）",
    "keep-home.png": "Keep 首頁",
    "leoao-home.png": "乐刻运动首頁",
    "supermonkey-home.png": "超级猩猩首頁",
}


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# copy screenshots
os.makedirs(SHOTS_DST, exist_ok=True)
for p in glob.glob(os.path.join(SHOTS_SRC, "*.png")):
    shutil.copy2(p, SHOTS_DST)

# build nav buttons
nav_items = ['<button class="nav-btn active" data-target="overview">總覽</button>']
for did, title, _ in DOCS:
    nav_items.append(f'<button class="nav-btn" data-target="{did}">{html.escape(title)}</button>')
nav_items.append('<button class="nav-btn" data-target="gallery">截圖（34）</button>')
nav_items.append('<a class="nav-btn nav-ext" href="exercises.html">動作庫（873）↗</a>')
nav_html = "\n".join(nav_items)

# build markdown script blocks + sections
md_blocks = []
sections = []
for did, title, path in DOCS:
    md = read(path)
    # guard against premature </script>
    md = md.replace("</script>", "<\\/script>")
    md_blocks.append(f'<script type="text/markdown" id="md-{did}">\n{md}\n</script>')
    sections.append(f'<section class="doc-section" id="sec-{did}" hidden><article class="md" id="art-{did}"></article></section>')

# gallery (competitor screenshots only; style-*.png are design mockups shown inline in the UI-style doc)
shots = sorted(
    (p for p in glob.glob(os.path.join(SHOTS_DST, "*.png"))
     if not os.path.basename(p).startswith("style-")),
    key=lambda p: os.path.basename(p),
)
cards = []
for p in shots:
    fn = os.path.basename(p)
    cap = CAPTIONS.get(fn, fn)
    cards.append(
        f'<figure class="shot"><img loading="lazy" src="screenshots/{fn}" alt="{html.escape(cap)}" '
        f'data-full="screenshots/{fn}"><figcaption>{html.escape(cap)}</figcaption></figure>'
    )
gallery_html = "\n".join(cards)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Yolian — 健身平台研究與產品藍圖</title>
<style>
:root{
  --accent:#14b8a6; --accent-d:#0d9488; --ink:#0f172a; --muted:#64748b;
  --bg:#f6f8fa; --card:#ffffff; --line:#e2e8f0; --sidebar:#0f172a;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang TC","Microsoft JhengHei","Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;-webkit-font-smoothing:antialiased}

/* password gate */
#gate{position:fixed;inset:0;z-index:1000;background:linear-gradient(135deg,#0f172a,#134e4a);display:flex;align-items:center;justify-content:center;padding:24px}
#gate .card{background:var(--card);border-radius:18px;padding:40px 34px;max-width:380px;width:100%;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.35)}
#gate .logo{font-size:30px;font-weight:800;letter-spacing:.5px}
#gate .logo span{color:var(--accent)}
#gate p{color:var(--muted);margin:.4em 0 1.4em;font-size:14px}
#gate input{width:100%;padding:13px 15px;font-size:18px;text-align:center;letter-spacing:.3em;border:1.5px solid var(--line);border-radius:11px;outline:none}
#gate input:focus{border-color:var(--accent)}
#gate button{margin-top:14px;width:100%;padding:13px;font-size:16px;font-weight:700;color:#fff;background:var(--accent);border:none;border-radius:11px;cursor:pointer}
#gate button:hover{background:var(--accent-d)}
#gate .err{color:#e11d48;font-size:13px;height:18px;margin-top:10px}

/* layout */
#app{display:none;min-height:100vh}
.sidebar{position:fixed;top:0;left:0;bottom:0;width:248px;background:var(--sidebar);color:#cbd5e1;padding:22px 16px;overflow-y:auto}
.brand{font-size:22px;font-weight:800;color:#fff;padding:6px 10px 4px}
.brand span{color:var(--accent)}
.tag{font-size:12px;color:#94a3b8;padding:0 10px 18px;border-bottom:1px solid #1e293b;margin-bottom:14px}
.nav-btn{display:block;width:100%;text-align:left;background:none;border:none;color:#cbd5e1;font-size:14.5px;padding:11px 12px;border-radius:9px;cursor:pointer;margin-bottom:3px;font-family:inherit}
.nav-btn:hover{background:#1e293b;color:#fff}
.nav-btn.active{background:var(--accent);color:#fff;font-weight:700}
a.nav-btn{text-decoration:none}
a.nav-ext{color:#5eead4;font-weight:600}
a.nav-ext:hover{background:#1e293b;color:#fff}
.side-foot{font-size:11px;color:#64748b;padding:16px 12px 0;margin-top:10px;border-top:1px solid #1e293b}
.main{margin-left:248px;padding:38px 46px 80px;max-width:1180px}

/* overview */
.hero{background:linear-gradient(135deg,#0f172a,#134e4a);color:#fff;border-radius:18px;padding:40px 38px;margin-bottom:30px}
.hero h1{margin:.1em 0 .3em;font-size:30px}
.hero .lead{font-size:17px;color:#a7f3d0;max-width:760px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:26px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px}
.kpi b{display:block;font-size:26px;color:var(--accent-d)}
.kpi span{font-size:13px;color:var(--muted)}
.callout{background:#ecfeff;border:1px solid #99f6e4;border-left:4px solid var(--accent);border-radius:10px;padding:16px 18px;margin:18px 0}
.ov-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:22px}
.ov-links button,.ov-links .ov-card-link{display:block;text-align:left;background:var(--card);border:1px solid var(--line);border-radius:13px;padding:18px;cursor:pointer;font-family:inherit;text-decoration:none;color:inherit}
.ov-links button:hover,.ov-links .ov-card-link:hover{border-color:var(--accent);box-shadow:0 6px 18px rgba(20,184,166,.12)}
.ov-links b{display:block;font-size:16px;margin-bottom:4px}
.ov-links span{font-size:13px;color:var(--muted)}
.ov-card-link{border-color:#99f6e4;background:#f0fdfa}

/* markdown */
.md{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:34px 40px}
.md h1{font-size:27px;border-bottom:2px solid var(--line);padding-bottom:.3em;margin-top:0}
.md h2{font-size:21px;margin-top:1.7em;border-bottom:1px solid var(--line);padding-bottom:.25em}
.md h3{font-size:17px;margin-top:1.4em}
.md h4{font-size:15px;color:var(--muted)}
.md p,.md li{font-size:14.5px}
.md a{color:var(--accent-d)}
.md code{background:#f1f5f9;padding:.15em .4em;border-radius:5px;font-size:.88em}
.md pre{background:#0f172a;color:#e2e8f0;padding:16px;border-radius:10px;overflow:auto;font-size:12.5px;line-height:1.5}
.md pre code{background:none;color:inherit;padding:0}
.md blockquote{margin:1em 0;padding:.6em 1.1em;background:#ecfeff;border-left:4px solid var(--accent);border-radius:6px;color:#0f172a}
.md table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:13px;display:block;overflow-x:auto}
.md th,.md td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
.md th{background:#f1f5f9;font-weight:700;white-space:nowrap}
.md tr:nth-child(even){background:#f8fafc}
.md hr{border:none;border-top:1px solid var(--line);margin:2em 0}

/* gallery */
.gal-head{margin-bottom:8px}
.gal-head p{color:var(--muted);font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:18px;margin-top:18px}
.shot{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;cursor:zoom-in}
.shot img{width:100%;height:170px;object-fit:cover;object-position:top;display:block;background:#eef2f6}
.shot figcaption{padding:10px 12px;font-size:12.5px;color:var(--muted)}

/* lightbox */
#lb{position:fixed;inset:0;z-index:900;background:rgba(15,23,42,.92);display:none;align-items:center;justify-content:center;padding:30px;cursor:zoom-out}
#lb img{max-width:96%;max-height:92%;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.5)}
#lb .cap{position:fixed;bottom:18px;left:0;right:0;text-align:center;color:#cbd5e1;font-size:13px}

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
    <div class="logo">Yo<span>lian</span></div>
    <p>健身平台研究與產品藍圖 · 請輸入存取密碼</p>
    <input id="pw" type="password" inputmode="numeric" autocomplete="off" placeholder="••••" autofocus>
    <button type="submit">進入</button>
    <div class="err" id="err"></div>
  </form>
</div>

<button class="menu-btn" id="menuBtn" aria-label="menu">☰</button>

<div id="app">
  <aside class="sidebar" id="sidebar">
    <div class="brand">Yo<span>lian</span></div>
    <div class="tag">健身教練 / 工作室營運平台</div>
    __NAV__
    <div class="side-foot">同業研究 · 競品深度拆解 · 產品藍圖<br>2026 · 內部文件</div>
  </aside>

  <main class="main">
    <section class="doc-section" id="sec-overview">
      <div class="hero">
        <h1>用「對話」就能跑的健身工作室營運系統</h1>
        <p class="lead">把「教練行政效率」「學員看得見成長」「跨模組 AI Agent 操作」三件事，第一次縫進同一個產品。</p>
      </div>
      <div class="cards">
        <div class="kpi"><b>3 地</b><span>台灣 / 國外 / 中國 完整盤點</span></div>
        <div class="kpi"><b>30+</b><span>競品逐一拆解</span></div>
        <div class="kpi"><b>34 張</b><span>實地探查截圖佐證</span></div>
        <div class="kpi"><b>0 家</b><span>同時做到訓練深度+完整營運+AI Agent</span></div>
      </div>
      <div class="callout"><b>核心發現：</b>全市場的 AI 只到三種——生成內容、唯讀查詢、對外客服賣課。<b>沒有人做「教練端、跨模組的對話式寫入操作」</b>，這就是 Yolian 的真空白。</div>
      <h3>文件導覽</h3>
      <div class="ov-links" id="ovLinks">
        <button data-target="research"><b>競品研究（台/外/中）</b><span>三地服務商總覽、功能、定價、AI 缺口分析</span></button>
        <button data-target="deepdive"><b>競品深度拆解</b><span>逐家功能/定價/後台/App 實機畫面 + 試用紀錄</span></button>
        <button data-target="product"><b>Yolian 產品架構</b><span>定位、資料模型、Agent 能力目錄、MVP 範圍</span></button>
        <button data-target="modalities"><b>工作室項目類型分析</b><span>窮舉 7 大家族 × T0–T3 引擎相容分級：客群要廣又對焦，誰服務誰排除</span></button>
        <button data-target="style"><b>UI 風格系統</b><span>6 風格原型 × Dark/Light × 多租戶品牌識別（Pencil 模擬）</span></button>
        <button data-target="opensource"><b>開源整併與授權</b><span>開源→商業服務策略、買借造矩陣、授權合規與地雷</span></button>
        <button data-target="ossstack"><b>開源採用與缺口</b><span>開源資源逐一採用方案、授權紅線、功能缺口評估</span></button>
        <button data-target="backlog"><b>開發項目</b><span>整併三份文件的可追蹤開發 backlog（Epic / 階段 / 依賴）</span></button>
        <button data-target="gallery"><b>截圖庫</b><span>34 張競品實地截圖</span></button>
        <a class="ov-card-link" href="exercises.html"><b>動作庫（873）↗</b><span>free-exercise-db 繁中化 · 分類/部位/器材篩選 + 搜尋 + YouTube 示範</span></a>
      </div>
    </section>

    __SECTIONS__

    <section class="doc-section" id="sec-gallery" hidden>
      <div class="gal-head"><h1>競品截圖庫</h1><p>實地走訪官網/功能頁/定價頁/App Store，逐一截圖存證（點圖放大）。</p></div>
      <div class="grid">__GALLERY__</div>
    </section>
  </main>
</div>

<div id="lb"><img src="" alt=""><div class="cap"></div></div>

<script src="marked.min.js"></script>
__MDBLOCKS__
<script>
(function(){
  var PW="__PASSWORD__";
  var gate=document.getElementById('gate'), app=document.getElementById('app');
  // session unlock
  if(sessionStorage.getItem('yolian_ok')==='1'){gate.style.display='none';app.style.display='block';}
  document.getElementById('gate-form').addEventListener('submit',function(e){
    e.preventDefault();
    var v=document.getElementById('pw').value.trim();
    if(v===PW){sessionStorage.setItem('yolian_ok','1');gate.style.display='none';app.style.display='block';render();}
    else{document.getElementById('err').textContent='密碼錯誤，請再試一次';document.getElementById('pw').value='';}
  });

  // render markdown lazily
  var rendered={};
  function renderDoc(id){
    if(rendered[id])return;
    var src=document.getElementById('md-'+id);
    var art=document.getElementById('art-'+id);
    if(src&&art){art.innerHTML=marked.parse(src.textContent);rendered[id]=true;}
  }
  function render(){ /* nothing eager */ }

  function show(target){
    document.querySelectorAll('.doc-section').forEach(function(s){s.hidden=true;});
    var sec=document.getElementById('sec-'+target);
    if(sec){sec.hidden=false;}
    if(target!=='overview'&&target!=='gallery')renderDoc(target);
    document.querySelectorAll('.nav-btn').forEach(function(b){b.classList.toggle('active',b.dataset.target===target);});
    window.scrollTo(0,0);
    document.getElementById('sidebar').classList.remove('open');
  }
  document.querySelectorAll('.nav-btn').forEach(function(b){if(!b.dataset.target)return;b.addEventListener('click',function(){show(b.dataset.target);});});
  document.getElementById('ovLinks').querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.target);});});

  document.getElementById('menuBtn').addEventListener('click',function(){document.getElementById('sidebar').classList.toggle('open');});

  // lightbox
  var lb=document.getElementById('lb'),lbImg=lb.querySelector('img'),lbCap=lb.querySelector('.cap');
  document.addEventListener('click',function(e){
    var img=e.target.closest('.shot img');
    if(img){lbImg.src=img.dataset.full;lbCap.textContent=img.alt;lb.style.display='flex';}
    else if(e.target.closest('#lb')){lb.style.display='none';lbImg.src='';}
  });
})();
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__NAV__", nav_html)
       .replace("__SECTIONS__", "\n".join(sections))
       .replace("__GALLERY__", gallery_html)
       .replace("__MDBLOCKS__", "\n".join(md_blocks))
       .replace("__PASSWORD__", PASSWORD))

with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(out)

print("Built docs/index.html  (%d docs, %d screenshots)" % (len(DOCS), len(shots)))
