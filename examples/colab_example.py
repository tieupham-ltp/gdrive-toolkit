"""
Example for Google Colab environment.
Ví dụ sử dụng trong Google Colab.

Copy this code into a Colab notebook cell and run it.
"""

# Install gdrive-toolkit (run once)
# !pip install git+https://github.com/yourusername/gdrive-toolkit.git

from gdrive_toolkit import quick_connect, upload_file, download_file, create_folder

# Quick connect - automatically uses Colab authentication
drive = quick_connect()

# Upload a file from Colab to Google Drive
file_id = upload_file(drive, "/content/sample_data/README.md")
print(f"Uploaded file ID: {file_id}")

# Create a folder
folder_id = create_folder(drive, "Colab Experiments")

# Upload to folder
file_id = upload_file(
    drive,
    "/content/sample_data/README.md",
    folder_id=folder_id
)

# Download from Google Drive to Colab
download_file(
    drive,
    file_id=file_id,
    save_path="/content/downloaded_readme.md"
)

print("✓ Operations completed in Colab!")
