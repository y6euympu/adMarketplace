from dataclasses import dataclass
from dotenv import load_dotenv

from os import path, environ

from .singleton import Singleton


project_folder = path.dirname(path.dirname(path.abspath(__file__)))
load_dotenv(path.join(project_folder, ".env"))

@dataclass(frozen=True)
class Settings(metaclass=Singleton):
    DATABASE_URL: str = environ.get("DATABASE_URL")

    BOT_TOKEN: str = environ.get("BOT_TOKEN")

    TELEGRAM_APPLICATION_API_HASH : str = environ.get("TELEGRAM_APPLICATION_API_HASH")
    TELEGRAM_APPLICATION_API_ID : int = int(environ.get("TELEGRAM_APPLICATION_API_ID"))

    TONCENTER_API_KEY : str = environ.get("TONCENTER_API_KEY")


    PATH = project_folder


settings = Settings()