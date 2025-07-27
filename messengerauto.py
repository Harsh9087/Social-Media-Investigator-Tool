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
chrome_driver_path = "C:/drivers/chromedriver-win64/chromedriver.exe"  # Change this to your path

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

    # Navigate to the chats list
    # This might require interaction to load the chats list
    # Adjust this wait time as necessary for your environment
    time.sleep(10)

    # Example selector for chat names (inspect and update based on actual page structure)
    chat_elements = driver.find_elements(By.CSS_SELECTOR, 'div._5l-3')  # Update this selector based on actual page structure

    # Store chat names in a list
    chats = [chat.text for chat in chat_elements if chat.text.strip() != '']

    # Print the list of chat names
    print("Chats:")
    for chat in chats:
        print(chat)

    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create the filename with the current time
    filename = f"login_page_{current_time}.png"

    # Take a screenshot of the home page
    driver.save_screenshot(filename)
    print(f"Screenshot saved as {filename}")

finally:
    # Close the browser
    driver.quit()
