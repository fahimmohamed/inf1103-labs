from product import Product


class OrderLine:
    """ONE product and quantity inside an Order. Only an Order creates OrderLines (composition)."""

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise ValueError("An order line must refer to a Product object.")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a whole number greater than 0.")

        self.__product: Product = product  # a reference only: the OrderLine does NOT own the Product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return round(self.__product.get_price() * self.__quantity, 2)

    def display_information(self) -> None:
        print(f"{self.__product.get_product_id()} | {self.__product.get_name()} | "
              f"{self.__quantity} x ${self.__product.get_price():.2f} = ${self.calculate_subtotal():.2f}")