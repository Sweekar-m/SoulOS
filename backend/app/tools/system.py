from __future__ import annotations

import platform
import shutil
import subprocess

from .base import Tool, ToolResult
from .schemas import OpenAppArguments


class OpenAppTool(Tool):
    name = "system.open_app"
    description = "Open an approved desktop application by name."
    arguments_model = OpenAppArguments

    # Explicit allowlist keeps raw LLM output away from shell execution.
    ALLOWED_APPS = {
        "calculator": ("calc.exe", "gnome-calculator", "kcalc"),
        "notepad": ("notepad.exe", "gedit", "kate"),
    }

    def execute(self, arguments: OpenAppArguments) -> ToolResult:
        app_name = arguments.app.strip().lower()
        candidates = self.ALLOWED_APPS.get(app_name)
        if not candidates:
            return ToolResult(success=False, error=f"application is not allowed: {app_name}")

        executable = next((candidate for candidate in candidates if shutil.which(candidate)), None)
        if executable is None:
            return ToolResult(success=False, error=f"application is unavailable: {app_name}")

        try:
            if platform.system() == "Windows":
                subprocess.Popen([executable], close_fds=True)
            else:
                subprocess.Popen([executable], close_fds=True)
        except OSError as exc:
            return ToolResult(success=False, error=f"failed to open application: {exc}")

        return ToolResult(
            success=True,
            output={"application": app_name},
            events=[{"type": "tool.completed", "tool": self.name}],
        )
