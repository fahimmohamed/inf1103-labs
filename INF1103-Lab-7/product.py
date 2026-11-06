import math


class Product:
    """Represents and manages ONE product (single responsibility)."""

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

    @staticmethod
    def _check_number(value, label):
        """Protected helper: subclasses reuse it to validate their own numbers."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{label} must be a number.")
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{label} must be a non-negative number.")
        return float(value) + 0  # + 0 turns -0.0 into 0.0

    def __valid_price(self, price):
        return round(self._check_number(price, "Price"), 2)

    def __valid_stock(self, stock):
        if isinstance(stock, bool) or not isinstance(stock, int):
            raise ValueError("Stock must be a whole number.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        return stock

    # ---------- getters (read-only access) ----------

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_transactions(self):
        return list(self.__transactions)  # a copy, so outside code cannot change the history

    def get_value(self):
        return self.__price * self.__stock

    # ---------- methods that change state ----------

    def update_stock(self, quantity):
        """Set the stock to `quantity` and record the difference as a transaction."""
        quantity = self.__valid_stock(quantity)
        change = quantity - self.__stock

        if change != 0:
            self.__transactions.append(change)

        self.__stock = quantity
        return change

    def set_price(self, price):
        self.__price = self.__valid_price(price)

    # ---------- display / conversion ----------

    def display_information(self, detailed=False):
        if detailed:
            print(f"ID: {self.__product_id}")
            print(f"Name: {self.__name}")
            print(f"Price: ${self.__price:.2f}")
            print(f"Stock: {self.__stock}")
        else:
            print(f"ID: {self.__product_id} | Name: {self.__name} | "
                  f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "product_name": self.__name,
            "product_price": self.__price,
            "current_stock": self.__stock,
            "transactions": list(self.__transactions),
        }

    @staticmethod
    def from_dict(data):
        return Product(data["product_id"], data["product_name"], data["product_price"],
                       data["current_stock"], data["transactions"])


class PhysicalProduct(Product):
    """A product that is stored and shipped. A PhysicalProduct IS-A Product."""

    def __init__(self, product_id, name, price, stock, weight, transactions=None):
        super().__init__(product_id, name, price, stock, transactions)  # reuse Product's constructor
        self.__weight = self._check_number(weight, "Weight")

    def get_weight(self):
        return self.__weight

    def display_information(self, detailed=False):
        super().display_information(detailed)  # common information comes from Product
        if detailed:
            print("Type: Physical")
            print(f"Weight: {self.__weight:.2f} kg")
        else:
            print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")


class DigitalProduct(Product):
    """A product delivered by download. A DigitalProduct IS-A Product."""

    def __init__(self, product_id, name, price, stock, download_size, transactions=None):
        super().__init__(product_id, name, price, stock, transactions)  # reuse Product's constructor
        self.__download_size = self._check_number(download_size, "Download size")

    def get_download_size(self):
        return self.__download_size

    def display_information(self, detailed=False):
        super().display_information(detailed)  # common information comes from Product
        if detailed:
            print("Type: Digital")
            print(f"Download size: {self.__download_size:.2f} MB")
        else:
            print(f"    Type: Digital | Download size: {self.__download_size:.2f} MB")