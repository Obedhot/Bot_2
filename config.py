import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def parse_coordinates(value: str | None, default: tuple[int, int]) -> tuple[int, int]:
    """Parse an x,y environment value, falling back to the supplied default."""
    try:
        x, y = (int(part.strip()) for part in (value or "").split(","))
        return x, y
    except (TypeError, ValueError):
        return default


def _seconds(name: str, default: int) -> int:
    try:
        return max(0, int(os.getenv(name, str(default))))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()
    whatsapp_sender_name: str = os.getenv("WHATSAPP_SENDER_NAME", "shahzaib").strip()
    bot_name: str = os.getenv("BOT_NAME", "Mr.Knight").strip()
    bot_real_name: str = os.getenv("BOT_REAL_NAME", "Obed Nasir").strip()
    bot_language: str = os.getenv("BOT_LANGUAGE", "English and Roman Urdu").strip()
    app_load_delay_seconds: int = _seconds("APP_LOAD_DELAY_SECONDS", 5)
    reply_delay_seconds: int = _seconds("REPLY_DELAY_SECONDS", 1)
    whatsapp_web_icon: tuple[int, int] = parse_coordinates(os.getenv("WHATSAPP_WEB_ICON"), (1134, 1036))
    right_click_position: tuple[int, int] = parse_coordinates(os.getenv("RIGHT_CLICK_POSITION"), (639, 869))
    select_messages_option: tuple[int, int] = parse_coordinates(os.getenv("SELECT_MESSAGES_OPTION"), (704, 716))
    reply_box: tuple[int, int] = parse_coordinates(os.getenv("REPLY_BOX"), (1039, 970))


settings = Settings()
