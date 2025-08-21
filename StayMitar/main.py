#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hotel Management System - Console Application
Refactored & Clean Version
"""

import os
import pickle


# -----------------------------
# Data Model
# -----------------------------
class Guest:
    """Represents a hotel guest booking."""

    def __init__(self, name, address, mobile_no, days, room=None, price=0):
        self.name = name
        self.address = address
        self.mobile_no = mobile_no
        self.days = days
        self.room = room
        self.price = price


# -----------------------------
# Constants
# -----------------------------
ROOM_TYPES = {
    1: {"name": "Deluxe", "rate": 2000, "rooms": list(range(1, 11))},
    2: {"name": "Semi-Deluxe", "rate": 1500, "rooms": list(range(11, 26))},
    3: {"name": "General", "rate": 1000, "rooms": list(range(26, 46))},
    4: {"name": "Joint", "rate": 1700, "rooms": [46, 47, 48, 49, 50]},
}


# -----------------------------
# Input Validators
# -----------------------------
def input_text(prompt: str) -> str:
    """Ask for non-empty text input."""
    while True:
        val = input(prompt).strip()
        if val and not val.isdigit():
            return val
        print("❌ Invalid input. Please try again.")


def input_number(prompt: str, length=None) -> str:
    """Ask for numeric input with optional fixed length."""
    while True:
        val = input(prompt).strip()
        if val.isdigit() and (length is None or len(val) == length):
            return val
        print("❌ Invalid number. Please try again.")


def input_choice(prompt: str, choices: list[str]) -> str:
    """Ask for a choice from a list of options."""
    while True:
        val = input(prompt).strip()
        if val in choices:
            return val
        print(f"❌ Invalid choice. Choose from {choices}.")


# -----------------------------
# Hotel Operations
# -----------------------------
class HotelSystem:
    """Hotel management system logic."""

    DATA_FILE = "hotel.dat"

    def __init__(self):
        self.guests = self.load_guests()

    # ----- Persistence -----
    def load_guests(self):
        guests = []
        try:
            with open(self.DATA_FILE, "rb") as f:
                while True:
                    try:
                        guests.append(pickle.load(f))
                    except EOFError:
                        break
        except FileNotFoundError:
            pass
        return guests

    def save_guests(self):
        with open(self.DATA_FILE, "wb") as f:
            for guest in self.guests:
                pickle.dump(guest, f, protocol=2)

    # ----- Booking -----
    def check_in(self):
        print("\n--- Guest Check-in ---")
        name = input_text("Enter guest name: ")
        address = input_text("Enter guest address: ")
        mobile_no = input_number("Enter mobile number (10 digits): ", length=10)
        days = int(input_number("Enter number of days: "))

        # Choose room type
        print("\nRoom Types:")
        for k, v in ROOM_TYPES.items():
            print(f"{k}. {v['name']} - ₹{v['rate']} per day")
        choice = int(input_choice("Choose room type (1-4): ", ["1", "2", "3", "4"]))

        # Calculate price
        base_price = ROOM_TYPES[choice]["rate"] * days

        # Payment method
        print("\nPayment Method:")
        print("1. Cash (No discount)")
        print("2. Card (10% discount)")
        pay_choice = int(input_choice("Choose payment method (1/2): ", ["1", "2"]))
        if pay_choice == 2:
            base_price -= base_price * 0.10

        # Assign room
        allocated_rooms = [g.room for g in self.guests]
        room_no = None
        for r in ROOM_TYPES[choice]["rooms"]:
            if r not in allocated_rooms:
                room_no = r
                break
        if not room_no:
            print("❌ No rooms available in this category.")
            return

        guest = Guest(name, address, mobile_no, days, room_no, base_price)
        self.guests.append(guest)
        self.save_guests()

        print(f"\n✅ Check-in successful! {guest.name} allocated Room {guest.room}.")
        print(f"Total Bill: ₹{guest.price}\n")

    # ----- Show List -----
    def show_guest_list(self):
        print("\n--- Guest List ---")
        if not self.guests:
            print("No guests currently checked in.")
            return
        print(f"{'Name':<20} {'Room No.':<10}")
        print("-" * 30)
        for g in self.guests:
            print(f"{g.name:<20} {g.room:<10}")

    # ----- Checkout -----
    def check_out(self):
        print("\n--- Guest Checkout ---")
        room_no = int(input_number("Enter room number: "))
        found = False
        updated_guests = []
        for g in self.guests:
            if g.room == room_no:
                found = True
                print(f"✅ Guest {g.name} has checked out. Thank you for staying with us!")
            else:
                updated_guests.append(g)
        if not found:
            print("❌ No guest found in that room.")
        self.guests = updated_guests
        self.save_guests()

    # ----- Get Info -----
    def get_info(self):
        print("\n--- Get Guest Info ---")
        room_no = int(input_number("Enter room number: "))
        found = False
        for g in self.guests:
            if g.room == room_no:
                found = True
                print(f"\n✅ Guest Found in Room {g.room}")
                print(f"   Name: {g.name}")
                print(f"   Address: {g.address}")
                print(f"   Mobile: {g.mobile_no}")
                print(f"   Total Bill: ₹{g.price}")
        if not found:
            print("❌ No guest found in that room.")


# -----------------------------
# Main Menu
# -----------------------------
def main():
    system = HotelSystem()
    while True:
        print("\n================ HOTEL MANAGEMENT SYSTEM ================")
        print("1. Check-in Guest")
        print("2. Show Guest List")
