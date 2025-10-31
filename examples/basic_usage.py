"""
Basic usage example for gdrive-toolkit.
Ví dụ sử dụng cơ bản gdrive-toolkit.
"""

from gdrive_toolkit import quick_connect, upload_file, download_file, search_files

def main():
    # 1. Connect to Google Drive (auto-detects environment)
    print("Connecting to Google Drive...")
    drive = quick_connect()
    
    # 2. Upload a file
    print("\n=== Uploading File ===")
    # Create a test file first
    with open("test_file.txt", "w") as f:
        f.write("Hello from gdrive-toolkit!")
    
    file_id = upload_file(drive, "test_file.txt")
    print(f"File uploaded with ID: {file_id}")
    
    # 3. Search for files
    print("\n=== Searching Files ===")
    files = search_files(drive, file_name="test_file", max_results=5)
    
    for file in files:
        print(f"- {file['title']} (ID: {file['id']})")
    
    # 4. Download file
    print("\n=== Downloading File ===")
    download_file(drive, file_id=file_id, save_path="downloaded_test.txt")
    
    # 5. Clean up
    import os
    os.remove("test_file.txt")
    os.remove("downloaded_test.txt")
    
    print("\n✓ Example completed successfully!")

if __name__ == "__main__":
    main()
