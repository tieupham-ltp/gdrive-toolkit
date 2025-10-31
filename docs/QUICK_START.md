# Quick Start Guide

Get started with gdrive-toolkit in 5 minutes!

## Installation

```bash
pip install git+https://github.com/yourusername/gdrive-toolkit.git
```

## Quick Test

```bash
python tests/test_install.py
```

## Setup Credentials

### Option 1: Local Machine (Recommended for first-time users)

1. Download OAuth credentials from Google Cloud Console
2. Save as `client_secrets.json` in your project
3. See [detailed instructions](CREDENTIALS_SETUP.md)

### Option 2: Google Colab

No setup needed! Just import and use.

### Option 3: Kaggle

Add secrets to Kaggle (see [Kaggle setup](CREDENTIALS_SETUP.md#for-kaggle))

## First Script

Create `test.py`:

```python
from gdrive_toolkit import quick_connect, upload_file

# Connect (auto-detects your environment)
drive = quick_connect()

# Create a test file
with open("hello.txt", "w") as f:
    f.write("Hello from gdrive-toolkit!")

# Upload it
file_id = upload_file(drive, "hello.txt")
print(f"Uploaded! File ID: {file_id}")
```

Run it:
```bash
python test.py
```

## Next Steps

- Check [examples/](../examples/) folder for more examples
- Read [API Reference](API_REFERENCE.md) for all functions
- Join the discussion in GitHub Issues

## Common Tasks

### Upload a file
```python
from gdrive_toolkit import quick_connect, upload_file

drive = quick_connect()
file_id = upload_file(drive, "myfile.txt")
```

### Download a file
```python
from gdrive_toolkit import download_file

download_file(drive, file_id="abc123", save_path="./downloads/")
```

### Search files
```python
from gdrive_toolkit import search_files

files = search_files(drive, file_name="report")
for f in files:
    print(f['title'])
```

### Create folder
```python
from gdrive_toolkit import create_folder

folder_id = create_folder(drive, "My Folder")
```

### Share file
```python
from gdrive_toolkit import share_file

link = share_file(drive, file_id="abc123")
print(f"Share: {link}")
```

## Troubleshooting

See [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md#troubleshooting) for common issues.

## Get Help

- 📖 [Full Documentation](API_REFERENCE.md)
- 💡 [Examples](../examples/)
- 🐛 [Report Issues](https://github.com/yourusername/gdrive-toolkit/issues)
