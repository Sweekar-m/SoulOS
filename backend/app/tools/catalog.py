from __future__ import annotations

from backend.app.tools.presentation import PRESENTATION_TOOLS
from backend.app.tools.search import WEB_TOOLS
from backend.app.tools.system import OpenAppTool


def builtin_tools():
    """Return the explicit built-in tool set in a deterministic order."""
    return (OpenAppTool(), *WEB_TOOLS, *PRESENTATION_TOOLS)
