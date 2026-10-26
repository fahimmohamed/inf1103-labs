import os
import json
import math

from product import Product
from inventory import Inventory

invalid_input_counter = 0
tax_rate = 0.10

inventory = Inventory()
new_products = []  # Product objects added this session (used for the tax calculation)

script_directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_directory, "inventory.json")


# ==================================================
#               File handling
# ==================================================

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

        for product_data in data:
            if not loaded_inventory.add_products(Product.from_dict(product_data)):
                raise ValueError("Duplicate product ID")

        for product in loaded_inventory.get_products():
            inventory.add_products(product)

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


def calculate_tax(amount):
    # tax = amount x tax rate (10%), rounded to cents
    return round(amount * tax_rate, 2)


# ==================================================
#               Menu options
# ==================================================

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

    if inventory.search_product(product_id):
        print(f"Product {product_id} already exists.")
        invalid_input_counter += 1
        return

    name = input("Product Name: ").strip()

    while not name:
        print("Product name cannot be empty.")
        invalid_input_counter += 1
        name = input("Product Name: ").strip()

    price = get_valid_input("Price: ", float)
    stock = get_valid_input("Stock Quantity: ", int)

    product = Product(product_id, name, price, stock)
    inventory.add_products(product)
    new_products.append(product)  # remembered for this session's tax calculation
    print("\n***** Product added successfully! *****")


#Option 3
def update_stock():
    global invalid_input_counter

    print("Update Stock")
    product = inventory.search_product(input("Enter Product ID: ").strip())

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
    new_price = round(get_valid_input("New Price: ", float, product.get_price()), 2)

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
    product = inventory.search_product(input("Enter Product ID: ").strip())

    if not product:
        print("Product not found.")
        invalid_input_counter += 1
        return

    print("Product Found")
    print("-" * 48)
    product.display_information(detailed=True)
    print("-" * 48)


#Option 6 (report shown on exit)
def generate_report():
    new_products_value = sum(product.get_value() for product in new_products)
    tax_amount = calculate_tax(new_products_value)

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
6. Exit
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
                    print("Saving inventory before exit...")
                    save_inventory(inventory, show_filename=False)
                    generate_report()
                    break

                case _:
                    invalid_input_counter += 1
                    print("***** Please enter a valid option from 1-6 *****")
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