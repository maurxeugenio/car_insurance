from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.commands.quote_command import QuoteCommand
from src.application.use_cases.calculate_premium import CalculatePremiumUseCase
from src.domain.services.policy_limit_calculation import PolicyLimitCalculationService
from src.domain.services.premium_calculation import PremiumCalculationService
from src.domain.services.rate_calculation import RateCalculationService
from src.domain.value_objects.address import Address
from src.domain.value_objects.rate import Rate


@pytest.fixture
def rate_service():
    svc = MagicMock(spec=RateCalculationService)
    svc.calculate.return_value = Rate(value=0.10)
    return svc


@pytest.fixture
def premium_service():
    from src.domain.value_objects.money import Money
    svc = MagicMock(spec=PremiumCalculationService)
    svc.calculate.return_value = Money(amount=9050.0)
    return svc


@pytest.fixture
def policy_limit_service():
    from src.domain.value_objects.money import Money
    svc = MagicMock(spec=PolicyLimitCalculationService)
    svc.calculate_limit.return_value = Money(amount=90000.0)
    svc.calculate_deductible_value.return_value = Money(amount=10000.0)
    return svc


@pytest.fixture
def gis_port():
    port = AsyncMock()
    port.adjust_rate.return_value = Rate(value=0.12)
    return port


@pytest.fixture
def use_case(rate_service, premium_service, policy_limit_service, gis_port):
    return CalculatePremiumUseCase(
        gis_port=gis_port,
        policy_limit_service=policy_limit_service,
        premium_service=premium_service,
        rate_service=rate_service,
    )


@pytest.fixture
def command():
    return QuoteCommand(
        broker_fee=50.0,
        deductible_percentage=0.10,
        make="Mitsubishi",
        model="ASX",
        value=100000.0,
        year=2015,
    )


class TestCalculatePremiumUseCase:
    async def test_returns_insurance_quote(self, use_case, command):
        from src.domain.entities.insurance_quote import InsuranceQuote
        quote = await use_case.execute(command)
        assert isinstance(quote, InsuranceQuote)

    async def test_rate_service_is_called(self, use_case, command, rate_service):
        await use_case.execute(command)
        rate_service.calculate.assert_called_once()

    async def test_gis_not_called_without_location(self, use_case, command, gis_port):
        await use_case.execute(command)
        gis_port.adjust_rate.assert_not_called()

    async def test_gis_called_with_location(self, use_case, gis_port):
        command = QuoteCommand(
            broker_fee=50.0,
            deductible_percentage=0.10,
            make="Mitsubishi",
            model="ASX",
            registration_location=Address(city="São Paulo", country="Brazil", state="SP"),
            value=100000.0,
            year=2015,
        )
        await use_case.execute(command)
        gis_port.adjust_rate.assert_called_once()

    async def test_gis_adjusted_rate_is_used(self, use_case, gis_port, premium_service):
        command = QuoteCommand(
            broker_fee=50.0,
            deductible_percentage=0.10,
            make="Mitsubishi",
            model="ASX",
            registration_location=Address(city="São Paulo", country="Brazil", state="SP"),
            value=100000.0,
            year=2015,
        )
        await use_case.execute(command)
        _, kwargs = premium_service.calculate.call_args
        assert kwargs["rate"].value == pytest.approx(0.12)

    async def test_quote_contains_all_fields(self, use_case, command):
        quote = await use_case.execute(command)
        assert quote.applied_rate is not None
        assert quote.calculated_premium is not None
        assert quote.policy_limit is not None
        assert quote.deductible_value is not None
        assert quote.car is not None