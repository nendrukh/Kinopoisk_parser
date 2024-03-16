import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как нет файла .env")
else:
    load_dotenv()

COOKIE: str = os.getenv("COOKIE")
USER_AGENT: str = os.getenv("USER_AGENT")
