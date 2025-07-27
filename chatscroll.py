from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")  # Start browser in full-screen mode

# Path to your ChromeDriver
chrome_driver_path = "C:\\drivers\\chromedriver-win64\\chromedriver.exe"  # Change this to your path

# Set up the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open Facebook Messenger login page
    driver.get("https://www.messenger.com/")

    # Give some time for the page to load
    time.sleep(5)

    # Find and fill the login fields
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "pass")

    # Replace these with your actual Facebook credentials
    email_field.send_keys("8855841592")
    password_field.send_keys("vasviharsh")
    password_field.send_keys(Keys.RETURN)

    # Wait for login to complete
    time.sleep(10)

    # Find the first chat element (modify the selector based on the actual structure)
    first_chat = driver.find_element(By.XPATH, '(//div[@aria-label="Chats"]//ul/li)[1]')
    
    # Click on the first chat to open it
    first_chat.click()

    # Wait for the chat to open
    time.sleep(5)

    # Get the current time for the screenshot filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create the filename with the current time
    filename = f"first_chat_{current_time}.png"

    # Take a screenshot of the open chat
    driver.save_screenshot(filename)
    print(f"Screenshot saved as {filename}")

finally:
    # Close the browser
    driver.quit()
