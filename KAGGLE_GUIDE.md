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

# ⚠️ NẾU AUTO-DETECT BỊ SAI (nhận diện là Colab thay vì Kaggle):
# Dùng option force_env để chỉ định rõ môi trường
drive = quick_connect(force_env='kaggle')
```

---

## 🔑 Thiết Lập Credentials

⚠️ **Lưu ý quan trọng:** Kaggle notebooks không hỗ trợ authentication interactive (nhập code trực tiếp). Bạn cần setup credentials trước bằng 1 trong 2 cách sau:

### Cách 1: Dùng Refresh Token (Khuyến nghị ⭐)

#### Bước 1: Tạo OAuth 2.0 Credentials trên Google Cloud

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới hoặc chọn project có sẵn
3. Enable **Google Drive API**:
   - Vào "APIs & Services" > "Library"
   - Tìm "Google Drive API" và click "Enable"

4. Tạo OAuth 2.0 Credentials:
   - Vào "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: **"Desktop app"** (quan trọng!)
   - Đặt tên: "Kaggle Drive Access"
   - Click "Create"

5. Download file JSON credentials (`client_secrets.json`)

#### Bước 2: Tạo Refresh Token (Trên Máy Local)

**Chạy script trên máy local để lấy refresh token:**

```bash
# Clone repo
git clone https://github.com/tieupham-ltp/gdrive-toolkit.git
cd gdrive-toolkit

# Cài pydrive2
pip install pydrive2

# Chạy script (client_secrets.json phải ở cùng folder)
python get_refresh_token.py
```

Script sẽ:
1. Mở browser để bạn đăng nhập Google
2. Sau khi authorize, hiển thị 3 giá trị:
   - `GDRIVE_CLIENT_ID`
   - `GDRIVE_CLIENT_SECRET`
   - `GDRIVE_REFRESH_TOKEN` ⭐
3. Lưu vào file `kaggle_secrets.txt`

💡 **Mẹo:** Nếu không có máy local, có thể chạy script này trên Google Colab!

#### Bước 3: Thêm vào Kaggle Secrets

1. Truy cập [Kaggle Settings > Secrets](https://www.kaggle.com/settings)
2. Click "Add a new secret"
3. Thêm **3 secrets** (copy từ output script):

```
Name: GDRIVE_CLIENT_ID
Value: [Paste client_id từ script output]

Name: GDRIVE_CLIENT_SECRET
Value: [Paste client_secret từ script output]

Name: GDRIVE_REFRESH_TOKEN
Value: [Paste refresh_token từ script output]
```

#### Bước 4: Enable Secrets trong Notebook

1. Mở Kaggle Notebook
2. Click **Settings** (⚙️ góc phải)
3. Trong **Secrets**, toggle ON cả 3:
   - ✅ GDRIVE_CLIENT_ID
   - ✅ GDRIVE_CLIENT_SECRET
   - ✅ GDRIVE_REFRESH_TOKEN

#### Bước 5: Sử Dụng

```python
from gdrive_toolkit import quick_connect

# Kết nối (tự động dùng refresh token từ Kaggle Secrets)
drive = quick_connect(force_env='kaggle')

# Upload file
from gdrive_toolkit import upload_file
upload_file(drive, '/kaggle/working/result.csv')
```

✅ **Xong!** Không cần authenticate lại, tự động hoạt động mỗi lần chạy!

---

### Cách 2: Upload Credentials File

Nếu bạn đã có file credentials từ máy local:

**Bước 1: Tạo credentials trên local**
```python
# Chạy trên máy local
from gdrive_toolkit import quick_connect
drive = quick_connect()  # Sẽ tạo file mycreds.txt
```

**Bước 2: Upload lên Kaggle**
1. Tạo dataset Kaggle chứa file `mycreds.txt`
2. Add dataset vào notebook

**Bước 3: Copy file trong notebook**
```python
# Copy credentials file
!cp /kaggle/input/your-dataset/mycreds.txt /kaggle/working/gdrive_credentials.json

# Sau đó connect (chỉ cần CLIENT_ID và CLIENT_SECRET secrets)
from gdrive_toolkit import quick_connect
drive = quick_connect(force_env='kaggle')
```

---

### So Sánh 2 Cách:

| | Cách 1: Refresh Token | Cách 2: Upload File |
|---|---|---|
| **Setup** | 1 lần trên local | Mỗi lần notebook mới |
| **Secrets cần** | 3 (CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN) | 2 + file upload |
| **Tiện lợi** | ⭐⭐⭐⭐⭐ Auto | ⭐⭐⭐ Phải copy file |
| **Bảo mật** | ⭐⭐⭐⭐⭐ Token trong Secrets | ⭐⭐⭐ File public nếu dataset public |

**→ Khuyến nghị: Dùng Cách 1 (Refresh Token)**

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

drive = quick_connect(force_env='kaggle')

# Upload 1 file - Lưu ý: dùng 'file_path' không phải 'local_path'
file_id = upload_file(
    drive, 
    file_path='/kaggle/input/dataset/data.csv',  # ✅ Đúng
    file_name='my_data.csv',
    folder_id=None  # None = upload vào root
)

print(f"File uploaded with ID: {file_id}")
```

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
    file_path='/kaggle/working/result.csv',  # ✅ Đúng: file_path
    folder_id=folder_id
)
```

### 4️⃣ Zip và Upload Folder

```python
from gdrive_toolkit import zip_and_upload

# Zip toàn bộ folder và upload lên Google Drive
file_id = zip_and_upload(
    drive,
    folder_path='/kaggle/working/output',
    zip_name='kaggle_results.zip',
    parent_id=None  # None = upload vào root
)

print(f"Zipped and uploaded! File ID: {file_id}")
```

---

## 🎯 Ví Dụ Thực Tế

### Ví dụ 1: Save Model vào Google Drive

```python
from gdrive_toolkit import quick_connect, create_folder_path, upload_file
import joblib

# 1. Train model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
# ... train model ...

# 2. Save model locally
joblib.dump(model, '/kaggle/working/model.pkl')

# 3. Upload lên Google Drive
drive = quick_connect(force_env='kaggle')

# Tạo folder cho project
folder_id = create_folder_path(drive, "Kaggle/Models/RandomForest")

# Upload model
model_id = upload_file(
    drive,
    file_path='/kaggle/working/model.pkl',  # ✅ Đúng: file_path
    file_name=f'model_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.pkl',
    folder_id=folder_id
)

print(f"✓ Model saved to Google Drive: {model_id}")
```

### Ví dụ 2: Download Dataset từ Google Drive

```python
from gdrive_toolkit import quick_connect, search_files, download_file
import pandas as pd

# Kết nối
drive = quick_connect(force_env='kaggle')

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
from gdrive_toolkit import quick_connect, create_folder_path, upload_file
from datetime import datetime

drive = quick_connect(force_env='kaggle')

# Tạo folder theo competition
competition_name = "titanic"
folder_path = f"Kaggle/Competitions/{competition_name}"
folder_id = create_folder_path(drive, folder_path)

# Upload submission file
submission_id = upload_file(
    drive,
    file_path='/kaggle/working/submission.csv',  # ✅ Đúng: file_path
    file_name=f'submission_{datetime.now():%Y%m%d_%H%M%S}.csv',
    folder_id=folder_id
)

# Upload notebook (nếu có export)
notebook_id = upload_file(
    drive,
    file_path='/kaggle/working/notebook.ipynb',  # ✅ Đúng: file_path
    file_name=f'notebook_{datetime.now():%Y%m%d_%H%M%S}.ipynb',
    folder_id=folder_id
)

print("✓ Backup completed!")
print(f"  - Submission: {submission_id}")
print(f"  - Notebook: {notebook_id}")
```

### Ví dụ 4: Upload Nhiều Files Cùng Lúc

```python
from gdrive_toolkit import batch_upload, quick_connect
import glob

drive = quick_connect(force_env='kaggle')

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

### Ví dụ 5: Zip và Upload Output Folder

```python
from gdrive_toolkit import quick_connect, create_folder_path, zip_and_upload
import pandas as pd

drive = quick_connect(force_env='kaggle')

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
from gdrive_toolkit import quick_connect, create_folder_path, upload_file, zip_and_upload

# Cell 3: Kết nối Google Drive
drive = quick_connect(force_env='kaggle')

# Cell 4: Setup folders
project_folder = create_folder_path(drive, "Kaggle/MyProject")
print(f"Project folder ID: {project_folder}")

# Cell 5: Your analysis/training code here
# ... your code ...

# Cell 6: Save results to Google Drive
# Upload predictions
upload_file(
    drive,
    file_path='/kaggle/working/predictions.csv',  # ✅ Đúng: file_path
    file_name='predictions.csv',
    folder_id=project_folder
)

# Backup all outputs
zip_and_upload(
    drive,
    folder_path='/kaggle/working',
    zip_name='kaggle_outputs.zip',
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

### Lỗi: "Detected environment: COLAB" trên Kaggle ⚠️

**Triệu chứng:** Khi chạy `quick_connect()` trên Kaggle nhưng hiện "Detected environment: COLAB"

**Nguyên nhân:** Một số Kaggle notebook có package `google.colab` được cài sẵn, gây nhầm lẫn trong auto-detection

**Giải pháp:**
```python
# Option 1: Force environment (Khuyến nghị)
from gdrive_toolkit import quick_connect
drive = quick_connect(force_env='kaggle')

# Option 2: Gọi trực tiếp hàm authenticate_kaggle
from gdrive_toolkit.auth import authenticate_kaggle
drive = authenticate_kaggle()
```

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

### Lỗi: Version cũ không update
```python
# Cài lại với force reinstall và no cache
!pip uninstall -y gdrive-toolkit
!pip install --no-cache-dir --force-reinstall git+https://github.com/tieupham-ltp/gdrive-toolkit.git

# Sau đó restart kernel: Session > Restart Session
```

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
