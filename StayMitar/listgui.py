#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hotel Management - Guest List Viewer (Tkinter GUI)
Refactored & Clean Version
"""

import pickle
from tkinter import *
import tkinter.ttk as ttk


# -----------------------------
# Data Model
# -----------------------------
class Booking:
    """Represents a hotel booking record."""

    def __init__(self, name, address, mobile_no, room_no, price):
        self.name = name
        self.address = address
        self.mobile_no = mobile_no
        self.room_no = room_no
        self.price = price


# -----------------------------
# Main Application
# -----------------------------
class GuestListApp:
    """Displays list of all guests and their room numbers."""

    def __init__(self):
        self.guest_names = []
        self.room_numbers = []

        self.load_data()

        # Tkinter Setup
        self.root = Tk()
        self.root.geometry("800x550")
        self.root.title("Hotel Management - Guest List")
        self.root.configure(background="white")

        self.setup_ui()
        self.root.mainloop()

    # -----------------------------
    # Load Data
    # -----------------------------
    def load_data(self):
        """Load guest data from hotel.dat."""
        try:
            with open("hotel.dat", "rb") as f:
                while True:
                    try:
                        record = pickle.load(f)
                        self.guest_names.append(record.name.upper())
                        self.room_numbers.append(record.room_no)
                    except EOFError:
                        break
        except FileNotFoundError:
            self.guest_names = []
            self.room_numbers = []

    # -----------------------------
    # GUI Setup
    # -----------------------------
    def setup_ui(self):
        """Setup UI for listing guests and room numbers."""
        label_frame = LabelFrame(self.root,
                                 text="List of All Guests",
                                 font=("Segoe UI", 16, "bold"),
                                 bg="white")
        label_frame.place(relx=0.02, rely=0.05, relheight=0.9, relwidth=0.95)

        # Left frame → Guest Names
        frame_left = Frame(label_frame, bg="#f0f0f0", borderwidth=2, relief=GROOVE)
        frame_left.place(relx=0.03, rely=0.1, relheight=0.85, relwidth=0.45)

        Label(frame_left,
              text="Guest Names",
              font=("Segoe UI", 14, "bold"),
              bg="#f0f0f0").pack(pady=5)

        self.text_names = Text(frame_left, font=("Times New Roman", 14), wrap=WORD)
        self.text_names.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Right frame → Room Numbers
        frame_right = Frame(label_frame, bg="#f0f0f0", borderwidth=2, relief=GROOVE)
        frame_right.place(relx=0.52, rely=0.1, relheight=0.85, relwidth=0.45)

        Label(frame_right,
              text="Room Numbers",
              font=("Segoe UI", 14, "bold"),
              bg="#f0f0f0").pack(pady=5)

        self.text_rooms = Text(frame_right, font=("Times New Roman", 14), wrap=WORD)
        self.text_rooms.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Populate lists
        self.populate_lists()

    # -----------------------------
    # Populate UI
    # -----------------------------
    def populate_lists(self):
        """Insert guest names and room numbers into text areas."""
        for name in self.guest_names:
            self.text_names.insert(INSERT, name + "\n")

        for room in self.room_numbers:
            self.text_rooms.insert(INSERT, str(room) + "\n")


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    GuestListApp()
