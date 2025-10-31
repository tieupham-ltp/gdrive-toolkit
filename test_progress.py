"""Test progress display for upload/download"""

from gdrive_toolkit import quick_connect, upload_file, download_file
import os

# Authenticate
print("Authenticating...")
drive = quick_connect()

# Test upload với progress
print("\n=== Testing Upload Progress ===")
file_id = upload_file(drive, "test_large.bin", file_name="test_progress.bin")

# Test download với progress  
print("\n=== Testing Download Progress ===")
download_file(drive, file_id=file_id, save_path="./downloaded_test.bin")

# Cleanup
print("\n=== Cleanup ===")
if os.path.exists("downloaded_test.bin"):
    os.remove("downloaded_test.bin")
    print("✓ Removed downloaded_test.bin")

print("\n✅ Test complete!")
