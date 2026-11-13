from discount_strategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    """Default strategy: the total is not changed."""

    def apply(self, total: float) -> float:
        return round(total, 2)