from dataclasses import dataclass, field
from uuid import UUID, uuid4
 
from src.domain.value_objects import (
    CarDetails,
    DeductiblePercentage,
    Money,
    Rate
)
 
 
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
 