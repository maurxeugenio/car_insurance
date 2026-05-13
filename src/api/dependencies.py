

from src.application.use_cases.calculate_premium import CalculatePremiumUseCase
from src.domain.services.policy_limit_calculation import PolicyLimitCalculationService
from src.domain.services.premium_calculation import PremiumCalculationService
from src.domain.services.rate_calculation import RateCalculationService
from src.infrastructure.adapters.gis_adapter import GISAdapter
from src.infrastructure.config.settings import get_settings


def get_calculate_premium_use_case() -> CalculatePremiumUseCase:
    settings = get_settings()

    rate_service = RateCalculationService(
        age_rate_per_year=settings.age_rate_per_year,
        value_rate_per_10k=settings.value_rate_per_10k
    )

    premium_service = PremiumCalculationService()

    policy_limit_service = PolicyLimitCalculationService(
        coverage_percentage=settings.coverage_percentage
    )

    gis_adapter = GISAdapter(
        max_adjustment=settings.gis_max_adjustment,
        service_url=settings.gis_service_url,
    )

    return CalculatePremiumUseCase(
        gis_port=gis_adapter,
        policy_limit_service=policy_limit_service,
        premium_service=premium_service,
        rate_service=rate_service 
    )