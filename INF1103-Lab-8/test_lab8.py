"""Lab 8 tests. Run with: python test_lab8.py"""

from supplier import Supplier


def test_supplier() -> None:
    print("=" * 48)
    print("TEST: Supplier")
    print("=" * 48)

    supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.sg")
    supplier.display_information()

    # invalid suppliers must be rejected
    for bad_values in [("", "Name", "a@b.com"), ("S 1", "Name", "a@b.com"),
                       ("S002", "  ", "a@b.com"), ("S003", "Name", "no-at-sign")]:
        try:
            Supplier(*bad_values)
            print(f"FAILED: {bad_values} was accepted")
        except ValueError as error:
            print(f"Rejected as expected: {error}")
    print()


if __name__ == "__main__":
    test_supplier()