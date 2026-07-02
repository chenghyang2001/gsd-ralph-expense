# expense-cli

## What This Is

一個單檔 Python CLI 記帳器，供使用者在終端機新增／列出／加總／刪除支出。設計上刻意極小、零第三方依賴，可交由 Ralph 自主迴圈無人值守實作到測試全綠。

## Core Value

四個記帳指令（add / list / total / rm）都正確運作、且 pytest 全綠 —— 若其他一切都失敗，這件事必須成立。

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

(None yet — ship to validate)

### Active

<!-- Current scope. Building toward these. -->

- [ ] `add <金額> <分類>`：新增支出，id 自動遞增，金額限正整數
- [ ] `list`：列出全部，格式 `[1] 120 食物`
- [ ] `total`：依分類加總並印總計，格式 `食物 120` / `交通 50` / `合計 170`
- [ ] `rm <id>`：刪除指定支出
- [ ] 錯誤處理：無效 id、非正整數金額、空分類皆拒絕並 exit code 1；資料檔不存在視為空清單
- [ ] pytest 測試涵蓋四指令 + 邊界（空清單、無效 id、非法金額）

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- 第三方套件 — 規格要求零依賴，只用標準庫（argparse / json / pathlib / sys）
- 多幣別／小數金額 — 規格限定金額為正整數
- 編輯既有支出 — 規格只有 add / list / total / rm 四個指令
- 資料庫（SQLite 等） — 規格指定用 JSON 檔 `expenses.json` 持久化
- 使用者認證、日期欄位、預算警示等額外功能 — 明確不在 scope 內，「不多做」

## Context

- 執行環境：Windows 10，Python 3（Windows Store 版），套件安裝用 `python -m pip`
- 這是一個 Ralph 自主執行的示範標的：規格刻意鎖死、範圍極窄，讓自主迴圈能跑到明確的完工訊號（pytest 全綠）而不失控
- 完整、自足的原始規格已存在於 repo 根目錄 `REQUIREMENTS.md`，本專案的 `.planning/REQUIREMENTS.md` 是其 GSD 格式化版本

## Constraints

- **Tech stack**: Python 3 標準庫，零第三方依賴 — 規格明訂，保持可攜與極簡
- **Persistence**: JSON 檔 `expenses.json`，放程式同目錄 — 規格指定
- **檔案結構**: 只有 `expense.py`（主程式）+ `test_expense.py`（測試） — 規格指定
- **完工定義**: `pytest test_expense.py` 全綠 — 唯一驗收信號

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
| ---------- | ----------- | --------- |
| 只用標準庫、零依賴 | 規格要求，且降低 Ralph 執行環境變數 | — Pending |
| JSON 檔持久化而非 DB | 規格指定，單檔可攜、無需安裝 | — Pending |
| 完工信號綁定 pytest 全綠 | 給自主迴圈明確、可自動判定的終止條件 | — Pending |
| 跳過 GSD 研究/計畫檢查/驗證 agent | 範圍極小且技術選型已定，測試本身即驗證 | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):

1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):

1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-07-03 after initialization*
