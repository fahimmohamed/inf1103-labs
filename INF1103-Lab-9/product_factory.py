from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:
    """Factory pattern: the ONE place that decides which Product subclass to create."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float, stock_quantity: int,
               supplier: Supplier, size: float = 0.0, transactions: list[int] | None = None) -> Product:
        # size = weight in kg for a physical product, download size in MB for a digital product
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, size, transactions)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, size, transactions)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

    @staticmethod
    def create_from_dict(data: dict, supplier: Supplier) -> Product:
        # used when loading inventory.json; the saved "type" decides which size field to read
        product_type = data["type"]

        if product_type == "physical":
            size = data["weight"]
        elif product_type == "digital":
            size = data["download_size"]
        else:
            raise ValueError(f"Unknown product type: {product_type}")

        return ProductFactory.create(product_type, data["product_id"], data["product_name"],
                                     data["product_price"], data["current_stock"], supplier,
                                     size, data["transactions"])