# Requirements: expense-cli

**Defined:** 2026-07-03
**Core Value:** 四個記帳指令（add / list / total / rm）都正確運作、且 pytest 全綠

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Commands

- [ ] **CMD-01**: 使用者可用 `add <金額> <分類>` 新增支出，id 自動遞增
- [ ] **CMD-02**: 使用者可用 `list` 列出全部支出，格式 `[1] 120 食物`
- [ ] **CMD-03**: 使用者可用 `total` 依分類加總並印總計，格式 `食物 120` / `合計 170`
- [ ] **CMD-04**: 使用者可用 `rm <id>` 刪除指定支出

### Data

- [ ] **DATA-01**: 支出以 `{ "id": int, "amount": int, "category": str }` 結構存入 JSON 檔 `expenses.json`
- [ ] **DATA-02**: `expenses.json` 不存在時視為空清單，程式不崩潰

### Validation

- [ ] **VAL-01**: `add` 金額非正整數（0、負數、非數字）時拒絕並報錯、exit code 1
- [ ] **VAL-02**: `add` 分類為空字串時拒絕並報錯、exit code 1
- [ ] **VAL-03**: `rm` 傳入無效 id 時印錯誤訊息、exit code 1

### Testing

- [ ] **TEST-01**: `pytest test_expense.py` 涵蓋 add / list / total / rm 正常路徑
- [ ] **TEST-02**: 測試涵蓋邊界：空清單、無效 id、非法金額
- [ ] **TEST-03**: `pytest test_expense.py` 全綠（完工定義）

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

(None — 規格明訂「不多做」，無 v2 範圍)

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --------- | -------- |
| 第三方套件依賴 | 規格要求零依賴，只用標準庫 |
| 多幣別／小數金額 | 規格限定金額為正整數 |
| 編輯既有支出 | 規格只有 add / list / total / rm 四指令 |
| SQLite / 資料庫 | 規格指定 JSON 檔持久化 |
| 使用者認證、日期欄位、預算警示 | 明確不在 scope 內 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
| ------------- | ------- | -------- |
| CMD-01 | Phase 1 | Pending |
| CMD-02 | Phase 1 | Pending |
| CMD-03 | Phase 1 | Pending |
| CMD-04 | Phase 1 | Pending |
| DATA-01 | Phase 1 | Pending |
| DATA-02 | Phase 1 | Pending |
| VAL-01 | Phase 1 | Pending |
| VAL-02 | Phase 1 | Pending |
| VAL-03 | Phase 1 | Pending |
| TEST-01 | Phase 1 | Pending |
| TEST-02 | Phase 1 | Pending |
| TEST-03 | Phase 1 | Pending |

**Coverage:**

- v1 requirements: 12 total
- Mapped to phases: 12 ✓
- Unmapped: 0

---
*Requirements defined: 2026-07-03*
*Last updated: 2026-07-03 after roadmap creation*
