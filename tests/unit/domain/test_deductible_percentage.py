import pytest

from src.domain.value_objects.deductible_percentage import DeductiblePercentage


class TestDeductiblePercentage:
    def test_creates_with_valid_value(self):
        d = DeductiblePercentage(value=0.10)
        assert d.value == 0.10

    def test_zero_is_valid(self):
        d = DeductiblePercentage(value=0.0)
        assert d.value == 0.0

    def test_one_is_valid(self):
        d = DeductiblePercentage(value=1.0)
        assert d.value == 1.0

    def test_raises_when_above_one(self):
        with pytest.raises(ValueError, match="deductible_percentage must be between 0 and 1"):
            DeductiblePercentage(value=1.01)

    def test_raises_when_negative(self):
        with pytest.raises(ValueError, match="deductible_percentage must be between 0 and 1"):
            DeductiblePercentage(value=-0.01)