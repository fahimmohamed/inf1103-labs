import os
import json
import math

from product import Product
from product_factory import ProductFactory
from supplier import Supplier
from inventory import Inventory
from order import Order

invalid_input_counter = 0
tax_rate = 0.10

inventory = Inventory()
new_products: list[Product] = []  # Product objects added this session (used for the tax calculation)
suppliers: dict[str, Supplier] = {}  # supplier ID (upper case) -> Supplier object, so products can share one Supplier
orders: list[Order] = []  # Order objects created this session (not saved to the JSON file)

script_directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_directory, "inventory.json")




# ==================================================
#               File handling
# ==================================================

def get_supplier_from_dict(supplier_data, known_suppliers):
    # reuse the Supplier object if this ID was already seen, so products share ONE Supplier
    supplier_id = supplier_data["supplier_id"]

    if not isinstance(supplier_id, str):  # e.g. 101 instead of "101" would crash .strip()
        raise ValueError("Supplier ID must be text.")

    supplier_id = supplier_id.strip().upper()

    if supplier_id not in known_suppliers:
        known_suppliers[supplier_id] = Supplier.from_dict(supplier_data)
    return known_suppliers[supplier_id]

def create_product_from_dict(data, known_suppliers):
    supplier = get_supplier_from_dict(data["supplier"], known_suppliers)  # KeyError if "supplier" is missing
    return ProductFactory.create_from_dict(data, supplier)  # ValueError if the type is unknown

def load_inventory(inventory):
    try:
        # utf-8-sig also reads files saved with a BOM (e.g. by Windows Notepad)
        with open(filename, "r", encoding="utf-8-sig") as file:
            is_content = file.read()

        print("inventory.json found")

        if not is_content.strip():
            raise ValueError("File is empty")

        data = json.loads(is_content)

        if not isinstance(data, list):
            raise ValueError("JSON is not a list of products")

        loaded_inventory = Inventory()  # filled first, so a bad file never half-loads
        loaded_suppliers = {}

        for product_data in data:
            if not loaded_inventory.add_product(create_product_from_dict(product_data, loaded_suppliers)):
                raise ValueError("Duplicate product ID")

        for product in loaded_inventory.get_products():
            inventory.add_product(product)
        suppliers.update(loaded_suppliers)

        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print(f"{filename} does not exist. Creating now...")
        initialize_file()

    except (ValueError, TypeError, KeyError):
        print("inventory.json is empty or does not contain valid inventory data.")
        print("Initializing it now...")
        initialize_file()

    except OSError as error:
        print(f"Could not read inventory.json ({error}). Starting with an empty inventory.")


def initialize_file():
    # keep a copy of a file we could not use, so no data is lost silently
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        os.replace(filename, filename + ".bak")
        print("The old file was kept as inventory.json.bak")

    with open(filename, "w", encoding="utf-8") as file:
        file.write("[]")


#Option 5
def save_inventory(inventory, show_filename=True):
    temp_filename = filename + ".tmp"
    data = [product.to_dict() for product in inventory.get_products()]

    try:
        with open(temp_filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        os.replace(temp_filename, filename)  # old file is replaced only after a complete write
    except OSError as error:
        print(f"Could not save inventory ({error}).")
        return False

    if show_filename:
        print("Inventory saved successfully to inventory.json.")
    else:
        print("Inventory saved successfully.")
    return True

#Accept valid input
def get_valid_input(prompt, cast, default=None):
    global invalid_input_counter

    while True:
        user_input = input(prompt).strip()

        if default is not None and user_input == "":
            return default  # Enter keeps the current value

        try:
            if "_" in user_input:  # Python accepts 1_000, which we do not want
                raise ValueError
            value = cast(user_input)
        except ValueError:
            print("Invalid input, please try again.")
            invalid_input_counter += 1
            continue

        if not math.isfinite(value):  # rejects nan, inf and numbers like 1e400
            print("Invalid input, please enter a real number.")
            invalid_input_counter += 1
            continue

        if value < 0:
            print("Value cannot be negative.")
            invalid_input_counter += 1
            continue

        return value + 0  # turns -0.0 into 0.0


#Ask until a positive amount is entered (e.g. a price)
def get_positive_float(prompt: str, default: float | None = None) -> float:
    global invalid_input_counter

    while True:
        user_input = input(prompt).strip()

        if default is not None and user_input == "":
            return default  # Enter keeps the current value

        try:
            if "_" in user_input:  # Python accepts 1_000, which we do not want
                raise ValueError
            value = float(user_input)  # raises ValueError for text like "abc"
            if not math.isfinite(value):  # nan / inf are not real amounts
                raise ValueError
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
            invalid_input_counter += 1
            continue

        if round(value, 2) <= 0:  # amounts are kept to cents, so 0.001 counts as 0
            print("Please enter a number greater than zero.")
            invalid_input_counter += 1
            continue

        return value


def calculate_tax(amount):
    # tax = amount x tax rate (10%), rounded to cents
    return round(amount * tax_rate, 2)


# ==================================================
#               Menu options
# ==================================================

def choose_product_type():
    global invalid_input_counter

    while True:
        print("Product Type:")
        print("1. Physical")
        print("2. Digital")
        choice = input("Choose type (1-2): ").strip()

        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"

        print("Please enter 1 or 2.")
        invalid_input_counter += 1

def choose_supplier():
    global invalid_input_counter

    if suppliers:
        print("Existing suppliers:")
        for supplier in suppliers.values():
            supplier.display_information()

    while True:
        supplier_id = input("Supplier ID: ").strip().upper()

        if not supplier_id or len(supplier_id.split()) > 1:
            print("Supplier ID cannot be empty or contain spaces.")
            invalid_input_counter += 1
            continue

        if supplier_id in suppliers:
            print(f"Using existing supplier {suppliers[supplier_id].get_name()}.")
            return suppliers[supplier_id]  # the same Supplier object is shared

        print("New supplier, please enter the details.")
        supplier_name = input("Supplier Name: ").strip()

        while not supplier_name:
            print("Supplier name cannot be empty.")
            invalid_input_counter += 1
            supplier_name = input("Supplier Name: ").strip()

        while True:
            contact_email = input("Supplier Email: ").strip()
            try:
                supplier = Supplier(supplier_id, supplier_name, contact_email)
                break
            except ValueError as error:  # the Supplier class decides what a valid email is
                print(error)
                invalid_input_counter += 1

        suppliers[supplier_id] = supplier
        return supplier

#Option 2
def add_products():
    global invalid_input_counter
    print("Add New Product")
    print("------------------------------------------------")
    product_id = input("Product ID: ").strip().upper()

    if not product_id:
        print("Product ID cannot be empty.")
        invalid_input_counter += 1
        return

    if len(product_id.split()) > 1:
        print("Product ID cannot contain spaces.")
        invalid_input_counter += 1
        return

    if inventory.find_product(product_id):
        print(f"Product {product_id} already exists.")
        invalid_input_counter += 1
        return

    name = input("Product Name: ").strip()

    while not name:
        print("Product name cannot be empty.")
        invalid_input_counter += 1
        name = input("Product Name: ").strip()

    supplier = choose_supplier()
    product_type = choose_product_type()

    price = get_positive_float("Price: ")
    stock = get_valid_input("Stock Quantity: ", int)

    if product_type == "physical":
        size = get_valid_input("Weight (kg): ", float)
    else:
        size = get_valid_input("Download Size (MB): ", float)

    product = ProductFactory.create(product_type, product_id, name, price, stock, supplier, size)
    inventory.add_product(product)
    new_products.append(product)  # remembered for this session's tax calculation
    print("\n***** Product added successfully! *****")


#Option 3
def update_stock():
    global invalid_input_counter

    print("Update Stock")
    product = inventory.find_product(input("Enter Product ID: ").strip())

    if not product:
        print("Product not found.")
        invalid_input_counter += 1
        return

    print("Product Found \n---------------------------")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    print(f"Current Price: ${product.get_price():.2f}")
    print("(Press Enter to keep a current value)")

    new_stock = get_valid_input("New Stock Quantity: ", int, product.get_stock())
    new_price = round(get_positive_float("New Price: ", product.get_price()), 2)

    if new_stock == product.get_stock() and new_price == product.get_price():
        print("No changes made.")
        return

    product.update_stock(new_stock)  # the Product decides how the change is applied
    product.set_price(new_price)
    print("Product updated successfully!")


#Option 4
def search_product():
    global invalid_input_counter

    print("Search Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())

    if not product:
        print("Product not found.")
        invalid_input_counter += 1
        return

    print("Product Found")
    print("-" * 48)
    product.display_information(detailed=True)
    print("-" * 48)


#Option 6
def create_order():
    global invalid_input_counter

    print("Create Order")
    print("-" * 48)
    order_id = input("Order ID: ").strip().upper()

    if not order_id or len(order_id.split()) > 1:
        print("Order ID cannot be empty or contain spaces.")
        invalid_input_counter += 1
        return

    for existing_order in orders:
        if existing_order.get_order_id() == order_id:
            print(f"Order {order_id} already exists.")
            invalid_input_counter += 1
            return

    order = Order(order_id)

    while True:
        print("\nEnter a Product ID to add, R to remove a line, or press Enter to finish.")
        product_id = input("Product ID: ").strip()

        if product_id == "":
            break

        if product_id.upper() == "R":
            removed = order.remove_order_line(input("Product ID to remove: "))  # removed THROUGH the Order
            if removed:
                print("Order line removed.")
            else:
                print("That product is not in this order.")
                invalid_input_counter += 1
            continue

        product = inventory.find_product(product_id)

        if not product:
            print("Product not found.")
            invalid_input_counter += 1
            continue

        quantity = get_valid_input("Quantity: ", int)

        try:
            order.add_order_line(product, quantity)  # the Order creates the OrderLine itself
            print(f"Added {quantity} x {product.get_name()}.")
        except ValueError as error:  # e.g. quantity 0 or product already in the order
            print(error)
            invalid_input_counter += 1

    if not order.get_order_lines():
        print("Order cancelled (no order lines).")
        return

    print()
    order.display_information()
    orders.append(order)
    print("\n***** Order created successfully! *****")


#Option 7 (report shown on exit)
def generate_report():
    new_products_value = sum(product.get_value() for product in new_products)
    tax_amount = calculate_tax(new_products_value)
    orders_value = sum(order.calculate_total() for order in orders)

    print(f'''
========================================
            INVENTORY REPORT
Total products: {inventory.get_product_count()}
Total units in stock: {inventory.get_total_stock()}
Invalid inputs entered: {invalid_input_counter}
----------------------------------------
New products this session: {len(new_products)}
Value of new products: ${new_products_value:.2f}
Tax on new products ({tax_rate:.0%}): ${tax_amount:.2f}
----------------------------------------
Orders created this session: {len(orders)}
Total value of orders: ${orders_value:.2f}
========================================
''')


# ==================================================
#               Main Loop
# ==================================================

def main():
    global invalid_input_counter

    print('''
========================================
INVENTORY MANAGEMENT SYSTEM
========================================''')

    load_inventory(inventory)  # Loads the inventory upon start up

    try:
        while True:
            print("""
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock or Price
4. Search Product
5. Save Inventory
6. Create Order
7. Exit
----------------------------\n""")

            main_menu_option = input("Enter option: ")
            print()
            match main_menu_option.strip():
                case "1":
                    inventory.display_all()

                case "2":
                    add_products()

                case "3":
                    update_stock()

                case "4":
                    search_product()

                case "5":
                    print("Saving inventory...")
                    save_inventory(inventory)

                case "6":
                    create_order()

                case "7":
                    print("Saving inventory before exit...")
                    save_inventory(inventory, show_filename=False)
                    generate_report()
                    break

                case _:
                    invalid_input_counter += 1
                    print("***** Please enter a valid option from 1-7 *****")
                    print("*****    No Alphabets or symbols please    *****")

    except (EOFError, KeyboardInterrupt):
        # Ctrl+C / Ctrl+D: save instead of losing the session's changes
        print("\n\nInput closed. Saving inventory before exit...")
        save_inventory(inventory, show_filename=False)
        generate_report()

    print("""
Thank you for using Inventory Management System.
Program terminated.
""")


if __name__ == "__main__":
    main()