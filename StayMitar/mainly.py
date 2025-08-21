
# -*- coding: utf-8 -*-
"""
Hotel Management System - Main Menu (Tkinter GUI)
Refactored & Clean Version
"""

import subprocess
import tkinter as tk
from tkinter import ttk


# -----------------------------
# Utility Functions
# -----------------------------
def open_checkin():
    subprocess.call(["python", "checkin_gui_and_program.py"])


def open_guest_list():
    subprocess.call(["python", "listgui.py"])


def open_checkout():
    subprocess.call(["python", "checkoutgui.py"])


def open_get_info():
    subprocess.call(["python", "getinfoui.py"])


# -----------------------------
# Main Menu Class
# -----------------------------
class HotelManagementApp:
    """Main menu window for Hotel Management."""

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f2f2f2")

        self.setup_ui()

    def setup_ui(self):
        """Setup the main menu UI components."""

        # Title
        tk.Label(
            self.root,
            text="🏨 WELCOME TO HOTEL MANAGEMENT SYSTEM 🏨",
            font=("Segoe UI", 24, "bold"),
            bg="#f2f2f2",
            fg="black",
            pady=20
        ).pack()

        # Frame for buttons
        frame = tk.Frame(self.root, bg="#f2f2f2")
        frame.pack(pady=40)

        # Menu buttons
        buttons = [
            ("1. Check In", open_checkin),
            ("2. Show Guest List", open_guest_list),
            ("3. Check Out", open_checkout),
            ("4. Get Info of Guest", open_get_info),
            ("5. Exit", self.root.quit),
        ]

        for text, command in buttons:
            b = tk.Button(
                frame,
                text=text,
                command=command,
                font=("Segoe UI", 16, "bold"),
                bg="#4CAF50" if "Exit" not in text else "#f44336",
                fg="white",
                activebackground="#45a049",
                activeforeground="white",
                relief="raised",
                bd=3,
                width=30,
                height=2
            )
            b.pack(pady=15)

        # Footer
        tk.Label(
            self.root,
            text="Developed with ❤️ using Python & Tkinter",
            font=("Segoe UI", 10, "italic"),
            bg="#f2f2f2",
            fg="gray"
        ).pack(side="bottom", pady=10)


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
