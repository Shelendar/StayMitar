#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hotel Management - Checkout System (Tkinter GUI)
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
# Utility Functions
# -----------------------------
def restart_program():
    """Restart the current Python program."""
    python = sys.executable
    os.execl(python, python, *sys.argv)


# -----------------------------
# Main Checkout Application
# -----------------------------
class CheckoutApp:
    """Main application class for Hotel Checkout."""

    def __init__(self):
        # Tkinter setup
        self.root = Tk()
        self.root.geometry("1011x750")
        self.root.title("Hotel Management - Checkout")
        self.root.configure(background="white")

        self.data = StringVar()
        self.setup_ui()

        self.root.mainloop()

    # -----------------------------
    # GUI Setup
    # -----------------------------
    def setup_ui(self):
        """Setup all checkout window UI components."""
        frame = Frame(self.root, bg="white", borderwidth=2, relief=GROOVE)
        frame.place(relx=0.04, rely=0.04, relheight=0.91, relwidth=0.91)

        # Label
        Label(frame,
              text="Enter Room No.:",
              font=("Segoe UI", 23, "bold"),
              bg="white").place(relx=0.14, rely=0.12, height=46, width=442)

        # Entry for room number
        Entry(frame,
              textvariable=self.data,
              font=("Courier New", 12),
              bg="white").place(relx=0.67, rely=0.12, height=44, relwidth=0.07)

        # Checkout Button
        Button(frame,
               text="CHECK OUT",
               font=("Segoe UI", 24, "bold"),
               bg="white",
               command=self.check_room).place(relx=0.34, rely=0.28, height=93, width=286)

        # Output text area
        self.console = Text(frame,
                            background="white",
                            foreground="black",
                            wrap=WORD,
                            font=("Segoe UI", 10))
        self.console.place(relx=0.05, rely=0.54, relheight=0.4, relwidth=0.89)

    # -----------------------------
    # Business Logic
    # -----------------------------
    def check_room(self):
        """Validate and process checkout for entered room number."""
        room_str = self.data.get().strip()

        if not room_str.isdigit():
            self.console.insert(INSERT, "Invalid input! Please enter a valid room number.\n")
            return

        room_no = int(room_str)
        guest_found = False
        guest_name = ""

        try:
            with open("hotel.dat", "rb") as infile, open("temp.dat", "ab") as outfile:
                while True:
                    try:
                        record = pickle.load(infile)
                        if record.room_no == room_no:
                            guest_found = True
                            guest_name = record.name
                            # Do not copy this record → removing guest
                        else:
                            pickle.dump(record, outfile)
                    except EOFError:
                        break
        except FileNotFoundError:
            self.console.insert(INSERT, "No booking records found.\n")
            return

        # Replace old file with updated one
        os.remove("hotel.dat")
        os.rename("temp.dat", "hotel.dat")

        if guest_found:
            self.console.insert(INSERT, f"Thank you {guest_name.upper()} for visiting us!\n")
        else:
            self.console.insert(INSERT, "No guest found with this room number.\n")


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    CheckoutApp()
