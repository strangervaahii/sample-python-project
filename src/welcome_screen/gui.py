"""Modern Tkinter GUI Welcome Screen."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from welcome_screen.core import WelcomeManager, get_system_info


class WelcomeScreenApp:
    """Tkinter-based Welcome Screen window."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Welcome Screen")
        self.root.geometry("640x480")
        self.root.minsize(520, 400)
        self.manager = WelcomeManager()

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Color palette
        self.bg_color = "#f5f6f8"
        self.card_bg = "#ffffff"
        self.primary_color = "#2563eb"
        self.text_color = "#1f2937"
        self.muted_color = "#6b7280"

        self.root.configure(bg=self.bg_color)
        style.configure("TFrame", background=self.bg_color)
        style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            background=self.primary_color,
            foreground="#ffffff",
            padding=(12, 6),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#1d4ed8")],
            foreground=[("active", "#ffffff")],
        )

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Header Section
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = tk.Label(
            header_frame,
            text=self.manager.get_welcome_message(),
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w",
        )
        title_label.pack(fill=tk.X)

        sys_info = self.manager.system_info
        subtitle_text = f"Python {sys_info['python_version']} on {sys_info['platform']} ({sys_info['architecture']})"
        subtitle_label = tk.Label(
            header_frame,
            text=subtitle_text,
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.muted_color,
            anchor="w",
        )
        subtitle_label.pack(fill=tk.X, pady=(2, 0))

        # Main Content Grid
        content_frame = ttk.Frame(container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)

        # Left Column: Recent Projects Card
        left_card = ttk.Frame(content_frame, style="Card.TFrame", padding=15)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        projects_title = tk.Label(
            left_card,
            text="Recent Projects",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
        )
        projects_title.pack(anchor="w", pady=(0, 10))

        self.projects_listbox = tk.Listbox(
            left_card,
            font=("Segoe UI", 10),
            bg="#fbfcfd",
            fg=self.text_color,
            selectbackground=self.primary_color,
            selectforeground="#ffffff",
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
        )
        self.projects_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self._refresh_projects()

        open_btn = ttk.Button(
            left_card,
            text="Open Selected Project",
            command=self._open_project,
        )
        open_btn.pack(fill=tk.X)

        # Right Column: Quick Actions Card
        right_card = ttk.Frame(content_frame, style="Card.TFrame", padding=15)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        actions_title = tk.Label(
            right_card,
            text="Quick Actions",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.text_color,
        )
        actions_title.pack(anchor="w", pady=(0, 15))

        new_proj_btn = ttk.Button(
            right_card,
            text="✨ New Project",
            style="Primary.TButton",
            command=self._new_project,
        )
        new_proj_btn.pack(fill=tk.X, pady=4)

        info_btn = ttk.Button(
            right_card,
            text="ℹ System Info",
            command=self._show_info,
        )
        info_btn.pack(fill=tk.X, pady=4)

        about_btn = ttk.Button(
            right_card,
            text="📖 About App",
            command=self._show_about,
        )
        about_btn.pack(fill=tk.X, pady=4)

        exit_btn = ttk.Button(
            right_card,
            text="🚪 Exit",
            command=self.root.quit,
        )
        exit_btn.pack(fill=tk.X, pady=(15, 4))

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            container,
            textvariable=self.status_var,
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg=self.muted_color,
            anchor="w",
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def _refresh_projects(self) -> None:
        self.projects_listbox.delete(0, tk.END)
        for proj in self.manager.recent_projects:
            self.projects_listbox.insert(tk.END, f"  📁 {proj}")

    def _new_project(self) -> None:
        name = simpledialog.askstring("New Project", "Enter project name:", parent=self.root)
        if name:
            self.manager.add_project(name.strip())
            self._refresh_projects()
            self.status_var.set(f"Created project: {name.strip()}")

    def _open_project(self) -> None:
        selection = self.projects_listbox.curselection()
        if not selection:
            messagebox.showinfo("Select Project", "Please select a project from the list.", parent=self.root)
            return
        project_name = self.manager.recent_projects[selection[0]]
        messagebox.showinfo("Project Opened", f"Opening: {project_name}", parent=self.root)
        self.status_var.set(f"Opened: {project_name}")

    def _show_info(self) -> None:
        info = get_system_info()
        details = "\n".join(f"• {k.replace('_', ' ').title()}: {v}" for k, v in info.items())
        messagebox.showinfo("System Information", details, parent=self.root)

    def _show_about(self) -> None:
        messagebox.showinfo(
            "About Welcome Screen",
            "Welcome Screen Sample Application\nVersion 1.0.0\n\nBuilt with Python & Tkinter.",
            parent=self.root,
        )


def run_gui() -> None:
    """Launch the GUI Welcome Screen."""
    root = tk.Tk()
    _ = WelcomeScreenApp(root)
    root.mainloop()
