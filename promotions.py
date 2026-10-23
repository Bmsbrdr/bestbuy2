from abc import ABC, abstractmethod
class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_discount(self, desired_quantity: int, total_price: float) -> float:
        """Return the positive amount saved on this product line."""
        raise NotImplementedError

class SecondHalfPricePromotion(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    @staticmethod
    def get_discount(desired_quantity: float, total_price: float) -> float:
        return (total_price / desired_quantity) * 0.5 if desired_quantity >= 2 else 0

class ThirdOneFreePromotion(Promotion):
    def __init__(self, name: str):
        super().__init__(name)
    @staticmethod
    def get_discount(desired_quantity: float, total_price: float) -> float:
        return total_price / desired_quantity if desired_quantity >= 3 else 0

class PercentDiscountPromotion(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100")
        self.__discount = percent
    @property
    def discount(self):
        return self.__discount

    def get_discount(self, desired_quantity: int, total_price: float) -> float:
        return total_price * self.__discount / 100
