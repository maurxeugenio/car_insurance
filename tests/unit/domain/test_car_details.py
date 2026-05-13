import pytest

from src.domain.value_objects.car_details import CarDetails


class TestCarDetailsCreation:
    def test_creates_with_valid_values(self):
        car = CarDetails(make="Mitsubishi", model="ASX", value=100000.0, year=2015)
        assert car.make == "Mitsubishi"
        assert car.model == "ASX"
        assert car.value == 100000.0
        assert car.year == 2015

    def test_raises_when_make_is_empty(self):
        with pytest.raises(ValueError, match="make must not be empty"):
            CarDetails(make="", model="ASX", value=100000.0, year=2015)

    def test_raises_when_model_is_empty(self):
        with pytest.raises(ValueError, match="model must not be empty"):
            CarDetails(make="Mitsubishi", model="", value=100000.0, year=2015)

    def test_raises_when_value_is_zero(self):
        with pytest.raises(ValueError, match="value must be greater than zero"):
            CarDetails(make="Mitsubishi", model="ASX", value=0.0, year=2015)

    def test_raises_when_value_is_negative(self):
        with pytest.raises(ValueError, match="value must be greater than zero"):
            CarDetails(make="Mitsubishi", model="ASX", value=-1.0, year=2015)

    def test_raises_when_year_is_before_1900(self):
        with pytest.raises(ValueError, match="year must be 1980 or later"):
            CarDetails(make="Mitsubishi", model="ASX", value=100000.0, year=1899)

    def test_immutability(self):
        car = CarDetails(make="Mitsubishi", model="ASX", value=100000.0, year=2015)
        with pytest.raises(Exception):
            car.make = "Honda"  # type: ignore[misc]