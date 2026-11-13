from product import Product
from order_line import OrderLine


class Order:
    """An Order creates and owns its OrderLines (composition): they live and die with the Order."""

    def __init__(self, order_id: str) -> None:
        if not isinstance(order_id, str) or not order_id.strip() or len(order_id.split()) > 1:
            raise ValueError("Order ID must be text without spaces.")

        self.__order_id: str = order_id.strip()
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)  # a copy, so lines can only be added/removed through the Order

    def add_order_line(self, product: Product, quantity: int) -> None:
        for order_line in self.__order_lines:
            if order_line.get_product() is product:
                raise ValueError(f"{product.get_product_id()} is already in this order.")

        order_line = OrderLine(product, quantity)  # the Order CREATES its own OrderLine
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        wanted_id = product_id.strip().lower()

        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().lower() == wanted_id:
                self.__order_lines.remove(order_line)  # the line is gone; the Product is untouched
                return True
        return False

    def calculate_total(self) -> float:
        # the Order asks each OrderLine for its own subtotal
        return round(sum(order_line.calculate_subtotal() for order_line in self.__order_lines), 2)

    def display_information(self) -> None:
        print(f"Order ID: {self.__order_id}")
        print("-" * 48)

        if not self.__order_lines:
            print("(no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()

        print("-" * 48)
        print(f"Order Total: ${self.calculate_total():.2f}")