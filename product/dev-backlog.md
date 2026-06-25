# Yolian 開發項目（Dev Backlog）v1

> 本文把三份來源**整併成可執行、可追蹤的開發項目**：
> `product-architecture.md`（藍圖）+ `user-journeys.md`（已定案 MVP 範圍）+ `oss-stack-and-gaps.md`（開源採用方案 + 功能缺口）。
> 日期：2026-06-25 · 狀態：v1 待排期
>
> **狀態圖例**：`[ ]` 未開始 · `[~]` 進行中 · `[x]` 完成　|　**階段**：MVP=Phase 0 · 1.5 · 2
> **ID 規則**：E{epic}.{n}，方便後續在 issue / 看板引用。

---

## 0. 已定案前提（來自 user-journeys.md，不再討論）
- **多教練進 MVP**（主理人 + 教練 + 學員三層權限）。
- **線上金流不進 MVP**：手動對帳（標記已收/部分/未收）。金流 → Phase 1.5。
- **MVP 飲食 = 對話 + 文字筆記**；拍照辨識/營養素 → Phase 2。
- **學員端跑在 LINE LIFF（零安裝）**；教練/主理人以 Web 後台為主 + Agent。
- **系統（UI/Dashboard）為主體、Agent 為加值窗口**：Agent 選擇性使用、省 token（簡單事走 UI、不丟 LLM）；**Agent 輸入框（教練端＋學員端）須支援語音輸入(STT)**。（架構設計原則 #4、#7）

> 整併時的去重原則：journeys §8 已納入的邊界情境（衝堂、no-show、取消政策、堂數用盡、離職交接、同名澄清）**不再當「新缺口」**，直接列為對應 Epic 的 MVP 開發項。`oss-stack-and-gaps.md §4` 真正**新增**的項目以 `★缺口` 標注。

---

## 1. 建議施工順序（關鍵路徑）
1. **E0 技術棧地基** → 沒有共用 Action 層 + Auth + 排程器，後面全卡。
2. **E1 動作庫匯入＋繁中化**（可與 E0 並行，資料前處理）。
3. **E2 CRM/合約 + E3 排課/消課**（核心營運閉環）。
4. **E4 Agent spike**（早期就驗繁中意圖準確率＝最大風險）→ 再長成完整 Agent。
5. **E5 LINE 交付**（先打通「上課提醒 push」這條最高 CP 值鏈）。
6. **E6 品牌頁 / E7 儀表板** 補完 MVP。

---

## 2. Epic E0 — 技術棧地基（Foundation）★最高優先

| ID | 項目 | 階段 | 依賴 | 來源/備註 |
|----|------|:--:|------|----------|
| E0.1 | 定主線技術棧：TypeScript 全棧 — Next.js(PWA) + Prisma + Postgres + Auth.js + Vercel AI SDK + line-bot-sdk + Recharts + BullMQ | MVP | — | oss §3 結論；全部 MIT/Apache 系，授權乾淨同生態 |
| E0.2 | **共用 Action / Query 層**：每個操作 = 一個型別化 Command/Query，**Zod schema 為單一事實來源**，同時供 UI 表單與 Agent tool 使用 | MVP | E0.1 | 架構 §3.1/§8.1；設計原則 #1 的技術載體 |
| E0.3 | 身分驗證：Auth.js + **LINE Login provider**（教練 Email/LINE、學員 LINE） | MVP | E0.1 | journeys §2 |
| E0.4 | **三層 RBAC**：店 → 教練 → 學員 資料邊界與權限 | MVP | E0.3 | journeys §1；架構 §5 有欄位但未設計授權模型 ★缺口 |
| E0.5 | **AgentActionLog（稽核/可撤銷）基礎建設**：所有寫入經此落痕 | MVP | E0.2 | 架構 §5/設計原則 #3 |
| E0.6 | **通知排程引擎**：BullMQ(Redis) + cron，供提醒/週摘要/到期推播 | MVP | E0.1 | ★缺口：journeys 有「規則版提醒」但無對應元件 |

---

## 3. Epic E1 — 動作庫與訓練（Exercise & Training）

| ID | 項目 | 階段 | 依賴 | 來源/備註 |
|----|------|:--:|------|----------|
| E1.1 | 匯入 `free-exercise-db`（800+ JSON + 圖）到**自有 DB / 物件儲存**（不 runtime 依賴對方 GitHub） | MVP | E0.1 | oss §2.1；Unlicense 可商用 |
| E1.2 | **動作庫繁中化**：800 筆 name/instructions LLM 批次初翻 + 教練校對 | MVP | E1.1 | ★缺口（隱性成本）：原資料純英文 |
| E1.3 | 器材/部位 enum 收斂成 Yolian 分類法（對方偶有 null） | MVP | E1.1 | oss §2.1 |
| E1.4 | Exercise / Program / Template 資料模型 + 模板複用 + 指派 | MVP | E0.2 | 架構 §5 |
| E1.5 | WorkoutLog：每組重量/次數、完成度、**本次 vs 上次** | MVP | E1.4 | journeys 教練 J2 |
| E1.6 | **RIR/RPE 自覺強度欄位** | MVP | E1.5 | ★缺口：低成本高價值 |
| E1.7 | 組類型最小化：正式組 / 熱身組 | MVP | E1.4 | ★缺口：Program 結構偏平 |
| E1.8 | 成長折線圖（各動作/體態，Recharts） | MVP | E1.5 | 架構 §6.5；指定圖表庫 |
| E1.9 | 動作影片（靜態圖之外） | 1.5 | E1.1 | free-exercise-db 只有圖，無影片 |
| E1.10 | 自動重量漸進規則（達標自動加重） | 2 | E1.4 | oss §4.2；wger 有，MVP 先手動 |

---

## 4. Epic E2 — CRM / 合約 / 消課

| ID | 項目 | 階段 | 依賴 | 來源/備註 |
|----|------|:--:|------|----------|
| E2.1 | Member CRM：檔案/標籤/來源/狀態 + 時間軸 | MVP | E0.4 | 架構 §5 |
| E2.2 | **健康篩查問卷（PAR-Q）**：新增學員流程內，記傷病/禁忌 | MVP | E2.1 | ★缺口：受傷與法律責任，業界常規 |
| E2.3 | Contract 合約/堂數包：建約、剩餘堂數、到期日 | MVP | E2.1 | 架構 §5 |
| E2.4 | **消課邏輯**：簽到→扣堂→到期/續約提醒鏈→餵流失風險 | MVP | E2.3, E3.4 | 架構 §5.2 核心鏈 |
| E2.5 | 到期提醒（規則版，走 E0.6 排程器） | MVP | E2.3, E0.6 | 架構 §6.3 |
| E2.6 | 手動對帳：合約標記「已收/部分/未收」 | MVP | E2.3 | journeys J3（無線上金流） |
| E2.7 | 彈性體測 Measurement 實體（腰圍/臂圍等自訂，不只 InBody） | 1.5 | E2.1 | ★缺口：BodyComposition 寫死 |
| E2.8 | 會員資料匯出 / 可攜 | 1.5 | E2.1 | ★缺口：信任門檻/隱私合規 |

---

## 5. Epic E3 — 排課 Booking

| ID | 項目 | 階段 | 依賴 | 來源/備註 |
|----|------|:--:|------|----------|
| E3.1 | Booking 模型：時間/教練/類型(1對1/團課)/狀態，**綁定 Contract 消課** | MVP | E0.2, E2.3 | 架構 §5；cal 沒有消課層→自建 |
| E3.2 | **CoachAvailability 可用時段 / 工作時間** | MVP | E3.1 | ★缺口：無此無法自助預約/算衝堂（journeys J1 已提「可預約時段規則」） |
| E3.3 | 衝堂偵測（場地/時段/教練） | MVP | E3.2 | journeys §8 |
| E3.4 | 簽到：LINE LIFF `scanCodeV2` QR → 扣堂 | MVP | E5.2 | journeys 教練 J2 |
| E3.5 | **No-show 狀態 + 消課規則**（爽約扣不扣堂） | MVP | E3.1 | journeys §8 已納入 |
| E3.6 | 取消政策 / 截止時間（太晚取消是否扣堂） | MVP | E3.1 | journeys §8 已納入 |
| E3.7 | 循環排課的 single / series 編輯語意（「改這堂 vs 改整列」） | MVP | E3.1 | ★缺口：經典難題，需明確設計 |
| E3.8 | 緩衝時間 buffer（連堂間隔） | 1.5 | E3.2 | ★缺口（參考 cal.diy） |
| E3.9 | 團課候補 waitlist + 遞補通知 | 1.5 | E3.1, E0.6 | ★缺口 |
| E3.10 | 外部行事曆雙向同步（Google/Apple/Outlook） | 1.5 | E3.1 | ★缺口：抄 cal.diy 設計，不抄碼 |

---

## 6. Epic E4 — Agent（核心差異化 / 護城河）

| ID | 項目 | 階段 | 依賴 | 來源/備註 |
|----|------|:--:|------|----------|
| E4.1 | **Agent 技術 spike**：AI SDK + 3~5 個 tool（排課/查堂數/記錄完課），跑通「繁中 NL → 確認 → 寫入 → 留痕」 | MVP | E0.2, E0.5 | oss §7；**最早期驗 §11 主要風險** |
| E4.2 | tool() ↔ Action 層對映：每個 Action 註冊成一個 tool，共用同一 Zod schema | MVP | E4.1 | oss §2.2 |
| E4.3 | **兩段式寫入確認**：LLM 產生意圖物件 → 回顯確認 → 後端執行 Action + 落 log | MVP | E4.2, E0.5 | oss §2.2；設計原則 #3 |
| E4.4 | 教練端寫入意圖全集（排課/改課表/記錄/通知/改取消/新增學員/指派課表） | MVP | E4.2 | 架構 §6.1 |
| E4.5 | 教練端查詢意圖（查堂數/進度/行程） | MVP | E4.2 | 架構 §6.2 |
| E4.6 | 歧義澄清（多個「小明」→ 反問） | MVP | E4.2 | journeys §8 |
| E4.7 | 多步驟 agent loop（`stopWhen`）做跨模組複合指令 | 1.5 | E4.4 | 架構 §6.3（部分 MVP） |
| E4.8 | 學員端 Agent over LINE（查詢/預約等 reply 情境） | 1.5 | E4.2, E5.1 | 架構 §9.7 |
| E4.9 | 經營副駕主動預警（流失/續約主動推播） | 2 | E4.7, E0.6 | 架構 §6.3 |
| E4.10 | 自動化工作流引擎（評估 Mastra） | 2 | E4.7 | oss §2.2 |
| E4.11 | **語音輸入 (STT)**：Agent 輸入框語音→文字（教練端＋學員端 LIFF）；行動端優先原生 STT / Web Speech API，繁中辨識品質要顧 | MVP | E4.1 | ★定位變更新增；架構原則 #7 |
| E4.12 | **省 token 路由**：明確/簡單/單一模組請求走規則或導去 Dashboard，不每次呼叫 LLM | MVP | E4.2 | ★定位變更新增；架構原則 #4 |

---

## 7. Epic E5 — LINE 交付

| ID | 項目 | 階段 | 依賴 | 來源/備註 |
|----|------|:--:|------|----------|
| E5.1 | LINE OA + Messaging API webhook 接進後端/Agent | MVP | E0.1 | oss §2.3；Apache-2.0 |
| E5.2 | **LIFF 學員端**：今日課表/記錄/成長，`getProfile` 自動身分 | MVP | E0.3 | journeys §5 |
| E5.3 | account link：LINE userId ⇄ Yolian Member 綁定 | MVP | E5.2, E0.3 | journeys §2 |
| E5.4 | Rich Menu（今日課表/我的進度/預約/聯絡教練） | MVP | E5.1 | journeys §2 |
| E5.5 | **reply(免費) / push(計費) 分流**：Agent 對話走 reply、提醒才 push | MVP | E5.1 | oss §2.3 省錢紀律 |
| E5.6 | 上課提醒 push + 一鍵確認/改期（**最高 CP 值鏈**） | MVP | E5.5, E0.6 | journeys 學員 J2 |
| E5.7 | 週摘要 push（規則版） | MVP | E0.6, E1.8 | journeys 學員 J5 |
| E5.8 | `shareTargetPicker` 轉介獲客 | MVP | E5.2 | journeys J6 |
| E5.9 | LINE Pay 金流選項 | 1.5 | E8.1 | ★缺口：journeys 未提；競品標配 |
| E5.10 | 分眾/標籤行銷推播 | 2 | E0.6 | ★缺口 |

---

## 8. Epic E6 / E7 — 品牌頁與儀表板（補完 MVP）

| ID | 項目 | 階段 | 依賴 | 來源/備註 |
|----|------|:--:|------|----------|
| E6.1 | 教練個人品牌頁：選版型自動生成（經歷/方案/成果/預約） | MVP | E0.1 | 架構 §7.1 |
| E6.2 | 品牌頁表單 → CRM 線索 | MVP | E2.1, E6.1 | journeys 教練 J5 |
| E7.1 | 經營儀表板：本週堂數/學員數/到期數（主理人全店 / 教練自己） | MVP | E2,E3 | journeys 主理人 J2 |
| E7.2 | 流失預警清單（規則版）+ 一鍵請教練關心 | MVP | E2.4 | journeys 主理人 J2 |

---

## 9. Phase 1.5 / Phase 2 集中清單（商業化與 AI 深化）

**Phase 1.5（商業化閉環）**
| ID | 項目 | 備註 |
|----|------|------|
| E8.1 | 台灣金流 + 電子發票（自接綠界/藍新官方 SDK） | ★開源缺口：台灣金流幾無成熟開源 |
| E8.2 | 業績薪資抽成自動計算 | 架構 §7.2；MVP 先給數據人工計薪 |
| E8.3 | 營收報表 + Agent 查營收 | 架構 §6.2 |
| — | 另含：E1.9 影片、E2.7 體測、E2.8 匯出、E3.8 buffer、E3.9 waitlist、E3.10 行事曆同步、E4.7/E4.8 | 散見各 Epic |

**Phase 2（AI 深化）**
| ID | 項目 | 備註 |
|----|------|------|
| E9.1 | **飲食：條碼記餐（Open Food Facts）先於拍照辨識** | oss §2.6/§4.3；更便宜準確。資料 ODbL 須標示 |
| E9.2 | 飲食拍照辨識 + AI 營養 + 每日目標達成 | 架構 §6.4 |
| E9.3 | AI 成長敘事（季度回顧把數據講成故事） | 架構 §6.5 留存王牌 |
| — | 另含：E1.10 自動漸進、E4.9 主動副駕、E4.10 工作流 | 散見各 Epic |

---

## 10. 授權守門（動工前再確認一次）
- ✅ 可直接進產品：free-exercise-db(Unlicense)、AI SDK / line-bot-sdk(Apache-2.0)、Next.js/Prisma/Auth.js/Recharts/BullMQ(MIT 系)。
- ◐ 須標示+相同分享：Open Food Facts 資料（ODbL/DbCL/CC-BY-SA）。
- ❌ 只看不抄碼：**wger(AGPL)**、**cal.com 本體(Open Core/AGPL)** → 排課要參考改造請用 **cal.diy(MIT)**。

> 詳見 `oss-stack-and-gaps.md` §6 授權紅線總表。
