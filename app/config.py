"""to config  a setting for database and jwt"""

from pydantic_settings import BaseSettings,SettingsConfigDict
_base_config = SettingsConfigDict(env_file="./.env",env_ignore_empty=True,extra="ignore")
class DataBaseSettings(BaseSettings):
    POSTGRES_SERVER:str
    POSTGRES_PORT:int
    POSTGRES_DB:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    REDIS_HOST:str
    REDIS_PORT:str

    model_config = _base_config
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

class JWTSetting(BaseSettings):
    JWT_SECRET:str
    JWT_ALGORITHM:str
    model_config = _base_config      

db_settings=DataBaseSettings()
jwt_setting=JWTSetting()
