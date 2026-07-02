<!-- GSD:project-start source:PROJECT.md -->
## Project

**expense-cli**

一個單檔 Python CLI 記帳器，供使用者在終端機新增／列出／加總／刪除支出。設計上刻意極小、零第三方依賴，可交由 Ralph 自主迴圈無人值守實作到測試全綠。

**Core Value:** 四個記帳指令（add / list / total / rm）都正確運作、且 pytest 全綠 —— 若其他一切都失敗，這件事必須成立。

### Constraints

- **Tech stack**: Python 3 標準庫，零第三方依賴 — 規格明訂，保持可攜與極簡
- **Persistence**: JSON 檔 `expenses.json`，放程式同目錄 — 規格指定
- **檔案結構**: 只有 `expense.py`（主程式）+ `test_expense.py`（測試） — 規格指定
- **完工定義**: `pytest test_expense.py` 全綠 — 唯一驗收信號
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
