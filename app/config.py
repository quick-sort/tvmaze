import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import field_validator, ConfigDict, FieldValidationInfo, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    TESTING: Optional[str] = None
    API_STR: str = "/api"
    PROJECT_NAME: str = 'tvmaze'
    API_KEY: str = secrets.token_urlsafe(64)
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEFAULT_JOB_COUNTRY: str = 'US'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite://'
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: int = 6379
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_TO: Optional[EmailStr] = None

settings = Settings()