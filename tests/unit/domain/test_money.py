import pytest

from src.domain.value_objects.deductible_percentage import DeductiblePercentage
from src.domain.value_objects.money import Money


class TestMoneyCreation:
    def test_creates_with_valid_values(self):
        m = Money(amount=100.0)
        assert m.amount == 100.0
        assert m.currency == "USD"

    def test_creates_with_custom_currency(self):
        m = Money(amount=50.0, currency="BRL")
        assert m.currency == "BRL"

    def test_raises_when_amount_is_negative(self):
        with pytest.raises(ValueError, match="amount must be zero or greater"):
            Money(amount=-1.0)

    def test_raises_when_currency_is_empty(self):
        with pytest.raises(ValueError, match="currency must not be empty"):
            Money(amount=10.0, currency="")

    def test_zero_amount_is_valid(self):
        m = Money(amount=0.0)
        assert m.amount == 0.0


class TestMoneyArithmetic:
    def test_add_same_currency(self):
        result = Money(amount=100.0) + Money(amount=50.0)
        assert result.amount == 150.0

    def test_sub_same_currency(self):
        result = Money(amount=100.0) - Money(amount=30.0)
        assert result.amount == 70.0

    def test_mul_by_float(self):
        result = Money(amount=100.0) * 0.10
        assert result.amount == pytest.approx(10.0)

    def test_mul_by_int(self):
        result = Money(amount=100.0) * 2
        assert result.amount == pytest.approx(200.0)

    def test_mul_by_value_object_with_value_attr(self):
        deductible = DeductiblePercentage(value=0.10)
        result = Money(amount=100.0) * deductible.value
        assert result.amount == pytest.approx(10.0)

    def test_add_different_currency_raises(self):
        with pytest.raises(ValueError, match="currency mismatch"):
            Money(amount=100.0, currency="USD") + Money(amount=50.0, currency="BRL")

    def test_sub_different_currency_raises(self):
        with pytest.raises(ValueError, match="currency mismatch"):
            Money(amount=100.0, currency="USD") - Money(amount=50.0, currency="BRL")

    def test_immutability(self):
        m = Money(amount=100.0)
        result = m * 2
        assert m.amount == 100.0  # original unchanged
        assert result.amount == 200.0