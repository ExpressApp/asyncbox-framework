from dotenv import load_dotenv

from asyncbox.tests.fixtures import credentials, environment

load_dotenv(".env")


__all__ = ["credentials", "environment"]
