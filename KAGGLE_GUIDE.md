# 🎯 Hướng Dẫn Sử Dụng gdrive-toolkit trên Kaggle

## 📋 Mục Lục
- [Cài Đặt Nhanh](#cài-đặt-nhanh)
- [Thiết Lập Credentials](#thiết-lập-credentials)
- [Sử Dụng Cơ Bản](#sử-dụng-cơ-bản)
- [Ví Dụ Thực Tế](#ví-dụ-thực-tế)

---

## 🚀 Cài Đặt Nhanh

### Bước 1: Cài đặt thư viện

Trong Kaggle Notebook, chạy cell đầu tiên:

```python
# Cài đặt gdrive-toolkit từ GitHub
!pip install git+https://github.com/tieupham-ltp/gdrive-toolkit.git

# Hoặc nếu đã publish lên PyPI:
# !pip install gdrive-toolkit
```

### Bước 2: Import và kết nối

```python
from gdrive_toolkit import quick_connect

# Kết nối tự động (tự phát hiện môi trường Kaggle)
drive = quick_connect()
```

---

## 🔑 Thiết Lập Credentials

### Cách 1: Sử dụng Kaggle Secrets (Khuyến nghị ⭐)

#### Bước 1: Tạo OAuth 2.0 Credentials trên Google Cloud

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới hoặc chọn project có sẵn
3. Enable **Google Drive API**:
   - Vào "APIs & Services" > "Library"
   - Tìm "Google Drive API" và click "Enable"

4. Tạo OAuth 2.0 Credentials:
   - Vào "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop app"
   - Đặt tên: "Kaggle Drive Access"
   - Click "Create"

5. Download file JSON credentials

#### Bước 2: Thêm vào Kaggle Secrets

1. Mở file `client_secrets.json` vừa download
2. Truy cập [Kaggle Settings](https://www.kaggle.com/settings)
3. Vào tab **Secrets** (hoặc Add-ons > Secrets)
4. Click "Add a new secret"
5. Thêm 2 secrets sau:

**Secret 1: GDRIVE_CLIENT_ID**
```
Name: GDRIVE_CLIENT_ID
Value: [Copy giá trị "client_id" từ file JSON]
```

**Secret 2: GDRIVE_CLIENT_SECRET**
```
Name: GDRIVE_CLIENT_SECRET
Value: [Copy giá trị "client_secret" từ file JSON]
```

#### Bước 3: Enable Secrets trong Notebook

1. Mở Kaggle Notebook của bạn
2. Click vào **Settings** (biểu tượng bánh răng ở góc phải)
3. Trong phần **Secrets**, bật (toggle ON):
   - ✅ GDRIVE_CLIENT_ID
   - ✅ GDRIVE_CLIENT_SECRET

#### Bước 4: Sử dụng trong Code

```python
from gdrive_toolkit import quick_connect

# Kết nối tự động - sẽ tự lấy credentials từ Kaggle Secrets
drive = quick_connect()
```

### Cách 2: Upload File Credentials

Nếu không dùng Secrets, bạn có thể upload file `client_secrets.json`:

```python
from gdrive_toolkit.auth import authenticate_kaggle
from pydrive2.drive import GoogleDrive

# Upload file client_secrets.json vào /kaggle/working/
# Sau đó:
drive = authenticate_kaggle(
    client_id='your_client_id',
    client_secret='your_client_secret'
)
```

---

## 💡 Sử Dụng Cơ Bản

### 1️⃣ Upload File

```python
from gdrive_toolkit import quick_connect, upload_file

drive = quick_connect()

# Upload 1 file
file_id = upload_file(
    drive, 
    local_path='/kaggle/input/dataset/data.csv',
    file_name='my_data.csv',
    folder_id=None  # None = upload vào root
)

print(f"File uploaded with ID: {file_id}")
```

### 2️⃣ Download File

```python
from gdrive_toolkit import download_file, search_files

# Tìm file theo tên
files = search_files(drive, query="name contains 'data.csv'")
if files:
    file_id = files[0]['id']
    
    # Download về Kaggle
    download_file(
        drive,
        file_id=file_id,
        save_path='/kaggle/working/downloaded_data.csv'
    )
```

### 3️⃣ Tạo và Upload vào Folder

```python
from gdrive_toolkit import create_folder_path, upload_file

# Tạo cấu trúc folder (giống mkdir -p)
folder_id = create_folder_path(drive, "Kaggle/Datasets/2025")

# Upload vào folder đó
upload_file(
    drive,
    local_path='/kaggle/working/result.csv',
    folder_id=folder_id
)
```

### 4️⃣ Upload ZIP

```python
from gdrive_toolkit.client import GDriveClient

client = GDriveClient(drive)

# Zip và upload toàn bộ folder
file_id = client.zip_and_upload(
    folder_path='/kaggle/working/output',
    zip_name='kaggle_results.zip',
    parent_id=None
)
```

---

## 🎯 Ví Dụ Thực Tế

### Ví dụ 1: Save Model vào Google Drive

```python
from gdrive_toolkit import quick_connect, create_folder_path
from gdrive_toolkit.client import GDriveClient
import joblib

# 1. Train model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
# ... train model ...

# 2. Save model locally
joblib.dump(model, '/kaggle/working/model.pkl')

# 3. Upload lên Google Drive
drive = quick_connect()
client = GDriveClient(drive)

# Tạo folder cho project
folder_id = create_folder_path(drive, "Kaggle/Models/RandomForest")

# Upload model
model_id = client.upload_file(
    local_path='/kaggle/working/model.pkl',
    file_name=f'model_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.pkl',
    parent_id=folder_id
)

print(f"✓ Model saved to Google Drive: {model_id}")
```

### Ví dụ 2: Download Dataset từ Google Drive

```python
from gdrive_toolkit import quick_connect, search_files, download_file
import pandas as pd

# Kết nối
drive = quick_connect()

# Tìm dataset trên Drive
files = search_files(drive, query="name = 'train_data.csv'")

if files:
    # Download về Kaggle
    download_file(
        drive,
        file_id=files[0]['id'],
        save_path='/kaggle/working/train_data.csv'
    )
    
    # Load vào pandas
    df = pd.read_csv('/kaggle/working/train_data.csv')
    print(f"Loaded {len(df)} rows")
else:
    print("Dataset not found on Google Drive")
```

### Ví dụ 3: Backup Kết Quả Competition

```python
from gdrive_toolkit import quick_connect, create_folder_path
from gdrive_toolkit.client import GDriveClient
from datetime import datetime

drive = quick_connect()
client = GDriveClient(drive)

# Tạo folder theo competition
competition_name = "titanic"
folder_path = f"Kaggle/Competitions/{competition_name}"
folder_id = create_folder_path(drive, folder_path)

# Upload submission file
submission_id = client.upload_file(
    local_path='/kaggle/working/submission.csv',
    file_name=f'submission_{datetime.now():%Y%m%d_%H%M%S}.csv',
    parent_id=folder_id
)

# Upload notebook (nếu có export)
notebook_id = client.upload_file(
    local_path='/kaggle/working/notebook.ipynb',
    file_name=f'notebook_{datetime.now():%Y%m%d_%H%M%S}.ipynb',
    parent_id=folder_id
)

print("✓ Backup completed!")
print(f"  - Submission: {submission_id}")
print(f"  - Notebook: {notebook_id}")
```

### Ví dụ 4: Upload Nhiều Files Cùng Lúc

```python
from gdrive_toolkit.utils import batch_upload
import glob

drive = quick_connect()

# Tìm tất cả file CSV trong working directory
csv_files = glob.glob('/kaggle/working/*.csv')

# Upload hết lên Google Drive
file_ids = batch_upload(
    drive,
    file_paths=csv_files,
    folder_id=None,  # hoặc chỉ định folder_id
    verbose=True
)

print(f"✓ Uploaded {len(file_ids)} files")
```

### Ví dụ 5: Sync Output Folder

```python
from gdrive_toolkit import quick_connect, create_folder_path
from gdrive_toolkit.client import GDriveClient

drive = quick_connect()
client = GDriveClient(drive)

# Tạo folder trên Drive
drive_folder_id = create_folder_path(drive, "Kaggle/Output")

# Zip toàn bộ output folder và upload
zip_id = client.zip_and_upload(
    folder_path='/kaggle/working',
    zip_name=f'kaggle_output_{pd.Timestamp.now():%Y%m%d}.zip',
    parent_id=drive_folder_id
)

print(f"✓ All output synced to Google Drive: {zip_id}")
```

---

## 🔧 Template Notebook Hoàn Chỉnh

```python
# Cell 1: Cài đặt
!pip install git+https://github.com/tieupham-ltp/gdrive-toolkit.git

# Cell 2: Import
import pandas as pd
from gdrive_toolkit import quick_connect, create_folder_path
from gdrive_toolkit.client import GDriveClient

# Cell 3: Kết nối Google Drive
drive = quick_connect()
client = GDriveClient(drive)

# Cell 4: Setup folders
project_folder = create_folder_path(drive, "Kaggle/MyProject")
print(f"Project folder ID: {project_folder}")

# Cell 5: Your analysis/training code here
# ... your code ...

# Cell 6: Save results to Google Drive
# Upload predictions
client.upload_file(
    local_path='/kaggle/working/predictions.csv',
    file_name='predictions.csv',
    parent_id=project_folder
)

# Backup all outputs
client.zip_and_upload(
    folder_path='/kaggle/working',
    zip_name='kaggle_outputs.zip',
    parent_id=project_folder
)

print("✓ All results saved to Google Drive!")
```

---

## ⚠️ Lưu Ý Quan Trọng

### 1. Kaggle Secrets
- **Bắt buộc** phải enable secrets trong notebook settings
- Secrets chỉ available khi notebook đang chạy
- Không thể access secrets từ forked notebooks (bảo mật)

### 2. Quyền Truy Cập
- Lần đầu chạy sẽ cần xác thực qua browser
- Link xác thực sẽ hiện trong output cell
- Copy link, mở trong tab mới, login và copy code về

### 3. Giới Hạn
- Kaggle có timeout cho notebook (9 hours max)
- Upload file lớn nên dùng `upload_large_file()` với chunk_size
- Google Drive API có quota limit (check tại Cloud Console)

### 4. Best Practices
- ✅ Dùng Kaggle Secrets cho credentials
- ✅ Tạo folder structure rõ ràng trên Drive
- ✅ Thêm timestamp vào tên file để tránh ghi đè
- ✅ Backup code và results sau mỗi experiment
- ✅ Xóa file tạm trong /kaggle/working sau khi upload

---

## 🆘 Xử Lý Lỗi Thường Gặp

### Lỗi: "Secrets not found"
```python
# Kiểm tra secrets có được enable không
import os
print("GDRIVE_CLIENT_ID:", os.getenv('GDRIVE_CLIENT_ID') is not None)
print("GDRIVE_CLIENT_SECRET:", os.getenv('GDRIVE_CLIENT_SECRET') is not None)
```
➡️ **Giải pháp**: Enable secrets trong Notebook Settings

### Lỗi: "Authentication failed"
➡️ **Giải pháp**: 
1. Kiểm tra client_id và client_secret có đúng không
2. Đảm bảo đã Enable Google Drive API
3. Thử xóa file `/kaggle/working/credentials.json` và authenticate lại

### Lỗi: "Quota exceeded"
➡️ **Giải pháp**: 
1. Check quota tại [Google Cloud Console](https://console.cloud.google.com/apis/api/drive.googleapis.com/quotas)
2. Đợi quota reset (thường reset hàng ngày)
3. Hoặc request tăng quota

---

## 📚 Tài Liệu Tham Khảo

- [API Reference](https://github.com/tieupham-ltp/gdrive-toolkit/blob/main/docs/API_REFERENCE.md)
- [CLI Guide](https://github.com/tieupham-ltp/gdrive-toolkit/blob/main/docs/CLI_GUIDE.md)
- [More Examples](https://github.com/tieupham-ltp/gdrive-toolkit/tree/main/examples)

---

## 💬 Hỗ Trợ

Gặp vấn đề? Tạo issue tại: https://github.com/tieupham-ltp/gdrive-toolkit/issues

---

**Happy Kaggling! 🎉**
