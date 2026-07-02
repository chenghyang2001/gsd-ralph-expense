# Demo 實錄：GSD 規劃 → VPS → Ralph 自主執行（expense-cli）

> 「本機用 GSD 把需求壓成可執行計劃 → 丟到 VPS 用 Ralph 無人值守迴圈蓋到測試全綠」的**第二次演練**。
> 專案：`chenghyang2001/gsd-ralph-expense` ｜ 完成日：2026-07-03
> 成果：Ralph 4 loop / 3 次 API call / 22,646 tokens（走 Claude Max，$0）→ **pytest 24 passed**，`exit_reason: plan_complete`。
> 前作：`gsd-ralph-todo`（todo-cli，2026-07-02）——本次驗證「App 換題材、流程零改動」。

---

## 0. 這次驗證什麼

同一條流水線換一個 App：從 todo-cli（add/list/done/rm）換成 expense-cli（add/list/total/rm），
其中 `total` 多了一個「依分類加總」的聚合邏輯 + 更嚴的輸入驗證。**目的：證明流程本身可複用，換的只是題材，不是複雜度。**

| 框架 | 角色 | 在哪跑 | 產出 |
|------|------|--------|------|
| **GSD** | 規劃大腦：模糊需求 → 機器可讀 `PLAN.md` | 本機 PC | `.planning/`（PROJECT / ROADMAP / PLAN / CONTEXT）|
| **Ralph**（frankbria/ralph-claude-code） | 執行手：讀計劃無人值守迴圈實作到測試全綠 | VPS | `expense.py` / `test_expense.py` + 自動 commit |

**核心洞見（同前作）**：GSD 的 `PLAN.md` 跟「誰施工」解耦，所以跳過 `/gsd-execute-phase`，把施工圖搬去 VPS 交給 Ralph。

---

## 1. 本機半段（GSD 規劃）

1. `~/workspace/gsd-ralph-expense` 開獨立 repo + `git init` + 手寫 `REQUIREMENTS.md`（4 指令、scope 鎖死）。
2. **另開一個 session**（cwd = 專案目錄）跑 `/gsd-new-project` → `/gsd-plan-phase 1`。
   - **為何另開 session**：GSD 狀態存專案內 `.planning/`（cwd 相對），主教學 session 的 cwd 鎖在別的 repo，直接跑會把 `.planning/` 汙染到錯的地方。
3. GSD 產出：`PROJECT.md` / `ROADMAP.md`（1 phase）/ `01-01-PLAN.md`（**3 個 TDD task**）/ `01-CONTEXT.md`（15 條決策 D-01~D-15）。
   - 本次 GSD 版本用 `01-CONTEXT.md` + 「Walking Skeleton Note」內嵌於 PLAN，**未另開 `SKELETON.md`**（前作 todo 有獨立 SKELETON.md）。
4. commit 根目錄 `REQUIREMENTS.md`（PLAN 用 `@REQUIREMENTS.md` 引用它，Ralph 要讀）+ `.gitignore` → `gh repo create --public --push`。
   - **坑**：`gh repo create --source=. --push` 推的是本地預設分支 `master`（不是 `main`），repo default branch 也成 `master`——不影響 Ralph（clone 預設分支即可）。

## 2. VPS 半段（Ralph 自主執行）

前作已在 VPS 一次性裝好：`ralph`（全域指令）、`pytest 9.1.1`、`claude 2.1.146`、`ANTHROPIC_API_KEY` 未設（Max $0）。**本次省掉 install.sh，直接：**

1. **clone**：`git clone https://.../gsd-ralph-expense.git ~/gsd-ralph-expense`（https 匿名 = 驗證 repo 真 public）。
2. **搭骨架**：`cd ~/gsd-ralph-expense && ralph-enable-ci` → 生成 `.ralph/{PROMPT,AGENT,fix_plan}.md` + `.ralphrc`（Node 預設）。
3. **接合縫翻譯**（唯一手工活）：
   - 本機 Write → `scp` 三檔：`.ralph/PROMPT.md`（目標+硬約束+`EXIT_SIGNAL` 退出塊）、`.ralph/fix_plan.md`（3 task 扁平勾選，翻自 GSD PLAN）、`.ralph/AGENT.md`（build/test/run）。
   - `.ralphrc`：直接 `cp` 前作 todo 的（已含正確 Python `ALLOWED_TOOLS`）再 `sed` 改 `PROJECT_NAME`——比重寫省事。
   - `cp .planning/{01-01-PLAN,01-CONTEXT}.md + REQUIREMENTS.md → .ralph/specs/`。
4. **dry-run**：`ralph --dry-run` 確認 config 載入、讀得到 PROMPT（不呼叫 API）。
5. **正式跑**：`tmux new-session -d -s ralph "... ralph --verbose > .ralph/logs/run.log 2>&1"`。

### Ralph 執行軌跡

```
Loop #1  test: 寫失敗 happy-path 測試（e02f1ea，TDD RED）
Loop #2  feat: walking skeleton load/save/add/list + argparse（b64b9fa，Task1 GREEN）
Loop #3  feat: compute_totals + remove_expense + 驗證 + total/rm CLI（c5bae04，全綠）
Loop #4  偵測 fix_plan 全勾 + pytest 綠 → graceful exit: plan_complete
```

- **pytest：24 passed in 0.54s**
- API：3 次呼叫 / 22,646 tokens / **走 Max = $0**
- 產物：`expense.py`（120 行 stdlib only：argparse/json/pathlib/sys/os）、`test_expense.py`（232 行，tmp_path 隔離）

## 3. 帶走的重點

1. **流程可複用得到驗證**：VPS 半段的 SOP 跟前作一字不差，只換了檔名與 4 個指令的語意。**接合縫翻譯是唯一隨題材變動的手工活。**
2. **規劃越硬、自主執行越準**（再次印證）：Ralph 忠實實作 15 條決策——`isinstance(amount, bool)` 擋掉布林當金額、`compute_totals` 保序 dict（D-03 首見順序）、`EXPENSE_DB` 路徑注入（D-07）——全是 GSD 事先鎖死、Ralph 沒自由發揮之處。
3. **token 隨 scope 線性成長、不失控**：todo（11 test）12.6k → expense（24 test）22.6k，多一個聚合 + 更嚴驗證約翻倍，仍 4 loop 一次收斂，無 scope creep。
4. **一次性設置能攤提**：VPS 上 ralph/pytest/auth 是耐久的，第二個專案起省掉整個 install 半段——長命 VPS 當 Ralph 執行器的規模效益。
5. 沿用前作踩坑：`ANTHROPIC_API_KEY` 未設走 Max、`ALLOWED_TOOLS` 要含 `Bash(python3 *)/Bash(pytest *)`、detached 用 tmux 不用 `ssh 'cmd &'`、`.md`/config 用本機 Write+scp 避 heredoc 引號地獄。
6. **跨平台編碼發現（done-gate 的隱藏假設）**：Ralph 在 VPS（Linux）24/24 全綠，但同一份碼在 Windows 本機 3 個 CLI 測試炸——`expense.py` 用 `print()` 輸出中文走**系統預設編碼**（Linux=UTF-8 過 / Windows=cp950，`食物` 的 `0xad` 是 Big5 碼），subprocess 測試以 UTF-8 解碼子程序輸出 → `UnicodeDecodeError`。**不是 Ralph 缺陷**（done-gate 只定義在 VPS，GSD PLAN 未要求跨平台），但正是「編碼防禦」的活教材：`print`/subprocess 不可依賴系統預設編碼（修法 `sys.stdout.reconfigure(encoding="utf-8")` 或測試端帶 `encoding="utf-8"`+`PYTHONUTF8=1`）。**教訓：done-gate 綠 = 在「執行環境」綠，不等於跨平台綠——自主執行的驗收判準要把目標平台講死。**

## 4. 怎麼重現（精簡）

```bash
# 本機
cd ~/workspace && mkdir gsd-ralph-expense && cd $_ && git init   # + 寫 REQUIREMENTS.md
# 另開 session（cwd=此目錄）：/gsd-new-project → /gsd-plan-phase 1
git add .gitignore REQUIREMENTS.md && git commit -m ...
gh repo create chenghyang2001/gsd-ralph-expense --public --source=. --push

# VPS（ralph/pytest/auth 前作已備）
git clone https://github.com/chenghyang2001/gsd-ralph-expense.git ~/gsd-ralph-expense
cd ~/gsd-ralph-expense && ralph-enable-ci
# scp 客製 .ralph/{PROMPT,fix_plan,AGENT}.md；cp 前作 .ralphrc + sed 改名；cp GSD PLAN/CONTEXT/REQUIREMENTS → .ralph/specs/
ralph --dry-run
tmux new-session -d -s ralph "cd ~/gsd-ralph-expense && export PATH=\$HOME/.local/bin:\$PATH && ralph --verbose > .ralph/logs/run.log 2>&1"
# 監控 .ralph/status.json 的 exit_reason=plan_complete；完成後 git push origin master
```
