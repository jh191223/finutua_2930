from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://healthapp_user:your_secure_password@localhost/healthapp"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: str = "redis://localhost:6379"
    S3_BUCKET: str = "healthapp-storage"
    AWS_REGION: str = "ap-northeast-2"
    
    class Config:
        env_file = ".env"

