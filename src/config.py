from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Debug line to check current working directory
print(f"Current working directory: {os.getcwd()}")
# Debug line to check if .env file exists
print(f".env file exists: {os.path.exists('.env')}")

class Settings(BaseSettings):
    SUPABASE_DB_URL: str = ""
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()