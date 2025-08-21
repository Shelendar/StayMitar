#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hotel Management - Check-in System (Tkinter GUI)
Cleaned & Refactored Version
"""

import os
import sys
import pickle
from subprocess import call
from tkinter import *
import tkinter.ttk as ttk

# -----------------------------
# Global Data & Constants
# -----------------------------
details_list = []

ROOM_TYPES = {
    1: {"name": "Deluxe", "price": 2000, "rooms": tuple(range(1, 11))},
    2: {"name": "Semi-Deluxe", "price": 1500, "rooms": tuple(range(11, 26))},
    3: {"name": "General", "price": 1000, "rooms": tuple(range(26, 46))},
    4: {"name": "Joint", "price": 1700, "rooms": (46, 47, 48, 49, 50)},
}

discount_methods = {
    1: {"name": "Cash", "discount": 0},
    2: {"name": "Credit/Debit Card", "discount": 10},
}


# -----------------------------
# Utility Functions
# -----------------------------
def restart_program():
    """Restart the current Python program."""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def save_booking(name, address, mobile, room_no, price):
    """Save booking details to file."""
    booking = Booking(name, address, mobile, room_no, price)

    # Save in binary file
    with open("hotel.dat", "ab") as f:
        pickle.dump(booking, f, protocol=2)

    # Save receipt
    with open("receipt.txt", "w+") as fo:
        for line in [name, address, mobile, str(room_no), str(price)]:
            fo.write(str(line) + "\n")

    # Open receipt program
    call(["python", "recipt.py"])
    restart_program()


# -----------------------------
# Data Model
# -----------------------------
class Booking:
    """Represents a booking record."""

    def __init__(self, name, address, mobile, room_no, price):
        self.name = name
        self.address = address
        self.mobile = mobile
        self.room_no = room_no
        self.price = price


# -----------------------------
# Main Application
# -----------------------------
class HotelManagementApp:
    """Main application class for Hotel Check-in GUI."""

    def __init__(self):
        # Booking details
        self.name = ""
        self.address = ""
        self.mobile = ""
        self.days = 0
        self.room_type = None
        self.payment_method = None
        self.price = 0
        self.room_no = None

        # Initialize GUI
        self.root = Tk()
        self.root.geometry("1069x742")
        self.root.title("Hotel Management - Check-in")
        self.root.configure(background="white")

        self.setup_ui()
        self.root.mainloop()

    # -----------------------------
    # GUI Setup
    # -----------------------------
    def setup_ui(self):
        """Setup all UI components."""
        # Output text area
        self.console = Text(self.root, background="white", foreground="black", wrap=WORD)
        self.console.place(relx=0.03, rely=0.65, relheight=0.29, relwidth=0.93)

        # Frame for header
        header = Frame(self.root, bg="white", borderwidth=2, relief=GROOVE)
        header.place(relx=0.03, rely=0.05, relheight=0.12, relwidth=0.93)

        Label(header, text="CHECK-IN", font=("Segoe UI", 30, "bold"), bg="white").pack()

        # Frame for form
        form = Frame(self.root, bg="white", borderwidth=2, relief=GROOVE)
        form.place(relx=0.03, rely=0.18, relheight=0.46, relwidth=0.93)

        # Name
        Label(form, text="Enter Your Name:", font=("Segoe UI", 14, "bold"), bg="white").grid(row=0, column=0, sticky=W, pady=5)
        self.entry_name = Entry(form, width=30)
        self.entry_name.grid(row=0, column=1, padx=10)

        # Address
        Label(form, text="Enter Your Address:", font=("Segoe UI", 14, "bold"), bg="white").grid(row=1, column=0, sticky=W, pady=5)
        self.entry_address = Entry(form, width=30)
        self.entry_address.grid(row=1, column=1, padx=10)

        # Mobile
        Label(form, text="Enter Your Mobile No:", font=("Segoe UI", 14, "bold"), bg="white").grid(row=2, column=0, sticky=W, pady=5)
        self.entry_mobile = Entry(form, width=30)
        self.entry_mobile.grid(row=2, column=1, padx=10)

        # Days
        Label(form, text="Number of Days:", font=("Segoe UI", 14, "bold"), bg="white").grid(row=3, column=0, sticky=W, pady=5)
        self.entry_days = Entry(form, width=30)
        self.entry_days.grid(row=3, column=1, padx=10)

        # Room type checkbuttons
        Label(form, text="Choose Your Room:", font=("Segoe UI", 14, "bold"), bg="white").grid(row=4, column=0, pady=10, sticky=W)
        self.room_choice = IntVar()
        for i, room in ROOM_TYPES.items():
            Checkbutton(form, text=room["name"], variable=self.room_choice, onvalue=i, bg="white").grid(row=4, column=i, padx=10)

        # Payment options
        Label(form, text="Choose Payment Method:", font=("Segoe UI", 14, "bold"), bg="white").grid(row=5, column=0, pady=10, sticky=W)
        self.pay_choice = IntVar()
        for i, pay in discount_methods.items():
            Checkbutton(form, text=pay["name"], variable=self.pay_choice, onvalue=i, bg="white").grid(row=5, column=i, padx=10)

        # Submit button
        Button(form, text="Submit", command=self.submit_booking, font=("Segoe UI", 14, "bold")).grid(row=6, column=1, pady=20)

    # -----------------------------
    # Booking Logic
    # -----------------------------
    def validate_inputs(self):
        """Validate form inputs."""
        self.name = self.entry_name.get().strip()
        self.address = self.entry_address.get().strip()
        self.mobile = self.entry_mobile.get().strip()
        days_str = self.entry_days.get().strip()

        if not self.name.isalpha():
            self.console.insert(INSERT, "Invalid Name!\n")
            return False
        if not self.address:
            self.console.insert(INSERT, "Invalid Address!\n")
            return False
        if not (self.mobile.isdigit() and len(self.mobile) == 10):
            self.console.insert(INSERT, "Invalid Mobile Number!\n")
            return False
        if not (days_str.isdigit() and int(days_str) > 0):
            self.console.insert(INSERT, "Invalid Number of Days!\n")
            return False

        self.days = int(days_str)
        return True

    def assign_room(self, room_type):
        """Assign next available room number from chosen room type."""
        allocated_rooms = []
        try:
            with open("hotel.dat", "rb") as f:
                while True:
                    booking = pickle.load(f)
                    allocated_rooms.append(booking.room_no)
        except (EOFError, FileNotFoundError):
            pass

        for r in ROOM_TYPES[room_type]["rooms"]:
            if r not in allocated_rooms:
                return r
        return None

    def submit_booking(self):
        """Handle booking submission."""
        if not self.validate_inputs():
            return

        self.room_type = self.room_choice.get()
        self.payment_method = self.pay_choice.get()

        if not self.room_type or not self.payment_method:
            self.console.insert(INSERT, "Please select room type & payment method!\n")
            return

        # Calculate price
        base_price = ROOM_TYPES[self.room_type]["price"] * self.days
        discount = discount_methods[self.payment_method]["discount"]
        self.price = base_price - (base_price * discount / 100)

        # Assign room
        self.room_no = self.assign_room(self.room_type)
        if not self.room_no:
            self.console.insert(INSERT, "No rooms available in this category!\n")
            return

        # Save booking
        details_list[:] = [self.name, self.address, self.mobile, self.room_no, self.price]
        save_booking(self.name, self.address, self.mobile, self.room_no, self.price)


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    HotelManagementApp()
