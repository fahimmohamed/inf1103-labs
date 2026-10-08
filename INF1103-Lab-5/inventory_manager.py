import os
import json

invalid_input_counter = 0

inventory = [
    {"product_id": "P001", "product_name": "Laptop", "product_price": 1200.00,
     "current_stock": 15, "transactions": [15]},
    {"product_id": "P002", "product_name": "Mouse", "product_price": 25.50,
     "current_stock": 40, "transactions": [40]},
    {"product_id": "P003", "product_name": "Keyboard", "product_price": 45.00,
     "current_stock": 25, "transactions": [25]},
]

script_directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_directory, "inventory.txt")

def load_inventory():
    try:
        with open(filename, "r") as file:
            is_content = file.read()

            if not is_content.strip():
                raise ValueError("File is empty")

            inventory = json.loads(is_content)

    except FileNotFoundError:
        print(f"{filename} does not exist. Creating now...")

    except (ValueError, json.JSONDecodeError):
        print(f"{filename} exists but has no data.")
    return

def save_inventory():
    return

def get_valid_input(prompt, cast):
    while True:
        try:
            value = cast(input(prompt.strip()))
        except ValueError:
            print("Invalid input, please enter only numbers 1-6")
            invalid_input_counter += 1
            continue
        
        if value < 1:
            print("Input cannot be 0 or negative, please enter only numbers 1-6")

        return value

def calculate_tax():
    return

def generate_report():
    total_stock = sum(product["current_stock]"] for product in inventory)
    print(f'''
========================================
            INVENTORY REPORT
Total products: {len(inventory)}
Total units in stock: {total_stock}
Invalid inputs entered: {invalid_input_counter}
========================================
''')
    return

def add_product():
    print("Add New Product")
    print("------------------------------------------------")
    product_id = input("Product ID: ").strip().upper()
 
    if not product_id:
        print("Product ID cannot be empty.")
        invalid_input_count += 1
        return
 
    if find_by_id(product_id):
        print(f"Product {product_id} already exists.")
        invalid_input_count += 1
        return
 
    product_name = input("Product Name: ").strip()
    product_price = get_valid_input("Price: ", float)
    current_stock = get_valid_input("Stock Quantity: ", int)
 
    inventory.append({"product_id": product_id, "product_name": product_name, "product_price": product_price, "current_stock": current_stock, "transactions": [current_stock]})
    print("\n***** Product added successfully! *****")
    return

def find_by_id(product_id):
    for product in inventory:
        if product["product_id"].lower() == product_id.lower():
            return product
    return None

def update_stock():
    return

def search_product():
    return

def current_inventory():
    print("Current Inventory")
    print("------------------------------------------------")
    for product in inventory:
        print(f"ID: {product['product_id']} | Name: {product['product_name']} | Price: {product['product_price']:.2f} | Stock: {product['current_stock']}")
    print("------------------------------------------------")
    return


# Main Loop

print('''
========================================
INVENTORY MANAGEMENT SYSTEM
========================================''')

while True:
    print("""
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
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
            break

        case _:
            print("***** Please enter a valid option from 1-6 *****")
            print("*****    No Alphabets or symbols please    *****")


print("""
Thank you for using Inventory Management System.
Program terminated.
""")

