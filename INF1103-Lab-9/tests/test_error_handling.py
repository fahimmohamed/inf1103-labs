"""Exception handling tests: bad input and bad files never crash the program."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from inventory import Inventory
from supplier import Supplier
from product_loader import load_products

LAB_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestGetPositiveFloat(unittest.TestCase):

    def test_asks_again_until_valid(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            value = main.get_positive_float("Price: ")
        self.assertEqual(value, 12.50)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_enter_keeps_default(self) -> None:
        with patch("builtins.input", return_value=""):
            self.assertEqual(main.get_positive_float("New Price: ", 9.99), 9.99)


class TestLoadProducts(unittest.TestCase):

    def setUp(self) -> None:
        self.inventory = Inventory()
        self.supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")

    def run_load(self, path: str) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue().splitlines()

    def test_lab_products_csv(self) -> None:
        lines = self.run_load(os.path.join(LAB_FOLDER, "products.csv"))
        self.assertEqual(self.inventory.get_product_count(), 3)
        self.assertEqual([p.get_product_id() for p in self.inventory.get_products()], ["P001", "D001", "P003"])
        self.assertEqual(lines, [
            "Row 4 skipped: Unknown product type: service",
            "Row 5 skipped: could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])

    def test_missing_file_handled(self) -> None:
        lines = self.run_load(os.path.join(LAB_FOLDER, "does_not_exist.csv"))
        self.assertEqual(self.inventory.get_product_count(), 0)
        self.assertTrue(lines[0].startswith("Products file not found:"))
        self.assertEqual(lines[-1], "Load attempt finished.")
        self.assertNotIn("products loaded.", " ".join(lines))  # else block did not run

    def test_bad_rows_skipped_and_duplicates_reported(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", encoding="utf-8") as file:
                file.write("product_type,product_id,name,price,stock_quantity\n"
                           "digital,D001,App,10.00,5\n"
                           "digital,D001,App Copy,12.00,5\n"   # duplicate ID
                           "physical,P001,Lamp,0,5\n"           # price not greater than zero
                           "physical,P002,Chair,20.00\n"        # missing a column
                           "\n"                                 # blank line is ignored
                           "physical,P003,Stand,39.50,7\n")
            lines = self.run_load(path)
        self.assertEqual(self.inventory.get_product_count(), 2)
        skipped_lines = [line for line in lines if "skipped:" in line]
        self.assertEqual(len(skipped_lines), 3)
        self.assertIn("2 products loaded.", lines)


if __name__ == "__main__":
    unittest.main()