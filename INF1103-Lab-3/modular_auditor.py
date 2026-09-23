# Initialize Inventory
inventory = 0
stock_value = 0
failed_entries = 0
deliveries_processed = 0
total_tax = 0
user_input = ""

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
def generate_report(total_units, total_deliveries, failed_attempts, delivery_tax):
    print("\n--- Final Audit Report ---")
    print(f"Total Units in Inventory: {total_units}")
    print(f"Total deliveries processed: {total_deliveries}")
    print(f"Number of Failed Entries: {failed_attempts}")
    print(f"Total tax: {delivery_tax}")
    return

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

generate_report(inventory, deliveries_processed, failed_entries, total_tax)