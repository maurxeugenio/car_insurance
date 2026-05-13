from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.entities.insurance_quote import InsuranceQuote


@dataclass(frozen=True)
class PremiumCalculatedEvent:
    """Raised when a quote is successfully calculated"""
    quote: InsuranceQuote
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )