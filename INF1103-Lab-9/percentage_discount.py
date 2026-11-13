from discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        if isinstance(percentage, bool) or not isinstance(percentage, (int, float)) or not 0 <= percentage <= 100:
            raise ValueError("Percentage must be a number from 0 to 100.")
        self.__percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return round(total * (1 - self.__percentage / 100), 2)