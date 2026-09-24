# Initialize Inventory
inventory = 0
stock_value = 0
failed_entries = 0
deliveries_processed = 0
total_tax = 0
user_input = ""
filename = "inventory.txt"
transaction_history = []

import os

#Loads inventory upon start up
def load_inventory():
    
    if not os.path.exists(filename):
        print("Inventory does not exist")
        return 0, []

    with open(filename, "r") as file:
        lines = file.read().splitlines()

    if not lines:
        print("Inventory is empty")
        return 0, []

    total_inventory = int(lines[0].strip())

    inventory_history = []
    for line in lines[1:]:
        if line.strip():
            inventory_history.append(int(line))

    return total_inventory, inventory_history



    
#Handles prompt
def get_valid_input():
    #Run in a continuous loop
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

        print(f"Stocks processed: {stock_value}")
        return stock_value

#Calculate new total
def process_delivery(current_total, new_value):
    return current_total + new_value

#Returns tax
def calculate_tax(amount):
    return amount * 0.1

#Final summary
def generate_report(total_units, total_deliveries, failed_attempts, delivery_tax, transaction_history):
    print("\n--- Final Audit Report ---")
    print(f"Total Units in Inventory: {total_units}")
    print(f"Total deliveries processed: {total_deliveries}")
    print(f"Number of Failed Entries: {failed_attempts}")
    print(f"Total tax: {delivery_tax}")
    print(f"Transaction History: {transaction_history}")

    return

#Main loop

inventory, transaction_history = load_inventory()

deliveries_processed = len(transaction_history)
total_tax = sum(transaction_history) * 0.1

while True:
    result = get_valid_input()
    if result == "quit":
        print("You have quit")
        break

    if result == "invalid":
        failed_entries += 1
        continue

    stock_value = result
    
    # Process the delivery total using our function
    inventory = process_delivery(inventory, stock_value)
    
    # Calculate the tax for this delivery
    delivery_tax = calculate_tax(stock_value)
    total_tax += delivery_tax
    
    # Update our successful delivery counter
    deliveries_processed += 1



generate_report(inventory, deliveries_processed, failed_entries, total_tax, transaction_history)