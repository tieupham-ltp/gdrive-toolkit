# API Reference

Complete API documentation for gdrive-toolkit.

## Table of Contents

- [Authentication](#authentication)
- [File Operations](#file-operations)
- [Folder Operations](#folder-operations)
- [Utilities](#utilities)

---

## Authentication

### quick_connect()

Auto-detect environment and authenticate to Google Drive.

```python
from gdrive_toolkit import quick_connect

drive = quick_connect(
    credentials_file="mycreds.txt",  # Optional, local only
    client_secrets_file="client_secrets.json"  # Optional, local only
)
```

**Parameters:**
- `credentials_file` (str): Path to save credentials (default: "mycreds.txt")
- `client_secrets_file` (str): Path to OAuth secrets (default: "client_secrets.json")

**Returns:** `GoogleDrive` - Authenticated drive instance

---

### authenticate_local()

Authenticate on local machine using OAuth.

```python
from gdrive_toolkit import authenticate_local

drive = authenticate_local()
```

**Returns:** `GoogleDrive` instance

---

### authenticate_colab()

Authenticate in Google Colab.

```python
from gdrive_toolkit import authenticate_colab

drive = authenticate_colab()
```

**Returns:** `GoogleDrive` instance

---

### authenticate_kaggle()

Authenticate in Kaggle using secrets.

```python
from gdrive_toolkit import authenticate_kaggle

drive = authenticate_kaggle()
```

**Returns:** `GoogleDrive` instance

**Requires:** Kaggle secrets (see [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md))

---

## File Operations

### upload_file()

Upload a file to Google Drive.

```python
from gdrive_toolkit import upload_file

file_id = upload_file(
    drive,
    file_path="data.csv",
    folder_id=None,  # Optional
    file_name="renamed_data.csv"  # Optional
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `file_path` (str): Local file path to upload
- `folder_id` (str, optional): Target folder ID
- `file_name` (str, optional): Custom name for uploaded file

**Returns:** `str` - File ID

---

### download_file()

Download a file from Google Drive.

```python
from gdrive_toolkit import download_file

path = download_file(
    drive,
    file_id="abc123",  # Optional
    file_name="data.csv",  # Optional
    save_path="./downloads/",
    query=None  # Optional
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `file_id` (str, optional): File ID to download
- `file_name` (str, optional): File name to search
- `save_path` (str): Save location (default: ".")
- `query` (str, optional): Custom search query

**Returns:** `str` - Path to downloaded file

**Note:** Either `file_id`, `file_name`, or `query` must be provided.

---

### search_files()

Search for files in Google Drive.

```python
from gdrive_toolkit import search_files

files = search_files(
    drive,
    query=None,
    folder_id=None,
    file_name=None,
    max_results=100,
    trashed=False
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `query` (str, optional): Custom search query
- `folder_id` (str, optional): Search in specific folder
- `file_name` (str, optional): Search by name
- `max_results` (int): Max results (default: 100)
- `trashed` (bool): Include trashed files (default: False)

**Returns:** `List[Dict]` - List of file metadata

**Example queries:**
```python
# Search CSV files
files = search_files(drive, query="mimeType = 'text/csv'")

# Search in folder
files = search_files(drive, folder_id="folder_id_here")

# Search by name
files = search_files(drive, file_name="report")
```

---

### delete_file()

Delete a file from Google Drive.

```python
from gdrive_toolkit import delete_file

success = delete_file(
    drive,
    file_id="abc123",  # Optional
    file_name="old_file.txt",  # Optional
    confirm=True
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `file_id` (str, optional): File ID
- `file_name` (str, optional): File name
- `confirm` (bool): Ask confirmation (default: True)

**Returns:** `bool` - True if deleted

---

### get_file_info()

Get detailed file information.

```python
from gdrive_toolkit import get_file_info

info = get_file_info(drive, file_id="abc123")
print(info['title'], info['size'])
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `file_id` (str): File ID

**Returns:** `Dict` - File metadata

---

## Folder Operations

### create_folder()

Create a new folder.

```python
from gdrive_toolkit import create_folder

folder_id = create_folder(
    drive,
    folder_name="My Folder",
    parent_id=None  # Optional
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `folder_name` (str): Name of folder
- `parent_id` (str, optional): Parent folder ID

**Returns:** `str` - Folder ID

---

### create_folder_path()

Create nested folder structure.

```python
from gdrive_toolkit import create_folder_path

folder_id = create_folder_path(
    drive,
    path="Projects/2025/Data",
    parent_id=None
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `path` (str): Folder path (e.g., "A/B/C")
- `parent_id` (str, optional): Parent folder ID

**Returns:** `str` - ID of final folder

---

### share_file()

Share a file or folder.

```python
from gdrive_toolkit import share_file

link = share_file(
    drive,
    file_id="abc123",
    permission="reader",  # or "writer", "commenter"
    share_type="anyone"
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `file_id` (str): File/folder ID
- `permission` (str): "reader", "writer", or "commenter"
- `share_type` (str): "anyone", "user", "group", "domain"

**Returns:** `str` - Shareable link

---

### list_folders()

List all folders.

```python
from gdrive_toolkit import list_folders

folders = list_folders(
    drive,
    parent_id=None,
    max_results=100
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `parent_id` (str, optional): Parent folder ID
- `max_results` (int): Max results

**Returns:** `List[Dict]` - List of folders

---

### delete_folder()

Delete a folder and its contents.

```python
from gdrive_toolkit import delete_folder

success = delete_folder(
    drive,
    folder_id="xyz789",  # Optional
    folder_name="Old Folder",  # Optional
    confirm=True
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `folder_id` (str, optional): Folder ID
- `folder_name` (str, optional): Folder name
- `confirm` (bool): Ask confirmation (default: True)

**Returns:** `bool` - True if deleted

---

## Utilities

### batch_upload()

Upload multiple files at once.

```python
from gdrive_toolkit import batch_upload

file_ids = batch_upload(
    drive,
    file_paths=["file1.txt", "file2.txt", "file3.txt"],
    folder_id=None,
    verbose=True
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `file_paths` (List[str]): List of file paths
- `folder_id` (str, optional): Target folder
- `verbose` (bool): Show progress

**Returns:** `List[str]` - List of file IDs

---

### batch_download()

Download multiple files at once.

```python
from gdrive_toolkit import batch_download

paths = batch_download(
    drive,
    file_ids=["id1", "id2", "id3"],
    save_dir="./downloads",
    verbose=True
)
```

**Parameters:**
- `drive` (GoogleDrive): Authenticated drive instance
- `file_ids` (List[str]): List of file IDs
- `save_dir` (str): Directory to save files
- `verbose` (bool): Show progress

**Returns:** `List[str]` - List of downloaded paths

---

### print_file_list()

Pretty print file list.

```python
from gdrive_toolkit import print_file_list, search_files

files = search_files(drive)
print_file_list(files, verbose=True)
```

**Parameters:**
- `files` (List[Dict]): List of file metadata
- `verbose` (bool): Show detailed info

---

### format_size()

Format bytes to human-readable size.

```python
from gdrive_toolkit import format_size

print(format_size(1536000))  # "1.46 MB"
```

**Parameters:**
- `size_bytes` (int): Size in bytes

**Returns:** `str` - Formatted size

---

## Google Drive Query Syntax

For advanced searches, use Google Drive query syntax with `search_files()`:

```python
# Search by MIME type
search_files(drive, query="mimeType = 'application/pdf'")

# Search by name contains
search_files(drive, query="title contains 'report'")

# Search by exact name
search_files(drive, query="title = 'data.csv'")

# Modified after date
search_files(drive, query="modifiedDate >= '2025-01-01'")

# Combine queries
search_files(drive, query="mimeType = 'text/csv' and title contains 'data'")

# Search in folder
search_files(drive, query="'folder_id' in parents")
```

Common MIME types:
- Text: `text/plain`
- CSV: `text/csv`
- PDF: `application/pdf`
- Folder: `application/vnd.google-apps.folder`
- Google Docs: `application/vnd.google-apps.document`
- Google Sheets: `application/vnd.google-apps.spreadsheet`
