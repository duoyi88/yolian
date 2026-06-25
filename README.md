# Noki — 健身教練 / 工作室營運平台

面向健身教練與個人工作室的營運平台研究與產品藍圖。核心願景：讓教練工作更輕鬆有效率、學員看得見成長、程式化前端 + Agent-like AI 操作窗口。

## 內容
- `research/competitor-research.md` — 台灣 / 國外 / 中國 同業研究 + AI 缺口分析
- `research/deep-dive-competitors.md` — 競品逐家深度拆解（含後台 / App 實機畫面）
- `research/screenshots/` — 34 張競品實地截圖
- `product/product-architecture.md` — Noki 產品架構、資料模型、Agent 能力目錄、MVP 範圍
- `docs/` — 由上述文件產生的可瀏覽網站（GitHub Pages 發布目錄）

## 線上瀏覽
GitHub Pages（發布目錄 `docs/`）。進入密碼：`555`（前端閘門，僅作輕量遮蔽，非資安加密）。

## 重新產生網站
編輯任一來源 Markdown 後執行：

```bash
python3 build_site.py
```

會讀取 `research/*.md` + `product/*.md`、複製 `research/screenshots/`，輸出 `docs/index.html`。

## 本機預覽
```bash
cd docs && python3 -m http.server
```
