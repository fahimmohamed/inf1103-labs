import math
from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Represents and manages ONE product (single responsibility)."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, transactions: list[int] | None = None) -> None:
        if not isinstance(product_id, str) or not product_id.strip() or len(product_id.split()) > 1:
            raise ValueError("Product ID must be text without spaces.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if not isinstance(supplier, Supplier):
            raise ValueError("A product must have a Supplier object.")

        self.__product_id: str = product_id.strip()
        self.__name: str = name.strip()
        self.__price: float = self.__valid_price(price)
        self.__stock: int = self.__valid_stock(stock)
        self.__supplier: Supplier = supplier  # a reference only: the Supplier is not part of the Product

        self.__transactions: list[int]

        if transactions is None:
            self.__transactions = [self.__stock]  # starting stock is the first transaction
        else:
            if not isinstance(transactions, list) or not all(
                    isinstance(t, int) and not isinstance(t, bool) for t in transactions):
                raise ValueError("Transactions must be a list of whole numbers.")
            self.__transactions = list(transactions)

    # ---------- private validation ----------

    @staticmethod
    def _check_number(value: float, label: str) -> float:
        """Protected helper: subclasses reuse it to validate their own numbers."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{label} must be a number.")
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{label} must be a non-negative number.")
        return float(value) + 0  # + 0 turns -0.0 into 0.0

    def __valid_price(self, price: float) -> float:
        return round(self._check_number(price, "Price"), 2)

    def __valid_stock(self, stock: int) -> int:
        if isinstance(stock, bool) or not isinstance(stock, int):
            raise ValueError("Stock must be a whole number.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        return stock

    # ---------- getters (read-only access) ----------

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_transactions(self) -> list[int]:
        return list(self.__transactions)  # a copy, so outside code cannot change the history

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_value(self) -> float:
        return self.__price * self.__stock

    # ---------- methods that change state ----------

    def update_stock(self, quantity: int) -> int:
        """Set the stock to `quantity` and record the difference as a transaction."""
        quantity = self.__valid_stock(quantity)
        change = quantity - self.__stock

        if change != 0:
            self.__transactions.append(change)

        self.__stock = quantity
        return change

    def set_price(self, price: float) -> None:
        self.__price = self.__valid_price(price)

    # ---------- display / conversion ----------

    def display_information(self, detailed: bool = False) -> None:
        if detailed:
            print(f"ID: {self.__product_id}")
            print(f"Name: {self.__name}")
            print(f"Price: ${self.__price:.2f}")
            print(f"Stock: {self.__stock}")
            self.__supplier.display_information()  # the Product asks its Supplier to display itself
        else:
            print(f"ID: {self.__product_id} | Name: {self.__name} | "
                  f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self) -> dict:
        return {
            "product_id": self.__product_id,
            "product_name": self.__name,
            "product_price": self.__price,
            "current_stock": self.__stock,
            "transactions": list(self.__transactions),
            "supplier": self.__supplier.to_dict(),
        }

    # ---------- every subclass MUST implement this ----------

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return text describing how this product is fulfilled."""
        pass