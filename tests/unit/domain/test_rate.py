import pytest

from src.domain.value_objects.rate import Rate


class TestRateCreation:
    def test_creates_with_valid_value(self):
        r = Rate(value=0.10)
        assert r.value == 0.10

    def test_zero_is_valid(self):
        r = Rate(value=0.0)
        assert r.value == 0.0

    def test_raises_when_negative(self):
        with pytest.raises(ValueError, match="rate must be zero or greater"):
            Rate(value=-0.01)


class TestRateOperations:
    def test_add_two_rates(self):
        result = Rate(value=0.05) + Rate(value=0.10)
        assert result.value == pytest.approx(0.15)

    def test_adjusted_positive(self):
        result = Rate(value=0.10).adjusted(0.02)
        assert result.value == pytest.approx(0.12)

    def test_adjusted_negative(self):
        result = Rate(value=0.10).adjusted(-0.02)
        assert result.value == pytest.approx(0.08)

    def test_adjusted_never_goes_below_zero(self):
        result = Rate(value=0.01).adjusted(-0.99)
        assert result.value == 0.0

    def test_immutability(self):
        r = Rate(value=0.10)
        r.adjusted(0.05)
        assert r.value == 0.10  # original unchanged