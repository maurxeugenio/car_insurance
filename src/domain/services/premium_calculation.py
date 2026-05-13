from src.domain.value_objects import (
    CarDetails,
    DeductiblePercentage,
    Money,
    Rate
)


class PremiumCalculationService:
    """
        Calculates the final insurance premium.

        Formula:
            base_premium = car.value * rate
            deductible_discount = base_premium * deductible_percentage
            final_premium = base_premium - deductible_discount + broker_fee
    """

    def calculate(
        self,
        broker_fee: Money,
        car: CarDetails,
        deductible_percentage: DeductiblePercentage,
        rate: Rate
    ) -> Money:
        base_premium = Money(amount=car.value * rate.value)
        deductible_discount = base_premium * deductible_percentage.value
        return base_premium - deductible_discount + broker_fee

        