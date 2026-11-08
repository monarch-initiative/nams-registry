"""Put the NAMO schema in place before any test loads the registry schema."""

import importlib.util
from pathlib import Path

_script = Path(__file__).resolve().parent.parent / "scripts" / "link_namo.py"
_spec = importlib.util.spec_from_file_location("link_namo", _script)
_link_namo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_link_namo)
_link_namo.main(quiet=True)
