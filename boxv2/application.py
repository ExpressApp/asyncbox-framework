"""Functions to make bot application."""

import os
from typing import Any, Callable, List, Optional

from botx import Bot, Collector
from fastapi import FastAPI

from boxv2.endpoints import get_router
from boxv2.plugin import get_plugin_by_path
from boxv2.settings import BaseAppSettings
from boxv2.utils.import_utils import import_object


def get_application(settings: Optional[BaseAppSettings] = None) -> FastAPI:
    """Create configured server application instance."""
    if settings is None:
        settings = get_app_settings()

    application = FastAPI(title=settings.NAME)
    plugin_classes = [get_plugin_by_path(plugin) for plugin in settings.PLUGINS]
    dependencies = _flatten_list(
        [plugin_class.dependencies for plugin_class in plugin_classes]
    )

    bot = Bot(  # type: ignore
        bot_accounts=settings.BOT_CREDENTIALS,
        dependencies=dependencies,
    )
    application.state = bot.state  # type: ignore
    application.state.settings = settings
    application.state.bot_name = settings.NAME
    application.state.bot = bot
    plugin_instances = [plugin(settings, application, bot) for plugin in plugin_classes]
    application.state.plugins = plugin_instances

    application.add_event_handler("startup", bot_startup(bot))
    application.add_event_handler("shutdown", bot_shutdown(bot))

    for plugin in plugin_instances:
        setattr(application.state, plugin.get_name(), plugin)
        application.add_event_handler("startup", plugin.on_startup)
        application.add_event_handler("shutdown", plugin.on_shutdown)

    collectors = get_collectors(settings)
    for collector in collectors:
        bot.include_collector(collector)

    router = get_router(bot)
    application.include_router(router)

    return application


def bot_startup(bot: Bot) -> Callable:
    """Bot startup event handler."""

    async def startup() -> None:  # noqa: WPS430
        await bot.start()

    return startup


def bot_shutdown(bot: Bot) -> Callable:
    """Bot shutdown event handler."""

    async def shutdown() -> None:  # noqa: WPS430
        await bot.shutdown()

    return shutdown


def get_app_settings() -> BaseAppSettings:
    """Return instance of the AppSettings object."""
    settings_path = os.environ.get("APP_SETTINGS") or "app.settings:AppSettings"
    settings_class = import_object(settings_path)
    return settings_class()


def get_collectors(settings: BaseAppSettings) -> list[Collector]:
    """Return list of registered Collectors."""
    return [import_object(collector_path) for collector_path in settings.COLLECTORS]


def _flatten_list(list_: List[List[Any]]) -> list[Any]:
    return [element for sublist in list_ for element in sublist]
