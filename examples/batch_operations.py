"""
Batch operations example for gdrive-toolkit.
Ví dụ thao tác hàng loạt.
"""

from gdrive_toolkit import (
    quick_connect,
    create_folder,
    batch_upload,
    batch_download,
    search_files,
)
import os

def main():
    # Connect
    print("Connecting to Google Drive...")
    drive = quick_connect()
    
    # Create test folder
    print("\n=== Creating Test Folder ===")
    folder_id = create_folder(drive, "batch-upload-test")
    
    # 1. Create multiple test files
    print("\n=== Creating Test Files ===")
    test_files = []
    for i in range(1, 6):
        filename = f"test_file_{i}.txt"
        with open(filename, "w") as f:
            f.write(f"This is test file number {i}")
        test_files.append(filename)
        print(f"Created: {filename}")
    
    # 2. Batch upload
    print("\n=== Batch Upload ===")
    file_ids = batch_upload(drive, test_files, folder_id=folder_id)
    print(f"Uploaded {len(file_ids)} files")
    
    # 3. Search uploaded files
    print("\n=== Searching Uploaded Files ===")
    files = search_files(drive, folder_id=folder_id)
    
    print(f"Found {len(files)} file(s) in folder:")
    for file in files:
        print(f"  - {file['title']}")
    
    # 4. Batch download
    print("\n=== Batch Download ===")
    os.makedirs("downloads", exist_ok=True)
    downloaded = batch_download(drive, file_ids, save_dir="downloads")
    print(f"Downloaded {len(downloaded)} files to ./downloads/")
    
    # 5. Clean up local files
    print("\n=== Cleaning Up ===")
    for filename in test_files:
        os.remove(filename)
    
    for filepath in downloaded:
        os.remove(filepath)
    
    os.rmdir("downloads")
    
    print("\n✓ Batch operations completed!")
    print(f"Note: Files are still on Google Drive in folder ID: {folder_id}")

if __name__ == "__main__":
    main()
