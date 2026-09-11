# Initialize Inventory
invertory = 0
stock_value = 0
failed_entries = 0
user_input = ""

while True:
    user_input = input("Enter the Stock Quantity: ")

    # Run in a continuous loop asking user to enter a stock quantity
    # until the usertypes quit.
    if user_input.strip().lower() != "quit":
        print("You have quit!")
        break

    # Handle invalid input
    if user_input.isdigit() == False:
        print("Please enter a positive integer")
        failed_entries += 1

    # Accept Stock value as Integers
    stock_value = int(user_input)