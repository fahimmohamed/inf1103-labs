import math

class Product:
    # def __init__(self, product_id, product_name, product_price, current_stock):
    #     self.__product_id = product_id.strip()
    #     self.__product_name = product_name
    #     self.__product_price = product_price
    #     self.current_stock = current_stock
    #     self.transactions = [current_stock]
    #     pass

    def __init__(self, product_id, name, price, stock, transactions=None):
        if not isinstance(product_id, str) or not product_id.strip() or len(product_id.split()) > 1:
            raise ValueError("Product ID must be text without spaces.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")

        self.__product_id = product_id.strip()
        self.__name = name.strip()
        self.__price = self.__valid_price(price)
        self.__stock = self.__valid_stock(stock)

        if transactions is None:
            self.__transactions = [self.__stock]  # starting stock is the first transaction
        else:
            if not isinstance(transactions, list) or not all(
                    isinstance(t, int) and not isinstance(t, bool) for t in transactions):
                raise ValueError("Transactions must be a list of whole numbers.")
            self.__transactions = list(transactions)

    # ---------- private validation ----------

    def __valid_price(self, price):
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError("Price must be a number.")
        if not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        return round(float(price), 2) + 0  # + 0 turns -0.0 into 0.0

    def __valid_stock(self, stock):
        if isinstance(stock, bool) or not isinstance(stock, int):
            raise ValueError("Stock must be a whole number.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        return stock

    


product1 = Product("P001", "Keyboard", 45.90, 10)
print(product1)