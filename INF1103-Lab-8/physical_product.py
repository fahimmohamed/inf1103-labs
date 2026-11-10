from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. A PhysicalProduct IS-A Product."""

    BASE_SHIPPING_COST = 5.00  # flat fee
    COST_PER_KG = 2.00         # plus this amount for every kilogram

    def __init__(self, product_id, name, price, stock, weight, transactions=None):
        super().__init__(product_id, name, price, stock, transactions)  # reuse Product's constructor
        self.__weight = self._check_number(weight, "Weight")

    def get_weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        return round(self.BASE_SHIPPING_COST + self.COST_PER_KG * self.__weight, 2)

    def display_information(self, detailed=False):
        super().display_information(detailed)  # common information comes from Product
        if detailed:
            print("Type: Physical")
            print(f"Weight: {self.__weight:.2f} kg")
            print(f"Fulfilment: {self.get_fulfilment_info()}")
            print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")
        else:
            print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def to_dict(self):
        data = super().to_dict()  # common fields come from Product
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @staticmethod
    def from_dict(data):
        return PhysicalProduct(data["product_id"], data["product_name"], data["product_price"],
                               data["current_stock"], data["weight"], data["transactions"])