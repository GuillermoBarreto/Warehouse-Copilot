# Warehouse-Copilot

An early-stage warehouse assistant project.

## Project status

This repository currently contains documentation and a license. There is no
runnable application or installation process yet.

## Proposed first milestone

Build a small inventory lookup prototype:

- Accept a product SKU or name.
- Display the matching item's storage location and available quantity.
- Show a clear message when an item cannot be found.

Before implementation, define a sample inventory format and choose the application
stack. Use sample data for the prototype so it can be tried without connecting to
a live warehouse system.

## Sample data format

`inventory.sample.json` holds the prototype data. Each item is one object with
exactly these fields:

| Field      | Type    | Description                                  |
|------------|---------|----------------------------------------------|
| `sku`      | string  | Unique product identifier (e.g. `WH-1001`)   |
| `name`     | string  | Human-readable product name                  |
| `location` | string  | Storage location, e.g. `Aisle A, Bin 12`     |
| `quantity` | integer | Units on hand; `0` means out of stock        |

Lookup rule for the prototype: match on `sku` (case-insensitive) or on a
case-insensitive substring of `name`. When nothing matches, show a clear
"item not found" message instead of an empty result.

## Contributing ideas

Open an issue describing the warehouse task, an example input, and the expected
result. Include any constraints the prototype should account for.
