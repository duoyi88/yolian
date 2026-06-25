# Noki 開源資源採用方案與功能缺口評估 v1

> 專案：Noki — 面向健身教練與個人工作室的營運平台
> 本文承接 `product-architecture.md`，把第一輪掃到的開源資源**逐一深挖成可執行的採用方案**（拿什麼／不拿什麼／怎麼接／授權紅線／風險），並反向用這些成熟專案**檢查藍圖漏掉了哪些功能**。
> 日期：2026-06-25 · 狀態：v1 · 視角：商用閉源 SaaS（授權合規優先於 star 數）

---

## 0. 這份文件回答兩個問題

1. **怎麼用？** — 每個開源資源的「採用層級（直接內嵌 / 改造 / 僅參考）+ 整合方式 + 授權限制 + 落地風險」。
2. **漏了什麼？** — 這些成熟產品已經踩過的坑，反推出 Noki 藍圖（§5 資料模型、§6 Agent、§7 MVP）目前**沒關注到的功能**。

---

## 1. 採用策略總綱（buy / borrow / build 的紀律）

一句話結論先講：**Noki 的差異化（跨模組 Agent + LINE 原生交付 + 成長敘事）在任何開源專案裡都不存在，所以開源只負責「商品化的底層」，護城河必須自建。**

| 層級 | 定義 | 適用授權 | 本文資源 |
|------|------|---------|---------|
| **直接採用（buy）** | 套件/資料直接進產品 | MIT / Apache-2.0 / Unlicense | free-exercise-db、AI SDK、line-bot-sdk、Open Food Facts 資料 |
| **改造參考（borrow）** | 抄架構/資料模型，自行實作 | 任意（含 AGPL，只看不抄碼） | wger 資料模型、cal.com 排程設計 |
| **自建（build）** | 沒有堪用開源、且是差異化 | — | 共用 Action 層、經營副駕、成長敘事、消課鏈 |

> **AGPL 鐵律**：AGPL-3.0 的程式碼**連 SaaS（不分發、只提供網路服務）都會觸發開源義務**。wger、cal.com 本體屬此類 → **只准讀設計、不准複製程式碼進 Noki**。資料（CC/開放資料授權）另計，可用但要遵守姓名標示/相同方式分享。

---

## 2. 逐資源深度採用方案

### 2.1 動作庫 — `yuhonas/free-exercise-db` ✅ 直接採用

- **授權**：Unlicense（公共領域）→ 商用零限制，可重新打包、可閉源、無需標示。**最乾淨的一個。**
- **內容**：800+ 動作，每筆獨立 JSON，欄位：`id / name / force(推拉) / level(難度) / mechanic(複合或孤立) / equipment(器材) / primaryMuscles / secondaryMuscles / instructions[] / category / images[]`。圖片可走 GitHub raw 或自架 CDN。
- **對應 Noki**：直接灌進 §5 的 **Exercise 動作庫**實體。欄位幾乎一對一，`primaryMuscles/equipment/level` 可直接當篩選維度。
- **採用方式**：
  1. 抓 `dist/exercises.json`（合併檔）+ 整包圖片 → 存進 Noki 自己的 DB 與物件儲存（**不要 runtime 依賴對方 GitHub**）。
  2. 建一張對照表，把英文 `name/instructions` 補上**繁中翻譯**（見下方風險）。
  3. 器材/部位的 enum 收斂成 Noki 自己的分類法（對方 enum 偶有 null）。
- **風險 / 缺口**：
  - ⚠️ **純英文**：動作名、步驟全英文。台灣教練/學員要繁中 → 需一次性翻譯（800 筆，可用 LLM 批次初翻 + 教練校對）。**這是隱性成本，要排進 MVP 工。**
  - 圖片是真人示範照（非統一風格），品牌一致性普通；MVP 可接受，Phase 2 再考慮統一重製或換繪。
  - 沒有影片（只有靜態圖）。Noki §5 Exercise 寫的是「影片/圖示」→ 影片要嘛自建、要嘛之後接 YouTube 連結。

### 2.2 AI Agent / 工具呼叫層 — Vercel AI SDK（`/vercel/ai`）★ 直接採用，這是漏研究的最關鍵一塊

> §6.6 的「意圖解析 → tool calling → 確認 → 留痕」整套機制，過去藍圖只有概念、沒有技術載體。**AI SDK 幾乎是為 Noki 設計原則 #1 量身打造的。**

- **授權**：Apache-2.0 ✅ 商用可用。TypeScript、provider 無關（可同時掛 OpenAI / Anthropic / Gemini / 阿里 Qwen，繁中可挑最強模型甚至 A/B）。
- **核心 API 與 Noki 的對應**：

| AI SDK 機制 | 做什麼 | 對應 Noki |
|------------|--------|----------|
| `tool({ description, inputSchema: z.object({...}), execute })` | 定義一個帶型別參數的工具 | **= 共用 Action 層的一個 Action**（設計原則 #1）。Booking/Program/Contract 每個 Action 就是一個 tool |
| `generateText({ model, tools, prompt })` | LLM 讀自然語言 → 自動選 tool、填參數、呼叫 | §6.6 意圖解析 + tool calling 一步到位 |
| `stopWhen: isStepCount(n)` | 多步驟 agent 迴圈（呼叫→看結果→再呼叫） | §6.3 跨模組複合指令（「剩 2 堂又沒進步 → 約續約 + 整理數據」要連續多動作）|
| `Output.object({ schema })` | 強制結構化輸出（Zod 驗證） | 歧義澄清、回顯確認卡的結構化欄位 |
| `execute` 不自動跑、改回傳「待確認」 | 人類確認後才真正寫入 | **設計原則 #3「寫入必經確認 + 留痕」** |

- **「寫入確認」怎麼落地**（重要架構細節）：
  - 把「寫」類 tool 的 `execute` 拆成兩段：LLM 先產生 **結構化意圖物件**（要做什麼、參數），UI/LINE 回顯「我要把小明本週三五 07:00 各排一堂，確認？」→ **使用者按確認後，後端才呼叫真正的 Action 並寫 AgentActionLog**。
  - 即 AI SDK 負責「解析+選工具+填參數」，真正的副作用由 Noki 的 Action 層在確認後執行 → 天然滿足「可撤銷、可留痕」。
- **一份 Zod schema 餵兩個前端**：同一個 `inputSchema`（Zod）既是 LLM 的 tool 參數定義，也能驅動程式化前端的表單驗證 → **真正做到「按鈕和對話呼叫同一套 Action」**。
- **注意版本**：AI SDK v6 起 `generateObject` 標記為 deprecated，結構化輸出改用 `generateText({ output: Output.object(...) })`。新做就直接走 v6 寫法。
- **替代/補充**：LangChain.js（MIT，生態大但偏重）、Mastra（MIT，agent 框架含 workflow/memory）。**建議主線用 AI SDK（輕、型別好、provider 無關），Phase 2 若要複雜自動化工作流再評估 Mastra。**

### 2.3 LINE — `line/line-bot-sdk-nodejs` + LIFF SDK ✅ 直接採用

- **授權**：Apache-2.0 ✅。需 Node.js 22+。
- **對應 §9 三積木**：
  - **Messaging API SDK**：webhook 收訊 → 進 Agent；`replyMessage`（免費）/ `pushMessage`（計費）；Flex Message 做課表卡/成長卡；Rich Menu 永久入口。
  - **LIFF SDK**（前端另裝 `@line/liff`）：學員端零安裝載體。`liff.getProfile()` 拿 userId、`liff.getIDToken()` 傳後端綁定 Member、`liff.scanCodeV2()` 做 QR 簽到消課、`liff.shareTargetPicker()` 做轉介。
- **採用架構**（省錢關鍵）：

```
教練/學員 LINE 訊息 ─webhook→ Noki 後端 ─→ AI SDK(意圖解析) ─→ 共用 Action 層
                                            └─reply(免費) 回覆
排程提醒/合約到期/成長敘事 ─→ push(計費，只在高價值時用)
Rich Menu ─→ 開 LIFF = Noki 學員端(面 3)
```

- **關鍵紀律**：**Agent 對話一律走 reply（免費），push 只留給「降爽約提醒、合約到期、成長摘要」這種高價值主動推播**（§9.6 計費模型）。架構上把兩條路分開。
- **風險**：LIFF 必須 HTTPS、OpenChat 不支援、外部瀏覽器無法 `scanCode`；健身鄰近健康業種，LINE 內建 AI bot(β) 可能被拒 → 用自有 Agent 走 webhook 不受限，但內容合規仍要留意。

### 2.4 排課 — `calcom/cal.diy` ◐ 偏參考，謹慎改造

> **務實提醒**：cal.com/cal.diy 的本質是「**Calendly 式的個人時段預約**」（某人開放空檔讓別人約），**不是「健身工作室多教練排班 + 團課名額 + 消合約堂數」**。兩者資料模型差很多。

- **授權**：cal.diy = MIT ✅（社群版，已剔除企業功能）；**cal.com 本體 = Open Core 含 AGPL ⚠️**，要用務必用 cal.diy。
- **技術棧**：Next.js + tRPC + Prisma + Tailwind（與 Noki 若走 TS 全棧高度相容）。
- **正確用法**：
  - ✅ **借設計**：可用時段計算、衝突偵測、行事曆雙向同步（Google/Apple/Outlook）、reschedule/cancel 流程、提醒工作流——這些是 cal 的強項，直接抄**設計與資料結構**。
  - ◐ **改造**：若要直接用其程式碼，要嫁接「Contract 堂數扣除、團課名額、教練抽成」等 cal 沒有的概念，整合成本可能高於自建。
  - ❌ **別期待**：開箱即用的「工作室排課系統」。
- **建議**：**MVP 排課自建**（Booking 資料模型本來就要綁 Contract 消課，cal 沒這層），但**把 cal.diy 當「排程邏輯的活字典」**：可用時段、緩衝時間、衝突演算法、外部行事曆同步照它做。

### 2.5 健身領域資料模型黃金參考 — `wger-project/wger` ⚠️ 只參考不抄碼

- **授權**：程式碼 **AGPL-3.0 ⚠️**（閉源 SaaS 不能用程式碼）；**資料（動作/食材）是 CC 授權，可用**（遵守標示/相同方式分享）。
- **價值**：目前最完整的開源健身管理，**它的資料模型是校準 Noki §5 的最佳對照**。它有的而 Noki 藍圖目前較弱或沒有的概念（→ 見 §4 缺口分析）：
  - **Routine 自動重量漸進規則**（progression rules）
  - **自訂體測項目**（custom measurements，不只 InBody 那幾項）
  - **飲食/食材庫 + 接 Open Food Facts**
  - **REST API 設計**（第三方整合）
- **用法**：讀它的 models 與 API 文件（readthedocs），把它驗證過的欄位與關係納入 Noki 自己的（自寫）schema。**一行程式碼都不要複製。**

### 2.6 飲食 / 營養 — Open Food Facts ◐ Phase 2 採用（資料 + API）

- **授權**：資料庫 ODbL、內容 DbCL、圖片 CC-BY-SA ⚠️ → **可商用但有「姓名標示 + 相同方式分享」義務**，要在產品內標示來源。
- **能力**：條碼 → 產品營養（Nutri-Score、NOVA、過敏原、四大營養素）；支援上傳照片由其 AI(Robotoff) 反算。
- **務實限制**：
  - 線上 API 有 **rate limit**（讀 15 req/min/IP、搜尋 10 req/min/IP），**不可拿來做 search-as-you-type**；量大要**下載 CSV/JSONL 自建本地庫**或自架 Product Opener。
  - 寫操作要自訂 User-Agent + 帳號。
- **對應 Noki**：§6.4 拍照記餐 / NutritionLog（Phase 2）。
- **重點機會（見 §4.3）**：**條碼掃描比「整盤拍照辨識」便宜且準**。Open Food Facts 天生是條碼庫 → Noki Phase 2 應**先做條碼記餐，再做拍照辨識**，成本/準確率都更友善。

---

## 3. 還沒納入的開源層（補齊技術棧）

第一輪只看了「健身/排課/LINE」，但要把 §8 技術架構落地，還缺這些層。以下都是商用友善授權：

| 層 | 對應 Noki | 建議開源 | 授權 | 備註 |
|----|----------|---------|------|------|
| **圖表（成長折線/儀表板）** | §6.5 成長可視化、§7.1 經營儀表板 | Recharts / Chart.js / visx / Tremor | MIT（Tremor Apache-2.0） | 成長折線王牌功能的視覺載體，過去沒指定 |
| **學員 intake / 健康問卷** | 新增學員、合規 | 自建（用 Zod schema）或 react-hook-form | MIT | **見 §4.5：PAR-Q 健康篩查是缺口** |
| **通知/提醒排程引擎** | §6.3 續約提醒、§9.5 上課提醒 | BullMQ（Redis 佇列）/ node-cron | MIT | 「規則版提醒」背後需要一個排程器，藍圖沒提 |
| **權限 / 多租戶 RBAC** | Studio→Coach→Member 權限 | CASL / 自建 | MIT | §5 有「角色權限」欄位但沒設計授權模型 |
| **PWA / 前端框架** | §8.2 PWA 起步 | Next.js（+ next-pwa） | MIT | 與 AI SDK、cal.diy 同生態 |
| **身分驗證** | 教練/學員登入、LINE 綁定 | Auth.js (NextAuth) | ISC/MIT | 支援 LINE Login provider |
| **台灣金流 / 電子發票** | §8.4、Phase 1.5 | 綠界/藍新多為 SDK 非開源 | — | **開源缺口：台灣金流幾乎無成熟開源，要自接官方 SDK** |

> 結論：**AI SDK + Next.js + Auth.js + line-bot-sdk + Recharts + BullMQ + Prisma** 可組成一條全 TS、授權乾淨、彼此同生態的主線技術棧。

---

## 4. 功能缺口評估 ★（OSS 揭露藍圖漏掉的東西）

> 方法：拿成熟產品「已經內建」的功能，逐項問「Noki §5/§6/§7 有沒有？」。下面只列**目前藍圖沒有或明顯偏弱**的。

### 4.1 排課域（對照 cal.com 的成熟度）

| 缺口 | 說明 | 為何重要 | 建議 |
|------|------|---------|------|
| **教練可用時段 / 工作時間** | §5 Booking 沒有「Coach 的 availability」實體 | 沒有它就無法做學員自助預約、也算不準衝堂 | **補進 MVP 資料模型**（CoachAvailability） |
| **No-show（爽約）處理** | 有「簽到」但沒有「未到」狀態 | 直接牽動消課：爽約到底扣不扣堂數？是營收/合約爭議點 | Booking 狀態機補 `no_show`，並定義消課規則 |
| **緩衝時間 buffer** | 課與課之間的整理/移動時間 | 教練連堂需要間隔，影響可約時段計算 | 排課邏輯補 buffer |
| **團課候補 waitlist** | §6 有團課但無滿員候補 | 團課滿了要候補+遞補通知，是高頻場景 | Phase 1.5 補 |
| **循環排課的編輯語意** | 「每週三五」是循環序列 | 「改這一堂 vs 改整個系列」是經典難題，藍圖沒定義 | 明確設計 single/series 編輯 |
| **外部行事曆雙向同步** | §5 Booking 未提 Google/Apple Calendar | 教練本來就活在自己行事曆，不同步會雙開 | Phase 1.5（cal.diy 有現成設計可抄） |
| **取消政策 / 截止時間** | Agent 可改可取消，但無「開課前 X 小時不可取消」 | 保護教練時段、減少臨時取消 | 規則設定 |

### 4.2 訓練域（對照 wger）

| 缺口 | 說明 | 建議 |
|------|------|------|
| **自動重量漸進規則** | §5 Program 有「建議重量」但無「達標自動加重」規則 | 進階賣點，Phase 2；MVP 先手動 |
| **RIR / RPE（自覺強度）** | WorkoutLog 只記重量/次數，沒有強度感受 | 低成本高價值，建議 MVP WorkoutLog 補一欄 |
| **組類型（superset/dropset/熱身組）** | Program 結構偏平，沒有組間關係 | 影響課表表達力；MVP 至少分「正式組/熱身組」 |
| **自訂體測項目** | §5 BodyComposition 寫死體重/體脂/骨骼肌/InBody | 教練常量腰圍/臂圍等自訂項 | 加一個彈性 Measurement 實體 |

### 4.3 飲食域

| 缺口 | 說明 | 建議 |
|------|------|------|
| **條碼記餐先於拍照辨識** | §6.4 只規劃「拍照辨識」（貴、難） | Open Food Facts 本質是條碼庫 → **Phase 2 先做條碼掃描記餐**，更便宜準確，拍照辨識當後續 |
| **營養目標 / 每日達成** | 有 NutritionLog 但無「目標熱量/巨量 + 每日達成率」 | 飲食功能的留存鉤子 |

### 4.4 LINE / 在地

| 缺口 | 說明 | 建議 |
|------|------|------|
| **LINE Pay 金流** | §9 強在交付/通知，但沒提金流 | 競品 BookFast 用 LINE Pay；Phase 1.5 台灣金流應含 LINE Pay 選項 |
| **分眾推播 / 標籤行銷** | push 只想到提醒 | 學員分眾（快到期/久未來）行銷，Phase 2 |

### 4.5 跨切面 / 平台

| 缺口 | 說明 | 為何重要 | 建議 |
|------|------|---------|------|
| **PAR-Q 健康篩查問卷** | 新增學員時無健康/傷病/禁忌篩查 | **健身有受傷與法律責任風險**，入會健康聲明是業界常規 | **建議納入 MVP 的新增學員流程** |
| **通知排程引擎** | 「規則版提醒」沒有對應的技術元件 | 沒有佇列/排程器，定時提醒做不出來 | 技術架構補 BullMQ/cron |
| **動作庫繁中化成本** | free-exercise-db 純英文 | 影響教練/學員體驗 | 列為 MVP 顯性工作項 |
| **資料匯出 / 退出** | 無會員資料可攜/匯出 | 教練換系統的信任門檻、隱私合規 | Phase 1.5 |
| **稽核/權限模型** | §5 有 AgentActionLog（好），但 RBAC 未設計 | 多教練工作室需要清楚的資料隔離 | MVP 設計基本 RBAC |

---

## 5. 對 `product-architecture.md` 的具體修訂建議

1. **§5 資料模型新增實體**：`CoachAvailability`（可用時段）、`Measurement`（彈性體測）；`Booking` 狀態補 `no_show` 並定義消課規則；`Member` 加 `HealthScreening`（PAR-Q）。
2. **§6.6 Agent 機制補技術載體**：明寫「以 Vercel AI SDK 的 `tool()` 實作共用 Action 層，Zod schema 同時驅動 LLM 與 UI 表單；寫入類 tool 採『產生意圖→確認→執行→AgentActionLog』兩段式」。
3. **§7.1 MVP IN 補三項**：動作庫繁中化、學員健康篩查問卷、RIR/RPE 記錄欄位。
4. **§8 技術架構**：補「通知排程引擎（佇列）」「外部行事曆同步」「身分驗證(Auth.js + LINE Login)」三個元件，並定出主線技術棧。
5. **§9 LINE**：在金流段補 LINE Pay；§6.4 飲食改為「條碼記餐先行，拍照辨識後續」。

---

## 6. 授權紅線總表（商用閉源視角）

| 資源 | 授權 | 能直接進產品？ | 用法 |
|------|------|:---:|------|
| free-exercise-db | Unlicense | ✅ 無限制 | 動作庫資料直接內嵌（需繁中化） |
| Vercel AI SDK | Apache-2.0 | ✅ | Agent/工具呼叫主線 |
| line-bot-sdk-nodejs + LIFF | Apache-2.0 | ✅ | LINE 整合主線 |
| cal.diy | MIT | ✅（謹慎改造） | 排程邏輯參考/改造 |
| Recharts/Chart.js/Next.js/Auth.js/BullMQ | MIT 系 | ✅ | 技術棧底層 |
| Open Food Facts 資料 | ODbL/DbCL/CC-BY-SA | ◐ 須標示+相同分享 | 飲食庫（Phase 2） |
| **wger 程式碼** | **AGPL-3.0** | ❌ 只看不抄 | 資料模型/API 設計參考 |
| **cal.com 本體** | Open Core/AGPL | ❌ | 改用 cal.diy |

---

## 7. 建議的下一步

1. **校準資料模型**：依 §5 修訂建議更新 `product-architecture.md` 的實體表。
2. **做一個 Agent 技術驗證（spike）**：用 AI SDK + 3~5 個 tool（排課/查堂數/記錄完課）跑通「繁中自然語言 → 確認 → 寫入 → 留痕」，**早期實測繁中意圖解析準確率**（這是 §11 列的主要風險）。
3. **動作庫前處理**：抓 free-exercise-db、設計繁中對照、收斂器材/部位分類法。
4. **排程器與 LINE 串接**：BullMQ + line-bot-sdk 先把「上課提醒 push」這條最高 CP 值的鏈打通。
