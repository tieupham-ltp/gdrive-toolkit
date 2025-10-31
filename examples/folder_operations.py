"""
Folder operations example for gdrive-toolkit.
Ví dụ thao tác với thư mục.
"""

from gdrive_toolkit import (
    quick_connect,
    create_folder,
    create_folder_path,
    upload_file,
    share_file,
    list_folders,
)

def main():
    # Connect
    print("Connecting to Google Drive...")
    drive = quick_connect()
    
    # 1. Create a folder
    print("\n=== Creating Folder ===")
    folder_id = create_folder(drive, "gdrive-toolkit-demo")
    
    # 2. Create nested folders
    print("\n=== Creating Folder Path ===")
    subfolder_id = create_folder_path(
        drive,
        "gdrive-toolkit-demo/2025/data",
    )
    
    # 3. Upload file to folder
    print("\n=== Uploading to Folder ===")
    with open("demo_data.txt", "w") as f:
        f.write("Demo data for gdrive-toolkit")
    
    file_id = upload_file(drive, "demo_data.txt", folder_id=subfolder_id)
    
    # 4. Share the folder
    print("\n=== Sharing Folder ===")
    link = share_file(drive, folder_id, permission="reader")
    print(f"Anyone with this link can view: {link}")
    
    # 5. List all folders
    print("\n=== Listing All Folders ===")
    folders = list_folders(drive, max_results=10)
    
    for folder in folders:
        print(f"- {folder['title']} (ID: {folder['id']})")
    
    # Clean up
    import os
    os.remove("demo_data.txt")
    
    print("\n✓ Folder operations completed!")

if __name__ == "__main__":
    main()
