import csv
import subprocess
import tkinter as tk
from tkinter import filedialog
import os

# Function to add a password to the Keychain
def add_password_to_keychain(service, account, password):
    try:
        # Command to add password using the security command-line tool
        subprocess.run([
            'security', 'add-internet-password', 
            '-a', account, 
            '-s', service, 
            '-w', password,
            '-T', '/Applications/Safari.app'
        ], check=True)
        print(f"Added password for {account} at {service}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add password for {account} at {service}: {e}")

# Main function to process the CSV file
def import_passwords_from_csv(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['url']
                username = row['username']
                password = row['password']
                add_password_to_keychain(url, username, password)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to open a file dialog and get the CSV file path
def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    return file_path

# Run the import process
def main():
    file_path = select_csv_file()
    if file_path:
        print(f"Selected file: {file_path}")
        import_passwords_from_csv(file_path)
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()