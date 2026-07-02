# Fix Plan — expense-cli（來源：.ralph/specs/ 的 GSD PLAN 01-01 + 01-CONTEXT）

## Priority 1：Walking Skeleton（失敗測試 + add + list）

- [x] Task 1（TDD RED）：寫「會失敗」的 test_expense.py — 用 pytest `tmp_path` 隔離，`from expense import add_expense, load_expenses`；happy path：`add_expense(db, 120, "食物")` 回傳 id==1、amount==120、category=="食物"，再 `load_expenses(db)` 應含該筆。此時 expense.py 尚無實作 → 必須紅燈（D-01/D-06/D-08）
- [ ] Task 2（轉綠）：實作 expense.py — load_expenses/save_expenses（path 參數；不存在回 []；json.dump indent=2 ensure_ascii=False，D-13）、add_expense（id=max+1，D-01/D-02）、list_expenses；argparse 子命令 add/list（add 取兩位置參數 金額、分類；D-14）；CLI 路徑 = 環境變數 EXPENSE_DB 優先否則 `Path(__file__).resolve().parent/"expenses.json"`（D-07）；list 格式 `[{id}] {amount} {category}`，空清單不印、exit 0（D-10）。Task 1 轉綠

## Priority 2：補完（total + rm + 驗證 + 邊界）

- [ ] Task 3（全綠）：補 compute_totals（保序 dict 累加，同分類合併、大小寫敏感，D-03/D-05；回傳 (保序 dict, 合計)）與 remove_expense（id 不存在 raise ValueError，VAL-03）；add_expense 加驗證（金額非正整數 / 分類 strip 後空 → raise ValueError，VAL-01/02/D-15）；main 補 total / rm 子命令（rm 取一 id，D-14），以 try/except ValueError 包核心呼叫 → 捕獲印繁中訊息到 stderr + return 1（D-09/D-12）；total 印每分類 `{分類} {加總}` 再 `合計 {總和}`，空清單只印 `合計 0`（D-04/D-11）。補齊 test_expense.py 涵蓋四指令正常路徑 + 邊界（空清單 list/total、rm 無效 id、add 非法金額、add 空分類、rm 後 add 的 id 仍 max+1）。`python3 -m pytest test_expense.py -q` 全綠

## 硬約束（不可違反）

- expense.py 只 import argparse/json/pathlib/sys/os；pytest 只當測試執行器，不被 expense.py import
- 恰好 4 指令：add/list/total/rm，不可加第 5 個指令或旗標
- 核心函式吃 path 參數（D-06）；CLI 路徑 = EXPENSE_DB 優先否則程式同目錄 expenses.json（D-07）；測試用 tmp_path 絕不碰真實檔（D-08）
- 錯誤訊息繁體中文、走 stderr、exit 1；正常輸出走 stdout（D-09/D-12）
- done-gate = `python3 -m pytest test_expense.py -q` 全綠

## Completed

- [x] Project enabled for Ralph（ralph-enable-ci）

## Discovered
<!-- Ralph 自己把過程中發現的任務補在這 -->
