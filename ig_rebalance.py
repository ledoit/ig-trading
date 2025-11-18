"""
IG Trading Portfolio Rebalancing Script
Logs in, captures portfolio state, and rebalances if needed.
"""

import time
from datetime import datetime
from ig_login import login_to_ig_trading, click_open_platform, load_secrets
from database import (
    init_database, save_portfolio_snapshot, save_rebalancing_action,
    get_latest_snapshot
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re


def extract_total_equity(driver):
    """
    Extract total equity from the IG Trading platform.
    
    Args:
        driver: WebDriver instance (should be on the trading platform)
    
    Returns:
        Float value of total equity, or None if not found
    """
    wait = WebDriverWait(driver, 20)
    
    try:
        print("Extracting total equity...")
        
        # Wait for platform to fully load
        time.sleep(3)
        
        # Find the total equity element using the provided XPath
        equity_xpath = "/html/body/div[2]/header/div[2]/div[1]/div/button[2]/div/div[1]/div[2]"
        equity_element = wait.until(EC.presence_of_element_located((By.XPATH, equity_xpath)))
        
        # Get the text content
        equity_text = equity_element.text.strip()
        print(f"Raw equity text: '{equity_text}'")
        
        # Parse the numeric value (remove currency symbols, commas, spaces)
        # Handle formats like: "€1,234.56", "1,234.56", "1234.56", etc.
        equity_value = None
        if equity_text:
            # Remove currency symbols, commas, spaces, and extract number
            # This regex finds numbers with optional decimal points
            numbers = re.findall(r'[\d,]+\.?\d*', equity_text.replace(',', ''))
            if numbers:
                try:
                    # Take the first number found and convert to float
                    equity_value = float(numbers[0].replace(',', ''))
                    print(f"Parsed total equity: {equity_value}")
                except ValueError:
                    print(f"Warning: Could not parse equity value from '{equity_text}'")
            else:
                print(f"Warning: No numeric value found in '{equity_text}'")
        
        return equity_value
        
    except TimeoutException:
        print("Error: Total equity element not found (timeout)")
        driver.save_screenshot("error_equity_extraction.png")
        return None
    except Exception as e:
        print(f"Error extracting total equity: {e}")
        driver.save_screenshot("error_equity_extraction.png")
        return None


def extract_portfolio_data(driver):
    """
    Extract current portfolio data from the IG Trading platform.
    
    Args:
        driver: WebDriver instance (should be on the trading platform)
    
    Returns:
        Dictionary with portfolio data
    """
    print("Extracting portfolio data...")
    
    portfolio_data = {
        'total_value': None,
        'cash_balance': None,
        'positions': [],
        'metadata': {}
    }
    
    try:
        # Extract total equity (total_value)
        total_equity = extract_total_equity(driver)
        portfolio_data['total_value'] = total_equity
        
        # TODO: Add extraction for:
        # - Cash balance
        # - List of positions (symbol, quantity, value, etc.)
        # - Account information
        
        print("Portfolio data extraction completed")
        
    except Exception as e:
        print(f"Error extracting portfolio data: {e}")
        raise
    
    return portfolio_data


def calculate_rebalancing_actions(current_data, target_allocation=None):
    """
    Calculate what rebalancing actions are needed.
    
    Args:
        current_data: Current portfolio data
        target_allocation: Target allocation (if None, uses default strategy)
    
    Returns:
        Dictionary with rebalancing plan
    """
    print("Calculating rebalancing actions...")
    
    # TODO: Implement rebalancing logic
    # This should:
    # 1. Compare current allocation to target
    # 2. Determine what trades are needed
    # 3. Check if rebalancing is within thresholds (e.g., 5% drift)
    # 4. Return list of actions (buy/sell orders)
    
    rebalancing_plan = {
        'action_type': 'no_action',  # 'buy', 'sell', 'rebalance', 'no_action'
        'actions': [],
        'reason': 'No rebalancing needed',
        'target_allocation': target_allocation or {},
        'current_allocation': {}
    }
    
    print("Rebalancing calculation completed (placeholder)")
    print("Note: Implement actual rebalancing logic based on your strategy")
    
    return rebalancing_plan


def execute_rebalancing_actions(driver, actions):
    """
    Execute the rebalancing actions on the platform.
    
    Args:
        driver: WebDriver instance
        actions: List of actions to execute
    
    Returns:
        Boolean indicating success
    """
    print("Executing rebalancing actions...")
    
    if not actions:
        print("No actions to execute")
        return True
    
    success = True
    executed_actions = []
    
    try:
        # TODO: Implement actual trade execution
        # This should:
        # 1. Navigate to trading interface
        # 2. For each action, place the order
        # 3. Verify order placement
        # 4. Log each action
        
        for action in actions:
            print(f"Executing action: {action}")
            # Place order logic here
            executed_actions.append({
                'action': action,
                'status': 'pending',  # 'pending', 'filled', 'rejected'
                'timestamp': datetime.now().isoformat()
            })
        
        print("Rebalancing actions execution completed (placeholder)")
        print("Note: Implement actual trade execution logic")
        
    except Exception as e:
        print(f"Error executing rebalancing actions: {e}")
        success = False
    
    return success, executed_actions


def main():
    """Main function to run the rebalancing script."""
    driver = None
    
    try:
        # Initialize database if needed
        print("Checking database...")
        try:
            init_database()
        except Exception as e:
            print(f"Database already exists or error: {e}")
        
        # Load credentials
        username, password = load_secrets()
        print(f"Loaded credentials for user: {username}")
        
        # Login and open platform
        print("\n=== Logging in ===")
        driver = login_to_ig_trading(username, password, headless=False)
        driver = click_open_platform(driver)
        
        # Extract current portfolio data
        print("\n=== Extracting Portfolio Data ===")
        portfolio_data = extract_portfolio_data(driver)
        
        # Save snapshot to database
        print("\n=== Saving Portfolio Snapshot ===")
        snapshot_id = save_portfolio_snapshot(
            total_value=portfolio_data.get('total_value'),
            cash_balance=portfolio_data.get('cash_balance'),
            positions=portfolio_data.get('positions'),
            metadata=portfolio_data.get('metadata')
        )
        
        # Calculate rebalancing actions
        print("\n=== Calculating Rebalancing Actions ===")
        rebalancing_plan = calculate_rebalancing_actions(portfolio_data)
        
        # Execute rebalancing if needed
        if rebalancing_plan['action_type'] != 'no_action':
            print("\n=== Executing Rebalancing ===")
            success, executed_actions = execute_rebalancing_actions(
                driver, 
                rebalancing_plan['actions']
            )
        else:
            print("\n=== No Rebalancing Needed ===")
            success = True
            executed_actions = []
        
        # Save rebalancing action to database
        print("\n=== Logging Rebalancing Action ===")
        save_rebalancing_action(
            snapshot_id=snapshot_id,
            action_type=rebalancing_plan['action_type'],
            target_allocation=rebalancing_plan.get('target_allocation'),
            current_allocation=rebalancing_plan.get('current_allocation'),
            actions_taken=executed_actions,
            reason=rebalancing_plan.get('reason'),
            success=success
        )
        
        print("\n=== Process Complete ===")
        print("Portfolio snapshot and rebalancing action saved to database")
        
        # Keep browser open for verification
        print("\nBrowser will stay open for 30 seconds for verification...")
        print("Press Ctrl+C to close early if needed.")
        
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\nClosing browser...")
        
        if driver:
            driver.quit()
        print("Browser closed.")
        
        return 0
        
    except Exception as e:
        print(f"\nError in rebalancing script: {e}")
        if driver:
            driver.save_screenshot("error_rebalance.png")
            driver.quit()
        return 1


if __name__ == "__main__":
    exit(main())

