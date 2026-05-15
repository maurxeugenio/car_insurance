from dataclasses import dataclass


@dataclass(frozen=True)
class Rate:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("rate must be zero or greater")

    def __add__(self, other: "Rate") -> "Rate":
        return Rate(value=self.value + other.value)

    def adjusted(self, adjustment: float) -> "Rate":
        """
            Return a new Rate with a GIS adjustment applied (e.g. +0.02 or -0.01)
        """
        return Rate(value=max(0.0, self.value + adjustment))
