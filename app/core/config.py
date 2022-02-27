from functools import lru_cache
from .settings.app import AppSettings

@lru_cache()
def get_settings():
    return AppSettings()