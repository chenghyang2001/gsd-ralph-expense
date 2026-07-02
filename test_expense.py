from expense import add_expense, load_expenses


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
