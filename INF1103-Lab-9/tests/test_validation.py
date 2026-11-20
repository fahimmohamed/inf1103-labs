"""Validation tests: each class rejects data that breaks its own rules."""
import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order


class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")

    def test_price_must_be_greater_than_zero(self) -> None:
        for price in [0, -5, 0.001]:
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P001", "Desk Lamp", price, 10, self.supplier)

    def test_set_price_must_be_greater_than_zero(self) -> None:
        product = ProductFactory.create("digital", "D001", "App", 10.00, 5, self.supplier)
        with self.assertRaises(ValueError):
            product.set_price(0)
        self.assertEqual(product.get_price(), 10.00)  # unchanged after the rejected value

    def test_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, -1, self.supplier)

    def test_update_stock_cannot_go_negative_for_either_type(self) -> None:
        for product_type in ["physical", "digital"]:  # LSP: both subclasses keep the parent's rule
            product = ProductFactory.create(product_type, "X1", "Item", 5.00, 3, self.supplier)
            with self.assertRaises(ValueError):
                product.update_stock(-1)
            self.assertEqual(product.get_stock(), 3)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier)
        order = Order("O001")
        for quantity in [0, -2]:
            with self.assertRaises(ValueError):
                order.add_order_line(product, quantity)
        self.assertEqual(order.get_order_lines(), [])


if __name__ == "__main__":
    unittest.main()