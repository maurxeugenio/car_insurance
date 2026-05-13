from src.api.v1.schemas.quote_request import AddressSchema, CarSchema
from pydantic import BaseModel


class QuoteResponse(BaseModel):
    applied_rate: float
    broker_fee: float
    calculated_premium: float
    car: CarSchema
    deductible_percentage: float
    deductible_value: float
    policy_limit: float
    registration_location: AddressSchema | None = None