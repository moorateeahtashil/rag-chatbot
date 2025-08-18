import yaml
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PINECONE_API_KEY: str
    PINECONE_CLOUD: str
    PINECONE_REGION: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

@lru_cache()
def get_domain_config(domain: str = "default"):
    config_path = f"configs/{domain}_domain.yaml"
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Fallback to default if domain config not found
        with open("configs/default_domain.yaml", "r") as f:
            return yaml.safe_load(f)
