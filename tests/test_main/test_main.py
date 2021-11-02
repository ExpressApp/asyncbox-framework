import pytest
from itertools import combinations
from shutil import rmtree
from asyncbox.main import make_project

plugins = ["debug", "logger", "prometheus", "redis", "sentry", "sqlalchemy"]


@pytest.mark.parametrize("plugins_list", combinations(plugins, 3))
def test_template(plugins_list: list[str]):
    bot_name = "test_bot_project_" + "_".join(plugins)
    make_project(plugin=plugins_list, template=None, bot_name=bot_name, verbose=2)
    rmtree(bot_name, ignore_errors=True)
