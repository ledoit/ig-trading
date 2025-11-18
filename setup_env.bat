@echo off
REM Windows Batch script to set up environment variables for IG Trading login
REM This sets the variables for the current command prompt session

echo Setting up IG Trading login environment variables...
echo.

set /p IG_LOGIN_USERNAME="Enter your IG Trading username: "
set /p IG_LOGIN_PASSWORD="Enter your IG Trading password: "

echo.
echo Environment variables set for this session!
echo.
echo To use them, run: python ig_login.py
echo.
echo Note: These variables are only set for this command prompt window.
echo       To make them permanent, add them to System Environment Variables.
echo.
pause

