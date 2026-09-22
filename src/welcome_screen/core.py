"""Core business logic for the WelcomeScreen application."""

from __future__ import annotations

import getpass
import platform
import sys
from datetime import datetime
from typing import Dict, Any


def get_time_greeting(now: datetime | None = None) -> str:
    """Return a contextual greeting based on the time of day."""
    if now is None:
        now = datetime.now()
    
    hour = now.hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"


def get_system_info() -> Dict[str, Any]:
    """Retrieve basic environment and system details."""
    try:
        username = getpass.getuser()
    except Exception:
        username = "User"

    return {
        "username": username,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "python_version": sys.version.split()[0],
        "architecture": platform.machine(),
    }


class WelcomeManager:
    """Manages application state and sample actions."""

    def __init__(self, username: str | None = None):
        sys_info = get_system_info()
        self.username = username or sys_info["username"]
        self.system_info = sys_info
        self.recent_projects: list[str] = [
            "Project Alpha (Demo)",
            "Data Analytics Workflow",
            "Web Automation Bot",
        ]

    def get_welcome_message(self) -> str:
        greeting = get_time_greeting()
        return f"{greeting}, {self.username}! Welcome to your Python App."

    def add_project(self, project_name: str) -> None:
        if project_name and project_name not in self.recent_projects:
            self.recent_projects.insert(0, project_name)
