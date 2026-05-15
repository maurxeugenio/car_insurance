from dataclasses import dataclass


@dataclass(frozen=True)
class CarDetails:
    make: str
    model: str
    value: float
    year: float

    def __post_init__(self) -> None:
        if not self.make:
            raise ValueError('make must not be empty')

        if not self.model:
            raise ValueError('model must not be empty')

        if self.value <= 0:
            raise ValueError('value must be greater than zero')

        if self.year < 1980:
            raise ValueError('year must be 1980 or later')