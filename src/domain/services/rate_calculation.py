import datetime

from src.domain.value_objects import CarDetails, Rate


class RateCalculationService:
    """
        Calculates the applied rate from car age and value
        Rules:
            - +0.5% per year of age
            - +0.5% per $10,0000 of car value
    """

    def __init__(
        self,
        age_rate_per_year: float = 0.005,
        value_rate_per_10k: float = 0.005
    ) -> None:
        self._age_rate_per_year = age_rate_per_year
        self._value_rate_per_10k = value_rate_per_10k

    def calculate(self, car: CarDetails) -> Rate:
        current_year = datetime.date.today().year
        age_rate = (current_year - car.year) * self._age_rate_per_year
        value_rate = (car.value / 10_000) * self._value_rate_per_10k

        return Rate(value=age_rate + value_rate)
        