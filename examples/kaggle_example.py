"""
Example for Kaggle environment.
Ví dụ sử dụng trong Kaggle.

Setup required in Kaggle:
1. Go to Add-ons → Secrets
2. Add these secrets:
   - GDRIVE_CLIENT_ID
   - GDRIVE_CLIENT_SECRET
   - GDRIVE_REFRESH_TOKEN

To get these credentials:
1. Create OAuth credentials in Google Cloud Console
2. Use the provided script to get refresh token
"""

# Install gdrive-toolkit (run in first cell)
# !pip install git+https://github.com/yourusername/gdrive-toolkit.git

from gdrive_toolkit import quick_connect, upload_file, download_file

# Quick connect - automatically uses Kaggle secrets
drive = quick_connect()

# Upload dataset from Kaggle to Google Drive
file_id = upload_file(drive, "/kaggle/input/your-dataset/file.csv")
print(f"Uploaded to Google Drive: {file_id}")

# Download from Google Drive to Kaggle
download_file(
    drive,
    file_id="your_file_id_here",
    save_path="/kaggle/working/downloaded_file.csv"
)

# Example: Backup Kaggle output to Google Drive
import os
for filename in os.listdir("/kaggle/working"):
    if filename.endswith(".csv"):
        file_path = os.path.join("/kaggle/working", filename)
        upload_file(drive, file_path)
        print(f"Backed up: {filename}")

print("✓ Operations completed in Kaggle!")
