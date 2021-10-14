"""Utility to create a project."""
import shutil
import sys
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional

import click
from cookiecutter.exceptions import CookiecutterException, RepositoryNotFound
from cookiecutter.main import cookiecutter  # type: ignore
from loguru import logger

from boxv2.plugin import get_plugin_by_path


@click.command()
@click.option("--verbose", "-v", count=True)
@click.option("--plugin", "-p", multiple=True, default=["debug", "logger"])
@click.option("--template", "-t", required=False)
@click.argument("bot_name", nargs=1, type=click.Path())
def main(
    plugin: list[str], template: Optional[str], bot_name: str, verbose: int
) -> None:
    """Create a bot project."""
    if Path(bot_name).exists():
        raise click.UsageError(f"Directory `{bot_name}` already exists.")
    logger.remove()
    logger.add(sys.stderr, level=_get_logger_level(verbose))

    extra_context = {"bot_name": bot_name, "plugins": {"plugins_list": list(plugin)}}

    template_path = Path(__file__).parent / "template"
    cookiecutter(str(template_path), extra_context=extra_context, no_input=True)
    if template is not None:
        render_extra_template(template, extra_context)
    for plg in plugin:
        render_plugins_template(plg, extra_context)


def render_plugins_template(plugin: str, extra_content: dict[str, str]) -> None:
    """Render plugin's template (if exists) and add it to project."""
    temp_dir = Path(mkdtemp())

    try:
        plugin_class = get_plugin_by_path(f"boxv2.plugins.{plugin}")
    except ImportError:
        logger.warning(f"Plugin `{plugin}` not found.")
        return

    template_path = plugin_class.get_template_path()
    try:
        cookiecutter(
            str(template_path),
            extra_context=extra_content,
            no_input=True,
            output_dir=temp_dir,
        )
    except RepositoryNotFound:
        logger.info(f"Plugin `{plugin}` have no templates to render.")
        return
    shutil.copytree(temp_dir, ".", ignore=_copy_inspect, dirs_exist_ok=True)
    shutil.rmtree(temp_dir)


def render_extra_template(template: str, extra_content: dict[str, str]) -> None:
    """Render template to overwrite existing default."""
    temp_dir = Path(mkdtemp())
    try:
        cookiecutter(
            str(template),
            extra_context=extra_content,
            no_input=True,
            output_dir=temp_dir,
        )
    except CookiecutterException:
        logger.exception(f"Cannot render template `{template}`.")
    shutil.copytree(temp_dir, ".", ignore=_copy_inspect, dirs_exist_ok=True)
    shutil.rmtree(temp_dir)


def _copy_inspect(path: str, names: list[str]) -> set[str]:
    ignore = set()
    for name in names:
        if name != "__pycache__":
            logger.debug(f"Copying file {path}/{name}...")
        else:
            ignore.add(name)
    return ignore


def _get_logger_level(int_level: int) -> str:
    """Make Loguru level from int."""
    if int_level >= 3:
        return "TRACE"
    elif int_level == 2:
        return "DEBUG"
    elif int_level == 1:
        return "INFO"
    else:
        return "WARNING"


if __name__ == "__main__":
    main()
