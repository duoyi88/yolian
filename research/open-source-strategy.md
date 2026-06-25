# 開源整併 → 商業服務 策略與授權合規研究

> 專案：Yolian — 面向健身教練與個人工作室的營運平台
> 本文回答一個問題：**Yolian 要如何「整併開源資源」做成可長期收費的商業 SaaS，而不在授權、護城河、可維護性上踩雷。**
> 收斂自 `competitor-research.md`、`deep-dive-competitors.md`、`product-architecture.md`。授權狀態以 2024–2026 一手來源查證（文中標注）。
> 日期：2026-06-25 · 狀態：v1 · 用途：建置前的選型與合規依據
>
> **與 `oss-stack-and-gaps.md` 的分工**：那份文件回答「**具體拿哪些開源、怎麼接、藍圖漏了什麼功能**」（free-exercise-db、Vercel AI SDK、line-bot-sdk、cal.diy、wger、Open Food Facts + 功能缺口）；本文回答上一層的「**整併開源變成可收費服務的策略、授權光譜、變天風險、合規工程與 AGPL 邊界**」。兩份建議對照閱讀。

---

## 0. 一句話心法

> **用寬鬆授權的開源把所有 commodity（DB、Auth、行事曆、圖表、LLM、LINE SDK、佇列、儲存）組起來，把唯一的工程火力集中在不可外包的護城河——共用 Action 層 + 跨模組 Agent + 經營副駕 + 成長敘事——再用「託管 + 繁中 + 台灣金流/發票/LINE 合規 + 支援 + SLA」包成付費服務。開源是你的「不用自己造」，不是你的「賣點」。**

對 Yolian 的意義：產品的差異化（見 `product-architecture.md` §0、§6.3）完全是自研層；底層全部站在巨人肩上。整併開源不是省成本的小事，而是**讓小團隊能在 MVP 期就擁有大廠級基礎設施**的關鍵槓桿。

---

## 1. 「開源 → 商業服務」的四種整併模式

| 模式 | 做法 | 代表 | Yolian 適用度 |
|------|------|------|:--:|
| **A. Host（託管原樣）** | 把一套開源軟體原封不動架起來收託管費 | AWS RDS、各家 Managed Redis | ✕ 非 Yolian 本業 |
| **B. Wrap & Integrate（包裹整併）** | 把多個開源元件當「零件」，縫進自有產品，客戶看不到底層 | Vercel、Supabase、絕大多數 SaaS | ★★★ **Yolian 就是這型** |
| **C. Open-Core（開放核心）** | 自家產品開源社群版，進階功能閉源收費 | GitLab、Cal.com、n8n | △ 早期不必，Phase 3 可考慮把 Action SDK 開源做生態 |
| **D. Build-on-Platform（平台之上）** | 在別人的開源/開放平台上做加值 | LINE LIFF 上的應用 | ★★ 學員端就是長在 LINE 上 |

> **對 Yolian 的啟示**：主體是 **B（Wrap & Integrate）**。客戶買的是「用講的就完成營運」，不是「我們用了 PostgreSQL」。這決定了授權策略——**只要底層元件不要求你開源自己的商業碼即可**（見 §2）。

---

## 2. 授權光譜（決定能不能商用的根本）

從「最自由」到「最危險」排列，重點是**對閉源 SaaS 的義務**：

| 類別 | 代表授權 | 對 Yolian（閉源 SaaS）的義務 | 判斷 |
|------|---------|--------------------------|:--:|
| **公眾領域** | CC0、Unlicense、0BSD | 無 | ✅ |
| **寬鬆 Permissive** | **MIT、ISC、BSD-2/3、Apache-2.0** | 僅需保留版權聲明；Apache-2.0 另含**專利授權**＋改檔需在 NOTICE 標注 | ✅ **後端預設只收這類** |
| **弱 Copyleft（檔案/連結級）** | **MPL-2.0、LGPL、EPL** | 只有「你直接改動的那些開源檔案」要開源；當函式庫呼叫、不改原碼，閉源產品不受影響 | ✅ 可用，勿改其原始檔 |
| **強 Copyleft** | **GPL-2.0 / GPL-3.0** | 連結進你的程式 → 整個衍生作品須以 GPL 釋出。**但**：作為獨立進程的工具（CLI/服務）由你呼叫，通常不傳染 | ⚠️ 僅限「獨立進程」用法 |
| **網路 Copyleft（SaaS 殺手）** | **AGPL-3.0** | 只要使用者「透過網路」用到，你就須對外提供（含你改動的）對應原始碼 | ⚠️ 見 §8，**能不碰主程式就不碰** |
| **源碼可見 ≠ 開源** | **SSPL、BUSL/BSL、Elastic License v2、Functional Source License（FSL）、n8n Sustainable Use、Commons Clause** | 常**明文禁止**「拿來當服務賣 / 與原廠競爭」，或要你連帶開源整個服務堆疊 | 🚫 商業核心**絕不**壓在上面 |

兩個最常被搞錯的點：
1. **「源碼放在 GitHub 上」不等於「開源授權」。** SSPL / BUSL / ELv2 / FSL 都看得到碼，但**不是 OSI 認證的開源授權**，且專為堵 SaaS 而生。
2. **Apache-2.0 > MIT 之處在「專利」。** Apache-2.0 內含明確專利授權與「專利報復」條款；對商業產品法務更安全，故元件同質時優先選 Apache-2.0。

> **對 Yolian 的啟示**：建立一條 CI 紅線——**新依賴若不是 §2 前三類（Permissive / 弱 Copyleft / 公眾領域），預設擋下，需人工審核**。AGPL 與所有 source-available 進「審核清單」。

---

## 3. 授權「變天」事件簿（2018–2026，皆一手查證）★ 這節是血淚教訓

開源商業公司近年密集「換約掐脖」以防雲端大廠白嫖。**踩到正在變動的專案 = 你的技術選型可能一夕違法或被迫遷移。**

| 年 | 專案 | 變動 | 社群 fork（救援） | 查證 |
|----|------|------|------------------|------|
| 2018 | MongoDB | AGPL → **SSPL** | — | — |
| 2018 | Redis 模組 | 加 **Commons Clause** | — | The Register |
| 2021 | Elasticsearch/Kibana | Apache-2.0 → **SSPL / ELv2** | **OpenSearch**（AWS，Apache-2.0） | — |
| 2021 | Grafana | Apache-2.0 → **AGPL-3.0** | — | — |
| 2023 | HashiCorp（Terraform/Vault…） | MPL-2.0 → **BUSL 1.1** | **OpenTofu**（Linux Foundation，MPL-2.0） | — |
| 2024.03 | Redis | BSD → **SSPL / RSALv2** | **Valkey**（Linux Foundation，**保留 BSD**，由 Redis 原作者參與） | Wikipedia/Valkey、LF |
| 2024.08 | Elasticsearch | **加回 AGPL**（重新成為開源） | （OpenSearch 已自立） | elastic.co 官方部落格 |
| 2025.05 | Redis | **Redis 8 加回 AGPLv3**（原作者 antirez 回鍋推動） | （Valkey 已自立） | redis.io 官方部落格 |

**兩個趨勢，直接影響選型：**
1. **2023 是「rug pull」高峰，2024–2025 出現回頭**：Redis、Elastic 因為 fork（Valkey/OpenSearch）真的成功了、社群出走痛，於是**加回 OSI 開源授權（都是 AGPL）**。但注意——加回的是 **AGPL**，仍是 SaaS 敏感授權（§8）。
2. **有基金會托管的 fork 是最穩的避風港**：Valkey、OpenTofu、OpenSearch 都進了 Linux Foundation / 多廠商治理，**不會被單一公司一夕改約**。

> **對 Yolian 的啟示（選型鐵則）**：同功能優先選**治理分散**者（Apache 基金會 / CNCF / Linux Foundation / 多廠商社群）勝過「單一公司主導」者。單一公司 + 創投背景 + 雲端競爭壓力 = 未來改約高風險。

---

## 4. Yolian「買 / 借 / 造」決策矩陣（逐模組）

對照 `product-architecture.md` §5 資料模型與 §4 三面。原則：**commodity 借開源、護城河自造、敏感合規買服務**。

| Yolian 模組 | 借（開源 commodity） | 典型授權 | 自造（護城河，不外包） |
|----------|---------------------|---------|----------------------|
| 前端框架 | Next.js / React / Vue / Svelte | MIT | 程式化前端的領域 UX |
| UI 元件 | Tailwind、shadcn/ui、Radix、MUI | MIT | Yolian 設計語言 |
| 排課行事曆 | FullCalendar、Schedule-X | MIT* | **衝堂偵測、消課狀態機**（§5.2） |
| 圖表 / 成長折線 | Recharts、Apache ECharts、visx | MIT / Apache-2.0 | **AI 成長敘事生成**（§6.5） |
| 身分 / 權限 | Auth.js、Keycloak、Ory、Supabase Auth | ISC / Apache-2.0 | **Coach/Studio/Member 權限規則** |
| 資料庫 | **PostgreSQL** | PostgreSQL（寬鬆） | 核心資料模型 |
| ORM | Prisma、Drizzle | Apache-2.0 | — |
| 快取 / 佇列 | **Valkey**（非 Redis 新版）、BullMQ | BSD / MIT | 提醒規則引擎排程 |
| 向量 / RAG | **pgvector**（長在 PG 裡） | PostgreSQL | 教練筆記脈絡組裝 |
| LLM 編排 | Vercel AI SDK、LangChain | Apache-2.0 / MIT | **意圖→Action 對應、寫入確認、audit** |
| LLM 模型 | **API（Claude/OpenAI/Gemini）** | 商業 API | 繁中 prompt / 工具定義 |
| 語音輸入 STT | Web Speech API / Whisper API / faster-whisper | 原生 / Apache-2.0 / MIT | 繁中語音辨識調校、輸入框語音鈕 |
| LINE | `@line/bot-sdk`、LIFF SDK | Apache-2.0 / 免費 SDK | webhook→Action 路由、帳號綁定 |
| 物件儲存（體態照） | **S3 / Cloudflare R2**；自架選 SeaweedFS | 商業 / Apache-2.0 | — |
| 站內搜尋 | **Meilisearch**（MIT）；勿用 Typesense(GPL-3) | MIT | — |
| 觀測 | Prometheus、OpenTelemetry、Grafana | Apache-2.0 / AGPL** | — |
| 金流 / 發票（TW） | 綠界 / 藍新 SDK（非開源議題，直接接） | 商業 | 對帳邏輯 |

\* FullCalendar **標準套件 MIT**，但「Scheduler / 資源時間軸」等進階外掛是**商業授權**——用到要付費，別誤用。
\** Grafana 是 AGPL，但**獨立進程**部署（你不改它、不連結進產品）即可安全使用（§8）。

> **對 Yolian 的啟示**：上表幾乎全是 Permissive。唯三需留意：**Valkey 取代 Redis**、**儲存用 S3/R2 不自架 MinIO**、**搜尋用 Meilisearch 不用 Typesense**。把這三條寫進工程規範即可避開九成地雷。

---

## 5. 建議技術堆疊（全部寬鬆 / 安全，可直接照建）

對齊 `product-architecture.md` §8（API-first + 共用 Action 層、PWA 起步、繁中 LLM）：

```
前端：Next.js (MIT) + Tailwind + shadcn/ui        ← 教練 Web 後台 + 學員 PWA/LIFF
行事曆：FullCalendar 標準版 (MIT) / Schedule-X
圖表：Recharts (MIT) 或 Apache ECharts (Apache-2.0)
後端：Node/TS 或 Go ─ 全部操作 = 型別化 Command/Query（單一事實來源）
資料庫：PostgreSQL (寬鬆) + pgvector (RAG)          ← 一個 DB 同時做關聯 + 向量，省一個元件
ORM：Prisma / Drizzle (Apache-2.0)
快取/佇列：Valkey (BSD) + BullMQ (MIT)             ← 注意：不是 Redis ≥7.4
Auth：Auth.js (ISC)；多租戶複雜時 Keycloak/Ory (Apache-2.0)
AI：Vercel AI SDK (Apache-2.0) + LLM 商業 API（function calling 接 Action 層）
語音：Web Speech API（瀏覽器原生·免費）/ Whisper API｜faster-whisper(MIT) 自架   ← Agent 語音輸入(STT)，設計原則 #7
儲存：Cloudflare R2 / S3（體態照、InBody 圖）
LINE：@line/bot-sdk (Apache-2.0) + LIFF
觀測：OpenTelemetry + Prometheus (Apache-2.0)；Grafana 獨立進程
部署：Docker + Kubernetes (Apache-2.0)；IaC 用 OpenTofu (MPL-2.0) 而非 Terraform
```

設計上每個外部元件都包在自有介面後（這正是 **`product-architecture.md` 設計原則 #1「共用 Action 層」的延伸**）：
- LLM 後面可換 Claude ↔ OpenAI ↔ 本地模型
- 儲存後面可換 S3 ↔ R2
- 這層抽象**同時是 anti-vendor-lock-in 與 anti-授權變天的縫**——某元件改約，只換一個 adapter，不動上層。

> **對 Yolian 的啟示**：**pgvector 長在 PostgreSQL 裡**，MVP 不必另立向量資料庫（省 Pinecone/Milvus 一個元件與一筆錢）；**Valkey 一物多用**（快取 + 佇列 + pub/sub）。小團隊把元件數壓到最低，可維護性最高。

---

## 6. 授權地雷清單（Yolian 路線圖上「最想用、卻有坑」的）

這些是**會直接咬到 Yolian 規劃**的具體陷阱：

| 想用它做… | 專案 | 授權真相 | 正解 |
|----------|------|---------|------|
| 排課（§4 面1） | **Cal.com** | 根目錄 **MIT，但 Open-Core**：`/ee`、含 `.ee.` 的目錄是**商業授權**，Teams/Org/Workflows/SSO 等都在裡面 | 用 MIT 部分自建，或用 100% MIT 的社群 fork **Cal.diy**；避免依賴 `/ee` 功能 |
| Phase 3 工作流市集（§7.2） | **n8n** | **Sustainable Use License**：僅限自用/非商業；**不可當服務賣給別人** | 自研 Action 編排引擎，或選 Apache/MIT 的工作流庫；要用 n8n 先讀條款談授權 |
| 快取 / 佇列 | **Redis ≥ 7.4** | 2024 起 SSPL/RSALv2、2025 Redis 8 改 AGPL | **Valkey（BSD）** |
| 體態照 / 檔案自架 | **MinIO** | **AGPL-3.0**，且 2025 砍社群版 console 功能 | **S3 / R2**（託管）；要自架用 SeaweedFS (Apache-2.0) |
| 站內搜尋 | **Typesense** | **GPL-3.0** | **Meilisearch（MIT）** 或 OpenSearch (Apache-2.0) |
| 錯誤追蹤自架 | **Sentry** | **FSL / BSL**（source-available） | 用 Sentry SaaS，或 fork **GlitchTip**；自架自有服務要看條款 |
| 日誌 / 搜尋 | **Elasticsearch** | 有 AGPL 選項但仍敏感 | 多數情境 **OpenSearch (Apache-2.0)** 更省心 |
| IaC | **Terraform** | **BUSL 1.1** | **OpenTofu（MPL-2.0）** |

> **對 Yolian 的啟示**：藍圖裡最危險的兩個「很想用」是 **Cal.com（排課）** 與 **n8n（工作流市集）**——兩者都是 Open-Core / source-available，**正好卡在 Yolian 的核心模組與變現模組上**。結論：**排課與工作流引擎都該自研**（反正它們本來就要接 Yolian 的 Action 層、是護城河的一部分，自研而非嵌入第三方反而更對）。

---

## 7. 合規工程化（把「不踩雷」變成自動化流程）

授權合規不能靠人腦記，要變成 **CI 關卡**。從第一天就建：

1. **SBOM（軟體物料清單）**：每次 build 產生依賴清單（CycloneDX / SPDX 格式），知道「我到底用了什麼、什麼授權」。
2. **授權掃描器擋 PR**：`license-checker`（JS）、FOSSA、ScanCode、Trivy；命中 §2「審核清單」（AGPL / SSPL / BUSL / GPL / FSL…）就**紅燈擋下**，需人工放行。
3. **依賴更新自動化**：Dependabot / Renovate——**順便偵測「授權變更」**（升版時授權可能變，如 Redis 7.2→7.4）。
4. **漏洞掃描**：Trivy / Grype 掃 CVE。
5. **NOTICE / 第三方授權頁**：保留所有 MIT/BSD/Apache 版權聲明，產品內附「開源授權」清單頁（法務義務，也是誠信）。
6. **CLA / DCO**（若 Phase 3 開源 Action SDK 收外部貢獻時才需要）。

> **對 Yolian 的啟示**：MVP 階段就把「**授權掃描 + SBOM**」加進 CI——這是一次性低成本投入，卻能擋掉未來「上線後才發現某依賴是 AGPL / 某升版偷改授權」的災難。對閉源商業 SaaS 而言，這是不可省的保險。

---

## 8. AGPL 深入（因為它現在是最關鍵的灰區）

Redis、Elastic、Grafana、MinIO 都回到或落在 **AGPL-3.0**，所以 Yolian 必須懂它的精確邊界：

- **AGPL 觸發點**：你**修改**了 AGPL 軟體，且讓使用者**透過網路互動**到它 → 你必須把「你改動的版本原始碼」對那些使用者提供。
- **安全用法（不傳染給 Yolian 商業碼）**：
  - ✅ **不改原碼**，把它當**獨立進程 / 獨立服務**部署（例如 Grafana 儀表板、AGPL 版資料庫當後端），你的產品只透過網路/標準協定呼叫它。多數法律意見認為這**不使你的應用變成 AGPL 衍生作品**。
  - ✅ 用它的**客戶端 driver**（driver 通常是寬鬆授權，非 AGPL）。
- **危險用法**：
  - 🚫 把 AGPL 程式庫**連結進**你的後端應用程式（in-process linking）。
  - 🚫 **改了** AGPL 軟體又對外提供服務，卻不釋出改動。
- **務實結論**：Yolian 對 AGPL 元件採「**不改、隔進程、用寬鬆 driver**」三原則即可安全使用；但**能用 Apache/BSD 同類就優先用**（如 Valkey 取代 Redis），省去整個灰區。

> **對 Yolian 的啟示**：把這三原則寫進工程規範。AGPL 不是「絕對不能碰」，而是「**碰主程式才致命**」——理解邊界比恐懼更有用。

---

## 9. 把「開源組合」變成「可收費服務」的加值層

客戶不會為「你用了 PostgreSQL」付錢。付費理由是你**在開源之上加的東西**——這也呼應研究中「定價透明、學員免費教練付費」（`competitor-research.md` §5.4）：

| 加值層 | 具體內容 | 對應研究痛點 |
|--------|---------|------------|
| **託管與可用性** | 客戶免運維、自動備份、SLA、監控 | 競品多為 SaaS，自架不是教練的事 |
| **在地化合規** | 繁中、台灣金流/電子發票、LINE 生態、個資/健康資料合規 | 國際大廠的弱點（`product-architecture.md` §1.1） |
| **整合與體驗** | 把零散開源縫成「一句話完成營運」的無縫體驗 | 全市場 0 家做到（§0 真空） |
| **資料主權與信任** | 客戶資料留在 Yolian schema，不鎖進第三方模型；寫入確認 + audit | 對標但超越對手（設計原則 #3） |
| **支援與成功** | 導入、教學、客服、教練社群 | 國內外都靠服務留存 |
| **持續演進** | 新 Action 一加，UI 與 Agent 同時獲得新能力 | 設計原則 #1 的複利 |

> **對 Yolian 的啟示**：**開源讓你「站上起跑線」，加值層才是「跑道」。** Yolian 的六層加值裡，「在地化合規」與「無縫整合體驗」是國際開源/大廠最難複製的，應作為定價與行銷的主訴求。

---

## 10. 風險與待決策

**待校準的關鍵分岔：**
1. **自架 vs 全託管**：MVP 是否全部用託管（Neon/Supabase Postgres、R2、LLM API），把運維降到最低？（建議：是，小團隊別自架 DB/儲存）
2. **排課自研 vs Cal.diy**：自研排課（與 Action 層整合最深），或先用 Cal.diy(MIT) 加速？（建議：自研，它是護城河；Cal.diy 可作參考實作）
3. **工作流引擎**：Phase 3 市集是自研 Action 編排，還是評估可商用的開源引擎？（建議：自研，n8n 授權不可商用轉售）
4. **是否開源 Action SDK**：Phase 3 要不要把共用 Action 層 SDK 開源，做開發者生態（Open-Core C 型）？

**主要風險與緩解：**
- **授權變天**（Redis 前例）→ 元件包在 adapter 後 + CI 授權掃描 + 優先選基金會治理專案。
- **AGPL 誤用**（連結進主程式）→ §8 三原則 + 掃描器擋 PR。
- **Open-Core 陷阱**（Cal.com `/ee`、n8n）→ 核心模組自研，不依賴他人商業層。
- **依賴升版偷改授權** → Renovate/Dependabot + 每次升版重掃授權。
- **過度整併、元件爆炸** → 一物多用（pgvector 在 PG、Valkey 當快取+佇列），壓低元件數與維運面。

---

## 附：本文授權狀態查證來源（一手）
- Elasticsearch 加回 AGPL（2024.08）：elastic.co/blog/elasticsearch-is-open-source-again
- Redis 8 加 AGPLv3（2025.05）：redis.io/blog/agplv3
- Valkey = BSD、Linux Foundation fork of Redis 7.2.4：en.wikipedia.org/wiki/Valkey
- n8n Sustainable Use License（自用/非商業、不可轉售為服務）：github.com/n8n-io/n8n/LICENSE.md
- Cal.com = MIT 根 + Open-Core（`.ee` 商業）；Cal.diy = 100% MIT fork：github.com/calcom
- 其餘（MongoDB SSPL、HashiCorp BUSL→OpenTofu、Grafana AGPL、MinIO AGPL、Typesense GPL-3、Sentry FSL/BSL）：各專案 LICENSE 與官方公告
> 鐵則：**採用任何元件前，到該專案當前 LICENSE 重新確認一次** —— 授權會變，本文是起點不是終點。
