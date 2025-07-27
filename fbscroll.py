import tkinter as tk
from tkinter import messagebox
import random
import string
import os
from PIL import Image, ImageTk
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from datetime import datetime

def create_icon_button(root, image_path, command=None):
    """Create a button with an icon."""
    image = Image.open(image_path)
    image = image.resize((50, 50), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    button = tk.Button(root, image=photo, command=command)
    button.image = photo  # Keep a reference to avoid garbage collection
    return button

def show_login_form(root):
    """Show the form for entering login credentials."""
    # Clear the frame
    for widget in root.winfo_children():
        widget.pack_forget()

    # Re-add the global heading
    heading = tk.Label(root, text="Social Media Investigator", font=("Arial", 24))
    heading.pack(pady=20)

    # Add page-specific heading
    page_heading = tk.Label(root, text="Enter Login Credentials", font=("Arial", 20, "bold"))
    page_heading.pack(pady=10)

    # Create a frame for the form
    form_frame = tk.Frame(root)
    form_frame.pack(pady=40)

    # Form fields
    tk.Label(form_frame, text="Username:", font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
    username_entry = tk.Entry(form_frame, width=40, font=("Arial", 18))
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="Password:", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
    password_entry = tk.Entry(form_frame, show="*", width=40, font=("Arial", 18))
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Submit button
    submit_button = tk.Button(form_frame, text="Submit", font=("Arial", 18), command=lambda: submit_login(root, username_entry, password_entry))
    submit_button.grid(row=2, column=1, padx=10, pady=20, sticky=tk.E)

def submit_login(root, username_entry, password_entry):
    """Handle login form submission."""
    username = username_entry.get()
    password = password_entry.get()

    # Store the credentials globally to use them in Selenium later
    root.username = username
    root.password = password

    # Proceed to data options
    show_data_options(root)

def show_data_options(root):
    """Show a dropdown for selecting data options."""
    # Clear the frame
    for widget in root.winfo_children():
        widget.pack_forget()

    # Re-add the global heading
    heading = tk.Label(root, text="Social Media Investigator", font=("Arial", 24))
    heading.pack(pady=20)

    # Add page-specific heading
    page_heading = tk.Label(root, text="Select Data", font=("Arial", 20, "bold"))
    page_heading.pack(pady=10)

    # Create a frame for the dropdown
    data_frame = tk.Frame(root)
    data_frame.pack(pady=40)

    # Create a variable for the dropdown
    data_option = tk.StringVar(root)
    data_option.set("Select Data")  # Default value

    # Dropdown menu options
    options = ["Posts", "Friends", "Feeds", "Saved", "Groups", "Memories"]
    dropdown = tk.OptionMenu(data_frame, data_option, *options, command=lambda selection: data_selected(root, selection))
    dropdown.config(font=("Arial", 18))
    dropdown.pack(pady=10)

def data_selected(root, selection):
    """Handle data selection from dropdown."""
    if selection == "Friends":
        # Create a folder named after the selected data option inside the app folder
        data_folder = os.path.join(root.app_folder, selection)
        os.makedirs(data_folder, exist_ok=True)
        
        # Run Selenium code in a separate thread to avoid blocking the GUI
        thread = Thread(target=run_selenium, args=(root, data_folder))
        thread.start()
    else:
        messagebox.showinfo("Data Selection", f"You selected {selection}.")

def run_selenium(root, save_folder):
    """Run the Selenium code to fetch friends' data."""
    sys.stdout.reconfigure(encoding='utf-8')

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://www.facebook.com/")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "pass")
        
        email_input.send_keys(root.username)
        password_input.send_keys(root.password)
        
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        time.sleep(15)
        driver.get("https://www.facebook.com/harsh.suryavanshi.967/friends")
        time.sleep(20)

    except Exception as e:
        print("Login failed or there's an issue:", str(e))
        driver.quit()
        return

    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"{root.case_id}-Facebook-Friends-{timestamp}.jpg"
        screenshot_path = os.path.join(save_folder, screenshot_filename)
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Reached the end of the page.")
    driver.quit()
    root.quit()

def show_icons_frame(root, icon_clicked=None):
    """Show the frame with social media icons."""
    for widget in root.winfo_children():
        widget.pack_forget()

    heading = tk.Label(root, text="Social Media Investigator", font=("Arial", 24))
    heading.pack(pady=20)

    page_heading = tk.Label(root, text="Select App", font=("Arial", 20, "bold"))
    page_heading.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=40)

    icons = {
        "Facebook": "icons/facebook.png",
        "Instagram": "icons/instagram.png",
        "Messenger": "icons/messenger.png",
        "WhatsApp": "icons/whatsapp.png",
        "Telegram": "icons/twitter.png"
    }

    for name, path in icons.items():
        button = create_icon_button(frame, path, command=lambda n=name: handle_icon_click(root, n))
        button.pack(side=tk.LEFT, padx=10)

def handle_icon_click(root, icon_name):
    """Handle icon click events."""
    if icon_name == "Facebook":
        root.app_folder = os.path.join(root.case_id, icon_name)
        os.makedirs(root.app_folder, exist_ok=True)
        
        show_login_form(root)
    else:
        show_icons_frame(root, icon_clicked=icon_name)

def generate_case_id():
    """Generate a random Case ID consisting of 6 characters and 4 alphabets."""
    letters = string.ascii_uppercase
    digits = string.digits
    case_id = ''.join(random.choices(letters + digits, k=10))
    return case_id

def show_case_details_form(root):
    """Show the form for entering case details."""
    for widget in root.winfo_children():
        widget.pack_forget()

    heading = tk.Label(root, text="Social Media Investigator", font=("Arial", 24))
    heading.pack(pady=20)

    page_heading = tk.Label(root, text="Enter Case Details", font=("Arial", 20, "bold"))
    page_heading.pack(pady=10)

    form_frame = tk.Frame(root)
    form_frame.pack(pady=40)

    tk.Label(form_frame, text="Investigator ID:", font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
    investigator_id = tk.Entry(form_frame, width=40, font=("Arial", 18))
    investigator_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="Name of Criminal:", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
    name_criminal = tk.Entry(form_frame, width=40, font=("Arial", 18))
    name_criminal.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="Name of Investigator:", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
    name_investigator = tk.Entry(form_frame, width=40, font=("Arial", 18))
    name_investigator.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="Case Description:", font=("Arial", 18)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.NE)
    case_description = tk.Text(form_frame, width=40, height=5, font=("Arial", 18))
    case_description.grid(row=3, column=1, padx=10, pady=10)

    submit_button = tk.Button(form_frame, text="Submit", font=("Arial", 18), command=lambda: submit_form(root, investigator_id, name_criminal, name_investigator, case_description))
    submit_button.grid(row=4, column=1, padx=10, pady=20, sticky=tk.E)

def submit_form(root, investigator_id, name_criminal, name_investigator, case_description):
    """Handle form submission."""
    inv_id = investigator_id.get()
    criminal_name = name_criminal.get()
    investigator_name = name_investigator.get()
    description = case_description.get("1.0", tk.END).strip()

    # Generate a case ID and create a directory for the case
    case_id = generate_case_id()
    case_dir = os.makedirs(case_id, exist_ok=True)

    # Prepare case details
    case_details = (
        f"Case ID: {case_id}\n"
        f"Investigator ID: {inv_id}\n"
        f"Criminal: {criminal_name}\n"
        f"Investigator: {investigator_name}\n"
        f"Description: {description}"
    )

    # Save the details to a text file inside the case_id directory
    with open(os.path.join(case_id, "description.txt"), "w") as file:
        file.write(case_details)

    # Show a success message
    messagebox.showinfo("Case Registered", f"Case Registered Successfully!\n\n{case_details}")

    # Save the case ID in the root and move to the next frame
    root.case_id = case_id
    show_icons_frame(root)

def main():
    root = tk.Tk()
    root.title("Social Media Investigator")
    root.geometry("800x600")

    # Run the GUI in full screen
    root.attributes("-fullscreen", True)

    show_case_details_form(root)
    root.mainloop()


if __name__ == "__main__":
    main()
