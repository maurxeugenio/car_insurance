from abc import ABC, abstractmethod
 
from src.domain.value_objects.address import Address
from src.domain.value_objects.rate import Rate
 
 
class IGISPort(ABC):
    """
        Domain port — infrastructure must implement this,
        never the other way around.
    """
 
    @abstractmethod
    def adjust_rate(self, address: Address, rate: Rate) -> Rate:
        """Return a new Rate adjusted by geographic risk factors."""
        ...
 