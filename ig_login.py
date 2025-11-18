"""
IG Trading Login Web Scraper
Logs into IG Trading (Irish online trading platform) using credentials from secrets.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


def load_secrets():
    """
    Load username and password from environment variables or .env file.
    Priority: Environment variables > .env file
    """
    username = os.getenv('IG_LOGIN_USERNAME')
    password = os.getenv('IG_LOGIN_PASSWORD')
    
    if not username:
        raise ValueError(
            "IG_LOGIN_USERNAME not found. Please:\n"
            "  1. Set it as an environment variable, OR\n"
            "  2. Create a .env file with IG_LOGIN_USERNAME=your_username\n"
            "  3. For GitHub Actions: Add it as a repository secret"
        )
    
    if not password:
        raise ValueError(
            "IG_LOGIN_PASSWORD not found. Please:\n"
            "  1. Set it as an environment variable, OR\n"
            "  2. Create a .env file with IG_LOGIN_PASSWORD=your_password\n"
            "  3. For GitHub Actions: Add it as a repository secret"
        )
    
    return username, password


def setup_driver(headless=False):
    """Set up and return a Chrome WebDriver instance."""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Set user agent to avoid detection
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Use webdriver-manager to automatically handle ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def login_to_ig_trading(username, password, headless=False):
    """
    Log into IG Trading platform.
    
    Args:
        username: IG Trading username
        password: IG Trading password
        headless: Whether to run browser in headless mode
    
    Returns:
        WebDriver instance after successful login
    """
    driver = setup_driver(headless=headless)
    
    try:
        # Navigate to IG Trading login page
        print("Navigating to IG Trading login page...")
        driver.get("https://www.ig.com/ie/login")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        
        # Wait for and find username field using exact XPath
        print("Looking for username field...")
        try:
            username_xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/form/div[1]/div/input"
            username_field = wait.until(EC.presence_of_element_located((By.XPATH, username_xpath)))
            
            # Enter username
            username_field.clear()
            username_field.send_keys(username)
            print("Username entered")
            
        except Exception as e:
            print(f"Error finding username field: {e}")
            # Take screenshot for debugging
            driver.save_screenshot("error_username_field.png")
            raise
        
        # Wait a bit before entering password
        time.sleep(1)
        
        # Handle cookie consent popup if present (OneTrust)
        print("Checking for cookie consent popup...")
        try:
            # Wait a moment for popup to appear
            time.sleep(2)
            
            # Try to find and close cookie consent overlay
            cookie_selectors = [
                (By.CSS_SELECTOR, "#onetrust-accept-btn-handler"),  # Accept All button
                (By.CSS_SELECTOR, "button[id*='onetrust']"),  # Any OneTrust button
                (By.CSS_SELECTOR, "button[class*='onetrust']"),  # Any OneTrust button
                (By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Accept All')]"),
                (By.XPATH, "//button[contains(@id, 'onetrust')]"),
            ]
            
            cookie_handled = False
            for by, selector in cookie_selectors:
                try:
                    cookie_button = driver.find_element(by, selector)
                    if cookie_button.is_displayed():
                        # Use JavaScript click to avoid interception
                        driver.execute_script("arguments[0].click();", cookie_button)
                        print("Cookie consent popup handled")
                        cookie_handled = True
                        time.sleep(1)  # Wait for overlay to fade out
                        break
                except (NoSuchElementException, ElementClickInterceptedException):
                    continue
            
            # If no button found, try to remove the overlay directly
            if not cookie_handled:
                try:
                    overlay = driver.find_element(By.CSS_SELECTOR, ".onetrust-pc-dark-filter")
                    if overlay.is_displayed():
                        # Remove overlay using JavaScript
                        driver.execute_script("arguments[0].style.display = 'none';", overlay)
                        print("Cookie consent overlay removed")
                        time.sleep(1)
                except NoSuchElementException:
                    print("No cookie consent popup found (this is fine)")
        except Exception as e:
            print(f"Note: Could not handle cookie popup (may not be present): {e}")
        
        # Find and enter password using exact XPath
        print("Looking for password field...")
        try:
            password_xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/form/div[2]/div/input"
            password_field = wait.until(EC.presence_of_element_located((By.XPATH, password_xpath)))
            
            # Enter password
            password_field.clear()
            password_field.send_keys(password)
            print("Password entered")
            
        except Exception as e:
            print(f"Error finding password field: {e}")
            driver.save_screenshot("error_password_field.png")
            raise
        
        # Find and click submit button using exact XPath
        print("Looking for submit button...")
        try:
            submit_xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/form/input[1]"
            submit_button = wait.until(EC.presence_of_element_located((By.XPATH, submit_xpath)))
            
            # Try regular click first, if intercepted use JavaScript click
            try:
                submit_button.click()
                print("Submit button clicked")
            except ElementClickInterceptedException:
                print("Submit button intercepted, using JavaScript click...")
                # Remove any remaining overlays
                try:
                    overlay = driver.find_element(By.CSS_SELECTOR, ".onetrust-pc-dark-filter")
                    driver.execute_script("arguments[0].style.display = 'none';", overlay)
                    time.sleep(0.5)
                except NoSuchElementException:
                    pass
                
                # Use JavaScript to click
                driver.execute_script("arguments[0].click();", submit_button)
                print("Submit button clicked (via JavaScript)")
            
        except Exception as e:
            print(f"Error finding/clicking submit button: {e}")
            driver.save_screenshot("error_submit_button.png")
            raise
        
        # Wait for login to complete (check for successful login indicators)
        print("Waiting for login to complete...")
        time.sleep(5)
        
        # Check if login was successful by looking for common post-login elements
        current_url = driver.current_url
        if "login" not in current_url.lower() or "dashboard" in current_url.lower() or "account" in current_url.lower():
            print("Login appears successful!")
            print(f"Current URL: {current_url}")
        else:
            print(f"Warning: Still on login page. Current URL: {current_url}")
            print("Please check if login was successful manually.")
            driver.save_screenshot("login_result.png")
        
        return driver
        
    except Exception as e:
        print(f"Error during login: {e}")
        driver.save_screenshot("error_login.png")
        raise


def click_open_platform(driver):
    """
    Click the 'Open Platform' button on the dashboard.
    
    Args:
        driver: WebDriver instance (should be logged in)
    
    Returns:
        WebDriver instance after clicking the button
    """
    wait = WebDriverWait(driver, 20)
    
    try:
        print("Waiting for dashboard to fully load...")
        # Wait a bit for the dashboard to fully render
        time.sleep(3)
        
        # Find and click the Open Platform button
        print("Looking for Open Platform button...")
        open_platform_xpath = "/html/body/div[3]/div[1]/ig-state-change-spinner/div/div/div/div/div/div/div[1]/div[4]/account-table/div/div/div[2]/div[1]/div/leveraged-account-table-row/div[1]/div[1]/platform-segmented-button/div/span/button"
        
        # Wait for the button to be present and clickable
        open_platform_button = wait.until(EC.element_to_be_clickable((By.XPATH, open_platform_xpath)))
        
        # Try regular click first, if intercepted use JavaScript click
        try:
            open_platform_button.click()
            print("Open Platform button clicked")
        except ElementClickInterceptedException:
            print("Button intercepted, using JavaScript click...")
            driver.execute_script("arguments[0].click();", open_platform_button)
            print("Open Platform button clicked (via JavaScript)")
        
        # Wait a moment for the platform to open
        time.sleep(3)
        
        # Check if platform opened successfully
        current_url = driver.current_url
        print(f"Current URL after clicking Open Platform: {current_url}")
        
        return driver
        
    except TimeoutException:
        print("Error: Open Platform button not found or not clickable")
        driver.save_screenshot("error_open_platform.png")
        raise
    except Exception as e:
        print(f"Error clicking Open Platform button: {e}")
        driver.save_screenshot("error_open_platform.png")
        raise


def main():
    """Main function to execute login."""
    try:
        # Load credentials from secrets
        username, password = load_secrets()
        print(f"Loaded credentials for user: {username}")
        
        # Login to IG Trading
        driver = login_to_ig_trading(username, password, headless=False)
        
        # Click Open Platform button
        driver = click_open_platform(driver)
        
        # Keep browser open for a bit to verify
        print("\nProcess completed. Browser will stay open for 30 seconds for verification...")
        print("Press Ctrl+C to close early if needed.")
        
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\nClosing browser...")
        
        driver.quit()
        print("Browser closed.")
        
    except Exception as e:
        print(f"Failed to login: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

