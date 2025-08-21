#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hotel Management - Get Guest Info (Tkinter GUI)
Refactored & Clean Version
"""

import os
import sys
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
class GetInfoApp:
    """Main application for retrieving guest info by room number."""

    def __init__(self):
        self.root = Tk()
        self.root.geometry("900x600")
        self.root.title("Hotel Management - Guest Info")
        self.root.configure(background="#d9d9d9")

        self.room_input = StringVar()
        self.setup_ui()
        self.root.mainloop()

    # -----------------------------
    # GUI Setup
    # -----------------------------
    def setup_ui(self):
        """Setup all UI components."""
        frame = Frame(self.root, bg="#d9d9d9", borderwidth=2, relief=GROOVE)
        frame.place(relx=0.02, rely=0.03, relheight=0.94, relwidth=0.94)

        # Title
        Message(frame,
                text="GET INFO HERE ..!!",
                font=("Segoe UI", 28, "bold"),
                bg="#d9d9d9",
                width=460).place(relx=0.22, rely=0.02, relheight=0.12, relwidth=0.56)

        # Label
        Label(frame,
              text="Enter Room No.:",
              font=("Segoe UI", 20, "bold"),
              bg="#d9d9d9").place(relx=0.12, rely=0.15, height=48, width=377)

        # Entry
        Entry(frame,
              textvariable=self.room_input,
              font=("Segoe UI", 14),
              bg="white").place(relx=0.65, rely=0.17, height=40, relwidth=0.1)

        # Submit button
        Button(frame,
               text="SUBMIT",
               font=("Segoe UI", 17, "bold"),
               bg="#d9d9d9",
               command=self.get_info).place(relx=0.39, rely=0.29, height=74, width=197)

        # Output text area
        self.console = Text(frame,
                            background="white",
                            foreground="black",
                            wrap=WORD,
                            font=("Segoe UI", 12))
        self.console.place(relx=0.04, rely=0.46, relheight=0.48, relwidth=0.93)

    # -----------------------------
    # Business Logic
    # -----------------------------
    def get_info(self):
        """Fetch guest info for a given room number."""
        room_str = self.room_input.get().strip()

        # Validate input
        if not room_str.isdigit():
            self.console.insert(INSERT, "❌ Invalid room number!\n")
            return

        room_no = int(room_str)
        found = False

        try:
            with open("hotel.dat", "rb") as f:
                while True:
                    try:
                        booking = pickle.load(f)
                        if booking.room_no == room_no:
                            found = True
                            self.display_info(booking)
                            break
                    except EOFError:
                        break
        except FileNotFoundError:
            self.console.insert(INSERT, "⚠️ No booking records found.\n")
            return

        if not found:
            self.console.insert(INSERT, f"❌ No guest found in room {room_no}\n")

    def display_info(self, booking):
        """Display booking info in the console box."""
        self.console.insert(INSERT, f"✅ Guest Found in Room {booking.room_no}\n")
        self.console.insert(INSERT, f"   Name: {booking.name}\n")
        self.console.insert(INSERT, f"   Address: {booking.address}\n")
        self.console.insert(INSERT, f"   Mobile: {booking.mobile_no}\n")
        self.console.insert(INSERT, f"   Total Bill: ₹{booking.price}\n\n")


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    GetInfoApp()
