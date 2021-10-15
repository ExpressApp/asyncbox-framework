"""Base class for bot plugins."""

import inspect
from pathlib import Path
from typing import Any, Optional, Type

from botx import Bot
from botx.dependencies.models import Depends
from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings

from boxv2.utils.import_utils import import_object


class BasePluginSettings(BaseSettings):
    """Main settings for splitting."""

    class Config:  # noqa: WPS431
        env_file = ".env"
        json_loads = lambda x: x  # noqa: E731,WPS111


class HealtCheckData(BaseModel):
    """Data returning by plugin's healthcheck method."""

    healthy: Optional[bool] = None  # True - ok, False - error, None - not supported
    information: dict[str, Any] = {}


class BasePlugin:
    """Base class for plugins."""

    settings_class = BasePluginSettings
    dependencies: list[Depends] = []

    # Path to template dir is relative to the dir where plugin class defined
    template = Path("template")

    def __init__(self, settings: BaseSettings, application: FastAPI, bot: Bot) -> None:
        """Plugin initialization."""
        self.settings = settings
        self.application = application
        self.bot = bot
        self._merge_settings()

    async def on_startup(self, *args: Any, **kwargs: Any) -> None:
        """Startup hook."""

    async def on_shutdown(self, *args: Any, **kwargs: Any) -> None:
        """Shutdown hook."""

    async def healthcheck(self) -> HealtCheckData:
        """Runtime check for plugin functioning."""
        return HealtCheckData()

    @classmethod
    def get_template_path(cls) -> Path:
        """Absolute path to plugin's template directory."""
        plugin_path = Path(inspect.getfile(cls)).resolve().parents[0]
        return plugin_path / cls.template

    @classmethod
    def get_name(cls) -> str:
        """Get plugin's name."""
        module = inspect.getmodule(cls)
        if module is not None:
            return module.__name__.split(".")[-2]
        return cls.__name__.lower()

    def _merge_settings(self) -> None:  # noqa: WPS231
        app_values = {}
        for key in self.settings.__fields__:
            if key not in self.settings_class.__fields__:
                continue
            field = self.settings_class.__fields__[key]
            field_required = field.required
            fied_has_default = field.default is not None
            value_is_none = getattr(self.settings, key) is None
            if (field_required or fied_has_default) and value_is_none:
                continue
            app_values[key] = getattr(self.settings, key)

        plugin_settings = self.settings_class(**app_values)
        for field_name in plugin_settings.__fields__:  # noqa: WPS609
            self.settings.__dict__[field_name] = getattr(plugin_settings, field_name)


def get_plugin_by_path(plugin_path: str) -> Type[BasePlugin]:
    """Return plugin's class from list it's path."""

    # add default plugin class name if it is not explicitly defined
    if ":" not in plugin_path:
        plugin_path = f"{plugin_path}:Plugin"

    return import_object(plugin_path)
