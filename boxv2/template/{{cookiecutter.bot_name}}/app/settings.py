"""Application settings."""

from typing import List

from boxv2.settings import BaseAppSettings


class AppSettings(BaseAppSettings):
    """Application settings."""

    NAME = "{{cookiecutter.bot_name}}"
    PLUGINS: List[str] = [
        {% for plugin in cookiecutter.plugins.plugins_list %}
        "boxv2.plugins.{{ plugin }}",
        {% endfor %}
    ]
    COLLECTORS: List[str] = [
        "app.commands:collector",
    ]
