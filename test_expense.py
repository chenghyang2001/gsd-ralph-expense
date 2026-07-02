import json
import subprocess
import sys

import pytest

from expense import (
    add_expense,
    compute_totals,
    list_expenses,
    load_expenses,
    remove_expense,
)

EXPENSE_PY = str(__import__("pathlib").Path(__file__).resolve().parent / "expense.py")


def _run(db, *args):
    return subprocess.run(
        [sys.executable, EXPENSE_PY, *args],
        capture_output=True,
        text=True,
        env={"EXPENSE_DB": str(db), "PATH": ""},
    )


# ---------- Task 1: walking skeleton happy path ----------


def test_add_expense_happy_path(tmp_path):
    db = tmp_path / "expenses.json"

    record = add_expense(str(db), 120, "食物")

    assert record["id"] == 1
    assert record["amount"] == 120
    assert record["category"] == "食物"

    stored = load_expenses(str(db))
    assert len(stored) == 1
    assert stored[0]["id"] == 1
    assert stored[0]["amount"] == 120
    assert stored[0]["category"] == "食物"


# ---------- core function coverage ----------


def test_load_missing_file_returns_empty(tmp_path):
    db = tmp_path / "nope.json"
    assert load_expenses(str(db)) == []


def test_add_expense_ids_are_monotonic(tmp_path):
    db = tmp_path / "expenses.json"
    r1 = add_expense(str(db), 120, "食物")
    r2 = add_expense(str(db), 50, "交通")
    assert r1["id"] == 1
    assert r2["id"] == 2


def test_save_uses_indent_and_utf8(tmp_path):
    db = tmp_path / "expenses.json"
    add_expense(str(db), 120, "食物")
    raw = db.read_text(encoding="utf-8")
    assert "食物" in raw  # ensure_ascii=False
    assert "\n" in raw    # indent=2 → multi-line JSON
    data = json.loads(raw)
    assert data == [{"id": 1, "amount": 120, "category": "食物"}]


def test_list_expenses_returns_records(tmp_path):
    db = tmp_path / "expenses.json"
    add_expense(str(db), 120, "食物")
    add_expense(str(db), 50, "交通")
    listed = list_expenses(str(db))
    assert [e["id"] for e in listed] == [1, 2]


def test_compute_totals_merges_and_preserves_order(tmp_path):
    db = tmp_path / "expenses.json"
    add_expense(str(db), 120, "食物")
    add_expense(str(db), 50, "交通")
    add_expense(str(db), 20, "食物")
    totals, grand = compute_totals(str(db))
    assert list(totals.items()) == [("食物", 140), ("交通", 50)]
    assert grand == 190


def test_compute_totals_case_sensitive(tmp_path):
    db = tmp_path / "expenses.json"
    add_expense(str(db), 100, "食物")
    add_expense(str(db), 30, "Food")
    totals, grand = compute_totals(str(db))
    assert list(totals.items()) == [("食物", 100), ("Food", 30)]
    assert grand == 130


def test_compute_totals_empty(tmp_path):
    db = tmp_path / "expenses.json"
    totals, grand = compute_totals(str(db))
    assert totals == {}
    assert grand == 0


def test_remove_expense_deletes_and_persists(tmp_path):
    db = tmp_path / "expenses.json"
    add_expense(str(db), 120, "食物")
    add_expense(str(db), 50, "交通")
    remove_expense(str(db), 1)
    remaining = load_expenses(str(db))
    assert [e["id"] for e in remaining] == [2]


def test_remove_expense_invalid_id_raises(tmp_path):
    db = tmp_path / "expenses.json"
    with pytest.raises(ValueError):
        remove_expense(str(db), 999)


def test_add_expense_rejects_non_positive_amount(tmp_path):
    db = tmp_path / "expenses.json"
    with pytest.raises(ValueError):
        add_expense(str(db), 0, "食物")
    with pytest.raises(ValueError):
        add_expense(str(db), -5, "食物")


def test_add_expense_rejects_empty_category(tmp_path):
    db = tmp_path / "expenses.json"
    with pytest.raises(ValueError):
        add_expense(str(db), 100, "")
    with pytest.raises(ValueError):
        add_expense(str(db), 100, "   ")


def test_id_not_backfilled_after_remove(tmp_path):
    # D-01/D-02: 新 id = max(現有 id)+1；不回填被刪掉的中低段 id。
    db = tmp_path / "expenses.json"
    add_expense(str(db), 120, "食物")   # id=1
    add_expense(str(db), 50, "交通")    # id=2
    remove_expense(str(db), 1)          # 刪除低段 id
    r3 = add_expense(str(db), 10, "娛樂")
    assert r3["id"] == 3                # 不回填 1，取 max(remaining)+1


# ---------- CLI subprocess coverage ----------


def test_cli_add_then_list_format(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "add", "120", "食物")
    assert r.returncode == 0
    r = _run(db, "list")
    assert r.returncode == 0
    assert r.stdout == "[1] 120 食物\n"


def test_cli_list_empty_prints_nothing(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "list")
    assert r.returncode == 0
    assert r.stdout == ""
    assert r.stderr == ""


def test_cli_total_format(tmp_path):
    db = tmp_path / "expenses.json"
    _run(db, "add", "120", "食物")
    _run(db, "add", "50", "交通")
    _run(db, "add", "20", "食物")
    r = _run(db, "total")
    assert r.returncode == 0
    assert r.stdout == "食物 140\n交通 50\n合計 190\n"


def test_cli_total_empty_prints_zero(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "total")
    assert r.returncode == 0
    assert r.stdout == "合計 0\n"


def test_cli_rm_success(tmp_path):
    db = tmp_path / "expenses.json"
    _run(db, "add", "120", "食物")
    r = _run(db, "rm", "1")
    assert r.returncode == 0
    assert load_expenses(str(db)) == []


def test_cli_add_invalid_amount_zero(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "add", "0", "食物")
    assert r.returncode == 1
    assert r.stdout == ""
    assert r.stderr != ""


def test_cli_add_invalid_amount_negative(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "add", "-5", "食物")
    assert r.returncode == 1
    assert r.stderr != ""


def test_cli_add_invalid_amount_non_numeric(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "add", "abc", "食物")
    assert r.returncode == 1
    assert r.stderr != ""


def test_cli_add_empty_category(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "add", "100", "")
    assert r.returncode == 1
    assert r.stderr != ""


def test_cli_rm_invalid_id_on_empty(tmp_path):
    db = tmp_path / "expenses.json"
    r = _run(db, "rm", "999")
    assert r.returncode == 1
    assert r.stderr != ""


def test_cli_missing_file_list_is_empty(tmp_path):
    db = tmp_path / "does_not_exist.json"
    r = _run(db, "list")
    assert r.returncode == 0
    assert r.stdout == ""
