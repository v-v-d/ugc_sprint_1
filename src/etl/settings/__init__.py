import os

from etl.settings.base import CommonSettings
from etl.settings.dev import DevSettings
from etl.settings.prod import ProdSettings

settings_module = os.environ.get("SETTINGS", "prod")

settings_classes = {
    "dev": DevSettings,
    "prod": ProdSettings,
}

if settings_module not in settings_classes:
    expected = ", ".join(settings_classes)
    raise ValueError(
        f"Wrong SETTINGS env value! Expected {expected}, got {settings_module}."
    )

settings: CommonSettings = settings_classes[settings_module]()
