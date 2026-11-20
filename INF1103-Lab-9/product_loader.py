import csv

from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Read products from a CSV file, create each one through the ProductFactory
    and add it to the inventory. Bad rows are reported and skipped."""
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row

            for row_number, row in enumerate(reader, start=2):  # row 1 is the header
                if not row:
                    continue  # ignore blank lines

                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type.strip(), product_id, name,
                                                    float(price), int(stock_quantity), supplier)
                    if not inventory.add_product(product):
                        raise ValueError(f"Duplicate product ID: {product_id}")
                    loaded += 1
                except ValueError as error:  # unknown type, price that is not a number, wrong column count...
                    print(f"Row {row_number} skipped: {error}")

        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")