"""
Client module - Advanced Google Drive operations.
Module client - Các thao tác nâng cao với Google Drive.
"""

import os
import zipfile
import shutil
from typing import Optional, List, Dict, Any, Callable
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile


def upload_file(
    drive: GoogleDrive,
    local_path: str,
    parent_id: Optional[str] = None,
    file_name: Optional[str] = None
) -> str:
    """
    Upload a file to Google Drive.
    Upload file lên Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        local_path: Path to local file
        parent_id: Parent folder ID (None for root)
        file_name: Custom name (None to use original)
    
    Returns:
        str: File ID
    """
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"File not found: {local_path}")
    
    metadata = {
        'title': file_name or os.path.basename(local_path)
    }
    
    if parent_id:
        metadata['parents'] = [{'id': parent_id}]  # type: ignore
    
    gfile = drive.CreateFile(metadata)
    gfile.SetContentFile(local_path)
    gfile.Upload()
    
    print(f"✓ Uploaded '{metadata['title']}' (ID: {gfile['id']})")
    return gfile['id']


def download_file(
    drive: GoogleDrive,
    file_id: str,
    dest_path: str
) -> str:
    """
    Download a file from Google Drive.
    Download file từ Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: File ID to download
        dest_path: Destination path
    
    Returns:
        str: Downloaded file path
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    # Determine output path
    if os.path.isdir(dest_path):
        output_path = os.path.join(dest_path, gfile['title'])
    else:
        output_path = dest_path
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    gfile.GetContentFile(output_path)
    print(f"✓ Downloaded '{gfile['title']}' to '{output_path}'")
    
    return output_path


def create_folder(
    drive: GoogleDrive,
    name: str,
    parent_id: str = "root"
) -> str:
    """
    Create a folder in Google Drive.
    Tạo folder trong Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        name: Folder name
        parent_id: Parent folder ID (default: "root")
    
    Returns:
        str: Folder ID
    """
    metadata = {
        'title': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_id}]
    }
    
    folder = drive.CreateFile(metadata)
    folder.Upload()
    
    print(f"✓ Created folder '{name}' (ID: {folder['id']})")
    return folder['id']


def list_folder(
    drive: GoogleDrive,
    parent_id: str = "root",
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    List files in a folder.
    Liệt kê file trong folder.
    
    Args:
        drive: Authenticated GoogleDrive instance
        parent_id: Folder ID (default: "root")
        max_results: Maximum results
    
    Returns:
        List[Dict]: List of files
    """
    query = f"'{parent_id}' in parents and trashed = false"
    
    file_list = drive.ListFile({
        'q': query,
        'maxResults': max_results
    }).GetList()
    
    results = []
    for f in file_list:
        results.append({
            'id': f['id'],
            'title': f['title'],
            'mimeType': f.get('mimeType', 'unknown'),
            'size': f.get('fileSize', 'N/A'),
            'modifiedDate': f.get('modifiedDate', 'N/A')
        })
    
    return results


def search_files(
    drive: GoogleDrive,
    name_contains: Optional[str] = None,
    mime_type: Optional[str] = None,
    parent_id: Optional[str] = None,
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    Search files in Google Drive.
    Tìm kiếm file trong Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        name_contains: Search by name
        mime_type: Filter by MIME type
        parent_id: Search in specific folder
        max_results: Maximum results
    
    Returns:
        List[Dict]: List of matching files
    """
    query_parts = ["trashed = false"]
    
    if name_contains:
        query_parts.append(f"title contains '{name_contains}'")
    
    if mime_type:
        query_parts.append(f"mimeType = '{mime_type}'")
    
    if parent_id:
        query_parts.append(f"'{parent_id}' in parents")
    
    query = " and ".join(query_parts)
    
    file_list = drive.ListFile({
        'q': query,
        'maxResults': max_results
    }).GetList()
    
    results = []
    for f in file_list:
        results.append({
            'id': f['id'],
            'title': f['title'],
            'mimeType': f.get('mimeType', 'unknown'),
            'size': f.get('fileSize', 'N/A'),
        })
    
    print(f"✓ Found {len(results)} file(s)")
    return results


def delete_file_or_folder(
    drive: GoogleDrive,
    file_id: str,
    confirm: bool = True
) -> bool:
    """
    Delete a file or folder.
    Xóa file hoặc folder.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: File/folder ID
        confirm: Ask for confirmation
    
    Returns:
        bool: True if deleted
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    title = gfile['title']
    
    if confirm:
        response = input(f"Delete '{title}' (ID: {file_id})? [y/N]: ")
        if response.lower() != 'y':
            print("Deletion cancelled")
            return False
    
    gfile.Delete()
    print(f"✓ Deleted '{title}'")
    return True


def share_anyone_reader(
    drive: GoogleDrive,
    file_id: str
) -> str:
    """
    Share file with anyone (read-only).
    Chia sẻ file cho mọi người (chỉ đọc).
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: File ID
    
    Returns:
        str: Shareable link
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    gfile.InsertPermission({
        'type': 'anyone',
        'role': 'reader',
        'withLink': True
    })
    
    link = gfile['alternateLink']
    print(f"✓ Shared '{gfile['title']}' (anyone can view)")
    
    return link


def get_shareable_link(
    drive: GoogleDrive,
    file_id: str,
    permission: str = "reader"
) -> str:
    """
    Get shareable link for a file.
    Lấy link chia sẻ của file.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: File ID
        permission: "reader", "writer", or "commenter"
    
    Returns:
        str: Shareable link
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    # Ensure file is shared
    try:
        gfile.InsertPermission({
            'type': 'anyone',
            'role': permission,
            'withLink': True
        })
    except:
        pass  # May already be shared
    
    return gfile.get('alternateLink', gfile.get('webViewLink', 'N/A'))


def zip_and_upload(
    drive: GoogleDrive,
    folder_path: str,
    parent_id: Optional[str] = None,
    zip_name: Optional[str] = None
) -> str:
    """
    Zip a folder and upload to Google Drive.
    Nén folder và upload lên Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        folder_path: Path to folder to zip
        parent_id: Parent folder ID in Drive
        zip_name: Custom zip name (default: folder name)
    
    Returns:
        str: Uploaded zip file ID
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"Not a directory: {folder_path}")
    
    # Determine zip name
    if zip_name is None:
        zip_name = os.path.basename(folder_path.rstrip('/\\')) + '.zip'
    elif not zip_name.endswith('.zip'):
        zip_name += '.zip'
    
    # Create temporary zip file
    temp_zip = os.path.join(os.path.dirname(folder_path), zip_name)
    
    print(f"Creating zip archive: {zip_name}")
    
    with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    
    # Upload zip
    print(f"Uploading {zip_name}...")
    file_id = upload_file(drive, temp_zip, parent_id=parent_id)
    
    # Clean up
    os.remove(temp_zip)
    print(f"✓ Zip created and uploaded (ID: {file_id})")
    
    return file_id


def upload_large_file(
    drive: GoogleDrive,
    local_path: str,
    parent_id: Optional[str] = None,
    chunk_size: int = 256 * 1024 * 1024,  # 256 MB
    callback: Optional[Callable[[int, int], None]] = None
) -> str:
    """
    Upload large file with chunking.
    Upload file lớn với chunking.
    
    Args:
        drive: Authenticated GoogleDrive instance
        local_path: Path to file
        parent_id: Parent folder ID
        chunk_size: Chunk size in bytes (default: 256 MB)
        callback: Progress callback (current, total)
    
    Returns:
        str: File ID
    """
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"File not found: {local_path}")
    
    file_size = os.path.getsize(local_path)
    file_name = os.path.basename(local_path)
    
    print(f"Uploading large file: {file_name} ({file_size:,} bytes)")
    
    metadata = {'title': file_name}
    if parent_id:
        metadata['parents'] = [{'id': parent_id}]  # type: ignore
    
    gfile = drive.CreateFile(metadata)
    gfile.SetContentFile(local_path)
    
    # Set chunk size
    gfile.Upload(param={'chunksize': chunk_size})
    
    if callback:
        callback(file_size, file_size)
    
    print(f"✓ Uploaded '{file_name}' (ID: {gfile['id']})")
    return gfile['id']


def download_file_with_progress(
    drive: GoogleDrive,
    file_id: str,
    dest_path: str,
    callback: Optional[Callable[[int, int], None]] = None
) -> str:
    """
    Download file with progress tracking.
    Download file với theo dõi tiến trình.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: File ID
        dest_path: Destination path
        callback: Progress callback (current, total)
    
    Returns:
        str: Downloaded file path
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    file_name = gfile['title']
    file_size = int(gfile.get('fileSize', 0))
    
    if os.path.isdir(dest_path):
        output_path = os.path.join(dest_path, file_name)
    else:
        output_path = dest_path
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    print(f"Downloading: {file_name} ({file_size:,} bytes)")
    
    # Download with progress
    gfile.GetContentFile(output_path)
    
    if callback:
        callback(file_size, file_size)
    
    print(f"✓ Downloaded to '{output_path}'")
    return output_path


def copy_file(
    drive: GoogleDrive,
    file_id: str,
    new_title: Optional[str] = None,
    parent_id: Optional[str] = None
) -> str:
    """
    Copy a file in Google Drive.
    Sao chép file trong Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: Source file ID
        new_title: New file name (None to use original)
        parent_id: Destination folder ID
    
    Returns:
        str: Copied file ID
    """
    source = drive.CreateFile({'id': file_id})
    source.FetchMetadata()
    
    metadata = {
        'title': new_title or f"Copy of {source['title']}"
    }
    
    if parent_id:
        metadata['parents'] = [{'id': parent_id}]  # type: ignore
    
    copied = source.Copy(metadata=metadata)  # type: ignore
    
    print(f"✓ Copied '{source['title']}' to '{metadata['title']}'")
    return copied['id']


def move_file(
    drive: GoogleDrive,
    file_id: str,
    new_parent_id: str
) -> bool:
    """
    Move a file to a different folder.
    Di chuyển file sang folder khác.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: File ID
        new_parent_id: New parent folder ID
    
    Returns:
        bool: True if moved
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    # Get current parents
    current_parents = gfile.get('parents', [])
    
    # Remove from current parents
    for parent in current_parents:
        gfile['parents'].remove(parent)
    
    # Add new parent
    gfile['parents'] = [{'id': new_parent_id}]
    gfile.Upload()
    
    print(f"✓ Moved '{gfile['title']}' to new folder")
    return True


def get_folder_size(
    drive: GoogleDrive,
    folder_id: str
) -> int:
    """
    Calculate total size of a folder.
    Tính tổng kích thước folder.
    
    Args:
        drive: Authenticated GoogleDrive instance
        folder_id: Folder ID
    
    Returns:
        int: Total size in bytes
    """
    total_size = 0
    
    query = f"'{folder_id}' in parents and trashed = false"
    file_list = drive.ListFile({'q': query}).GetList()
    
    for f in file_list:
        mime_type = f.get('mimeType', '')
        
        if mime_type == 'application/vnd.google-apps.folder':
            # Recursive for subfolders
            total_size += get_folder_size(drive, f['id'])
        else:
            # Add file size
            size = f.get('fileSize')
            if size:
                total_size += int(size)
    
    return total_size
