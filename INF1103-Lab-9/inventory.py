from product import Product


class Inventory:
    """Groups Product objects (aggregation). It does NOT create or destroy them."""

    def __init__(self) -> None:
        self.__products: list[Product] = []  # typed as Product, so ANY subclass can be stored

    #Add an existing product. Returns False (and adds nothing) if the ID already exists.
    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False

        self.__products.append(product)
        return True

    #Return the matching Product, or None if there is no match.
    def find_product(self, product_id: str) -> Product | None:
        wanted_id = product_id.strip().lower()

        for product in self.__products:
            if product.get_product_id().lower() == wanted_id:
                return product
        return None

    #Take the product's reference out of this inventory. The Product object itself is NOT destroyed.
    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)

        if product is not None:
            self.__products.remove(product)
        return product  # handed back, so it can be added to another inventory

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 48)

        for product in self.__products:
            product.display_information()

        print("-" * 48)

    def get_products(self) -> list[Product]:
        return list(self.__products)  # a copy of the list (the Product objects are shared)

    def get_product_count(self) -> int:
        return len(self.__products)

    def get_total_stock(self) -> int:
        return sum(product.get_stock() for product in self.__products)