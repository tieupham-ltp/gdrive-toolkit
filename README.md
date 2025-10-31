# 🚀 gdrive-toolkit

A lightweight and user-friendly Python library for working with Google Drive across multiple environments (Kaggle, Google Colab, local machines, servers).

## ✨ Features

- 🔐 **Smart Authentication**: Auto-detects environment (Colab, Kaggle, local) and authenticates accordingly
- 📤 **Upload Files**: Easy file upload with progress tracking
- 📥 **Download Files**: Download files by ID or name
- 🔍 **Search Files**: Find files and folders with flexible queries
- 🗑️ **Delete Files**: Remove files from Google Drive
- 📁 **Folder Management**: Create folders and organize files
- 🔗 **Share Links**: Generate shareable links with customizable permissions
- 🎯 **Simple API**: Clean, intuitive function names and parameters
- 🌍 **Multi-Environment**: Works seamlessly on Kaggle, Colab, and local machines

## 📦 Installation

### From GitHub

```bash
pip install git+https://github.com/yourusername/gdrive-toolkit.git
```

### From source

```bash
git clone https://github.com/yourusername/gdrive-toolkit.git
cd gdrive-toolkit
pip install -e .
```

## 🚀 Quick Start

### 1. Authentication

The library provides a `quick_connect()` function that automatically detects your environment:

```python
from gdrive_toolkit import quick_connect

# Automatically detects Colab, Kaggle, or local environment
drive = quick_connect()
```

### 2. Upload Files

```python
from gdrive_toolkit import upload_file

# Upload a single file
file_id = upload_file(drive, "path/to/local/file.txt", folder_id=None)
print(f"Uploaded file ID: {file_id}")

# Upload to a specific folder
file_id = upload_file(drive, "data.csv", folder_id="your_folder_id")
```

### 3. Download Files

```python
from gdrive_toolkit import download_file

# Download by file ID
download_file(drive, file_id="file_id_here", save_path="downloaded_file.txt")

# Download by file name (searches and downloads first match)
download_file(drive, file_name="myfile.txt", save_path="./downloads/")
```

### 4. Search Files

```python
from gdrive_toolkit import search_files

# Search by name
files = search_files(drive, query="title contains 'report'")

# Search in specific folder
files = search_files(drive, folder_id="folder_id_here")

# Get all files
all_files = search_files(drive)

for file in files:
    print(f"{file['title']} - {file['id']}")
```

### 5. Create Folders

```python
from gdrive_toolkit import create_folder

# Create folder in root
folder_id = create_folder(drive, "My New Folder")

# Create subfolder
subfolder_id = create_folder(drive, "Subfolder", parent_id=folder_id)
```

### 6. Delete Files

```python
from gdrive_toolkit import delete_file

# Delete by file ID
delete_file(drive, file_id="file_id_here")

# Delete by file name
delete_file(drive, file_name="unwanted_file.txt")
```

### 7. Share Files

```python
from gdrive_toolkit import share_file

# Get shareable link (anyone with link can view)
link = share_file(drive, file_id="file_id_here")
print(f"Share link: {link}")

# Share with edit permission
link = share_file(drive, file_id="file_id_here", permission="writer")
```

## 🔧 Advanced Usage

### Custom Authentication

```python
from gdrive_toolkit.auth import authenticate_local, authenticate_colab, authenticate_kaggle

# Force specific authentication method
# Local (uses browser OAuth)
drive = authenticate_local()

# Colab (uses Colab's built-in auth)
drive = authenticate_colab()

# Kaggle (uses kaggle_secrets)
drive = authenticate_kaggle()
```

### Batch Operations

```python
from gdrive_toolkit import upload_file, create_folder
import os

# Create a folder and upload multiple files
folder_id = create_folder(drive, "Batch Upload")

for filename in os.listdir("./data"):
    if filename.endswith(".csv"):
        file_path = os.path.join("./data", filename)
        upload_file(drive, file_path, folder_id=folder_id)
        print(f"Uploaded: {filename}")
```

## 📋 Environment Setup

### Local Machine

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `client_secrets.json` and place it in your project root
6. Run `quick_connect()` - it will open browser for authentication

### Google Colab

No setup needed! Just run:

```python
from gdrive_toolkit import quick_connect
drive = quick_connect()
```

### Kaggle

1. Add Google credentials as Kaggle secrets:
   - Go to Kaggle Account Settings → Add-ons → Secrets
   - Add secrets: `GDRIVE_CLIENT_ID`, `GDRIVE_CLIENT_SECRET`, `GDRIVE_REFRESH_TOKEN`
2. Run `quick_connect()` in your Kaggle notebook

## 🛠️ API Reference

### Authentication

- `quick_connect()` - Auto-detect environment and authenticate
- `authenticate_local()` - Authenticate on local machine
- `authenticate_colab()` - Authenticate in Google Colab
- `authenticate_kaggle()` - Authenticate in Kaggle

### File Operations

- `upload_file(drive, file_path, folder_id=None)` - Upload a file
- `download_file(drive, file_id=None, file_name=None, save_path=".")` - Download a file
- `search_files(drive, query=None, folder_id=None, max_results=100)` - Search files
- `delete_file(drive, file_id=None, file_name=None)` - Delete a file

### Folder Operations

- `create_folder(drive, folder_name, parent_id=None)` - Create a folder
- `share_file(drive, file_id, permission="reader")` - Share a file/folder

## 📝 Requirements

- Python >= 3.9
- pydrive2 >= 1.15.0
- google-auth >= 2.0.0
- google-auth-oauthlib >= 1.0.0
- google-auth-httplib2 >= 0.1.0

## 📄 License

MIT License - feel free to use in your projects!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Issues

If you encounter any issues, please report them on the [GitHub Issues page](https://github.com/yourusername/gdrive-toolkit/issues).

## 🌟 Support

If you find this library useful, please give it a star on GitHub! ⭐
