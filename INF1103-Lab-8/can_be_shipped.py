from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract: anything that can be shipped must calculate its shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the cost of shipping this item."""
        pass