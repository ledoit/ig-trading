#!/bin/bash
# Shell script to set up environment variables for IG Trading login (Git Bash)
# This sets the variables for the current shell session

echo "Setting up IG Trading login environment variables..."
echo ""

read -p "Enter your IG Trading username: " IG_LOGIN_USERNAME
read -sp "Enter your IG Trading password: " IG_LOGIN_PASSWORD
echo ""

export IG_LOGIN_USERNAME
export IG_LOGIN_PASSWORD

echo ""
echo "Environment variables set for this session!"
echo ""
echo "To use them, run: python ig_login.py"
echo ""
echo "Note: These variables are only set for this shell session."
echo "      To make them permanent, add them to your ~/.bashrc or ~/.bash_profile"
echo ""

