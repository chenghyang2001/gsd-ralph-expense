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
    expenses = load_expenses(path)
    next_id = max((e["id"] for e in expenses), default=0) + 1
    record = {"id": next_id, "amount": amount, "category": category}
    expenses.append(record)
    save_expenses(path, expenses)
    return record


def list_expenses(path):
    return load_expenses(path)


def _resolve_path():
    env = os.environ.get("EXPENSE_DB")
    if env:
        return env
    return str(Path(__file__).resolve().parent / "expenses.json")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="expense")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("amount")
    p_add.add_argument("category")

    sub.add_parser("list")

    args = parser.parse_args(argv)
    path = _resolve_path()

    if args.cmd == "add":
        amount = int(args.amount)
        add_expense(path, amount, args.category)
        return 0
    if args.cmd == "list":
        for e in list_expenses(path):
            print(f"[{e['id']}] {e['amount']} {e['category']}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
