from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """A fixed 5% discount for students. Added without changing Order (Open/Closed Principle)."""

    STUDENT_PERCENTAGE: float = 5.0

    def apply(self, total: float) -> float:
        return round(total * (1 - self.STUDENT_PERCENTAGE / 100), 2)