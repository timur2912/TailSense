import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # API конфигурация
    api_title: str = "TailSense Backend API"
    api_description: str = "Backend API for TailSense veterinary AI assistant"
    api_version: str = "1.0.0"
    
    # Внешний API
    external_api_url: str = "http://localhost:7860/api/v1/run/e68ff0eb-0690-43b7-acb6-c3e8ea8ecea1"
    external_api_key: str = "sk-WFRz8a28DHL31Sr-qN0K8WFFnzKeeVaJJLq5RYAF7dg"
    
    # Сервер настройки
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS настройки
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    cors_headers: list[str] = ["*"]
    
    # Timeout настройки
    request_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Глобальный экземпляр настроек
settings = Settings()
