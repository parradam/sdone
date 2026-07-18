"""Shared Jinja2 templating configuration.

Feature specs extend the environment on this instance (e.g. spec 003 registers
the ``highlight_todo`` filter).
"""

from pathlib import Path

from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
