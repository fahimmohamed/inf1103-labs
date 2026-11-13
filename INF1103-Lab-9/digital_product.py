from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download. A DigitalProduct IS-A Product."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier,
                 download_size: float, transactions: list[int] | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier, transactions)  # reuse Product's constructor
        self.__download_size: float = self._check_number(download_size, "Download size")

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally by download."

    def display_information(self, detailed: bool = False) -> None:
        super().display_information(detailed)  # common information comes from Product
        if detailed:
            print("Type: Digital")
            print(f"Download size: {self.__download_size:.2f} MB")
            print(f"Fulfilment: {self.get_fulfilment_info()}")
        else:
            print(f"    Type: Digital | Download size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict:
        data = super().to_dict()  # common fields come from Product
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @staticmethod
    def from_dict(data: dict, supplier: Supplier) -> "DigitalProduct":
        # the Supplier object is created (or reused) by the caller and passed in
        return DigitalProduct(data["product_id"], data["product_name"], data["product_price"],
                              data["current_stock"], supplier, data["download_size"], data["transactions"])