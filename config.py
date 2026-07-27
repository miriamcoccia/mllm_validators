"""
config.py: This file contains the instructions to handle various I/O operations safely
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, ConfigDict
import yaml
from pathlib import Path
from decimal import Decimal

class Secrets(BaseSettings): 
    """
    Reads API keys from environment variables (or a .env file).
    Never commit real values.
    """
    model_config = SettingsConfigDict(extra="forbid", env_file=".env")

    openai_api_key: str
    nebius_api_key: str


class ModelConfig(BaseModel):
    """
    Settings for one AI model, loaded from configs/models/<name>.yaml
    """
    model_config = ConfigDict(extra="forbid")

    name: str
    provider: str


class ModelPricing(BaseModel):
    """
    Pricing info for one AI model, loaded from configs/pricing.yaml
    """
    model_config = ConfigDict(extra="forbid")

    input_per_million: Decimal
    output_per_million: Decimal


def load_model_config(path: Path) -> ModelConfig:
    """
    Reads a YAML file and returns a validated ModelConfig.
    Raises yaml.YAMLError if the file isn't valid YAML,
    or pydantic.ValidationError if the fields don't match ModelConfig.
    """
    with open(path) as file:
        data = yaml.safe_load(file)
    return ModelConfig(**data)


def load_pricing(path: Path) -> dict[str, ModelPricing]:
    """
    Reads pricing.yaml and eturns a dict mapping model name -> ModelPricing.
    """
    with open(path) as file:
        data = yaml.safe_load(file)
        return {key: ModelPricing(**value) for key, value in data.items()}