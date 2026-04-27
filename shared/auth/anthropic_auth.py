import anthropic
from shared.config import get_settings


def get_anthropic_client() -> anthropic.Anthropic:
    settings = get_settings()
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)
