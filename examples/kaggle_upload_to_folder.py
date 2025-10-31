"""
Example: Upload file to specific Google Drive folder on Kaggle
Ví dụ: Upload file vào folder cụ thể trên Google Drive từ Kaggle
"""

from gdrive_toolkit import quick_connect, upload_file
import pandas as pd

# Kết nối Google Drive
print("Connecting to Google Drive...")
drive = quick_connect(force_env='kaggle')

print("\n" + "=" * 70)
print("Creating test file...")
print("=" * 70)

# Tạo file CSV test
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney'],
    'Score': [95, 87, 92, 88, 91]
}

df = pd.DataFrame(data)
test_file = '/kaggle/working/test_data.csv'
df.to_csv(test_file, index=False)

print(f"✓ Created test file: {test_file}")
print(f"  Rows: {len(df)}")
print(f"  Columns: {list(df.columns)}")

print("\n" + "=" * 70)
print("Uploading to Google Drive...")
print("=" * 70)

# Upload vào folder cụ thể
folder_id = '1WJEvJdWmQdRB2AA82umDrYPXeUKSoQC1'

file_id = upload_file(
    drive,
    file_path=test_file,
    folder_id=folder_id,
    file_name='kaggle_test_data.csv'
)

print("\n" + "=" * 70)
print("Upload completed!")
print("=" * 70)
print(f"File ID: {file_id}")
print(f"You can view the file at: https://drive.google.com/file/d/{file_id}/view")
print(f"Folder: https://drive.google.com/drive/folders/{folder_id}")
