from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    city: str
    country: str
    state: str

    def __post_init(self) -> None:
        if not self.city:
            raise ValueError("city must not be empty")
        
        if not self.country:
            raise ValueError("country must not be empty")
        
        if not self.state:
            raise ValueError("state must not be empty")