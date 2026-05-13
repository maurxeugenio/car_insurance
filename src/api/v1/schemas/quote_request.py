from pydantic import BaseModel, Field


class CarSchema(BaseModel):
    make: str = Field(..., examples=["Mitsubish", "Toyota"])
    model: str = Field(..., examples=["ASX", "Corolla CROOS"])
    value: float = Field(..., gt=0, examples=[100000.00])
    year: int = Field(..., ge=1980, le=2026, examples=[2026])


class AddressSchema(BaseModel):
    city: str = Field(..., examples=["Divinolândia de Minas"])
    country: str = Field(..., examples=["Brazil"])
    state: str = Field(..., examples=["MG"])


class QuoteRequest(BaseModel):
    broker_fee: float = Field(..., ge=0, examples=[50.0])
    car: CarSchema
    deductible_percentage: float = Field(..., ge=0, le=1, examples=[0.10])
    registration_location: AddressSchema | None = None
