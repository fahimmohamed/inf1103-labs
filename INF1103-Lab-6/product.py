class Product:
    def __init__(self, product_id, product_name, product_price, current_stock):
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.current_stock = current_stock
        self.transactions = [current_stock]
        pass


product1 = Product("P001", "Keyboard", 45.90, 10)
print(product1)