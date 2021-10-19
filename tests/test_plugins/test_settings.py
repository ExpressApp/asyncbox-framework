from typing import Optional

import pytest
from pydantic.error_wrappers import ValidationError

from asyncbox.plugin import BasePlugin, BasePluginSettings
from asyncbox.settings import BaseAppSettings


class AppSettings(BaseAppSettings):
    REQ_STR: Optional[str] = None


class PluginSettings0(BasePluginSettings):
    REQ_STR: str


class PluginSettings1(BasePluginSettings):
    REQ_STR: str = "default value"


class Plugin0(BasePlugin):
    settings_class = PluginSettings0


class Plugin1(BasePlugin):
    settings_class = PluginSettings1


def test_required_setting_no_default(environment) -> None:
    """Plugin requires a setting, but application do not sets it."""
    app_settings = AppSettings()
    with pytest.raises(ValidationError):
        Plugin0(app_settings, None, None)


def test_required_setting_with_default(environment) -> None:
    """Plugin have a setting with default and application do not sets it."""
    app_settings = AppSettings()
    plugin1 = Plugin1(app_settings, None, None)
    assert plugin1.settings.REQ_STR == "default value"


def test_setting_replacement(environment) -> None:
    """Plugin have a setting with default and application replace it's value."""
    app_settings = AppSettings(REQ_STR="new value")
    plugin1 = Plugin1(app_settings, None, None)
    assert plugin1.settings.REQ_STR == "new value"
