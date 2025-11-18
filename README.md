# IG Trading Portfolio Rebalancing System

Automated portfolio tracking and rebalancing system for IG Trading (Irish online trading platform). Logs in, captures portfolio state, and automatically rebalances when needed.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database:**
   ```bash
   python init_db.py
   ```
   This creates the SQLite database for storing portfolio snapshots and rebalancing actions.

3. **Set up credentials:**
   - **For GitHub Actions:** Add repository secrets:
     - `IG_LOGIN_USERNAME` - Your IG Trading username
     - `IG_LOGIN_PASSWORD` - Your IG Trading password
   - **For local development:** Export environment variables:
     ```bash
     export IG_LOGIN_USERNAME="your_username"
     export IG_LOGIN_PASSWORD="your_password"
     ```
     On Windows:
     ```cmd
     set IG_LOGIN_USERNAME=your_username
     set IG_LOGIN_PASSWORD=your_password
     ```

## Usage

### Main Rebalancing Script

Run the rebalancing script (recommended):
```bash
python ig_rebalance.py
```

This script will:
1. Log into IG Trading
2. Open the trading platform
3. Extract current portfolio data
4. Save a snapshot to the database
5. Calculate rebalancing actions (if needed)
6. Execute rebalancing trades (if needed)
7. Log all actions to the database

### Simple Login Script

For testing login only:
```bash
python ig_login.py
```

### View Database Contents

To view stored portfolio snapshots and rebalancing actions:
```bash
python view_db.py
```

## Database Structure

The system uses SQLite to store:

- **Portfolio Snapshots**: Historical records of portfolio state (positions, values, cash balance)
- **Rebalancing Actions**: Log of all rebalancing decisions and trades executed

The database file (`ig_trading.db`) persists between script runs and is excluded from git.

## Security

- **Credentials are loaded from environment variables** - never hardcode them in the script
- GitHub secrets are automatically available as environment variables in GitHub Actions
- Keep your credentials secure and never commit them to the repository

## Troubleshooting

If login fails:
- Check the generated screenshot files (`.png`) for debugging
- Verify your credentials are correct
- IG Trading may have updated their login page structure - you may need to update the selectors in the script
- Some sites may require additional verification (2FA, CAPTCHA, etc.)

## Scripts Overview

- **`ig_rebalance.py`**: Main script for portfolio tracking and rebalancing
- **`ig_login.py`**: Login and platform opening functionality
- **`database.py`**: Database helper functions for storing snapshots and actions
- **`init_db.py`**: Initialize the database schema
- **`view_db.py`**: View database contents for monitoring

## Implementation Notes

### Current Status

The framework is set up with:
- ✅ Login and platform access
- ✅ Database schema for snapshots and actions
- ✅ Rebalancing workflow structure
- ⚠️ Portfolio data extraction (needs IG Trading platform selectors)
- ⚠️ Rebalancing logic (needs your strategy implementation)
- ⚠️ Trade execution (needs IG Trading API/interface integration)

### Next Steps

1. **Add portfolio data extraction**: Update `extract_portfolio_data()` in `ig_rebalance.py` with actual selectors from the IG Trading platform
2. **Implement rebalancing logic**: Update `calculate_rebalancing_actions()` with your rebalancing strategy
3. **Add trade execution**: Update `execute_rebalancing_actions()` to place actual trades on the platform

## Technical Details

- Uses Selenium WebDriver for browser automation
- SQLite database for persistent storage
- Includes anti-detection measures to avoid being flagged as a bot
- Uses full XPath selectors for reliable element location
- Runs in non-headless mode so you can see the browser automation in action

