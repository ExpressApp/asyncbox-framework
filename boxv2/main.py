"""Utility to create a project."""
from pathlib import Path
from typing import Optional
import shutil
from tempfile import mkdtemp
import click
from cookiecutter.main import cookiecutter  # type: ignore
from cookiecutter.exceptions import RepositoryNotFound, CookiecutterException
from boxv2.plugin import get_plugin_by_path


VERBOSE = False


@click.command()
@click.option("--verbose", "-v", is_flag=True)
@click.option("--plugin", "-p", multiple=True, default=["debug", "logger"])
@click.option("--template", "-t", required=False)
@click.argument("bot_name", nargs=1, type=click.Path(file_okay=False, dir_okay=False))
def main(plugin: list[str], template: Optional[str], bot_name: str, verbose: bool) -> None:
    """Create a bot project."""
    globals()["VERBOSE"] = verbose

    extra_context = {"bot_name": bot_name, "plugins": {"plugins_list": list(plugin)}}

    template_path = Path(__file__).parent / "template"
    cookiecutter(
        str(template_path), extra_context=extra_context, no_input=True
    )
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
        _print(f"Plugin `{plugin}` not found.")
        return

    template_path = plugin_class.get_template_path()
    try:
        cookiecutter(
            str(template_path), extra_context=extra_content, no_input=True, output_dir=temp_dir
        )
    except RepositoryNotFound:
        _print(f"Plugin `{plugin}` have no templates to render.")
        return
    shutil.copytree(temp_dir, ".", ignore=_copy_inspect, dirs_exist_ok=True)
    shutil.rmtree(temp_dir)


def render_extra_template(template: str, extra_content: dict[str, str]) -> None:
    """Render template to overwrite existing default."""
    temp_dir = Path(mkdtemp())
    try:
        cookiecutter(
            str(template), extra_context=extra_content, no_input=True, output_dir=temp_dir
        )
    except CookiecutterException as exc:
        _print(f"Cannot render template `{template}`.")
        _traceback(exc)
    shutil.copytree(temp_dir, ".", ignore=_copy_inspect, dirs_exist_ok=True)
    shutil.rmtree(temp_dir)


def _print(*args, **kwargs) -> None:
    if globals()["VERBOSE"]:
        print(*args, **kwargs)


def _traceback(exc: Exception) -> None:
    if globals()["VERBOSE"]:
        raise exc
    print("An error occurred. Add -v switch to verbose output.")
    raise SystemExit


def _copy_inspect(path: str, names: list[str]) -> set[str]:
    ignore = set()
    for name in names:
        if name != "__pycache__":
            print(f"Copying file {path}/{name}...")
        else:
            ignore.add(name)
    return ignore


if __name__ == "__main__":
    main()
