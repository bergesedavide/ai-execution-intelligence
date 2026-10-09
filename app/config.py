import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.environ["DATABASE_URL"]

OLLAMA_HOST = os.environ.get(
    "OLLAMA_HOST",
    "http://localhost:11435",
)

ANALYZER_MODEL = os.environ.get(
    "ANALYZER_MODEL",
    "llama3.1:8b",
)