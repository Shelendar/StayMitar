#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hotel Management - Receipt Viewer (Tkinter GUI)
Refactored & Clean Version
"""

import os
import tkinter as tk
from tkinter import messagebox


# -----------------------------
# Utility to Load Receipt Data
# -----------------------------
def load_receipt_data(filename="recipt.txt"):
    """Load receipt details from file and return as a dict."""
    if not os.path.exists(filename):
        messagebox.showerror("Error", f"Receipt file '{filename}' not found.")
        return None

    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # Expecting: Name, Address, Mobile, Room, Price
        data = {
            "name": lines[0],
            "address": lines[1],
            "mobile": lines[2],
            "room": lines[3],
            "price": lines[4],
        }
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load receipt: {e}")
        return None


# -----------------------------
# Receipt Window
# -----------------------------
class ReceiptWindow:
    """Tkinter GUI to display hotel receipt."""

    def __init__(self, root, data):
        self.root = root
        self.root.title("Hotel Receipt")
        self.root.geometry("600x500")
        self.root.configure(bg="white")

        self.data = data
        self.setup_ui()

    def setup_ui(self):
        """Setup UI components for receipt display."""

        # Title
        tk.Label(
            self.root,
            text="🏨 PROJECTWORLDS HOTEL & RESORTS 🏨",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="black",
            pady=15
        ).pack()

        tk.Label(
            self.root,
            text="📍 Bhilai, Chhattisgarh | Serving Guests Since 2000",
            font=("Segoe UI", 12, "italic"),
            bg="white",
            fg="gray"
        ).pack(pady=(0, 20))

        # Receipt details frame
        frame = tk.Frame(self.root, bg="#f9f9f9", bd=2, relief="solid")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        details = [
            ("Guest Name", self.data["name"]),
            ("Address", self.data["address"]),
            ("Mobile No.", self.data["mobile"]),
            ("Room Number", self.data["room"]),
            ("Total Bill", f"₹ {self.data['price']}"),
        ]

        for i, (label, value) in enumerate(details):
            tk.Label(
                frame, text=f"{label}:", font=("Segoe UI", 14, "bold"),
                bg="#f9f9f9", anchor="w"
            ).grid(row=i, column=0, sticky="w", padx=10, pady=8)

            tk.Label(
                frame, text=value, font=("Segoe UI", 14),
                bg="#f9f9f9", anchor="w"
            ).grid(row=i, column=1, sticky="w", padx=10, pady=8)

        # Footer
        tk.Label(
            self.root,
            text="✨ Thank you for choosing ProjectWorlds Hotel ✨",
            font=("Segoe UI", 12, "italic"),
            bg="white",
            fg="black",
            pady=15
        ).pack(side="bottom")


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    data = load_receipt_data()
    if data:
        root = tk.Tk()
        app = ReceiptWindow(root, data)
        root.mainloop()
