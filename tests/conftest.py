from dotenv import load_dotenv

from boxv2.tests.fixtures import credentials, environment

load_dotenv(".env")


__all__ = ["credentials", "environment"]
