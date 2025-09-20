# Albert Thomson
# Compress and Extract files (ZIP/UNZIP)

import zipfile       # Module for creating and extracting ZIP files
import os            # Module for interacting with the file system
import tkinter as tk  # GUI library for building the interface
from tkinter import filedialog, messagebox  # Dialogs for selecting files/folders and showing messages


def zip_file_or_folder():
    """
    Open dialog to pick multiple files OR a folder, then compress them into a ZIP file.
    """

    # Ask the user to select multiple files (Ctrl/Shift allows multi-select)
    input_paths = filedialog.askopenfilenames(title="Select Files to Compress")

    # If no files were selected, allow user to pick a folder instead
    if not input_paths:
        folder = filedialog.askdirectory(title="Or Select a Folder to Compress")
        if not folder:  # If still nothing chosen, exit function
            return
        input_paths = [folder]  # Store folder as a single-item list

    # Ask the user where to save the resulting ZIP file
    output_zip = filedialog.asksaveasfilename(
        defaultextension=".zip", filetypes=[("ZIP files", "*.zip")]
    )
    if not output_zip:  # If user cancels save dialog, exit
        return

    # Create the ZIP file in write mode with compression enabled
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in input_paths:  # Loop over all chosen files/folders
            if os.path.isfile(path):
                # Add single file (store only filename, not full path)
                zipf.write(path, os.path.basename(path))
            else:
                # Walk through a folder and add all files inside it
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)  # Full path of file
                        # Store relative path so folder structure is preserved
                        arcname = os.path.relpath(file_path, start=path)
                        zipf.write(file_path, arcname)

    # Show success message popup
    messagebox.showinfo("Success", f"Compressed into {output_zip}")


def unzip_file():
    """
    Open dialog to pick a ZIP file, then extract it into the same location
    using the ZIP's filename (without .zip) as the folder name.
    """

    # Ask the user to select a ZIP file
    zip_path = filedialog.askopenfilename(
        filetypes=[("ZIP files", "*.zip")], title="Select a ZIP File"
    )
    if not zip_path:  # Exit if no file chosen
        return

    # Extract to the same directory as the zip file
    base_dir = os.path.dirname(zip_path)  # Get folder containing the zip
    folder_name = os.path.splitext(os.path.basename(zip_path))[0]  # Name without .zip
    extract_to = os.path.join(base_dir, folder_name)

    # Create the extraction folder if it doesn't exist
    os.makedirs(extract_to, exist_ok=True)

    # Open the ZIP file in read mode and extract everything
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_to)

    # Show success message popup
    messagebox.showinfo("Success", f"Extracted to {extract_to}")


def main():
    """
    Create the main GUI window with buttons for compressing and extracting.
    """

    root = tk.Tk()  # Initialize Tkinter window
    root.title("ZIP / UNZIP Tool")  # Set window title
    root.geometry("300x300")  # Set fixed window size (width x height)

    # Button for compressing (calls zip_file_or_folder)
    compress_btn = tk.Button(
        root, text="Compress (Zip)", command=zip_file_or_folder, width=20, height=2
    )
    compress_btn.pack(pady=10)  # Add padding around button

    # Button for extracting (calls unzip_file)
    extract_btn = tk.Button(
        root, text="Extract (Unzip)", command=unzip_file, width=20, height=2
    )
    extract_btn.pack(pady=10)

    # Button to exit/close the application
    exit_btn = tk.Button(root, text="Exit", command=root.destroy, width=20, height=2)
    exit_btn.pack(pady=10)

    # Run the Tkinter event loop (keeps window open)
    root.mainloop()


# Run main() only if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()