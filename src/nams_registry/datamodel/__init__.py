"""Data model package for nams-registry."""

from pathlib import Path
from .nam_resources import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "nam_resources.yaml"
NAM_SCHEMA_PATH = SCHEMA_DIRECTORY / "nam_records.yaml"
