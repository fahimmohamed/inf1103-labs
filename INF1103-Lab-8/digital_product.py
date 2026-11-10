from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download. A DigitalProduct IS-A Product."""

    def __init__(self, product_id, name, price, stock, supplier: Supplier, download_size, transactions=None):
        super().__init__(product_id, name, price, stock, supplier, transactions)  # reuse Product's constructor
        self.__download_size = self._check_number(download_size, "Download size")

    def get_download_size(self):
        return self.__download_size

    def get_fulfilment_info(self):
        return "Delivered digitally by download."

    def display_information(self, detailed=False):
        super().display_information(detailed)  # common information comes from Product
        if detailed:
            print("Type: Digital")
            print(f"Download size: {self.__download_size:.2f} MB")
            print(f"Fulfilment: {self.get_fulfilment_info()}")
        else:
            print(f"    Type: Digital | Download size: {self.__download_size:.2f} MB")

    def to_dict(self):
        data = super().to_dict()  # common fields come from Product
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @staticmethod
    def from_dict(data, supplier: Supplier):
        # the Supplier object is created (or reused) by the caller and passed in
        return DigitalProduct(data["product_id"], data["product_name"], data["product_price"],
                              data["current_stock"], supplier, data["download_size"], data["transactions"])