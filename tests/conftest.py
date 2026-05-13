import pytest
from httpx import ASGITransport, AsyncClient

from src.api.main import create_app
from src.domain.value_objects.address import Address
from src.domain.value_objects.car_details import CarDetails
from src.domain.value_objects.deductible_percentage import DeductiblePercentage
from src.domain.value_objects.money import Money
from src.domain.value_objects.rate import Rate


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
def car():
    return CarDetails(make="Mitsubishi", model="ASX", value=100000.0, year=2015)


@pytest.fixture
def deductible():
    return DeductiblePercentage(value=0.10)


@pytest.fixture
def broker_fee():
    return Money(amount=50.0)


@pytest.fixture
def rate():
    return Rate(value=0.10)


@pytest.fixture
def address():
    return Address(city="São Paulo", country="Brazil", state="SP")


@pytest.fixture
def quote_payload():
    return {
        "broker_fee": 50.0,
        "car": {
            "make": "Mitsubishi",
            "model": "ASX",
            "value": 100000.0,
            "year": 2015,
        },
        "deductible_percentage": 0.10,
    }