# Phase 1: Expense CLI - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-03
**Phase:** 1-Expense CLI
**Areas discussed:** ID 配置策略, total 分類排序, 測試隔離, 輸出串流與空狀態

---

## ID 配置策略

| Option | Description | Selected |
|--------|-------------|----------|
| max(現有)+1，不重用 | id 單調遞增，rm 後 add 仍取 max+1 | ✓ |
| count+1 / 序號重排 | id 依清單長度或重新編號 | |

**User's choice:** Claude 依慣例拍板（使用者授權「你決定」）
**Notes:** 選 max+1 不重用，因 id 穩定、無碰撞、測試斷言明確。

---

## total 分類排序

| Option | Description | Selected |
| -------- | ------------- | ---------- |
| 首次出現順序 | dict 保序，符合規格範例 | ✓ |
| 字母序 | 分類名排序 | |
| 金額高到低 | 依加總金額排序 | |

**User's choice:** Claude 依慣例拍板
**Notes:** 首次出現順序最貼合規格範例 `食物 120 / 交通 50 / 合計 170`；合計固定末行。

---

## 測試隔離

| Option | Description | Selected |
|--------|-------------|----------|
| path 參數 + EXPENSE_DB env + tmp_path | 核心函式吃 path，CLI 用 env 覆蓋，測試用 tmp_path 注入 | ✓ |
| 固定路徑，測試 chdir | 寫死程式同目錄，測試切工作目錄 | |

**User's choice:** Claude 依慣例拍板
**Notes:** 可注入路徑讓 pytest 完全不污染真實檔、測試間互不干擾、CI 安全。

---

## 輸出串流與空狀態

| Option | Description | Selected |
|--------|-------------|----------|
| 錯誤→stderr+exit1；list 空印空；total 空印「合計 0」 | stream 分流 + 明確空狀態 | ✓ |
| 全部走 stdout / 空清單印提示訊息 | 較口語但難精確斷言 | |

**User's choice:** Claude 依慣例拍板
**Notes:** stderr/stdout 分流是慣例；空狀態行為固定、可測。錯誤訊息用繁中。

---

## Claude's Discretion

使用者明確表示「你決定就好，用慣例定好，直接進 plan-phase」。全部四個灰區 + 隱含項（argparse subparsers、大小寫敏感、JSON 格式、金額/分類驗證）皆由 Claude 依慣例拍板，詳見 CONTEXT.md D-01~D-15。

## Deferred Ideas

None — 討論守在 phase scope 內，無延後項目。
