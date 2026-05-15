import datetime

import pytest

from src.domain.services.rate_calculation import RateCalculationService
from src.domain.value_objects.car_details import CarDetails


@pytest.fixture
def service():
    return RateCalculationService(age_rate_per_year=0.005, value_rate_per_10k=0.005)


@pytest.fixture
def current_year():
    return datetime.date.today().year


class TestRateCalculationService:
    def test_rate_from_age_only(self, service, current_year):
        # 10-year-old car worth $10k: age=5%, value=0.5% → 5.5%
        car = CarDetails(
            make="Mitsubishi",
            model="ASX",
            value=10000.0,
            year=current_year - 10,
        )
        rate = service.calculate(car)
        expected = (10 * 0.005) + (1 * 0.005)
        assert rate.value == pytest.approx(expected)

    def test_rate_from_value_only(self, service, current_year):
        # brand-new car worth $100k: age=0%, value=5%
        car = CarDetails(
            make="Mitsubishi",
            model="ASX",
            value=100000.0,
            year=current_year,
        )
        rate = service.calculate(car)
        expected = (0 * 0.005) + (10 * 0.005)
        assert rate.value == pytest.approx(expected)

    def test_rate_combined(self, service, current_year):
        # spec example: 10-year-old, $100k → 5% + 5% = 10%
        car = CarDetails(
            make="Mitsubishi",
            model="ASX",
            value=100000.0,
            year=current_year - 10,
        )
        rate = service.calculate(car)
        assert rate.value == pytest.approx(0.10)

    def test_custom_rates(self, current_year):
        service = RateCalculationService(
            age_rate_per_year=0.01,
            value_rate_per_10k=0.01,
        )
        car = CarDetails(
            make="Mitsubishi",
            model="ASX",
            value=50000.0,
            year=current_year - 5,
        )
        rate = service.calculate(car)
        expected = (5 * 0.01) + (5 * 0.01)
        assert rate.value == pytest.approx(expected)

    def test_rate_is_never_negative(self, service, current_year):
        car = CarDetails(
            make="Mitsubishi",
            model="ASX",
            value=1000.0,
            year=current_year,
        )
        rate = service.calculate(car)
        assert rate.value >= 0.0
