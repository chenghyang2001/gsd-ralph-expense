# Phase 1: Expense CLI - Context

**Gathered:** 2026-07-03
**Status:** Ready for planning

<domain>
## Phase Boundary

交付單檔 Python CLI 記帳器：四個指令（add / list / total / rm）、JSON 檔持久化、輸入驗證，且 `pytest test_expense.py` 全綠。零第三方依賴，只用標準庫（argparse / json / pathlib / sys）。檔案結構固定為 `expense.py`（主程式）+ `test_expense.py`（測試）。

使用者選擇「你決定，用慣例定好」——以下所有實作決策由 Claude 依慣例拍板，下游 planner / executor 直接照做，不需再問使用者。

</domain>

<decisions>
## Implementation Decisions

### ID 配置策略

- **D-01:** 新 id = `max(現有所有 id, 預設 0) + 1`。清單為空時第一筆 id = 1。
- **D-02:** id **不重用**。`rm` 刪除後再 `add`，仍取 `max+1`（單調遞增），不回填被刪掉的 id。理由：id 穩定、無碰撞，測試斷言明確。

### total 分類排序

- **D-03:** 加總輸出依分類**首次出現順序**列出（利用 Python dict 保序特性），符合規格範例 `食物 120` / `交通 50`。
- **D-04:** `合計 <總和>` 一律印在最後一行。
- **D-05:** 相同分類字串合併加總；分類**大小寫敏感**（`食物` 與 `Food` 視為不同分類），不做正規化——最簡慣例。

### 測試隔離與資料檔路徑

- **D-06:** 核心邏輯函式（load / save / add / remove / …）接受明確的 `path` 參數，不在函式內硬讀固定路徑。
- **D-07:** CLI 入口決定實際路徑：優先讀環境變數 `EXPENSE_DB`，否則預設程式同目錄 `expenses.json`（`Path(__file__).parent / "expenses.json"`）。
- **D-08:** `test_expense.py` 用 pytest `tmp_path` fixture 產生隔離路徑注入核心函式，**絕不**碰真實 `expenses.json`。理由：測試間互不干擾、可重複執行、CI 安全。

### 輸出串流與空狀態

- **D-09:** 錯誤訊息一律寫到 `stderr` 並 `sys.exit(1)`；正常輸出寫 `stdout`。
- **D-10:** `list` 遇空清單 → 不印任何行（exit 0）。
- **D-11:** `total` 遇空清單 → 只印 `合計 0`（exit 0）。
- **D-12:** 錯誤訊息文字用繁體中文（與規格範例語言一致）。

### 資料格式與解析

- **D-13:** `expenses.json` 內容為 JSON 陣列，元素 `{"id": int, "amount": int, "category": str}`；寫檔用 `json.dump(..., indent=2, ensure_ascii=False)` 讓中文可讀。
- **D-14:** CLI 用 `argparse` subparsers（`add` / `list` / `total` / `rm`）；`add` 取 `<金額> <分類>` 兩個位置參數，`rm` 取 `<id>` 一個位置參數。
- **D-15:** 金額驗證：解析為 `int`，須 `> 0`；`0`、負數、非數字皆拒絕（stderr + exit 1）。分類驗證：`strip()` 後非空字串，否則拒絕。`rm` 的 id 不存在於清單時拒絕。

### Claude's Discretion

使用者明確授權「你決定就好」。上述 D-01~D-15 皆為 Claude 依慣例拍板；planner 若發現更好的等價做法可微調，但**輸出格式、exit code、id 語意、測試隔離**這四類為硬約束，不得偏離（否則 pytest 對不上）。

</decisions>

<canonical_refs>

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求與規格

- `.planning/REQUIREMENTS.md` — v1 需求（CMD/DATA/VAL/TEST 共 12 項）與 out-of-scope 邊界
- `.planning/PROJECT.md` — 專案核心價值、約束（零依賴、JSON 持久化、完工=pytest 全綠）
- `.planning/ROADMAP.md` §Phase 1 — 五條 Success Criteria（實作必須逐條滿足）
- `REQUIREMENTS.md`（repo 根目錄）— 使用者原始人類可讀規格，含四指令輸出格式範例

無其他外部 ADR / spec 文件。

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- 無 —— greenfield 專案，尚無任何 `.py` 檔或既有元件可重用。

### Established Patterns

- 無既有 code pattern。唯一約束來自規格：單檔主程式 + 單檔測試、標準庫、JSON 持久化。

### Integration Points

- 無外部系統整合。程式唯一 I/O 邊界為本機 `expenses.json` 檔案（讀/寫）。

</code_context>

<specifics>
## Specific Ideas

- 輸出格式範例（來自規格，測試必須精確比對）：
  - `list`：`[1] 120 食物`（`[id] amount category`，空格分隔）
  - `total`：每分類一行 `食物 120`，最後 `合計 170`
- 完工唯一信號：`pytest test_expense.py` 全綠。

</specifics>

<deferred>
## Deferred Ideas

None — 討論全程守在 phase scope 內，使用者未提出額外能力。規格已明訂「不多做」，無 v2 範圍。

</deferred>

---

*Phase: 1-Expense CLI*
*Context gathered: 2026-07-03*
