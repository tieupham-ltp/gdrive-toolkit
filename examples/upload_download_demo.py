"""
Upload and Download Demo
Demo upload và download file với gdrive-toolkit
"""

import os
from gdrive_toolkit import (
    quick_connect,
    upload_file,
    download_file,
    create_folder,
    search_files,
    share_file,
    print_file_list,
)


def main():
    print("=" * 70)
    print("gdrive-toolkit - Upload & Download Demo")
    print("=" * 70)
    print()
    
    # 1. Connect
    print("Step 1: Connecting to Google Drive...")
    drive = quick_connect()
    print()
    
    # 2. Create demo folder
    print("Step 2: Creating demo folder...")
    folder_name = "gdrive-toolkit-demo"
    folder_id = create_folder(drive, folder_name)
    print()
    
    # 3. Create some test files
    print("Step 3: Creating test files...")
    test_files = []
    
    # Text file
    with open("demo_text.txt", "w", encoding="utf-8") as f:
        f.write("Hello from gdrive-toolkit!\n")
        f.write("This is a demo text file.\n")
        f.write("Vietnamese: Xin chào! 👋\n")
    test_files.append("demo_text.txt")
    
    # CSV file
    with open("demo_data.csv", "w", encoding="utf-8") as f:
        f.write("Name,Age,City\n")
        f.write("Alice,25,Hanoi\n")
        f.write("Bob,30,Saigon\n")
        f.write("Charlie,35,Da Nang\n")
    test_files.append("demo_data.csv")
    
    # Markdown file
    with open("demo_notes.md", "w", encoding="utf-8") as f:
        f.write("# Demo Notes\n\n")
        f.write("## Features\n\n")
        f.write("- Easy upload\n")
        f.write("- Easy download\n")
        f.write("- Multi-environment support\n")
    test_files.append("demo_notes.md")
    
    print(f"✓ Created {len(test_files)} test files")
    print()
    
    # 4. Upload files
    print("Step 4: Uploading files to Google Drive...")
    uploaded_ids = []
    
    for file_path in test_files:
        file_id = upload_file(drive, file_path, folder_id=folder_id)
        uploaded_ids.append(file_id)
        print(f"  ✓ {file_path} → {file_id}")
    
    print()
    
    # 5. Search uploaded files
    print("Step 5: Searching uploaded files...")
    files = search_files(drive, folder_id=folder_id)
    print_file_list(files)
    
    # 6. Share folder
    print("Step 6: Sharing folder...")
    link = share_file(drive, folder_id, permission="reader")
    print(f"\n🔗 Shareable link:")
    print(f"   {link}")
    print()
    
    # 7. Download files
    print("Step 7: Downloading files...")
    download_dir = "downloaded_demos"
    os.makedirs(download_dir, exist_ok=True)
    
    for file_id in uploaded_ids:
        download_file(drive, file_id=file_id, save_path=download_dir)
    
    print()
    
    # 8. Verify downloads
    print("Step 8: Verifying downloads...")
    downloaded = os.listdir(download_dir)
    print(f"✓ Downloaded {len(downloaded)} files:")
    for filename in downloaded:
        file_path = os.path.join(download_dir, filename)
        size = os.path.getsize(file_path)
        print(f"  - {filename} ({size} bytes)")
    
    print()
    
    # 9. Clean up local files (optional)
    print("Step 9: Cleanup...")
    response = input("Remove local test files? [y/N]: ")
    
    if response.lower() == 'y':
        # Remove original test files
        for file_path in test_files:
            os.remove(file_path)
            print(f"  Removed: {file_path}")
        
        # Remove downloaded files
        for filename in downloaded:
            os.remove(os.path.join(download_dir, filename))
        os.rmdir(download_dir)
        print(f"  Removed directory: {download_dir}")
    else:
        print("  Skipped cleanup")
    
    print()
    print("=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70)
    print()
    print("What was demonstrated:")
    print("  1. ✓ Authentication with quick_connect()")
    print("  2. ✓ Folder creation")
    print("  3. ✓ File upload (multiple files)")
    print("  4. ✓ File search")
    print("  5. ✓ File sharing")
    print("  6. ✓ File download (multiple files)")
    print("  7. ✓ Verification")
    print()
    print(f"Your files are still on Google Drive in folder: {folder_name}")
    print(f"Folder ID: {folder_id}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
