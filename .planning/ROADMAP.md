# Roadmap: expense-cli

## Overview

單檔 Python CLI 記帳器，從零到完工只需交付一個緊密耦合的垂直切片：四個指令（add / list / total / rm）、JSON 檔持久化、輸入驗證與 pytest 測試。因為所有需求彼此依存（指令需要持久化與驗證，測試即完工訊號），且範圍刻意鎖死、零第三方依賴，整個專案構成單一交付邊界。完工的唯一信號是 `pytest test_expense.py` 全綠。

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Expense CLI** - 交付 add/list/total/rm 四指令、JSON 持久化、輸入驗證，pytest 全綠

## Phase Details

### Phase 1: Expense CLI

**Goal**: 使用者可在終端機用四個指令管理支出，資料以 JSON 檔持久化、輸入受驗證保護，且完整測試套件全綠
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: CMD-01, CMD-02, CMD-03, CMD-04, DATA-01, DATA-02, VAL-01, VAL-02, VAL-03, TEST-01, TEST-02, TEST-03
**Success Criteria** (what must be TRUE):

  1. 使用者可執行 `add <金額> <分類>` 新增支出（id 自動遞增），`list` 以 `[1] 120 食物` 格式列出全部
  2. 使用者可執行 `total` 看到依分類加總與合計（`食物 120` / `合計 170`），並用 `rm <id>` 刪除指定支出
  3. 支出以 `{id, amount, category}` 結構存入 `expenses.json`；檔案不存在時視為空清單、程式不崩潰
  4. 非正整數金額、空分類、無效 rm id 皆被拒絕並印錯誤訊息、exit code 1
  5. `pytest test_expense.py` 涵蓋四指令正常路徑與邊界（空清單、無效 id、非法金額）且全綠
**Plans**: TBD

Plans:

- [ ] 01-01: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Expense CLI | 0/TBD | Not started | - |
