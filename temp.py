from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to log in to Facebook
def login_to_facebook(driver, email, password):
    driver.get('https://www.facebook.com/login')

    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "pass")
    
    email_input.send_keys(email)
    password_input.send_keys(password)

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    
    time.sleep(5)  # Wait for the login to complete

# Navigate to Messenger
def go_to_messenger(driver):
    driver.get('https://www.facebook.com/messages/t/')
    time.sleep(5)  # Wait for Messenger page to load

# Scroll and take screenshot of a single chat
def scroll_and_capture(driver, chat, chat_index):
    print(f"Opening chat {chat_index + 1}")
    
    # Click to open chat
    chat.click()
    time.sleep(3)  # Wait for the chat to open

    # Scroll up to load more messages
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, 0);")  # Scroll up
        time.sleep(2)  # Wait for loading
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Take screenshot after scrolling
    screenshot_filename = f'messenger_chat_{chat_index + 1}.png'
    driver.save_screenshot(screenshot_filename)
    print(f"Screenshot saved as {screenshot_filename}")
    time.sleep(2)  # Wait before moving to the next chat

# Select and capture all chats
def open_and_capture_all_chats(driver):
    print("Finding chat elements...")
    
    # Find all chat elements (adjust the selector as needed)
    chats = driver.find_elements(By.CSS_SELECTOR, 'div[aria-expanded="false"][role="button"]')

    print(f"Found {len(chats)} chats")

    for index, chat in enumerate(chats):
        try:
            scroll_and_capture(driver, chat, index)
        except Exception as e:
            print(f"Error capturing chat {index + 1}: {e}")
        time.sleep(3)  # Wait before moving to the next chat

if __name__ == "__main__":
    # Replace with your actual Facebook login credentials
    email = "8855841592"
    password = "vasviharsh"

    # Create a new instance of Chrome WebDriver
    driver = webdriver.Chrome(executable_path=r"C:\drivers\chromedriver-win64\chromedriver.exe")

    try:
        # Step 1: Login
        login_to_facebook(driver, email, password)
        
        # Step 2: Go to Messenger
        go_to_messenger(driver)

        # Step 3: Capture chats
        open_and_capture_all_chats(driver)

    finally:
        # Close the browser when done
        driver.quit()
