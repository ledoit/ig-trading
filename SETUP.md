# Setup Guide for IG Trading Login

This guide will help you set up your credentials for the IG Trading login scraper.

## Quick Setup (Easiest Method)

**Option 1: Use the Python setup script (Recommended)**
```bash
python setup_env.py
```
This will create a `.env` file with your credentials. The password will be hidden as you type.

**Option 2: Manually create .env file**
1. Copy `env_template.txt` to `.env`
2. Open `.env` in a text editor
3. Replace `your_username_here` with your actual IG Trading username
4. Replace `your_password_here` with your actual IG Trading password
5. Save the file

## Alternative Methods

### Method 1: Using .env file (Recommended for local development)
1. Create a file named `.env` in the project root
2. Add these lines:
   ```
   IG_LOGIN_USERNAME=your_actual_username
   IG_LOGIN_PASSWORD=your_actual_password
   ```
3. The script will automatically load these when you run it

### Method 2: Using environment variables (Windows Command Prompt)
Run `setup_env.bat` or manually set:
```cmd
set IG_LOGIN_USERNAME=your_username
set IG_LOGIN_PASSWORD=your_password
python ig_login.py
```

### Method 3: Using environment variables (Git Bash)
Run `setup_env.sh` or manually set:
```bash
export IG_LOGIN_USERNAME="your_username"
export IG_LOGIN_PASSWORD="your_password"
python ig_login.py
```

### Method 4: GitHub Actions (Already configured)
If you're using GitHub Actions, the secrets `IG_LOGIN_USERNAME` and `IG_LOGIN_PASSWORD` are automatically available as environment variables.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up credentials using one of the methods above

3. Run the script:
   ```bash
   python ig_login.py
   ```

## Security Notes

- The `.env` file is already in `.gitignore` and won't be committed
- Never commit your actual credentials to the repository
- For GitHub Actions, use repository secrets (Settings → Secrets and variables → Actions)

## Troubleshooting

**"IG_LOGIN_USERNAME not found" error:**
- Make sure you've created a `.env` file OR set environment variables
- Check that `.env` file is in the same directory as `ig_login.py`
- Verify the variable names are exactly: `IG_LOGIN_USERNAME` and `IG_LOGIN_PASSWORD`

**Password not working:**
- Make sure there are no extra spaces in your `.env` file
- The format should be: `IG_LOGIN_USERNAME=username` (no spaces around the `=`)

