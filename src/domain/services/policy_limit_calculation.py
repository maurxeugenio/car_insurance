from src.domain.value_objects import CarDetails, DeductiblePercentage, Money


class PolicyLimitCalculationService:
    """
        Calculates the final policy limit and deductible value.
        Formula:
            base_policy_limit = car.value * coverage_percentage
            deductible_value = base_policy_limit * deductible_percentage
            final_limit = base_policy_limit - deductible_value
    """

    def __init__(self, coverage_percentage: float = 1.0) -> None:
        if not (0 < coverage_percentage <= 1):
            raise ValueError("coverage_percentage must be between 0 (exclusive) and 1")
        
        self._coverage_percentage = coverage_percentage
    

    def calculate_limit(
        self,
        car: CarDetails,
        deductible_percentage: DeductiblePercentage
    ) -> Money:
        base = Money(amount=car.value * self._coverage_percentage)
        deductible = base * deductible_percentage.value
        return base - deductible
    
    def calculate_deductible_value(
        self,
        car: CarDetails,
        deductible_percentage: DeductiblePercentage
    ) -> Money:
        base = Money(amount=car.value * self._coverage_percentage)
        return base * deductible_percentage.value