import os
import requests

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://backend:8000")


def get_health() -> dict:
    response = requests.get(f"{BACKEND_BASE_URL}/health", timeout=5)
    response.raise_for_status()
    return response.json()
