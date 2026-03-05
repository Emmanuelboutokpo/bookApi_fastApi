from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    refresh_token_secret_key: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()