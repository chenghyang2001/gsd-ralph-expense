# expense-cli 需求規格

> 給 GSD 規劃訪談與 Ralph 自主執行參照。**scope 就是這些，不多做**。

## 目標

一個單檔 Python CLI 記帳器，無人值守可由 Ralph 自主實作到測試全綠。

## 技術約束

- Python 3，只用標準庫（argparse / json / pathlib / sys），零第三方依賴
- 資料存 JSON 檔 `expenses.json`（放程式同目錄）

## 功能（就這 4 個，不多做）

| 指令 | 行為 |
| ------ | ------ |
| `add <金額> <分類>` | 新增支出，id 自動遞增，金額為正整數 |
| `list` | 列出全部，格式：`[1] 120 食物` |
| `total` | 依分類加總並印總計，格式：`食物 120` / `交通 50` / `合計 170` |
| `rm <id>` | 刪除支出 |

## 資料模型

```
expense = { "id": int, "amount": int, "category": str }
```

## 錯誤處理

- 無效 id（`rm`）→ 印錯誤訊息、exit code 1
- `add` 金額非正整數（0、負數、非數字）→ 拒絕並報錯、exit code 1
- `add` 分類空字串 → 拒絕並報錯、exit code 1
- `expenses.json` 不存在 → 視為空清單（不崩潰）

## 測試

- `pytest test_expense.py`，涵蓋 add / list / total / rm + 邊界（空清單、無效 id、非法金額）

## 檔案結構

- `expense.py`（主程式）
- `test_expense.py`（測試）

## 完工定義

**pytest 全綠**
