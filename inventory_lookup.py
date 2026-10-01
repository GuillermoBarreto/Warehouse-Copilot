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


def load_inventory(path=INVENTORY_PATH):
    """Load the item list from the sample inventory JSON file."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["items"]


def find_item(items, query):
    """Return the item matching a SKU (case-insensitive), or the first item
    whose name contains the query. Returns None when nothing matches."""
    q = query.strip().lower()
    if not q:
        return None
    for item in items:
        if item["sku"].lower() == q:
            return item
    for item in items:
        if q in item["name"].lower():
            return item
    return None


def main(argv):
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
    print(f"{item['name']} ({item['sku']})")
    print(f"Location: {item['location']}")
    # The sample data includes an out-of-stock item (quantity 0); surface that
    # explicitly instead of printing a bare zero.
    stock = "Out of stock" if item["quantity"] == 0 else f"{item['quantity']} in stock"
    print(f"Available quantity: {stock}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
