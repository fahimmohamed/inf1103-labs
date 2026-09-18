# Initialize Inventory
inventory = 0
stock_value = 0
failed_entries = 0
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
            
        return stock_value

#Calculate new total
def process_delivery(current_total, new_value):
    return current_total + new_value

#Returns tax
def calculate_tax(amount):
    return amount * 0.1

#Final summary
def generate_report(total_units, failed_attempts):
    print("\n--- Final Audit Report ---")
    print(f"Total Units in Inventory: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    return