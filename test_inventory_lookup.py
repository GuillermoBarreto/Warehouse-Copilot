"""Tests for inventory_lookup."""

import json

import pytest

import inventory_lookup as il

ITEMS = [
    {"sku": "WH-1001", "name": "Work Gloves", "location": "Aisle A, Bin 12", "quantity": 42},
    {"sku": "WH-1002", "name": "Safety Goggles", "location": "Aisle B, Bin 3", "quantity": 0},
    {"sku": "WH-1003", "name": "Work Boots", "location": "Aisle A, Bin 14", "quantity": 7},
]


def test_find_item_matches_sku_case_insensitively():
    assert il.find_item(ITEMS, "wh-1001")["name"] == "Work Gloves"


def test_find_item_matches_name_substring():
    assert il.find_item(ITEMS, "goggles")["sku"] == "WH-1002"


def test_find_item_returns_none_without_match():
    assert il.find_item(ITEMS, "forklift") is None
    assert il.find_item(ITEMS, "   ") is None


def test_find_all_items_returns_every_name_match_in_order():
    matches = il.find_all_items(ITEMS, "work")
    assert [m["sku"] for m in matches] == ["WH-1001", "WH-1003"]


def test_find_all_items_lists_sku_matches_before_name_matches():
    items = ITEMS + [{"sku": "work", "name": "Workbench", "location": "X", "quantity": 1}]
    matches = il.find_all_items(items, "work")
    assert matches[0]["sku"] == "work"
    assert len(matches) == 3  # no duplicates


def test_format_item_handles_missing_fields():
    out = il.format_item({"name": "Mystery Box"})
    assert "Mystery Box" in out
    assert "unknown SKU" in out
    assert "unknown location" in out
    assert "quantity unknown" in out


def test_format_item_marks_zero_quantity_out_of_stock():
    assert "Out of stock" in il.format_item(ITEMS[1])


def test_load_inventory_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        il.load_inventory(tmp_path / "missing.json")


def test_load_inventory_reads_items(tmp_path):
    path = tmp_path / "inv.json"
    path.write_text(json.dumps({"items": ITEMS}), encoding="utf-8")
    assert il.load_inventory(path) == ITEMS


def test_main_usage_error(capsys):
    assert il.main(["inventory_lookup.py"]) == 2
    assert "Usage" in capsys.readouterr().out


def test_main_missing_inventory_file(capsys, tmp_path, monkeypatch):
    monkeypatch.setattr(il, "INVENTORY_PATH", tmp_path / "missing.json")
    assert il.main(["inventory_lookup.py", "WH-1001"]) == 2
    assert "not found" in capsys.readouterr().out


def test_main_item_not_found(capsys, monkeypatch):
    monkeypatch.setattr(il, "load_inventory", lambda path=None: ITEMS)
    assert il.main(["inventory_lookup.py", "forklift"]) == 1
    assert "not found" in capsys.readouterr().out


def test_main_prints_match(capsys, monkeypatch):
    monkeypatch.setattr(il, "load_inventory", lambda path=None: ITEMS)
    assert il.main(["inventory_lookup.py", "WH-1001"]) == 0
    out = capsys.readouterr().out
    assert "Work Gloves" in out and "Aisle A, Bin 12" in out


def test_main_all_lists_every_match(capsys, monkeypatch):
    monkeypatch.setattr(il, "load_inventory", lambda path=None: ITEMS)
    assert il.main(["inventory_lookup.py", "--all", "work"]) == 0
    out = capsys.readouterr().out
    assert "Work Gloves" in out and "Work Boots" in out
