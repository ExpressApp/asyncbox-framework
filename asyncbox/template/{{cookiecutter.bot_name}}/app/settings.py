"""Application settings."""

from typing import List

from asyncbox.settings import BaseAppSettings


class AppSettings(BaseAppSettings):
    """Application settings."""

    NAME = "{{cookiecutter.bot_name}}"
    PLUGINS: List[str] = [
        {% for plugin in cookiecutter.plugins.plugins_list %}
        "asyncbox.plugins.{{ plugin }}",
        {% endfor %}
    ]
    COLLECTORS: List[str] = [
        "app.commands:collector",
    ]
