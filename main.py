"""Main entry point for WelcomeScreen application."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add src to sys.path so welcome_screen package is discoverable
sys.path.insert(0, str(Path(__file__).parent / "src"))

from welcome_screen.cli import run_cli
from welcome_screen.gui import run_gui


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Welcome Screen Sample Application"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in command-line interface mode instead of GUI",
    )
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        try:
            run_gui()
        except Exception as exc:
            print(f"Failed to launch GUI ({exc}). Falling back to CLI mode.\n")
            run_cli()


if __name__ == "__main__":
    main()
