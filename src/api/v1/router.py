from fastapi import APIRouter, Depends

from src.api.v1.schemas.quote_request import QuoteRequest
from src.api.v1.schemas.quote_response import QuoteResponse
from src.api.dependencies import get_calculate_premium_use_case
from src.application.use_cases.calculate_premium import CalculatePremiumUseCase
from src.application.commands.quote_command import QuoteCommand
from src.domain.value_objects.address import Address


router = APIRouter(tags=["quotes"])


@router.post(
    "/quotes",
    response_model=QuoteResponse,
    summary="Calculate insurance premium",
    status_code=200,
)
async def calculate_quote(
    body: QuoteRequest,
    use_case: CalculatePremiumUseCase = Depends(get_calculate_premium_use_case),
) -> QuoteResponse:
    registration_location: Address | None = None
    if body.registration_location:
        registration_location = Address(
            city=body.registration_location.city,
            country=body.registration_location.country,
            state=body.registration_location.state,
        )

    command = QuoteCommand(
        broker_fee=body.broker_fee,
        deductible_percentage=body.deductible_percentage,
        make=body.car.make,
        model=body.car.model,
        registration_location=registration_location,
        value=body.car.value,
        year=body.car.year,
    )

    quote = await use_case.execute(command)

    return QuoteResponse(
        applied_rate=quote.applied_rate.value,
        broker_fee=body.broker_fee,
        calculated_premium=quote.calculated_premium.amount,
        car=body.car,
        deductible_percentage=body.deductible_percentage,
        deductible_value=quote.deductible_value.amount,
        policy_limit=quote.policy_limit.amount,
        registration_location=body.registration_location,
    )