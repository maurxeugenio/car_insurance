from dataclasses import dataclass


@dataclass(frozen=True)
class DeductiblePercentage:
    value: float

    def __post_init__(self) -> None:
        if not (0 <= self.value <=1):
            raise ValueError("deductible_percentage must be between 0 and 1")