import tkinter as tk
from tkinter import messagebox
import random
import string
from PIL import Image, ImageTk

def create_icon_button(root, image_path, command=None):
    """Create a button with an icon."""
    image = Image.open(image_path)
    image = image.resize((50, 50), Image.Resampling.LANCZOS)  # Updated resampling method
    photo = ImageTk.PhotoImage(image)
    button = tk.Button(root, image=photo, command=command)
    button.image = photo  # Keep a reference to avoid garbage collection
    return button

def show_data_options(root):
    """Show a dropdown for selecting data options."""
    # Clear the frame
    for widget in root.winfo_children():
        widget.pack_forget()

    # Re-add the global heading
    heading = tk.Label(root, text="Social Media Investigator", font=("Arial", 16))
    heading.pack(pady=10)

    # Add page-specific heading
    page_heading = tk.Label(root, text="Select Data", font=("Arial", 14, "bold"))
    page_heading.pack(pady=5)

    # Create a frame for the dropdown
    data_frame = tk.Frame(root)
    data_frame.pack(pady=20)

    # Create a variable for the dropdown
    data_option = tk.StringVar(root)
    data_option.set("Select Data")  # Default value

    # Dropdown menu options
    options = ["Images", "Posts", "Friends", "Feeds"]
    dropdown = tk.OptionMenu(data_frame, data_option, *options, command=data_selected)
    dropdown.pack(pady=10)

def data_selected(selection):
    """Handle data selection from dropdown."""
    messagebox.showinfo("Data Selection", f"You selected {selection}.")

def show_icons_frame(root, icon_clicked=None):
    """Show the frame with social media icons."""
    # Clear the window
    for widget in root.winfo_children():
        widget.pack_forget()

    # Re-add the global heading
    heading = tk.Label(root, text="Social Media Investigator", font=("Arial", 16))
    heading.pack(pady=10)

    # Add page-specific heading
    page_heading = tk.Label(root, text="Select App", font=("Arial", 14, "bold"))
    page_heading.pack(pady=5)

    # Create a frame for the icons
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Paths to your icon images
    icons = {
        "Facebook": "icons/facebook.png",
        "Instagram": "icons/instagram.png",
        "Messenger": "icons/messenger.png",
        "WhatsApp": "icons/whatsapp.png",
        "Telegram": "icons/twitter.png"  # Fixed typo in icon path
    }

    # Create and place icon buttons
    for name, path in icons.items():
        button = create_icon_button(frame, path, command=lambda n=name: icon_clicked(n))
        button.pack(side=tk.LEFT, padx=5)

    if icon_clicked == "Facebook":
        show_data_options(root)

def generate_case_id():
    """Generate a random Case ID consisting of 6 characters and 4 alphabets."""
    letters = string.ascii_uppercase
    digits = string.digits
    case_id = ''.join(random.choices(letters + digits, k=10))  # 6 letters + 4 digits
    return case_id

def show_case_details_form(root):
    """Show the form for entering case details."""
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.pack_forget()

    # Re-add the global heading
    heading = tk.Label(root, text="Social Media Investigator", font=("Arial", 16))
    heading.pack(pady=10)

    # Add a page-specific heading
    page_heading = tk.Label(root, text="Enter Case Details", font=("Arial", 14, "bold"))
    page_heading.pack(pady=5)

    # Create a frame for the form
    form_frame = tk.Frame(root)
    form_frame.pack(pady=20)

    # Form fields
    tk.Label(form_frame, text="Investigator ID:").grid(row=0, column=0, padx=10, pady=5)
    investigator_id = tk.Entry(form_frame, width=50)
    investigator_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Name of Criminal:").grid(row=1, column=0, padx=10, pady=5)
    name_criminal = tk.Entry(form_frame, width=50)
    name_criminal.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Name of Investigator:").grid(row=2, column=0, padx=10, pady=5)
    name_investigator = tk.Entry(form_frame, width=50)
    name_investigator.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Case Description:").grid(row=3, column=0, padx=10, pady=5)
    case_description = tk.Text(form_frame, width=50, height=5)
    case_description.grid(row=3, column=1, padx=10, pady=5)

    # Submit button
    submit_button = tk.Button(form_frame, text="Submit", command=lambda: submit_form(root, investigator_id, name_criminal, name_investigator, case_description))
    submit_button.grid(row=4, column=1, padx=10, pady=20, sticky=tk.E)

def submit_form(root, investigator_id, name_criminal, name_investigator, case_description):
    """Handle form submission."""
    # Collect form data
    inv_id = investigator_id.get()
    criminal_name = name_criminal.get()
    investigator_name = name_investigator.get()
    description = case_description.get("1.0", tk.END).strip()

    # Generate a Case ID
    case_id = generate_case_id()

    # Show case details and confirmation message
    case_details = (f"Case ID: {case_id}\n"
                    f"Investigator ID: {inv_id}\n"
                    f"Criminal: {criminal_name}\n"
                    f"Investigator: {investigator_name}\n"
                    f"Description: {description}")
    messagebox.showinfo("Case Registered", f"Case Registered Successfully!\n\n{case_details}")

    # Show the icons frame
    show_icons_frame(root)

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Social Media Investigator")
    
    # Set window to half screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width / 2)
    window_height = screen_height
    root.geometry(f"{window_width}x{window_height}+0+0")  # Full height, half width

    # Show the case details form initially
    show_case_details_form(root)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
