"""Application settings."""

from asyncbox.settings import BaseAppSettings


class AppSettings(BaseAppSettings):
    """Application settings."""

    NAME = "{{cookiecutter.bot_name}}"
    PLUGINS: list[str] = [
        {%- for plugin in cookiecutter.plugins.plugins_list %}
        "asyncbox.plugins.{{ plugin }}",
        {%- endfor %}
    ]
    COLLECTORS: list[str] = [
        "app.commands:collector",
    ]
