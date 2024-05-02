import os
import json
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog  # Import filedialog module for opening folder location
from shutil import rmtree  # Import rmtree function for deleting folders

# Color palette
primary_color = "#3F51B5"  # Dark blue
secondary_color = "#FF5722"  # Deep orange
background_color = "#87CEEB"  # Sky blue
treeview_bg_color = "#FFFFFF"  # White

# Function to create a new folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        show_folder_structure()  # Update folder structure after creating folder

# Function to save URLs to a specific folder
def save_url(url, folder_name):
    create_folder(folder_name)
    file_path = f"{folder_name}/urls.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            urls = json.load(file)
            if url in urls:
                return False  # URL already exists
            urls.append(url)
        with open(file_path, "w") as file:
            json.dump(urls, file, indent=4)
    else:
        with open(file_path, "w") as file:
            json.dump([url], file, indent=4)
    return True  # URL saved successfully

# Function to list all URLs in a specific folder
def list_urls(folder_name):
    create_folder(folder_name)
    file_path = f"{folder_name}/urls.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            urls = json.load(file)
            messagebox.showinfo("URLs in Folder", "\n".join(urls))
    else:
        messagebox.showinfo("URLs in Folder", "No URLs found in this folder.")

# Function to handle saving URL button click
def save_url_click(event=None):  # Modified to accept an event argument for binding to <Return>
    url = url_entry.get()
    folder_name = folder_entry.get()
    if url.strip() == "" or folder_name.strip() == "":
        messagebox.showerror("Error", "URL and Folder Name cannot be empty.")
        return
    if save_url(url, folder_name):
        messagebox.showinfo("Success", "URL saved successfully.")
        url_entry.delete(0, tk.END)  # Clear URL entry field after successful save
    else:
        messagebox.showerror("Error", "URL already exists in this folder.")

# Function to handle listing URL button click
def list_urls_click():
    folder_name = folder_entry.get()
    if folder_name.strip() == "":
        messagebox.showerror("Error", "Folder Name cannot be empty.")
        return
    list_urls(folder_name)

# Function to handle creating folder button click
def create_folder_click():
    folder_name = new_folder_entry.get()
    if folder_name.strip() == "":
        messagebox.showerror("Error", "Folder Name cannot be empty.")
        return
    create_folder(folder_name)

# Function to open the folder location
def open_folder_location():
    folder_name = folder_entry.get()
    if folder_name.strip() == "":
        messagebox.showerror("Error", "Folder Name cannot be empty.")
        return
    os.system(f'explorer "{os.path.abspath(folder_name)}"')  # Open folder location in file explorer

# Function to delete the selected folder
def delete_folder():
    folder_name = folder_entry.get()
    if folder_name.strip() == "":
        messagebox.showerror("Error", "Folder Name cannot be empty.")
        return
    if messagebox.askyesno("Confirmation", f"Are you sure you want to delete the folder '{folder_name}'?"):
        try:
            rmtree(folder_name)  # Delete the folder
            messagebox.showinfo("Success", f"Folder '{folder_name}' deleted successfully.")
            show_folder_structure()  # Update folder structure after deleting folder
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete folder: {e}")

# Function to open the selected JSON file in Notepad++
# Function to open the selected JSON file in Notepad++
# Function to open the selected JSON file in Notepad++
def open_json_file_notepadpp():
    folder_name = folder_entry.get()
    selected_item = tree_view.focus()
    selected_file = tree_view.item(selected_item, "text")
    if folder_name.strip() == "":
        messagebox.showerror("Error", "Folder Name cannot be empty.")
        return
    json_file_path = os.path.join(folder_name, "urls.json")
    if os.path.exists(json_file_path):
        os.system(f'notepad++ "{os.path.abspath(json_file_path)}"')  # Open JSON file with Notepad++
    else:
        messagebox.showerror("Error", "urls.json file not found in this folder.")


# Function to show the folder structure of the project folder
def show_folder_structure():
    tree_view.delete(*tree_view.get_children())
    root_dir = os.getcwd()  # Get the current working directory
    parent_node = tree_view.insert('', 'end', text=root_dir, open=True)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if dirpath == root_dir:  # Only top-level directories
            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                tree_view.insert(parent_node, 'end', text=full_path, open=True)

# Function to handle single-click event on tree view items
def tree_item_single_click(event):
    item_id = tree_view.focus()
    folder_path = tree_view.item(item_id, "text")
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

# Create main window
root = tk.Tk()
root.title("URL Manager")
root.geometry("600x400")  # Set the size of the window

# Set background color
root.configure(bg=background_color)

# Create and place widgets for managing URLs
url_label = tk.Label(root, text="URL:", bg=background_color)
url_label.pack()

url_entry = tk.Entry(root, width=150)
url_entry.pack()

folder_label = tk.Label(root, text="Folder:", bg=background_color)
folder_label.pack()

folder_entry = tk.Entry(root, width=150)
folder_entry.pack()

save_button = tk.Button(root, text="Save URL", command=save_url_click, bg=secondary_color, fg="white")
save_button.pack(pady=5)

list_button = tk.Button(root, text="List URLs", command=list_urls_click, bg=secondary_color, fg="white")
list_button.pack(pady=5)

# Create and place widgets for managing folders
folder_management_frame = tk.LabelFrame(root, text="Folder Management", bg=background_color)
folder_management_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

new_folder_label = tk.Label(folder_management_frame, text="New Folder:", bg=background_color)
new_folder_label.grid(row=0, column=0, sticky="e")

new_folder_entry = tk.Entry(folder_management_frame, width=40)
new_folder_entry.grid(row=0, column=1)

create_folder_button = tk.Button(folder_management_frame, text="Create Folder", command=create_folder_click, bg=primary_color, fg="white")
create_folder_button.grid(row=0, column=2, padx=5)

# Button to open folder location
open_location_button = tk.Button(folder_management_frame, text="Open Folder Location", command=open_folder_location, bg=primary_color, fg="white")
open_location_button.grid(row=0, column=3, padx=5)

# Button to delete folder
delete_folder_button = tk.Button(folder_management_frame, text="Delete Folder", command=delete_folder, bg=primary_color, fg="white")
delete_folder_button.grid(row=0, column=4, padx=5)

# Button to open JSON file in Notepad++
open_notepad_button = tk.Button(folder_management_frame, text="Open JSON in Notepad++", command=open_json_file_notepadpp, bg=primary_color, fg="white")
open_notepad_button.grid(row=1, column=0, columnspan=5, pady=5)

# Create and place widgets for showing folder structure
show_structure_button = tk.Button(folder_management_frame, text="Show Folder Structure", command=show_folder_structure, bg=primary_color, fg="white")
show_structure_button.grid(row=2, column=0, columnspan=5, pady=5)

tree_view_frame = tk.Frame(folder_management_frame)  # Set background color for tree view
tree_view_frame.grid(row=3, column=0, columnspan=5, pady=5, sticky="nsew")

tree_view_scroll = tk.Scrollbar(tree_view_frame)
tree_view_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree_view = ttk.Treeview(tree_view_frame, yscrollcommand=tree_view_scroll.set)  # Set background color for tree view
tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tree_view_scroll.config(command=tree_view.yview)

# Bind single-click event to tree view items
tree_view.bind("<ButtonRelease-1>", tree_item_single_click)

# Configure row and column weights for grid
folder_management_frame.grid_rowconfigure(3, weight=1)
folder_management_frame.grid_columnconfigure(0, weight=1)

# Bind <Return> key press event to the URL entry field
url_entry.bind("<Return>", save_url_click)

# Start the main event loop
root.mainloop()
