from __future__ import annotations

from .registry import ToolRegistry
from .system import OpenAppTool


registry = ToolRegistry([OpenAppTool()])
