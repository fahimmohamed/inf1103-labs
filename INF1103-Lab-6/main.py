import os
import json
import math

from product import Product
from inventory import Inventory

invalid_input_counter = 0
tax_rate = 0.10

inventory = Inventory()
new_products = []

script_directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_directory, "inventory.json")


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