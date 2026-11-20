"""Strategy pattern tests. Run all tests from the lab folder with: python -m unittest discover -s tests -v"""
import inspect
import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount


class TestDiscountStrategies(unittest.TestCase):

    def test_no_discount_keeps_total(self) -> None:
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self) -> None:
        self.assertEqual(PercentageDiscount(10).apply(250), 225.0)

    def test_bulk_discount_at_and_below_threshold(self) -> None:
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250), 230.0)
        self.assertEqual(bulk.apply(200), 180.0)   # exactly the threshold still counts
        self.assertEqual(bulk.apply(150), 150)     # below the threshold: unchanged

    def test_student_discount(self) -> None:
        self.assertEqual(StudentDiscount().apply(300), 285.0)

    def test_invalid_discount_settings_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 20)

    def test_discount_strategy_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()  # type: ignore[abstract]


class TestOrderUsesStrategy(unittest.TestCase):

    def setUp(self) -> None:
        supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")
        lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 125.00, 10, supplier, 1.0)
        self.order = Order("O001")
        self.order.add_order_line(lamp, 2)  # lines add up to 250

    def test_default_is_no_discount(self) -> None:
        self.assertIsInstance(self.order.get_discount(), NoDiscount)
        self.assertEqual(self.order.calculate_total(), 250)

    def test_strategy_given_when_created(self) -> None:
        order = Order("O002", BulkDiscount(200, 20))
        self.assertIsInstance(order.get_discount(), BulkDiscount)

    def test_set_discount_changes_strategy(self) -> None:
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(self.order.calculate_total(), 230.0)
        self.order.set_discount(PercentageDiscount(10))  # replaces the bulk discount
        self.assertEqual(self.order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self) -> None:
        self.order.set_discount(StudentDiscount())
        self.assertEqual(self.order.calculate_total(), 237.5)

    def test_set_discount_rejects_non_strategy(self) -> None:
        with self.assertRaises(ValueError):
            self.order.set_discount("bulk")  # type: ignore[arg-type]

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        self.assertIs(Order("A", shared).get_discount(), Order("B", shared).get_discount())

    def test_order_has_no_discount_if_elif(self) -> None:
        # Order must not mention any specific discount except its default NoDiscount()
        source = inspect.getsource(Order)
        for name in ["PercentageDiscount", "BulkDiscount", "StudentDiscount", "discount_type"]:
            self.assertNotIn(name, source)


if __name__ == "__main__":
    unittest.main()