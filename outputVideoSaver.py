import os
parent_folder_name = "wys"
# Get the path of the user's Videos directory
videos_dir = os.path.join(os.path.expanduser("~"), "Videos")

# Create the full path of the parent folder
parent_folder_path = os.path.join(videos_dir, parent_folder_name)

# Create the parent folder if it doesn't already exist
os.makedirs(parent_folder_path, exist_ok=True)

def getOutputFileFolder():
    return parent_folder_path

