from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. A PhysicalProduct IS-A Product."""

    BASE_SHIPPING_COST: float = 5.00  # flat fee
    COST_PER_KG: float = 2.00         # plus this amount for every kilogram

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier,
                 weight: float, transactions: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier, transactions)  # reuse Product's constructor
        self.__weight: float = self._check_number(weight, "Weight")

    def get_weight(self) -> float:
        return self.__weight

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return round(self.BASE_SHIPPING_COST + self.COST_PER_KG * self.__weight, 2)

    def display_information(self, detailed: bool = False) -> None:
        super().display_information(detailed)  # common information comes from Product
        if detailed:
            print("Type: Physical")
            print(f"Weight: {self.__weight:.2f} kg")
            print(f"Fulfilment: {self.get_fulfilment_info()}")
            print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")
        else:
            print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def to_dict(self) -> dict:
        data = super().to_dict()  # common fields come from Product
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @staticmethod
    def from_dict(data: dict, supplier: Supplier) -> "PhysicalProduct":
        # the Supplier object is created (or reused) by the caller and passed in
        return PhysicalProduct(data["product_id"], data["product_name"], data["product_price"],
                               data["current_stock"], supplier, data["weight"], data["transactions"])