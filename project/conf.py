from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth_secret_key: str
    auth_token_encode_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    smtp_port: int = 465
    smtp_server: str
    smtp_login: str
    smtp_password: str
    smtp_sender: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
