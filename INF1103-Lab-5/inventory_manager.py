import os
import json



invalid_input_counter = 0

inventory = []
new_products = []

script_directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_directory, "inventory.json")

print("Current Working Directory:", os.getcwd())
print("Inventory File:", filename)

# ==================================================
#               File related functions
# ==================================================

def load_inventory():
    global inventory

    try:
        with open(filename, "r") as file:
            is_content = file.read()

        print("inventory.json found")

        if not is_content.strip():
            raise ValueError("File is empty")

        inventory = json.loads(is_content)

        if not isinstance(inventory, list):
            raise ValueError("JSON is not a list of products")
 
        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print(f"{filename} does not exist. Creating now...")
        initialize_file()

    except (ValueError, json.JSONDecodeError):
        print(f"{filename} exists but has no data.")
        print("Initializing it now...")
        initialize_file()

def initialize_file():
    global inventory
    inventory = []
 
    with open(filename, "w") as file:
        file.write("[]")

def save_inventory(show_filename=True):

    with open(filename, "w") as file:
        json.dump(inventory, file, indent=4)
 
    if show_filename:
        print("Inventory saved successfully to inventory.json.")
    else:
        print("Inventory saved successfully.")
    return

def current_inventory():
    global inventory
    if not inventory:
        print("No products found.")
        return
    print("Current Inventory")
    print("------------------------------------------------")
    for product in inventory:
        print(f"ID: {product['product_id']} | Name: {product['product_name']} | Price: {product['product_price']:.2f} | Stock: {product['current_stock']}")
    print("------------------------------------------------")
    return


# ==================================================
#               Input Validation functions
# ==================================================

def get_valid_input(prompt, cast, default=None):
    global invalid_input_counter
 
    while True:
        user_input = input(prompt).strip()
 
        if default is not None and user_input == "":
            return default  # Enter keeps the current value
 
        try:
            value = cast(user_input)
        except ValueError:
            print("Invalid input, please try again.")
            invalid_input_counter += 1
            continue
 
        if value < 0:
            print("Value cannot be negative.")
            invalid_input_counter += 1
            continue
 
        return value

# ==================================================
#               Report Generation functions
# ==================================================

def calculate_tax():
    total_tax = 0

    for product in new_products:
        total_tax += product["product_price"] * product["current_stock"] * 0.10

    return total_tax

def generate_report():
    global inventory

    total_tax = calculate_tax()
    total_stock = sum(product["current_stock"] for product in inventory)
    print(f'''
========================================
            INVENTORY REPORT
Total products: {len(inventory)}
Total units in stock: {total_stock}
Total Tax on new products: ${total_tax:.2f}
Invalid inputs entered: {invalid_input_counter}
========================================
''')
    return

# ==================================================
#               Product related functions
# ==================================================

def add_product():
    global invalid_input_counter
    print("Add New Product")
    print("------------------------------------------------")
    product_id = input("Product ID: ").strip().upper()
 
    if not product_id:
        print("Product ID cannot be empty.")
        invalid_input_counter += 1
        return
 
    if find_by_id(product_id):
        print(f"Product {product_id} already exists.")
        invalid_input_counter += 1
        return
 
    product_name = input("Product Name: ").strip()
    while not product_name:
        print("Product Name cannot be empty.")
        invalid_input_counter += 1
        product_name = input("Product Name: ").strip()

    existing_product = find_by_name(product_name)
    if existing_product:
        print(f"\nA product named '{product_name}' already exists (ID: {existing_product['product_id']}).")
        choice = input("Would you like to update its stock/price instead? (y/n): ").strip().lower()
        
        if choice in ['y', 'yes']:
            print()
            # Redirect directly to update_stock logic using the found product
            update_stock(existing_product)
            return
        else:
            print("Product addition cancelled.")
            return

    product_price = get_valid_input("Price: ", float)
    current_stock = get_valid_input("Stock Quantity: ", int)
 
    product = {"product_id": product_id, "product_name": product_name, "product_price": product_price, "current_stock": current_stock, "transactions": [current_stock]}

    inventory.append(product)
    new_products.append(product)
    print("\n***** Product added successfully! *****")
    return

def find_by_name(product_name):
    for product in inventory:
        if product["product_name"].lower() == product_name.lower():
            return product
    return None

def find_by_id(product_id):
    for product in inventory:
        if product["product_id"].lower() == product_id.lower():
            return product
    return None

def update_stock(product=None):
    global invalid_input_counter
 
    print("Update Stock")
    if product is None:
        product = find_by_id(
            input("Enter Product ID: ").strip().upper()
        )
 
    if not product:
        print("Product not found.")
        invalid_input_counter += 1
        return
 
    print("Product Found \n---------------------------")
    print(f"Name: {product['product_name']}")
    print(f"Current Stock: {product['current_stock']}")
    print(f"Current Price: ${product['product_price']:.2f}")
    print("(Press Enter to keep a current value)")
 
    new_stock = get_valid_input("New Stock Quantity: ", int, product["current_stock"])
    new_price = get_valid_input("New Price: ", float, product["product_price"])
 
    stock_change = new_stock - product["current_stock"]
 
    if stock_change == 0 and new_price == product["product_price"]:
        print("No changes made.")
        return
 
    if stock_change != 0:
        product["transactions"].append(stock_change)  # keep the history, not just the total
 
    product["current_stock"] = new_stock
    product["product_price"] = new_price
    if product not in new_products:
        new_products.append(product)

    print("Product updated successfully!")

def search_product():
    global invalid_input_counter
 
    print("Search Product")
    product = find_by_id(input("Enter Product ID: ").strip().upper())
 
    if not product:
        print("Product not found.")
        invalid_input_counter += 1
        return
 
    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['product_id']}")
    print(f"Name: {product['product_name']}")
    print(f"Price: ${product['product_price']:.2f}")
    print(f"Stock: {product['current_stock']}")
    print("-" * 48)
    return




# ==================================================
#               Main Loop
# ==================================================

print('''
========================================
INVENTORY MANAGEMENT SYSTEM
========================================''')

load_inventory() # Loads the inventory upon start up

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
            current_inventory()

        case "2":
            add_product()

        case "3":
            update_stock()

        case "4":
            search_product()

        case "5":
            print("Saving inventory...")
            save_inventory()

        case "6":
            print("Saving inventory before exit...")
            save_inventory(show_filename=False)
            generate_report()
            break

        case _:
            invalid_input_counter += 1
            print("***** Please enter a valid option from 1-6 *****")
            print("*****    No Alphabets or symbols please    *****")


print("""
Thank you for using Inventory Management System.
Program terminated.
""")
