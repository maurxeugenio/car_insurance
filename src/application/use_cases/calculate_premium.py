from src.application.commands.quote_command import QuoteCommand
from src.domain.entities.insurance_quote import InsuranceQuote
from src.domain.events.premium_calculated import PremiumCalculatedEvent
from src.domain.ports.gis_port import IGISPort

from src.domain.services import (
    PolicyLimitCalculationService,
    PremiumCalculationService,
    RateCalculationService
)
from src.domain.value_objects import CarDetails, DeductiblePercentage, Money


class CalculatePremiumUseCase:
    def __init__(
        self,
        gis_port: IGISPort,
        policy_limit_service: PolicyLimitCalculationService,
        premium_service: PremiumCalculationService,
        rate_service: RateCalculationService,
    ) -> None:
        self._gis_port = gis_port
        self._policy_limit_service = policy_limit_service
        self._premium_service = premium_service
        self._rate_service = rate_service

    async def execute(self, command: QuoteCommand) -> InsuranceQuote:
        car = CarDetails(
            make=command.make,
            model=command.model,
            value=command.value,
            year=command.year,
        )
        broker_fee = Money(amount=command.broker_fee)
        deductible = DeductiblePercentage(value=command.deductible_percentage)

        rate = self._rate_service.calculate(car)

        if command.registration_location is not None:
            rate = await self._gis_port.adjust_rate(
                address=command.registration_location,
                rate=rate,
            )

        calculated_premium = self._premium_service.calculate(
            broker_fee=broker_fee,
            car=car,
            deductible_percentage=deductible,
            rate=rate,
        )
        policy_limit = self._policy_limit_service.calculate_limit(
            car=car,
            deductible_percentage=deductible,
        )
        deductible_value = self._policy_limit_service.calculate_deductible_value(
            car=car,
            deductible_percentage=deductible,
        )

        quote = InsuranceQuote(
            applied_rate=rate,
            broker_fee=broker_fee,
            calculated_premium=calculated_premium,
            car=car,
            deductible_percentage=deductible,
            deductible_value=deductible_value,
            policy_limit=policy_limit,
        )

        _event = PremiumCalculatedEvent(quote=quote)

        return quote
