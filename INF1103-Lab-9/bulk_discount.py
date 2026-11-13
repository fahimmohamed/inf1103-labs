from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold, e.g. BulkDiscount(200, 20)."""

    def __init__(self, threshold: float, amount: float) -> None:
        for value, label in [(threshold, "Threshold"), (amount, "Discount amount")]:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"{label} must be a number that is not negative.")
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return round(max(total - self.__amount, 0.0), 2)  # a total can never go below 0
        return round(total, 2)