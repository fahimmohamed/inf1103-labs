"""Lab 8 tests. Run with: python test_lab8.py"""

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


def test_supplier() -> None:
    print("=" * 48)
    print("TEST: Supplier")
    print("=" * 48)

    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")
    supplier.display_information()

    # invalid suppliers must be rejected
    for bad_values in [("", "Name", "a@b.com"), ("S 1", "Name", "a@b.com"),
                       ("S002", "  ", "a@b.com"), ("S003", "Name", "no-at-sign")]:
        try:
            Supplier(*bad_values)
            print(f"FAILED: {bad_values} was accepted")
        except ValueError as error:
            print(f"Rejected as expected: {error}")
    print()


def test_association() -> None:
    print("=" * 48)
    print("TEST: Association (Supplier -- Product)")
    print("Predict first (2.2): write your prediction BEFORE running")
    print("=" * 48)

    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.2)
    antivirus = DigitalProduct("P003", "Antivirus Software", 49.99, 100, supplier, 250.0)

    print("Supplier through each Product:")
    laptop.get_supplier().display_information()
    antivirus.get_supplier().display_information()

    print(f"Both products refer to the SAME Supplier object: {laptop.get_supplier() is antivirus.get_supplier()}")
    print(f"Supplier and Product are separate objects: {supplier is not laptop}")
    print(f"id(supplier) = {id(supplier)}, id(laptop) = {id(laptop)}, id(antivirus) = {id(antivirus)}")

    del supplier
    print("After 'del supplier':")
    laptop.get_supplier().display_information()
    antivirus.get_supplier().display_information()

    # a Product without a Supplier object must be rejected
    try:
        PhysicalProduct("P009", "Cable", 5.00, 10, "TechWorld", 0.2)
        print("FAILED: a supplier name (text) was accepted instead of a Supplier object")
    except ValueError as error:
        print(f"Rejected as expected: {error}")
    print()


def test_aggregation() -> None:
    print("=" * 48)
    print("TEST: Aggregation (Inventory <>-- Product)")
    print("Predict first (3.2): write your prediction BEFORE running")
    print("=" * 48)

    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")

    # 1. the Product exists BEFORE any Inventory
    mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, supplier, 0.1)
    inventory_a = Inventory()
    inventory_b = Inventory()

    # 2. add it to Inventory A
    inventory_a.add_product(mouse)
    print(f"In A: {inventory_a.find_product('P002') is not None} | In B: {inventory_b.find_product('P002') is not None}")

    # 3. remove it from Inventory A, then use the Product
    removed = inventory_a.remove_product("P002")
    print(f"remove_product returned the same object: {removed is mouse}")
    print(f"In A: {inventory_a.find_product('P002') is not None} | Products left in A: {inventory_a.get_product_count()}")
    print("Using the Product after removal:")
    mouse.update_stock(35)
    mouse.display_information()

    # 4. add the SAME object to Inventory B
    inventory_b.add_product(mouse)
    print(f"In B: {inventory_b.find_product('P002') is not None} | Same object in B: {inventory_b.find_product('P002') is mouse}")

    # 5. empty Inventory B: the Product still exists
    inventory_b.remove_product("P002")
    print(f"Products left in B: {inventory_b.get_product_count()}")
    print(f"Product still usable: {mouse.get_name()} has {mouse.get_stock()} in stock")

    # removing something that is not there
    print(f"Remove unknown ID returns: {inventory_b.remove_product('P999')}")
    print()


if __name__ == "__main__":
    test_supplier()
    test_association()
    test_aggregation()