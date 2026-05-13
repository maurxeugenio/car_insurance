from dataclasses import dataclass

from src.domain.value_objects.address import Address


@dataclass(frozen=True)
class QuoteCommand:
    broker_fee: float
    deductible_percentage: float
    make: str
    model: str
    value: float
    year: int
    registration_location: Address | None = None