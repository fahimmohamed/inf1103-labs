import os

# Initialize Inventory
inventory = 0
stock_value = 0
failed_entries = 0
deliveries_processed = 0
total_tax = 0.0
user_input = ""
product_name = ""
filename = "inventory.txt"

transaction_history = [] 
next_id = 1001

# Find the exact folder path where this script file lives
script_directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_directory, "inventory.txt")


# Loads inventory upon start up
def load_inventory():
    if not os.path.exists(filename):
        print("Inventory does not exist")
        return 0, [], 1001 
    else:
        print("Inventory exists!")

    with open(filename, "r") as file:
        lines = file.read().splitlines()

    if not lines:
        print("Inventory is empty")
        return 0, [], 1001
    else:
        print("Inventory is not empty!")

    total_inventory = int(lines[0].strip())
    current_next_id = 1001

    inventory_history = []
    for line in lines[1:]:
        if line.strip():
            parts = line.split(",")
            if len(parts) >= 3:
                item_id = int(parts[0].strip())
                item_name = parts[1].strip()
                item_qty = int(parts[2].strip())
                
                # Append the list row to our master history list
                inventory_history.append([item_id, item_name, item_qty])
                
                if item_id >= current_next_id:
                    current_next_id = item_id + 1

    return total_inventory, inventory_history, current_next_id


# Save inventory
def save_inventory(total_units, history_list):
    with open(filename, "w") as file:
        file.write(f"{total_units}\n")
        for order in history_list:
            file.write(f"{order[0]}, {order[1]}, {order[2]}\n")

    print("Any changes to inventory.txt have been saved.")

    
# Handles prompt
def get_valid_input(product_name, current_id):
    while True:
        user_input = input("Enter the Stock Quantity or type 'quit': ").strip()
        
        if user_input.lower() == "quit":
            return "quit"
        
        if not user_input.isdigit():
            print("Please enter a positive integer")
            return "invalid"
            
        stock_value = int(user_input)
        
        if stock_value < 0:
            print("Please enter a positive number")
            return "invalid"

        print(f"\nNew Order added: \n{current_id}, {product_name}, {stock_value}")
        print(f"Orders added to inventory successfully!\n")
        return stock_value


# Calculate new total
def process_delivery(current_total, new_value):
    return current_total + new_value


# Returns tax
def calculate_tax(amount):
    return amount * 0.1


# Final summary
def generate_report(total_units, total_deliveries, failed_attempts, delivery_tax, history_list):
    print("\n--- Final Audit Report ---")
    print(f"Total Units in Inventory: {total_units}")
    print(f"Total deliveries processed: {total_deliveries}")
    print(f"Number of Failed Entries: {failed_attempts}")
    print(f"Total tax: {delivery_tax:.2f}")
    print(f"Transaction History:")
    for order in history_list:
        print(f"{order[0]}, {order[1]}, {order[2]}")
    return



# Main loop
inventory, transaction_history, next_id = load_inventory()

deliveries_processed = len(transaction_history)
total_tax = 0.0

for order in transaction_history:
    total_tax += calculate_tax(order[2])

print("Current record: \n")
if not transaction_history:
    print("(No previous database records found - starting fresh)")
else:
    for order in transaction_history:
        print(f"ID: {order[0]} | Product: {order[1]} | Quantity: {order[2]}")
    print("\n")

while True:
    product_name = input("Enter the Product Name: ").strip()

    if product_name.lower() == "quit":
        print("\nYou have quit\n")
        break

    result = get_valid_input(product_name, next_id)
    if result == "quit":
        print("\nYou have quit\n")
        break

    if result == "invalid":
        failed_entries += 1
        continue

    stock_value = result
    transaction_history.append([next_id, product_name, stock_value])
    inventory = process_delivery(inventory, stock_value)
    
    # Calculate the tax for this delivery
    delivery_tax = calculate_tax(stock_value)
    total_tax += delivery_tax
    
    deliveries_processed += 1
    next_id += 1

save_inventory(inventory, transaction_history)

generate_report(inventory, deliveries_processed, failed_entries, total_tax, transaction_history)
