# CLI Usage Guide

gdrive-toolkit comes with a powerful command-line interface (CLI) for quick operations.

## Installation

After installing gdrive-toolkit, you get two CLI commands:
- `gdrive-toolkit` (full name)
- `gdt` (short alias)

```bash
pip install git+https://github.com/yourusername/gdrive-toolkit.git
```

## Quick Reference

```bash
# Show help
gdrive-toolkit --help
gdt --help

# Show version
gdrive-toolkit --version

# Show environment info
gdrive-toolkit info
```

## Commands

### Upload

Upload a file to Google Drive:

```bash
# Upload to root
gdrive-toolkit upload myfile.txt

# Upload to a folder
gdrive-toolkit upload myfile.txt --folder "My Documents"

# Upload with custom name
gdrive-toolkit upload myfile.txt --name "renamed.txt"

# Upload and share
gdrive-toolkit upload myfile.txt --share
```

### Download

Download a file from Google Drive:

```bash
# Download to current directory
gdrive-toolkit download FILE_ID

# Download to specific path
gdrive-toolkit download FILE_ID --output ./downloads/

# Short alias
gdt download FILE_ID -o ./data/
```

### Search

Search for files:

```bash
# Search by name
gdrive-toolkit search "report"

# Search in specific folder
gdrive-toolkit search --folder FOLDER_ID

# Filter by type
gdrive-toolkit search --type "text/csv"

# Limit results
gdrive-toolkit search "data" --limit 10

# Short alias
gdt search "*.pdf" -l 5
```

### List Files

List files in a folder:

```bash
# List root folder
gdrive-toolkit ls

# List specific folder
gdrive-toolkit ls FOLDER_ID

# Limit results
gdt ls --limit 20
```

### Create Folder

Create a new folder:

```bash
# Create in root
gdrive-toolkit mkdir "My Folder"

# Create in specific parent
gdrive-toolkit mkdir "Subfolder" --parent PARENT_ID

# Short alias
gdt mkdir "Projects"
```

### Delete

Delete a file or folder:

```bash
# Delete with confirmation
gdrive-toolkit delete FILE_ID

# Delete without confirmation
gdrive-toolkit delete FILE_ID --yes

# Short alias
gdt delete FILE_ID -y
```

### Share

Get a shareable link:

```bash
# Share file (anyone can view)
gdrive-toolkit share FILE_ID

# Output:
# ✅ Shareable link:
# https://drive.google.com/file/d/...
```

### Zip and Upload

Zip a folder and upload:

```bash
# Zip and upload
gdrive-toolkit zip-upload ./my_folder

# Custom zip name
gdrive-toolkit zip-upload ./data --name "backup.zip"

# Upload to specific folder
gdt zip-upload ./project --folder FOLDER_ID
```

### Info

Show environment and authentication info:

```bash
gdrive-toolkit info

# Output:
# ============================================================
# gdrive-toolkit - Information
# ============================================================
# Version: 0.1.0
# Environment: LOCAL
# Python: 3.11.0
# Credentials file: ✓ mycreds.txt
# Client secrets: ✓ client_secrets.json
# ============================================================
```

## Examples

### Complete Workflow

```bash
# 1. Check setup
gdt info

# 2. Create a project folder
gdt mkdir "ML Project"

# 3. Search for the folder ID
gdt search "ML Project"
# Copy the folder ID

# 4. Upload files to the folder
gdt upload data.csv --folder FOLDER_ID
gdt upload model.pkl --folder FOLDER_ID

# 5. List folder contents
gdt ls FOLDER_ID

# 6. Share the folder
gdt share FOLDER_ID

# 7. Download when needed
gdt download FILE_ID -o ./backups/
```

### Backup Workflow

```bash
# Create backup folder
gdt mkdir "Backups $(date +%Y-%m-%d)"

# Get folder ID
BACKUP_ID=$(gdt search "Backups" | grep "ID:" | head -1 | awk '{print $2}')

# Zip and upload current project
gdt zip-upload ./my_project --folder $BACKUP_ID

# Share backup
gdt share $BACKUP_ID
```

### Search and Download

```bash
# Find all CSV files
gdt search --type "text/csv" -l 100 > csv_files.txt

# Download specific file
gdt download abc123xyz -o ./data/

# Batch download (manual)
for id in file_id_1 file_id_2 file_id_3; do
    gdt download $id -o ./downloads/
done
```

## Options

### Global Options

All commands support:

```bash
--help     Show help message
--version  Show version
```

### Common Options

```bash
-f, --folder    Folder name or ID
-o, --output    Output path
-n, --name      Custom name
-t, --type      MIME type filter
-l, --limit     Maximum results
-y, --yes       Skip confirmation
--share         Share after upload
```

## Troubleshooting

### Authentication Issues

```bash
# Check credentials
gdt info

# If credentials missing, run in Python:
python -c "from gdrive_toolkit import quick_connect; quick_connect()"
```

### Permission Denied

Make sure you have proper permissions on Google Drive.

### File Not Found

```bash
# Search first to get correct ID
gdt search "filename"

# Then use the ID
gdt download CORRECT_FILE_ID
```

## Advanced Usage

### Combining with Other Tools

```bash
# Find and delete old files
gdt search "old" | grep "ID:" | cut -d' ' -f2 | while read id; do
    gdt delete $id -y
done

# Download all PDFs
gdt search --type "application/pdf" -l 100 > pdfs.txt
# Process pdfs.txt to extract IDs and download

# Backup multiple folders
for folder in Documents Photos Videos; do
    gdt zip-upload ./$folder --name "${folder}_backup.zip"
done
```

### Scripting

Create a backup script (`backup.sh`):

```bash
#!/bin/bash

echo "Starting backup..."

# Create dated folder
FOLDER_NAME="Backup_$(date +%Y%m%d)"
gdt mkdir "$FOLDER_NAME"

# Upload files
gdt upload important.txt --folder "$FOLDER_NAME"
gdt upload data.csv --folder "$FOLDER_NAME"

# Share and save link
gdt share $(gdt search "$FOLDER_NAME" | grep ID | cut -d' ' -f2) > backup_link.txt

echo "Backup complete! Link saved to backup_link.txt"
```

## Tips

1. **Use short alias**: `gdt` is faster to type than `gdrive-toolkit`

2. **Save folder IDs**: Store frequently used folder IDs in a file

3. **Batch operations**: Use shell scripting for bulk operations

4. **Search first**: Always search to get correct IDs before operations

5. **Check info**: Run `gdt info` to verify setup before starting work

## Getting Help

```bash
# General help
gdt --help

# Command-specific help
gdt upload --help
gdt search --help
gdt download --help
```

For more detailed documentation, see:
- [API Reference](API_REFERENCE.md)
- [Quick Start](QUICK_START.md)
- [Examples](../examples/)
