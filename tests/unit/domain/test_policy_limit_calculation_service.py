import pytest

from src.domain.services.policy_limit_calculation import PolicyLimitCalculationService
from src.domain.value_objects.car_details import CarDetails
from src.domain.value_objects.deductible_percentage import DeductiblePercentage


@pytest.fixture
def car():
    return CarDetails(make="Mitsubishi", model="ASX", value=100000.0, year=2015)


class TestPolicyLimitCalculationService:
    def test_limit_with_full_coverage_no_deductible(self, car):
        service = PolicyLimitCalculationService(coverage_percentage=1.0)
        limit = service.calculate_limit(car, DeductiblePercentage(value=0.0))
        assert limit.amount == pytest.approx(100000.0)

    def test_limit_with_deductible(self, car):
        # base  = 100000 * 1.0  = 100000
        # ded   = 100000 * 0.10 = 10000
        # final = 100000 - 10000 = 90000
        service = PolicyLimitCalculationService(coverage_percentage=1.0)
        limit = service.calculate_limit(car, DeductiblePercentage(value=0.10))
        assert limit.amount == pytest.approx(90000.0)

    def test_limit_with_partial_coverage(self, car):
        # base  = 100000 * 0.80 = 80000
        # ded   = 80000  * 0.10 = 8000
        # final = 80000 - 8000  = 72000
        service = PolicyLimitCalculationService(coverage_percentage=0.80)
        limit = service.calculate_limit(car, DeductiblePercentage(value=0.10))
        assert limit.amount == pytest.approx(72000.0)

    def test_deductible_value(self, car):
        # base  = 100000 * 1.0  = 100000
        # ded   = 100000 * 0.10 = 10000
        service = PolicyLimitCalculationService(coverage_percentage=1.0)
        ded_value = service.calculate_deductible_value(car, DeductiblePercentage(value=0.10))
        assert ded_value.amount == pytest.approx(10000.0)

    def test_raises_when_coverage_is_zero(self):
        with pytest.raises(ValueError, match="coverage_percentage"):
            PolicyLimitCalculationService(coverage_percentage=0.0)

    def test_raises_when_coverage_above_one(self):
        with pytest.raises(ValueError, match="coverage_percentage"):
            PolicyLimitCalculationService(coverage_percentage=1.01)