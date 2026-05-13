from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    env: str = "development"
    age_rate_per_year: float = 0.005
    coverage_percentage: float = 1.0
    gis_max_adjustment: float = 0.02
    gis_service_url: str = ""
    value_rate_per_10k: float = 0.005


def get_settings() -> Settings:
    return Settings()