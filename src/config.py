from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    refresh_token_secret_key: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    redis_host: str
    redis_port: int
    jti_expiration_seconds: int
    resend_api_key: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()