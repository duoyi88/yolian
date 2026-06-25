# 健身平台競品深度拆解（B 端 + C 端 + 教練軟體）

> 專案：Noki — 面向健身教練與個人工作室的營運平台
> 本文是 `competitor-research.md` 的深度版：逐一實地探查官網/功能頁/定價頁，並嘗試試用 demo/註冊流程，全程截圖佐證。
> 探查方式：瀏覽器實地走訪（非二手轉述），截圖存於 `research/screenshots/`
> 日期：2026-06-25
> 範圍：教練↔學員軟體（P0）＋ 場館營運 B 端 ＋ C 端大平台

---

## 0. 截圖索引（research/screenshots/）

| 檔名 | 內容 |
|------|------|
| onefloors-home.png | OneFloors 首頁（功能/雙角色/FAQ/團隊方案） |
| onefloors-pricing.png | OneFloors 三方案定價 |
| onefloors-coach-templates.png | OneFloors 7 種教練網站版型 |
| onefloors-coach-ironclad.png | OneFloors 教練個人網站實例（Ironclad） |
| simpletraining-home.png | SimpleTraining 首頁（7 模組/定價/PWA/官網） |
| simpletraining-signup.png | SimpleTraining 註冊頁（Google OAuth only） |
| simpletraining-guide.png | SimpleTraining 使用指南（後台模組流程） |
| trainerize-features.png | Trainerize 功能總頁 |
| trainerize-pricing.png | Trainerize 定價與功能比較表 |
| mohot-home.png | MoHot 全產品線（App/MERP/超級總教練/PT） |
| 17fit-home.png | 17FIT 首頁（經營者/消費者雙入口） |
| 17fit-business.png | 17FIT 商家端 11 模組 |
| mindbody-home.png | Mindbody 首頁（7 模組 tab） |
| mindbody-pricing.png | Mindbody 三方案 + 功能比較 + Messenger[ai] |
| pushpress-pricing.png | PushPress 定價 + AI Assistant + 完整功能表 |
| glofox-pricing.png | Glofox 詢價頁（價格不公開） |
| styd-home.png | 三体云动首頁（SaaS 8 端 + AIoT） |
| styd-ai-assistant.png | 三体「AI 小助理」實測對話 |
| qingcheng-home.png | 青橙科技首頁（AI 賦能/19.9 元/自由教練） |
| keep-home.png | Keep 首頁 |
| leoao-home.png | 乐刻运动首頁（2000+ 門店） |
| supermonkey-home.png | 超级猩猩首頁（按次付費） |
| **onefloors-appstore.png** | OneFloors App Store 頁（規格/隱私/評論） |
| **onefloors-app-screens.png** | OneFloors App 實際畫面 1-3（拍照記餐/一句話調目標/課表） |
| **onefloors-app-screens2.png** | OneFloors App 實際畫面 2-4（含 InBody 90 天折線） |
| **onefloors-coach-atelier.png** | OneFloors 教練網站版型 Atelier（瑜伽） |
| **onefloors-coach-concrete.png** | OneFloors 教練網站版型 Concrete（極簡黑白） |
| **mindbody-scheduling.png** | Mindbody 排程功能頁 |
| **mindbody-messenger-ai.png** | Mindbody Messenger[ai] AI 前台完整頁 |
| **17fit-booking.png** | 17FIT 預約模組（一對多/一對一/候補/共享方案） |
| **17fit-report.png** | 17FIT 報表模組（20+ 報表交叉分析） |
| **17fit-customer.png** | 17FIT 客戶管理模組 |
| **17fit-pos.png** | 17FIT POS 模組 |
| **17fit-iot.png** | 17FIT 入出場 IoT 模組 |

---

## 1. P0 直接競品深度拆解

### 1.1 OneFloors（onefloors.cc）— 願景最接近 Noki ★★★

**定位**：AI 教練 × 學員的訓練/飲食/體態 App（iOS）。Slogan：「讓習慣便宜、讓回饋誠實」。

**雙角色設計（核心洞察）**：一個 App、兩種角色。
- **學員端**：今日課表在首頁（不點三層）、拍照記錄飲食（幾秒）、AI 營養師依紀錄回答、進度條
- **教練端**：每位學員的本週填寫率/蛋白達標率/訓練完成率一頁看完、改目標/課表/建議重量學員端即時生效、從教練網頁直接接收預約

**功能清單（首頁實證）**：
1. AI 拍照記錄飲食（拍盤子→模型約 1 秒回 1–2 個最像的菜→調份量）— 不靠食物資料庫，用視覺模型辨識整盤
2. 4 大營養素即時（熱量/蛋白/碳水/脂肪），教練調目標即時同步
3. 自主訓練紀錄（課表預填建議重量、第二次點擊完成該組、本次 vs 上次對照）
4. 12 週進展折線圖（每個動作旁一鍵打開）
5. 體態追蹤 + InBody 報告拍照自動入帳
6. AI 營養師對話
7. 教練學員儀表板
8. 教練↔學員預約

**定價（pricing 頁實證）**：
| 方案 | 價格 | 學員上限 | 重點 |
|------|------|---------|------|
| 免費版 | NT$0 永久 | 3 位 | **已含 AI 智能課表生成**、課程模板庫、排課預約、飲食/訓練監督、InBody 追蹤 |
| Pro | NT$490/月 | 30 位 | 形象履歷 + onefloors.cc 個人網站、完整訓練歷史、Pro 徽章 |
| Enterprise | 客製 | 無限 | 多教練/多分店、客製導入、專屬窗口 |

- 學員端永久免費；Pro 走 App Store 內購；發票由 Apple 開立

**教練個人網站（/coach 實證）**：7 種版型（Ironclad 肌力健力 / Smash 球類競技 / Atelier 瑜伽體態 / Concrete 極簡黑白 / Velour 高階質感 / Verdant 療癒復健 / Voltage 能量競速）。實例 Ironclad 含：Hero、想解決的問題、訓練方案（多卡片含週期/形式/說明）、教練背景與認證（NSCA-CSCS/USAPL 等）、學員成果見證（量化數字 +62.5kg）、FAQ、預約聯絡（LINE/Email/IG/電話/場地）。網址格式 `onefloors.cc/coach/<名>`。

**對 Noki 的啟示**：
- ✅ 雙角色同 App、教練改動學員端即時同步 — 這套「即時雙向」是體驗關鍵，Noki 必學
- ✅ 免費版就放 AI 課表生成 — 把 AI 當獲客鉤子
- ✅ 教練個人網站做成「可選版型 + 自動生成」是低成本高感知價值
- ⚠️ 弱點：**僅 iOS、無 Android、無 Web 後台**、場館營運（金流/會籍/門禁/多分店）薄弱、AI 仍是「功能點」非「操作中樞」
- 🎯 Noki 切入：補 Android/Web、補營運層、把 AI 從「飲食辨識 + 問答」升級到「對話式操作整個平台」

### 1.2 SimpleTraining 簡單練（simpletraining.co）— 教練行政 SaaS 標竿 ★★★

**定位**：專為台灣健身教練/工作室的全方位管理平台（PWA，免下載）。Slogan：「把時間留給學員，行政交給簡單練」。

**痛點行銷（首頁敘事，值得學）**：用 6 個「教練都懂的煩惱」對應 6 個解法：
1. LINE 排課訊息爆炸 → 拖拉行事曆
2. Excel 管合約漏續約 → 自動到期提醒
3. 押金/所得算半天 → 即時營收儀表板
4. 多教練衝堂 → 智能衝堂偵測（5 分鐘排完整週）
5. 學員問上次練什麼翻不到 → 學員時間軸一秒調出
6. 大系統每月上千元用不到一半 → 不到十分之一價格

**7 大核心模組（首頁實證）**：學員管理、智能排課、合約管理、經營儀表板、業績管理（底薪/售課抽成/完課獎金階梯/自動算月薪）、行動優先（PWA）、專屬品牌官網。額外：完全客製化（時段/合約規則/前台/表單）。

**定價（首頁實證）**：
| 方案 | 價格 | 上限 | 重點 |
|------|------|------|------|
| FREE | 永久免費 | 10 會員/5 合約/1 教練 | 排課、電子簽名、訓練紀錄、諮詢管理、Classic 模板官網、14 天 PRO 試用 |
| PRO | NT$399/30天 起（360 天約 NT$10/天） | 無限會員/合約、10 教練 | QR 簽到、優惠活動、團課、數據儀表板、教練績效、業績/薪資、Google Calendar 匯出、CSV、多管理員、**會員客戶端入口** |
| Enterprise | 聯絡 | 無限 | 白標、API、多據點、專屬 CSM、資料遷移 |

**後台結構（guide 頁實證）**：系統設定 → 銷售管理(合約) → 排課管理 → 數據統計 → 業績管理 → 品牌官網。排課有「**草稿模式**」：可先排好整週再一次送出（避免排錯），這是很貼心的細節。

**試用嘗試結果**：註冊頁 `/auth/signup` **僅支援 Google 帳號 OAuth**，無 email/密碼註冊，無法在不綁真實 Google 帳號下進入後台。後台畫面只能透過官方 guide 頁的文字流程推得，無公開 demo。

**對 Noki 的啟示**：
- ✅ 行政流程（合約/業績/薪資/排課）完整度是台灣標竿，且定價極低（預付制）
- ✅ 「痛點→解法」的敘事與「草稿模式排課」細節值得抄
- ✅ 已有「會員客戶端入口」(PRO) — 但學員端偏輕
- ⚠️ 弱點：**完全沒有 AI**、無訓練動作庫、無飲食/體態辨識、學員成長深度弱、無原生 App
- 🎯 Noki 切入：SimpleTraining 的行政 + OneFloors 的 AI/學員成長 = 兩者交集正是空白

### 1.3 Trainerize（ABC Trainerize）— 全球標準 ★★★

**定位**：線上教練的黃金標準（被 ABC Fitness 收購）。功能頁分 5 大塊：Coach / Engage / Manage / Add-ons / Integrations。

**Coach（教練交付）**：
- **AI Workout Builder**（描述目標與偏好→生成結構化課表→可編輯排程）
- 自訂分期化課表（從零或複製模板）
- 動作/課表庫（專業動作、隨選課表、完整課表可即時指派）

**Engage（互動激勵）**：1-1/群組訊息、**語音訊息**、**視訊通話**（可變現）、自動訊息、群組社群、挑戰（排行榜/門檻）、WOD、群組激勵、徽章里程碑、High-five 反應

**Manage（營運）**：排程（自助預約 book-buy-coach）、預約與課程、Trainerize.me 個人檔案與商店、行事曆同步、諮詢表單、產品銷售自動化、堂數包、金流

**5 大 Add-ons**：Business（$25）、Advanced Nutrition（$20–45，2400+ 食譜/智能餐單/購物清單）、Video Coaching（$10，視訊通話 50h/串流 100h）、Custom Branded App（一次性 $169）、Stripe Integrated Payments（$10）

**整合**：Apple Watch/Health、Garmin、Fitbit、Withings、MyFitnessPal、YouTube、Zapier、**Mindbody、Glofox**（與場館系統互補）

**定價（pricing 頁實證）**：
| 方案 | 價格 | 客戶上限 | 重點 |
|------|------|---------|------|
| Basic | 免費 | 1 | 基本課表/追蹤/訊息/營養追蹤 |
| Grow | $9/月 | 2 | + AI Workout Builder、Trainerize.me、穿戴整合、自動交付、Zapier |
| Pro | $23 起/月（可選到 200 客戶，$79@30、$275@500 級距） | 5–200 | + Live 客服、白標 App（可加購） |
| Studio Plus | $248/月/分店 | 500 | 場館級白標 App、含全部 add-ons、API、多分店、SSO |

**對 Noki 的啟示**：
- ✅ 動作庫 + 影音/語音/視訊 + 社群挑戰 = 學員黏著與激勵的完整工具箱
- ✅ AI Workout Builder 從 $9 方案就給 — 同 OneFloors 把 AI 下放
- ✅ per-client 級距定價，從個人教練到 500 人場館一條龍
- ✅ 與 Mindbody/Glofox 整合（承認自己不做場館營運，靠整合）
- ⚠️ 弱點：加購後昂貴、學習曲線陡、AI 僅止於生成課表/餐單；介面對純面授教練過重
- 🎯 Noki 切入：把 Trainerize 要靠 5 個 add-ons + 整合才能拼出的東西，用一個 Agent 介面統合輸入

---

## 2. 場館營運 B 端深度拆解

### 2.1 17FIT（台灣 B 端龍頭，運動 + 美容）

**規模**：1200+ 店家、1200 萬累計預約人次、365 種功能、95% 續約率。已從健身擴張到**美容業雙產業**。

**11 大功能模組（business 頁實證，每個都有獨立頁）**：
LINE 外掛模組、行銷（優惠券/紅利/促銷）、預約（全通路 24h）、支付（全台第一不需履保信託的金流）、POS（電腦即結帳）、報表（50+ 種、交叉分析）、客戶（會員輪廓）、員工（排程/表現/自動結算薪資）、入出場（IoT 通關/點名/票券/人流）、專屬網站、品牌 APP。

**雙入口**：經營者（線上開館）vs 消費者（探索店家）— 平台自帶導流。
**試用**：有 `/b/free-trial` 免費試用入口（需填資料）。
**AI**：❌ 無明顯 AI。
**啟示**：B 端標準功能集的完整參照；龍頭但無 AI、無訓練成長深度。被部分競品點名「平台抽成、稀釋私域」。

### 2.2 MoHot 摩哈特（台灣，B + C 全產品線）

**產品線（首頁實證）**：
- **MoHot App**（免費，1500+ 動作不鎖）：教練幫學員編排課表遠端監督、課表內留言、報表（日/週/月訓練量、卡路里趨勢、部位圓餅圖）、好友課表觀摩、課表輸出網頁
- **MoHot MERP**（場館 POS，租賃制）：會員/產品/訂單、教練課團課排程預約、會員卡進出場、金流/線上刷卡/電子發票、統計報表、客戶端 App（購買紀錄/團課預約/師資）
- **超級總教練**：30 秒向客戶展現專業價值的行銷工具
- **MoHot PT**（升級教練版免費）：管理訂單/帳務、電腦版看學員月曆與報表

**試用嘗試結果**：超級總教練有公開 demo（superdemo.mohot.com，帳號 superdemo@mohot.com / super2019 已預填），但**實測登入後端回傳「不明錯誤，請稍後再試」，demo 已失修**（網站 ©2019，整體偏舊）。
**AI**：❌ 無。
**啟示**：訓練紀錄/動作庫深度與「教練幫學員開課表 + 學員看成長」這條線很早就做了，是門檻；但 UI 老舊、無 AI、飲食/體態弱、demo 年久失修反映產品停滯。

### 2.3 Mindbody（全球 B 端巨頭，上市）

**規模**：40,000+ 商家、3M+ App 月活用戶（市集導流）、600M+ 年預約量、平均 6 個月營收 +45%。

**7 大模組（首頁 tab 實證）**：Payments、Marketing（自動 email/SMS）、Staff management（排班/代課/薪資）、Booking（全裝置）、Scheduling（單一日曆即時同步）、Reporting、Branded App。

**進階（pricing + FAQ 實證）**：
- **Lead Management**：銷售漏斗儀表板（拖拉式階段、自動捕捉名單、跟進任務、漏斗分析、Google Ads 表單串接）
- 多分店（datashare / Enterprise 企業級跨店報表）
- **Messenger[ai]**：24/7 AI 客服機器人（答客問、回覆未接來電、帶訂課促購）— add-on
- Mindbody Capital（無需申請/擔保/查信用的營運資金）、Mindbody Insurance
- 金流 Mindbody Payments（powered by Stripe）

**定價（pricing 頁實證）**：Starter $99/分店起 → Accelerate（進階報表/資源管理/Pick-a-Spot/促銷碼）→ Ultimate（email/SMS 行銷自動化 + Lead management）。品牌 App 與 Messenger[ai] 為 add-on。
**啟示**：B 端功能最全 + 自帶 3M 用戶市集（雙邊網路效應），這是 Noki 短期無法複製的護城河；但貴、複雜、學習成本高、有 Dark Pattern 爭議。其 Messenger[ai] 是「AI 客服」非「AI 操作」。

### 2.4 PushPress（全球 B 端，主打 AI + 免費層）★ AI 觀察重點

**重大發現**：定價頁頂部直接主打 **AI Assistant — 「Know what's happening. Just ask.」「Your gym has answers.」** 用自然語言問會員、出席、名單、營收（"Get instant answers about members, attendance, leads, and revenue. No spreadsheets required."）。**但這是唯讀問答，不是操作型 Agent**。

**另有 Member Intel**：每堂課前一小時在 Staff App 主動浮現「里程碑、新面孔、值得行動的時刻」，免準備。

**定價（pricing 頁實證）**：
| 方案 | 價格 | 重點 |
|------|------|------|
| Free | $0（無月費，金流 4.99%+.30） | 無限 leads/admins/members/staff、AI Support、Screens/Members/Staff/Kiosk App |
| Pro | $159/月（金流降 2.89%） | + 進階報表/自動化 |
| Max | $229/月（金流 2.75%） | + 完整功能 |
| Train | $79 起 | 課表追蹤（≤20 客戶） |
| Grow | $329 | 完整 CRM + 自動化 + email/SMS + 官網 |
| Full Stack | ~$559 | 全包 |

其他亮點：Rank Tracking（武術段位）、Committed Club（出席遊戲化）、品牌 App（$81–97 add-on）、由健身房老闆打造、AI 客服解 60% 對話。
**啟示**：PushPress 是國際上**最接近「AI 即介面」**的 B 端玩家（自然語言查經營數據），但仍停在「查詢/洞察」，沒做到「用一句話完成操作」。**這正好驗證 Noki 的 Agent 操作中樞是真空白**。

### 2.5 Glofox（全球 B 端，精品工作室）

定價頁為**詢價表單，價格不公開**。已知（前期研究）：白標 App 含基本價、乾淨 UI、CRM、Email/SMS/推播、每週省 2–4 小時行政。被 Trainerize 列為整合對象。

### 2.6 三体云动 STYD（中國 B 端龍頭）★ AI 觀察重點

**規模**：50,000+ 場館、239 城、310+ 功能、近百項數據分析與「經營處方」、月均新增/優化 27 個功能。

**SaaS 8 端（首頁實證）**：老闆端（數據看板/員工）、財務端（流水/智能統計）、市場端（品牌/引流）、前台端（訪客/簽到）、會籍端（獲客簽單/維護）、教練端（排課約課/消課續費）、會員端（購卡約課）、多平台（App/小程序/瀏覽器）。
**AIoT**：人臉閘機、智能門禁、儲物櫃、體測儀、超級團課心率系統等軟硬一體閉環。

**重大發現 —「三体 AI 小助理」（2025.05 上線）**：
- 官方定位：「功能秒回答、數據自動出、會員自動跟」
- **行業首家接入微信 AI 生態**（2025.06）
- **實測**（我直接在官網對話框問「私教课怎么提升续费率」）：回傳結構化三點建議（增強體驗信任/降低續費門檻/強化教練協同），並**引用自家功能**（體驗卡插件、包月私教、多教練代約課）+ 文檔連結。→ 屬 **RAG 知識型助理（偏經營諮詢 + 產品導覽）**，非直接操作後台 CRUD。
**啟示**：中國龍頭已把 AI 當賣點，但仍是「問答/諮詢 + 自動跟進」層級；軟硬一體 + 微信生態是其護城河；功能冗餘度高、學習成本高。

### 2.7 青橙科技（中國 B 端新銳）

**首頁實證**：四大切入（健身房/健身產業鏈/健身教練/**AI 賦能**）。AI 賦能定位「基於人工智能算法，深入挖掘健身產業數據，快速感知行業動態」。
**定價創新**：Pro 版「**按帳號數**」**19.9 元/員工/月**起（≤10 人小工作室），首月不扣費。
**產品線**：24h 自助健身房（物聯網 + 無人值守）、**自由教練專用管理系統**（19.9 元/月，獨立授課/會員管理/多渠道營銷獲客）。API 開放度國內最高。
**啟示**：低價 + 自由教練專屬系統 + AI 排課，是針對「超級個體教練」的精準打法，與 Noki 目標客群高度重疊。

---

## 3. C 端大平台（截圖留檔，內容詳見 v1 報告）

- **Keep**（gotokeep.com）：2 億+ 用戶，C 端內容/社群/電商/智能硬體生態。首頁以 App 下載導引為主。
- **乐刻运动**（leoao.com）：2000+ 門店、24h 自助、月卡制、量身私教課/包月私教、線上「跟我練」、OMO。
- **超级猩猩**（supermonkey.com.cn）：按次付費不辦卡、~100 種團課、24h 自助（Sream 智能系統）、教練 KOL 化、私教為第二曲線。

**C 端啟示**：C 端是「內容 + 流量 + 消費」生意，與 Noki 的「教練營運工具」不同層；但其「教練 KOL 化、學員追隨、按次付費去推銷化」的信任模型，可借鏡到 Noki 的教練個人品牌頁與學員關係設計。

---

## 4. 試用 / Demo 探查結果彙總

| 服務 | 試用入口 | 實測結果 |
|------|---------|---------|
| OneFloors | App Store（iOS） | 需 iOS 裝置安裝；Web 端僅行銷頁 + 教練網站預覽可看（已截 Ironclad 實例） |
| SimpleTraining | /auth/signup | **僅 Google OAuth**，無法免綁帳號進後台；後台流程靠官方 guide 頁推得 |
| Trainerize | 30 天免費試用（需註冊） | 功能/定價頁資訊極完整，未實際註冊 |
| MoHot 超級總教練 | superdemo.mohot.com（帳密公開預填） | **demo 已失修，登入回「不明錯誤」**（站點 ©2019） |
| 17FIT | /b/free-trial | 需填資料由業務跟進 |
| Mindbody | Get a demo（表單） | 無自助試用，需業務 demo |
| PushPress | signup.pushpress.com（Free $0） | 有真免費層可註冊；功能表完整已擷取 |
| Glofox | 詢價表單 | 價格不公開 |
| 三体云动 | 立即免費體驗（填手機） | **AI 小助理可直接在官網對話實測**（已截圖） |
| 青橙 | /feedback 提交諮詢 | 需諮詢；定價透明（19.9 元/帳號） |

> 結論：B 端 SaaS 普遍「業務驅動、需 demo 預約」，少有自助試用；台灣兩大直接競品（OneFloors iOS-only、SimpleTraining Google-only）都無法在無真實帳號下深入後台。PushPress 的真免費層 + STYD 的官網 AI 對話框，是少數能即時體驗的。

---

## 5. AI / Agent 能力總表（本次最關鍵產出）

| 服務 | 有無 AI | AI 類型 | 能否「對話式操作平台」 |
|------|--------|---------|--------------------|
| OneFloors | ✅ | 拍照辨識飲食 + AI 營養師問答 + AI 課表生成 | ❌ 僅功能點 |
| Trainerize | ✅ | AI Workout Builder（生成課表） | ❌ 僅生成 |
| PushPress | ✅ | **AI Assistant 自然語言查經營數據**（唯讀）+ Member Intel | ⚠️ 最接近，但只查不做 |
| Mindbody | ✅ | Messenger[ai] 24/7 客服機器人 | ❌ 對外客服 |
| 三体云动 | ✅ | AI 小助理（RAG 經營諮詢 + 產品導覽）+ 接微信 AI | ❌ 問答/諮詢 |
| 青橙 | ✅ | AI 賦能（數據洞察）+ AI 智能排課 | ❌ 單點自動化 |
| SimpleTraining | ❌ | — | ❌ |
| 17FIT | ❌ | — | ❌ |
| MoHot | ❌ | — | ❌ |
| Glofox | ❌（行銷自動化） | — | ❌ |

### 結論：全球都還沒有「Agent 操作中樞」
- 最強的 AI 也只到三種：**生成內容（課表/餐單）**、**查詢/洞察數據（PushPress 自然語言、STYD 小助理）**、**對外客服（Mindbody Messenger[ai]）**。
- **沒有任何一家**做到讓教練用一句話完成跨模組操作：例如「把王小明這週的課改到三、五早上，深蹲加 5 公斤，並通知他、順便看他這個月還剩幾堂」——這需要 AI 同時讀寫排課 + 訓練 + 溝通 + 合約。
- PushPress 已喊出「Just ask」但只敢做唯讀查詢；這恰恰證明**「對話式寫入操作」是真空白，也是 Noki 最尖銳的差異化**。

---

## 6. 功能覆蓋矩陣（B 端 vs C 端 vs 教練端）

| 能力 | OneFloors | SimpleTraining | Trainerize | 17FIT | MoHot | Mindbody | PushPress | 三体云动 | 青橙 |
|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 會員 CRM | ◐ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 排課/預約 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 合約/堂數 | ◐ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 金流/POS | ❌ | ◐ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 訓練動作庫 | ✅ | ◐ | ✅✅ | ❌ | ✅✅ | ❌ | ◐ | ◐ | ◐ |
| 飲食/營養 | ✅✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 體態/InBody | ✅ | ❌ | ✅ | ❌ | ◐ | ❌ | ❌ | ✅(體測) | ◐ |
| 學員成長可視化 | ✅✅ | ◐ | ✅ | ◐ | ✅ | ❌ | ◐ | ◐ | ◐ |
| 業績/薪資 | ❌ | ✅ | ◐ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 門禁/IoT | ❌ | ❌ | ❌ | ✅ | ✅ | ◐ | ◐ | ✅✅ | ✅ |
| 品牌官網/App | ✅(網站) | ✅(官網) | ✅(白標App) | ✅ | ◐ | ✅ | ✅ | ✅ | ✅ |
| 多分店 | ◐ | ✅(企業) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅✅ | ✅ |
| AI 能力 | ✅✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Agent 操作中樞 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 原生 App | iOS | PWA | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> ✅✅=業界最強 ✅=完整 ◐=部分 ❌=無

**讀表結論**：
1. 行政營運（CRM/排課/合約/金流/業績/多分店）是紅海，人人都有。
2. 訓練深度（動作庫/飲食/體態/成長可視化）只有教練類 App 強（OneFloors/Trainerize/MoHot），B 端場館系統幾乎空白。
3. **「訓練深度 + 完整營運 + AI Agent」三者同時具備者：0 家。** 這就是 Noki 的座標。

---

## 6.5 第二輪深探：App 實機畫面 + 後台真實操作（2026-06-25 補充）

> 本輪聚焦兩件事：① OneFloors 因 iOS-only 無法在本機安裝，改抓 **App Store 官方預覽截圖**（即 App 實際畫面）；② Mindbody / 17FIT 後台需業務 demo 或登入帳號，改抓**功能子頁的後台 UI + Help Center**。皆有截圖佐證。

### A. OneFloors App 實際畫面（App Store 預覽，4 格主流程）

App Store 規格：開發者 LIN YI、健康與健身類、**iOS 14.0+、47.9 MB、僅英文介面、16+、免費含 App 內購**、評論數未達顯示門檻（新 App）。一句話定位：「**你的口袋健身管家**」「**台灣第一款「教練 × 學員」雙端健身 App**」。

4 格官方截圖揭露的真實 App 畫面與標語（重要）：
1. **「拍一張，全部幫你記。」** — AI 食物辨識 30 秒填完，TDEE/宏量/步數一次到位（首頁：熱量圓環 1983、三大營養素條、今日餐段卡片、底部 4 tab）
2. **「一句話，AI 幫你重算。」** — 說出今天的狀態，三大營養素與熱量目標立刻更新（畫面是黃色 AI 對話卡 + 2320 kcal 重算結果）← **這是學員端的自然語言輸入，比官網行銷頁更接近 Agent**
3. **「教練、課表，排進一張表。」** — 預約教練、自主訓練全裝進同一行事曆（月曆 + 「新增什麼？」底部選單：電話教練/自主運動）
4. **「九十天，看見改變。」** — 體重/體脂/骨骼肌/InBody 一張圖看完（身體 tab：每日體態 + InBody 紀錄四條折線）

> **關鍵更新**：先前只從官網記到「AI 營養師對話」，App 實機畫面證實學員端已有「**說一句話 → AI 重算當日營養目標**」的自然語言互動。但仍侷限「飲食目標」單一車道，未擴及排課/訓練/溝通等跨模組操作。截圖上印有「iOS · ANDROID」字樣，但 App Store 實際標註「僅適用於 iPhone」→ Android 仍是行銷宣稱、尚未落地。

### B. OneFloors 教練網站版型（再補 2 種）
除前次 Ironclad（肌力健力），本輪截 Atelier（瑜伽體態，柔和留白）與 Concrete（極簡黑白）。7 種版型共用同一資訊架構（Hero／想解決的問題／訓練方案／背景認證／學員成果／FAQ／預約），差異在配色與字體調性 → 印證「**選版型 + 填內容 = 自動生成教練官網**」的低成本高感知打法。

### C. Mindbody 後台與 AI（功能子頁 + Messenger[ai] 深探）
- **排程後台**（/business/scheduling）：單一日曆同時管理排班與預約、班表/預約即時跨觸點同步、易設定與編輯。
- **Messenger[ai]（AI 前台，深探 /business/messenger-ai）**：
  - 可被「**訓練成你的品牌語氣**」回覆問題與訂課請求；需真人時自動標記轉接
  - 24/7 即時客服（少電話、多訊息）
  - 跨渠道（簡訊 / Facebook / 網頁聊天）自動回覆，可群發重要更新
  - **自動銷售**：每位新客課後自動跟進，並能經 text/webchat 自動賣套餐與會籍
  - 統一對話儀表板（client + staff 通訊一處管理）
  - 獨立登入入口 messenger.mindbodyonline.com
  - → 定性：**「對外客服 + 銷售」型 AI，能「執行動作」但只在客服/銷售車道**（賣課、訂課、回訊），不是教練端「跨模組營運操作」。
- 後台實際操作畫面需登入帳號（clients.mindbodyonline.com）或業務 demo，無公開自助試用；Support Center 為 Salesforce 動態頁、截圖價值低。

### D. 17FIT 後台模組（功能子頁逐一深探，繁中後台 UI）
逐頁拆解（每頁皆含後台 UI 渲染圖，已截圖）：
- **預約**：一對多課程 + 一對一服務（美睫/美甲/沙龍）、線上預約+付款同步、自訂取消政策、**候補即時通知**、**家庭/企業/好友共享方案（全台唯一支援團體式線上預約）**、出席提醒提升 20% 出席率
- **報表**：20+ 報表，銷售/客戶/人員三面向 + 交叉分析、每日經營數據即時、可搭配優惠券/訊息活動/方案系統
- **客戶**：會員資訊一站整合、會員輪廓洞察、精細化服務
- **POS**：電腦即可操作結帳、無需額外軟硬體
- **入出場 IoT**：場館通關/點名/票券/人流顯示智能化

> 17FIT 定性：**B 端營運深度（預約金流會員報表門禁）非常完整、繁中在地、含美容跨業**，但全線**無 AI、無訓練成長**。是 Noki「行政營運層」最完整的在地對標。

### E. 本輪結論（不改變總判斷，反而強化）
- OneFloors 的「一句話重算營養」證明：**對話式輸入在學員端已被驗證可行且體驗好**，但全市場仍把它鎖在單一車道（飲食目標）。
- Mindbody Messenger[ai] 證明：**AI「執行寫入動作」已商業化**，但鎖在「對外客服/賣課」車道。
- 把這兩點合起來看：**「教練端、跨模組（排課+訓練+合約+溝通）的對話式寫入操作」依然 0 家** —— Noki 的 Agent 操作中樞定位再次被驗證為真空白。

---

## 7. 對 Noki 的可執行結論

1. **必備（門檻）**：CRM、排課（含草稿模式/衝堂偵測）、合約堂數、金流、業績薪資、品牌官網、多分店、學員端入口 — 直接對標 SimpleTraining + 17FIT 的完整度。
2. **訓練深度（學員成長）**：動作庫、訓練紀錄「本次 vs 上次」、12 週折線、體態/InBody、飲食辨識 — 對標 OneFloors + Trainerize + MoHot。
3. **差異化王牌（Agent 操作中樞）**：教練/學員用「一句話/一張照片」完成跨模組讀寫，AI 同時看得到訓練 + 合約 + 溝通 + 續約風險。**這是全球 0 家做到的真空白**，PushPress 的「Just ask」唯讀版已驗證市場渴望。
4. **平台策略**：跨平台（iOS + Android + Web 後台），補 OneFloors(iOS-only) 與 SimpleTraining(PWA) 的缺。
5. **商業模式**：學員端免費、教練端低價訂閱（OneFloors/SimpleTraining 已驗證）；定價透明（反中國不標價陋習）；教練個人網站自動生成（OneFloors/SimpleTraining 都證明有需求）。
6. **獲客鉤子**：把 AI（課表生成 + 對話操作）放進免費層，如 OneFloors/Trainerize 把 AI 下放到免費/$9 方案。

> 下一步可選：① 進一步用 iOS 實機安裝 OneFloors 走完整學員/教練流程截圖 ② 約 Mindbody/17FIT 業務 demo 看後台真實操作 ③ 直接進 Noki 的資訊架構 / MVP 功能地圖規劃。
