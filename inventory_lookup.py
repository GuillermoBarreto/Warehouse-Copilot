"""Small inventory lookup prototype for the Warehouse-Copilot milestone.

Reads inventory.sample.json and prints the storage location and available
quantity for a product SKU or name, or a clear message when nothing matches.

Usage:
    python inventory_lookup.py <SKU or product name>
"""

import json
import sys
from pathlib import Path

INVENTORY_PATH = Path(__file__).with_name("inventory.sample.json")


def load_inventory(path=None):
    """Load the item list from the sample inventory JSON file.

    ``path`` defaults to the JSON next to this script; taking it as a
    parameter (instead of a bound default) keeps the lookup testable.
    """
    if path is None:
        path = INVENTORY_PATH
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["items"]


def find_all_items(items, query):
    """Return every item matching a SKU (case-insensitive) or whose name
    contains the query. SKU matches come first, then name matches."""
    q = query.strip().lower()
    if not q:
        return []
    sku_hits = [item for item in items if str(item.get("sku", "")).lower() == q]
    name_hits = [
        item for item in items
        if q in str(item.get("name", "")).lower() and item not in sku_hits
    ]
    return sku_hits + name_hits


def find_item(items, query):
    """Return the first item matching a SKU (case-insensitive) or whose name
    contains the query. Returns None when nothing matches."""
    matches = find_all_items(items, query)
    return matches[0] if matches else None


def format_item(item):
    """Render one item's location and quantity without crashing on missing
    or malformed fields (hand-edited JSON happens)."""
    name = item.get("name") or "Unnamed item"
    sku = item.get("sku") or "unknown SKU"
    location = item.get("location") or "unknown location"
    quantity = item.get("quantity")
    if quantity == 0:
        stock = "Out of stock"
    elif isinstance(quantity, bool) or not isinstance(quantity, (int, float)):
        stock = "quantity unknown"
    else:
        stock = f"{quantity} in stock"
    return f"{name} ({sku})\nLocation: {location}\nAvailable quantity: {stock}"


def main(argv):
    """Look up one item by SKU or name and print its location and quantity."""
    if len(argv) != 2:
        print("Usage: python inventory_lookup.py <SKU or product name>")
        return 2
    try:
        items = load_inventory()
    except FileNotFoundError:
        print(f"Inventory file not found: {INVENTORY_PATH}. Place inventory.sample.json next to this script.")
        return 2
    except (json.JSONDecodeError, KeyError) as exc:
        print(f"Could not read the inventory data: {exc}")
        return 2
    item = find_item(items, argv[1])
    if item is None:
        print(f"Item not found: {argv[1]!r}. Check the SKU and try again.")
        return 1
    # The sample data includes an out-of-stock item (quantity 0); surface that
    # explicitly instead of printing a bare zero.
    print(format_item(item))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
