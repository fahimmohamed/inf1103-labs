"""Lab 8 tests. Run with: python test_lab8.py"""

from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from product import Product


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

def test_composition() -> None:
    print("=" * 48)
    print("TEST: Composition (Order <*>-- OrderLine)")
    print("Predict first (4.3): write your prediction BEFORE running")
    print("=" * 48)

    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.2)
    antivirus = DigitalProduct("P003", "Antivirus Software", 49.99, 100, supplier, 250.0)

    # the Order creates its OrderLines from a Product and a quantity
    order_1 = Order("O001")
    order_1.add_order_line(laptop, 2)
    order_1.add_order_line(antivirus, 3)
    order_1.display_information()

    # the SAME Product in a different Order
    order_2 = Order("O002")
    order_2.add_order_line(laptop, 1)
    order_2.display_information()

    line_in_order_1 = order_1.get_order_lines()[0]
    line_in_order_2 = order_2.get_order_lines()[0]
    print(f"Same OrderLine object in both orders: {line_in_order_1 is line_in_order_2}")
    print(f"id of the two OrderLines: {id(line_in_order_1)}, {id(line_in_order_2)}")
    print(f"Same Product object in both lines: {line_in_order_1.get_product() is line_in_order_2.get_product()}")
    print(f"id of the Product in each line: {id(line_in_order_1.get_product())}, {id(line_in_order_2.get_product())}")

    # lines are removed THROUGH the Order
    print(f"Remove P003 from O001: {order_1.remove_order_line('P003')}")
    print(f"Remove P999 from O001: {order_1.remove_order_line('P999')}")
    order_1.display_information()

    # invalid lines are rejected by the Order / OrderLine
    for product, quantity in [(laptop, 1), (antivirus, 0), (antivirus, 2.5)]:
        try:
            order_1.add_order_line(product, quantity)
            print(f"FAILED: {product.get_product_id()} x {quantity} was accepted")
        except ValueError as error:
            print(f"Rejected as expected: {error}")

    # the Order is removed: its OrderLines go with it, the Product does not
    del order_1
    print("After 'del order_1':")
    print(f"Laptop still exists: {laptop.get_name()} has {laptop.get_stock()} in stock")
    print(f"O002 total is still: ${order_2.calculate_total():.2f}")
    print()

def show_product_details(product: Product) -> None:
    # accepts ANY Product: it never checks which subclass it was given
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp() -> None:
    print("=" * 48)
    print("TEST: Liskov Substitution (subclasses used as Product)")
    print("=" * 48)

    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")
    keyboard = PhysicalProduct("P005", "Keyboard", 21.00, 5, supplier, 0.8)
    office = DigitalProduct("P004", "Office 365", 138.00, 50, supplier, 380.6)

    # 1. the SAME function works with both subclasses, unchanged
    show_product_details(keyboard)
    show_product_details(office)

    # 2. both can be managed by an Inventory through normal operations
    inventory = Inventory()
    print(f"Add keyboard: {inventory.add_product(keyboard)} | Add office: {inventory.add_product(office)}")
    print(f"Find P004 returns office: {inventory.find_product('P004') is office}")
    print(f"Total stock: {inventory.get_total_stock()}")

    # 3. the expectation set by Product.update_stock() holds for BOTH subclasses:
    #    it sets the new stock, records the change, and returns the change as an int
    for product in inventory.get_products():
        change = product.update_stock(product.get_stock() + 10)
        print(f"{product.get_product_id()}: change returned = {change} ({type(change).__name__}), "
              f"stock = {product.get_stock()}, transactions = {product.get_transactions()}")
    print()


def test_polymorphism() -> None:
    print("=" * 48)
    print("TEST: Polymorphism (one loop over the Product collection)")
    print("Predict first (7.2): write your prediction BEFORE running")
    print("=" * 48)

    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.2))
    inventory.add_product(DigitalProduct("P003", "Antivirus Software", 49.99, 100, supplier, 250.0))

    # ONE loop, no isinstance(): each object runs its own version of the methods
    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())
        print()

if __name__ == "__main__":
    test_supplier()
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()