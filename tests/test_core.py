"""Unit tests for WelcomeScreen core logic."""

import unittest
from datetime import datetime
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from welcome_screen.core import get_time_greeting, get_system_info, WelcomeManager


class TestCore(unittest.TestCase):
    def test_get_time_greeting(self):
        # Morning (08:00)
        morning_dt = datetime(2026, 1, 1, 8, 0, 0)
        self.assertEqual(get_time_greeting(morning_dt), "Good morning")

        # Afternoon (14:00)
        afternoon_dt = datetime(2026, 1, 1, 14, 0, 0)
        self.assertEqual(get_time_greeting(afternoon_dt), "Good afternoon")

        # Evening (19:00)
        evening_dt = datetime(2026, 1, 1, 19, 0, 0)
        self.assertEqual(get_time_greeting(evening_dt), "Good evening")

        # Night (23:00)
        night_dt = datetime(2026, 1, 1, 23, 0, 0)
        self.assertEqual(get_time_greeting(night_dt), "Good night")

    def test_get_system_info(self):
        info = get_system_info()
        self.assertIn("username", info)
        self.assertIn("platform", info)
        self.assertIn("python_version", info)
        self.assertIn("architecture", info)

    def test_welcome_manager(self):
        mgr = WelcomeManager(username="Alice")
        self.assertEqual(mgr.username, "Alice")
        msg = mgr.get_welcome_message()
        self.assertIn("Alice", msg)

        # Adding new project
        initial_count = len(mgr.recent_projects)
        mgr.add_project("New Test Project")
        self.assertEqual(len(mgr.recent_projects), initial_count + 1)
        self.assertEqual(mgr.recent_projects[0], "New Test Project")


if __name__ == "__main__":
    unittest.main()
