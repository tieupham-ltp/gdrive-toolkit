# gdrive-toolkit

```
   ____  ____       _             _____           _ _    _ _   
  / ___|  _ \ _ __(_)_   _____  |_   _|__   ___ | | | _(_) |_ 
 | |  _| | | | '__| \ \ / / _ \   | |/ _ \ / _ \| | |/ / | __|
 | |_| | |_| | |  | |\ V /  __/   | | (_) | (_) | |   <| | |_ 
  \____|____/|_|  |_| \_/ \___|   |_|\___/ \___/|_|_|\_\_|\__|
                                                                
```

**Thư viện Python gọn nhẹ để làm việc với Google Drive trên mọi môi trường**

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Tính năng chính

- ✅ **Auto-detect môi trường**: Tự động nhận diện Colab, Kaggle, hay local
- ✅ **API đơn giản**: Dễ sử dụng, tên hàm rõ ràng
- ✅ **Upload/Download**: Tải lên và tải xuống file nhanh chóng
- ✅ **Tìm kiếm mạnh mẽ**: Hỗ trợ Google Drive query syntax
- ✅ **Quản lý folder**: Tạo, chia sẻ, xóa folder dễ dàng
- ✅ **Batch operations**: Xử lý nhiều file cùng lúc
- ✅ **Multi-environment**: Hoạt động trên Kaggle, Colab, local
- ✅ **Tiếng Việt**: Docstring + comments song ngữ

---

## 📦 Cài đặt

```bash
pip install git+https://github.com/yourusername/gdrive-toolkit.git
```

## 🚀 Sử dụng nhanh

```python
from gdrive_toolkit import quick_connect, upload_file, download_file

# Kết nối tự động (nhận diện môi trường)
drive = quick_connect()

# Upload file
file_id = upload_file(drive, "myfile.txt")

# Download file
download_file(drive, file_id=file_id, save_path="./downloads/")

# Tìm kiếm file
from gdrive_toolkit import search_files
files = search_files(drive, file_name="report")

# Tạo folder
from gdrive_toolkit import create_folder
folder_id = create_folder(drive, "My Project")

# Chia sẻ file
from gdrive_toolkit import share_file
link = share_file(drive, file_id=folder_id)
print(f"Link chia sẻ: {link}")
```

## 📖 Tài liệu

- [Quick Start Guide](docs/QUICK_START.md) - Bắt đầu trong 5 phút
- [API Reference](docs/API_REFERENCE.md) - Tài liệu đầy đủ
- [Credentials Setup](docs/CREDENTIALS_SETUP.md) - Hướng dẫn thiết lập
- [Examples](examples/) - Các ví dụ mẫu

## 🎓 Ví dụ

### Colab
```python
# Không cần setup gì cả!
from gdrive_toolkit import quick_connect
drive = quick_connect()
```

### Kaggle
```python
# Thêm secrets vào Kaggle (xem docs/CREDENTIALS_SETUP.md)
from gdrive_toolkit import quick_connect
drive = quick_connect()
```

### Local
```python
# Cần file client_secrets.json (xem docs/CREDENTIALS_SETUP.md)
from gdrive_toolkit import quick_connect
drive = quick_connect()
```

## 🛠️ Chức năng

| Chức năng | Hàm |
|-----------|-----|
| Xác thực tự động | `quick_connect()` |
| Upload file | `upload_file()` |
| Download file | `download_file()` |
| Tìm kiếm file | `search_files()` |
| Xóa file | `delete_file()` |
| Tạo folder | `create_folder()` |
| Tạo nested folder | `create_folder_path()` |
| Chia sẻ file/folder | `share_file()` |
| Batch upload | `batch_upload()` |
| Batch download | `batch_download()` |

## 🔧 Requirements

- Python ≥ 3.9
- pydrive2 ≥ 1.15.0
- google-auth ≥ 2.0.0

## 📁 Cấu trúc project

```
gdrive-toolkit/
├── gdrive_toolkit/          # Package chính
│   ├── __init__.py         # Main exports
│   ├── auth.py             # Authentication
│   ├── operations.py       # File operations
│   ├── folder.py           # Folder operations
│   └── utils.py            # Utilities
├── examples/               # Ví dụ sử dụng
│   ├── basic_usage.py
│   ├── folder_operations.py
│   ├── batch_operations.py
│   ├── colab_example.py
│   └── kaggle_example.py
├── docs/                   # Tài liệu
│   ├── QUICK_START.md
│   ├── API_REFERENCE.md
│   └── CREDENTIALS_SETUP.md
├── tests/                  # Tests
│   └── test_install.py
├── setup.py               # Setup script
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🧪 Kiểm tra

```bash
python tests/test_install.py
```

## 🤝 Đóng góp

Contributions rất được hoan nghênh! Xem [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 License

MIT License - xem [LICENSE](LICENSE)

## 🌟 Credits

- Built with [PyDrive2](https://github.com/iterative/PyDrive2)
- Inspired by the need for simple Google Drive operations

## 💬 Support

- 📖 [Documentation](docs/)
- 💡 [Examples](examples/)
- 🐛 [Issues](https://github.com/yourusername/gdrive-toolkit/issues)

---

**Made with ❤️ for data scientists and developers working with Google Drive**
