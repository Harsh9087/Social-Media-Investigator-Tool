from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

# Initialize the WebDriver (e.g., for Chrome)
driver = webdriver.Chrome()

# Maximize the browser window
driver.maximize_window()

# Open the target website (e.g., Facebook)
driver.get("https://www.facebook.com/")

# Wait for the page to load
time.sleep(2)

# Find the login fields and enter credentials
email_field = driver.find_element("id", "email")
password_field = driver.find_element("id", "pass")

# Input your credentials
email_field.send_keys("8855841592")
password_field.send_keys("vasviharsh")

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the login to complete
time.sleep(20)

# Get the current time for the filename
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Take a screenshot of the homepage and save it with the current time
homepage_screenshot = f"screenshot_homepage_{current_time}.png"
driver.save_screenshot(homepage_screenshot)
print(f"Homepage screenshot saved as {homepage_screenshot}")

# Navigate to your account page
driver.get("https://www.facebook.com/harsh.suryavanshi.967/")  # Replace with your actual profile URL

# Wait for the account page to load
time.sleep(5)

# Get the current time again for the next screenshot (in case the time has changed)
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Take a screenshot of the account page and save it with the current time
account_screenshot = f"screenshot_account_{current_time}.png"
driver.save_screenshot(account_screenshot)
print(f"Account screenshot saved as {account_screenshot}")

# Close the browser
driver.quit()
