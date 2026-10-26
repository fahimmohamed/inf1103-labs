class Inventory:
    def __init__(self):
        self.__products = []

    #Add a product. Returns False (and adds nothing) if the ID already exists.
    def add_products(self, product):

        if self.search_product(product.get_product_id()) is not None:
            return False
 
        self.__products.append(product)
        return True
        pass

    #Return the matching Product, or None if there is no match.
    def search_product(self, product_id):
        
        wanted_id = product_id.strip().lower()
 
        for product in self.__products:
            if product.get_product_id().lower() == wanted_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory")
        print("-" * 48)
 
        for product in self.__products:
            product.display_information()
 
        print("-" * 48)

    def get_products(self):
        return list(self.__products)  # a copy of the list (the Product objects are shared)
 
    def get_product_count(self):
        return len(self.__products)
 
    def get_total_stock(self):
        return sum(product.get_stock() for product in self.__products)