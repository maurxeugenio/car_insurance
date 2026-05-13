from dataclasses import dataclass, field
from uuid import UUID, uuid4
 
from src.domain.value_objects.car_details import CarDetails
from src.domain.value_objects.deductible_percentage import DeductiblePercentage
from src.domain.value_objects.money import Money
from src.domain.value_objects.rate import Rate
 
 
@dataclass
class InsuranceQuote:
    """Aggregate root — owns all output values of a quote calculation."""
 
    applied_rate: Rate
    broker_fee: Money
    calculated_premium: Money
    car: CarDetails
    deductible_percentage: DeductiblePercentage
    deductible_value: Money
    policy_limit: Money
    id: UUID = field(default_factory=uuid4)
 