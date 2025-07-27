from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Force UTF-8 encoding for the output
sys.stdout.reconfigure(encoding='utf-8')

# Initialize the WebDriver and open WhatsApp Web
driver = webdriver.Chrome()

# Maximize the browser window to full screen
driver.maximize_window()

driver.get("https://web.whatsapp.com/")

# Wait for QR code scan
# input("Please scan the QR code on WhatsApp Web and press Enter once done...")

# Wait explicitly for the contacts list to be visible
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat list']"))
    )
except Exception as e:
    print("Contacts did not load in time or there's an issue:", str(e))
    driver.quit()
    exit()

# Get all contact elements
contacts = driver.find_elements(By.XPATH, "//div[@aria-label='Chat list']//span[@title]")

# Check if contacts were found and store the first 10 contact names in a list
if contacts:
    contact_names = [contact.get_attribute('title') for contact in contacts[:10]]
    
    # Print the list of the first 10 contact names
    print("Your First 10 WhatsApp Contacts:")
    for name in contact_names:
        print(name)
else:
    print("No contacts found or contacts did not load properly.")

# Optionally, close the browser after you're done
driver.quit()
