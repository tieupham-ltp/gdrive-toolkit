"""
Utility functions for gdrive-toolkit.
Các hàm tiện ích cho gdrive-toolkit.
"""

from typing import List, Dict, Any, Optional
import os
import sys
import mimetypes


def format_size(size_bytes: float) -> str:
    """
    Format file size to human-readable format.
    Định dạng kích thước file dễ đọc.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        str: Formatted size (e.g., "1.5 MB")
    """
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def print_file_list(files: List[Dict[str, Any]], verbose: bool = False) -> None:
    """
    Pretty print a list of files.
    In đẹp danh sách file.
    
    Args:
        files: List of file metadata dictionaries
        verbose: Show detailed information (default: False)
    """
    if not files:
        print("No files found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(files)} file(s)")
    print(f"{'='*80}\n")
    
    for i, file in enumerate(files, 1):
        title = file.get('title', 'Untitled')
        file_id = file.get('id', 'N/A')
        mime_type = file.get('mimeType', 'unknown')
        
        print(f"{i}. {title}")
        print(f"   ID: {file_id}")
        
        if verbose:
            size = file.get('size', 'N/A')
            if size != 'N/A' and size.isdigit():
                size = format_size(int(size))
            
            created = file.get('createdDate', 'N/A')
            modified = file.get('modifiedDate', 'N/A')
            link = file.get('webViewLink', 'N/A')
            
            print(f"   Type: {mime_type}")
            print(f"   Size: {size}")
            print(f"   Created: {created}")
            print(f"   Modified: {modified}")
            print(f"   Link: {link}")
        
        print()


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path exists and is accessible.
    Kiểm tra file path có tồn tại không.
    
    Args:
        file_path: Path to validate
    
    Returns:
        bool: True if valid
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)


def get_mime_type(file_path: str) -> str:
    """
    Get MIME type from file extension.
    Lấy MIME type từ phần mở rộng file.
    
    Args:
        file_path: Path to file
    
    Returns:
        str: MIME type
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'


def guess_mime_type(file_path: str) -> str:
    """
    Guess MIME type from file extension.
    Đoán MIME type từ phần mở rộng file.
    
    Alias for get_mime_type().
    
    Args:
        file_path: Path to file
    
    Returns:
        str: MIME type
    """
    return get_mime_type(file_path)


def detect_environment() -> str:
    """
    Detect the current environment.
    Phát hiện môi trường hiện tại.
    
    Returns:
        str: 'colab', 'kaggle', or 'local'
    """
    # Check for Google Colab
    try:
        import google.colab  # noqa: F401  # type: ignore
        return 'colab'
    except ImportError:
        pass
    
    # Check for Kaggle
    if os.path.exists('/kaggle/working'):
        return 'kaggle'
    
    # Default to local
    return 'local'


def print_progress_bar(
    current: int,
    total: int,
    prefix: str = '',
    suffix: str = '',
    length: int = 50,
    fill: str = '█'
) -> None:
    """
    Print a progress bar to console.
    In thanh tiến trình lên console.
    
    Args:
        current: Current progress value
        total: Total value
        prefix: Prefix text
        suffix: Suffix text
        length: Bar length in characters
        fill: Fill character
    """
    if total == 0:
        percent = 100.0
    else:
        percent = min(100.0 * current / total, 100.0)
    
    filled_length = int(length * current // total) if total > 0 else length
    bar = fill * filled_length + '-' * (length - filled_length)
    
    # Print the progress bar
    sys.stdout.write(f'\r{prefix} |{bar}| {percent:.1f}% {suffix}')
    sys.stdout.flush()
    
    # Print newline when complete
    if current >= total:
        print()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size to human-readable format.
    Định dạng kích thước file dễ đọc.
    
    Alias for format_size().
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        str: Formatted size
    """
    return format_size(size_bytes)


def batch_upload(
    drive,
    file_paths: List[str],
    folder_id: Optional[str] = None,
    verbose: bool = True
) -> List[str]:
    """
    Upload multiple files at once.
    Upload nhiều file cùng lúc.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_paths: List of file paths to upload
        folder_id: Target folder ID
        verbose: Print progress
    
    Returns:
        List[str]: List of uploaded file IDs
    """
    from .operations import upload_file
    
    file_ids = []
    total = len(file_paths)
    
    if verbose:
        print(f"Uploading {total} file(s)...")
    
    for i, file_path in enumerate(file_paths, 1):
        if verbose:
            print(f"\n[{i}/{total}] Uploading {os.path.basename(file_path)}...")
        
        try:
            file_id = upload_file(drive, file_path, folder_id=folder_id)
            file_ids.append(file_id)
        except Exception as e:
            print(f"✗ Failed to upload {file_path}: {e}")
    
    if verbose:
        print(f"\n✓ Successfully uploaded {len(file_ids)}/{total} files")
    
    return file_ids


def batch_download(
    drive,
    file_ids: List[str],
    save_dir: str = ".",
    verbose: bool = True
) -> List[str]:
    """
    Download multiple files at once.
    Download nhiều file cùng lúc.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_ids: List of file IDs to download
        save_dir: Directory to save files
        verbose: Print progress
    
    Returns:
        List[str]: List of downloaded file paths
    """
    from .operations import download_file
    
    os.makedirs(save_dir, exist_ok=True)
    
    downloaded_paths = []
    total = len(file_ids)
    
    if verbose:
        print(f"Downloading {total} file(s)...")
    
    for i, file_id in enumerate(file_ids, 1):
        if verbose:
            print(f"\n[{i}/{total}] Downloading file ID: {file_id}...")
        
        try:
            path = download_file(drive, file_id=file_id, save_path=save_dir)
            downloaded_paths.append(path)
        except Exception as e:
            print(f"✗ Failed to download {file_id}: {e}")
    
    if verbose:
        print(f"\n✓ Successfully downloaded {len(downloaded_paths)}/{total} files")
    
    return downloaded_paths


def create_readme_file(drive, folder_id: str, content: str) -> str:
    """
    Create a README file in a folder.
    Tạo file README trong thư mục.
    
    Args:
        drive: Authenticated GoogleDrive instance
        folder_id: Folder ID to create README in
        content: Content of the README
    
    Returns:
        str: File ID of created README
    """
    import tempfile
    
    # Create temporary README file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    try:
        from .operations import upload_file
        file_id = upload_file(
            drive,
            temp_path,
            folder_id=folder_id,
            file_name="README.txt"
        )
        return file_id
    finally:
        os.unlink(temp_path)
