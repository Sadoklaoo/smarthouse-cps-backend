import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Smart House Backend"
    PROJECT_VERSION: str = "1.0"

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/smart_house"
    )

    # MQTT Configuration
    MQTT_BROKER: str = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))

    # Redis for Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://:redis:6379")
    
    broker_connection_retry_on_startup = True
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
