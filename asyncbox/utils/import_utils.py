"""Helper functions to import plugins."""

from importlib import import_module
from typing import Any


def import_object(object_path: str) -> Any:
    module_path, object_name = object_path.split(":")
    return getattr(import_module(module_path), object_name)
