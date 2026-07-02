import argparse
import json
import os
import sys
from pathlib import Path


def load_expenses(path):
    p = Path(path)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(path, expenses):
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)


def add_expense(path, amount, category):
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("金額必須為正整數")
    if not isinstance(category, str) or category.strip() == "":
        raise ValueError("分類不可為空")
    expenses = load_expenses(path)
    next_id = max((e["id"] for e in expenses), default=0) + 1
    record = {"id": next_id, "amount": amount, "category": category}
    expenses.append(record)
    save_expenses(path, expenses)
    return record


def list_expenses(path):
    return load_expenses(path)


def compute_totals(path):
    totals = {}
    grand = 0
    for e in load_expenses(path):
        cat = e["category"]
        amt = e["amount"]
        totals[cat] = totals.get(cat, 0) + amt
        grand += amt
    return totals, grand


def remove_expense(path, expense_id):
    expenses = load_expenses(path)
    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            del expenses[i]
            save_expenses(path, expenses)
            return
    raise ValueError(f"找不到 id {expense_id}")


def _resolve_path():
    env = os.environ.get("EXPENSE_DB")
    if env:
        return env
    return str(Path(__file__).resolve().parent / "expenses.json")


def _parse_positive_int(raw):
    try:
        value = int(raw)
    except (TypeError, ValueError):
        raise ValueError("金額必須為正整數")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(prog="expense")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("amount")
    p_add.add_argument("category")

    sub.add_parser("list")
    sub.add_parser("total")

    p_rm = sub.add_parser("rm")
    p_rm.add_argument("id")

    args = parser.parse_args(argv)
    path = _resolve_path()

    try:
        if args.cmd == "add":
            amount = _parse_positive_int(args.amount)
            add_expense(path, amount, args.category)
            return 0
        if args.cmd == "list":
            for e in list_expenses(path):
                print(f"[{e['id']}] {e['amount']} {e['category']}")
            return 0
        if args.cmd == "total":
            totals, grand = compute_totals(path)
            for cat, amt in totals.items():
                print(f"{cat} {amt}")
            print(f"合計 {grand}")
            return 0
        if args.cmd == "rm":
            try:
                target_id = int(args.id)
            except (TypeError, ValueError):
                raise ValueError("id 必須為整數")
            remove_expense(path, target_id)
            return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
