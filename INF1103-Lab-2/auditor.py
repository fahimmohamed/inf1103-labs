# Initialize Inventory
inventory = 0
stock_value = 0
failed_entries = 0
user_input = ""

while True:
    user_input = input("Enter the Stock Quantity or type 'quit': ")

    # Run in a continuous loop asking user to enter a stock quantity
    # until the usertypes quit.
    if user_input.strip().lower() == "quit":
        print("You have quit!")
        break

    # Handle invalid input
    # No negative numbers
    if user_input.isdigit() == False:
        print("Please enter a positive integer")
        failed_entries += 1
        continue

    # Accept Stock value as Integers
    stock_value = int(user_input)

    # Keep a running total of the inventory
    inventory += stock_value
    print(f"Successfully processed {stock_value} units. (Current Total: {inventory})")

    # Trigger overstock alert
    if inventory > 500:
        print("ALERT: Stock Value exceeded 500 units.")
        break

# Reporting
print(f"Total Units: {inventory}")
print(f"Number of Failed Entries: {failed_entries}")