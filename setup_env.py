#!/usr/bin/env python3
"""
Interactive setup script to create .env file for IG Trading login.
This is the easiest way to set up your credentials locally.
"""

import os
import getpass

def create_env_file():
    """Create .env file with user credentials."""
    env_file = '.env'
    
    # Check if .env already exists
    if os.path.exists(env_file):
        response = input(f"{env_file} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled. Keeping existing .env file.")
            return
    
    print("Setting up IG Trading login credentials...")
    print("(Your credentials will be saved in .env file, which is git-ignored)")
    print()
    
    # Get username
    username = input("Enter your IG Trading username: ").strip()
    if not username:
        print("Error: Username cannot be empty!")
        return
    
    # Get password (hidden input)
    password = getpass.getpass("Enter your IG Trading password: ").strip()
    if not password:
        print("Error: Password cannot be empty!")
        return
    
    # Write to .env file
    try:
        with open(env_file, 'w') as f:
            f.write("# IG Trading Login Credentials\n")
            f.write("# This file is git-ignored and won't be committed\n")
            f.write("\n")
            f.write(f"IG_LOGIN_USERNAME={username}\n")
            f.write(f"IG_LOGIN_PASSWORD={password}\n")
        
        print()
        print(f"✓ Successfully created {env_file} file!")
        print("You can now run: python ig_login.py")
        print()
        print("Note: The .env file is already in .gitignore and won't be committed.")
        
    except Exception as e:
        print(f"Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()

