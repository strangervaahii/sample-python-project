"""Command-line interface for the Welcome Screen application."""

from __future__ import annotations

from welcome_screen.core import WelcomeManager, get_system_info


def run_cli() -> None:
    """Run interactive terminal welcome interface."""
    manager = WelcomeManager()
    
    print("=" * 55)
    print(f"  {manager.get_welcome_message()}")
    print("=" * 55)

    sys_info = get_system_info()
    print("\n[System Info]")
    for key, value in sys_info.items():
        print(f"  - {key.replace('_', ' ').title():<18}: {value}")

    print("\n[Recent Projects]")
    for idx, proj in enumerate(manager.recent_projects, 1):
        print(f"  {idx}. {proj}")

    print("\nType 'help' for options or 'exit' to quit.")
    while True:
        try:
            cmd = input("\nWelcomeApp> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not cmd:
            continue
        elif cmd in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        elif cmd == "help":
            print("Available commands:")
            print("  list         - Show recent projects")
            print("  new <name>   - Add a new project")
            print("  info         - Print system information")
            print("  help         - Show this help menu")
            print("  exit         - Exit the program")
        elif cmd == "list":
            print("\nRecent Projects:")
            for idx, proj in enumerate(manager.recent_projects, 1):
                print(f"  {idx}. {proj}")
        elif cmd.startswith("new "):
            name = cmd[4:].strip()
            if name:
                manager.add_project(name)
                print(f"✓ Added project: '{name}'")
            else:
                print("Please provide a project name. Usage: new <name>")
        elif cmd == "info":
            for key, value in get_system_info().items():
                print(f"  - {key.replace('_', ' ').title():<18}: {value}")
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for a list of commands.")
