# -*- coding: utf-8 -*-
"""
?? Login & Signup System
Coded by: Mr. Sabaz Ali Khan
Pakistani White Hat Hacker | Ethical Hacker | Cyber Security Expert

? Features:
   � Secure Password Hashing (PBKDF2 + SHA256)
   � Salted Hash Storage
   � Uses getpass for secure input
   � JSON-based Database (users.json)
   � Simple & Clean CLI Interface

For Educational & Ethical Use Only
"""

import json
import os
import hashlib
import getpass

DATABASE_FILE = "users.json"


def load_users():
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_users(users):
    with open(DATABASE_FILE, "w") as file:
        json.dump(users, file, indent=4)


def hash_password(password):
    """Secure password hashing using PBKDF2"""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + key.hex()


def verify_password(stored_hash, password):
    """Verify password against stored hash"""
    salt = bytes.fromhex(stored_hash[:64])
    stored_key = bytes.fromhex(stored_hash[64:])
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return new_key == stored_key


def signup():
    print("\n" + "="*50)
    print("               ? CREATE NEW ACCOUNT ?")
    print("="*50)
    
    username = input("\nEnter Username: ").strip()
    
    if not username:
        print("? Username cannot be empty!")
        return
    
    password = getpass.getpass("Enter Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    
    if password != confirm_password:
        print("? Passwords do not match!")
        return
    
    users = load_users()
    
    if username in users:
        print("? Username already exists!")
        return
    
    users[username] = hash_password(password)
    save_users(users)
    
    print(f"? Signup Successful! Welcome, {username}!")


def login():
    print("\n" + "="*50)
    print("               ?? USER LOGIN ??")
    print("="*50)
    
    username = input("\nEnter Username: ").strip()
    password = getpass.getpass("Enter Password: ")
    
    users = load_users()
    
    if username in users and verify_password(users[username], password):
        print(f"\n? Login Successful! Welcome back, {username}!")
        print("?? You are now logged in.")
    else:
        print("? Invalid Username or Password!")


def main():
    print("?? Login & Signup System")
    print("Coded by Mr. Sabaz Ali Khan\n")
    
    while True:
        print("\n[1] Signup")
        print("[2] Login")
        print("[3] Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("\nThank you for using the system. Stay Safe! ??")
            break
        else:
            print("? Invalid option! Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()