"""Factory pattern tests."""
import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from product_factory import ProductFactory


class TestProductFactory(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier, 1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 1.2)  # type: ignore[attr-defined]

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, self.supplier, 350)
        self.assertIsInstance(product, DigitalProduct)

    def test_returns_a_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, self.supplier)
        self.assertIsInstance(product, Product)
        self.assertIs(product.get_supplier(), self.supplier)

    def test_unknown_type_raises_clear_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_create_from_dict_round_trip(self) -> None:
        original = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier, 1.2)
        copy = ProductFactory.create_from_dict(original.to_dict(), self.supplier)
        self.assertIsInstance(copy, PhysicalProduct)
        self.assertEqual(copy.to_dict(), original.to_dict())

    def test_create_from_dict_unknown_type(self) -> None:
        data = ProductFactory.create("digital", "D001", "App", 5.00, 1, self.supplier).to_dict()
        data["type"] = "service"
        with self.assertRaises(ValueError):
            ProductFactory.create_from_dict(data, self.supplier)


if __name__ == "__main__":
    unittest.main()