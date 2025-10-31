"""
File operations module for Google Drive.
Các thao tác với file trên Google Drive.
"""

import os
import time
from typing import Optional, List, Dict, Any
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFile


def upload_file(
    drive: GoogleDrive,
    file_path: str,
    folder_id: Optional[str] = None,
    file_name: Optional[str] = None,
    show_progress: bool = True
) -> str:
    """
    Upload a file to Google Drive.
    Upload file lên Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_path: Path to the local file to upload
        folder_id: ID of the target folder (None for root)
        file_name: Custom name for uploaded file (None to use original name)
        show_progress: Show upload progress bar (default: True)
    
    Returns:
        str: ID of the uploaded file
        
    Example:
        >>> file_id = upload_file(drive, "data.csv")
        >>> print(f"Uploaded with ID: {file_id}")
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Use original filename if not specified
    if file_name is None:
        file_name = os.path.basename(file_path)
    
    # Get file size for progress tracking
    file_size = os.path.getsize(file_path)
    
    # Create file metadata
    metadata = {'title': file_name}
    
    if folder_id:
        metadata['parents'] = [{'id': folder_id}]  # type: ignore
    
    # Create and upload file
    gfile = drive.CreateFile(metadata)
    gfile.SetContentFile(file_path)
    
    if show_progress and file_size > 1024 * 1024:  # Show progress for files > 1MB
        from .utils import format_size
        print(f"📤 Uploading '{file_name}' ({format_size(file_size)})...")
        
        start_time = time.time()
        gfile.Upload()
        elapsed = time.time() - start_time
        
        if elapsed > 0:
            speed = file_size / elapsed
            print(f"  ✓ Upload complete! ({format_size(int(speed))}/s)")
        else:
            print(f"  ✓ Upload complete!")
    else:
        gfile.Upload()
    
    file_id = gfile['id']
    
    # Get file info to show location
    gfile.FetchMetadata()
    
    # Build Google Drive URL
    web_url = f"https://drive.google.com/file/d/{file_id}/view"
    
    # Show upload info
    print(f"✓ Uploaded '{file_name}'")
    print(f"  File ID: {file_id}")
    print(f"  View URL: {web_url}")
    
    # Show folder location
    if 'parents' in gfile and len(gfile['parents']) > 0:
        parent_id = gfile['parents'][0]['id']
        if parent_id == 'root' or not parent_id:
            print(f"  Location: My Drive (Root)")
        else:
            print(f"  Location: Folder ID {parent_id}")
            print(f"  Folder URL: https://drive.google.com/drive/folders/{parent_id}")
    else:
        print(f"  Location: My Drive (Root)")
    
    return file_id


def download_file(
    drive: GoogleDrive,
    file_id: Optional[str] = None,
    file_name: Optional[str] = None,
    save_path: str = ".",
    query: Optional[str] = None,
    show_progress: bool = True
) -> str:
    """
    Download a file from Google Drive.
    Download file từ Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: ID of the file to download (preferred)
        file_name: Name of the file to search and download
        save_path: Local path to save the file (directory or full path)
        query: Custom search query (advanced usage)
        show_progress: Show download progress (default: True)
    
    Returns:
        str: Path to the downloaded file
        
    Example:
        >>> download_file(drive, file_id="abc123", save_path="./downloads/")
        >>> download_file(drive, file_name="data.csv", save_path="./data.csv")
    """
    if file_id is None and file_name is None and query is None:
        raise ValueError("Either file_id, file_name, or query must be provided")
    
    # Get file by ID or search by name/query
    if file_id:
        gfile = drive.CreateFile({'id': file_id})
        gfile.FetchMetadata()
    else:
        # Search for file
        if query is None:
            query = f"title = '{file_name}'"
        
        file_list = drive.ListFile({'q': query}).GetList()
        
        if not file_list:
            raise FileNotFoundError(
                f"No file found matching: {file_name or query}"
            )
        
        if len(file_list) > 1:
            print(f"⚠ Found {len(file_list)} files, downloading the first one")
        
        gfile = file_list[0]
    
    # Determine save path
    title = gfile['title']
    
    if os.path.isdir(save_path):
        output_path = os.path.join(save_path, title)
    else:
        output_path = save_path
    
    # Create directory if needed
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Show progress for large files
    if show_progress:
        file_size = int(gfile.get('fileSize', 0))
        
        if file_size > 1024 * 1024:  # Show progress for files > 1MB
            from .utils import format_size
            from .client import _monitor_transfer_progress
            
            print(f"📥 Downloading '{title}' ({format_size(file_size)})...")
            
            # Start progress monitor
            stop_event = _monitor_transfer_progress(output_path, file_size, mode='download')
            
            try:
                start_time = time.time()
                gfile.GetContentFile(output_path)
                elapsed = time.time() - start_time
                
                # Stop monitor
                stop_event.set()
                time.sleep(0.1)  # Give monitor time to finish
                
                if elapsed > 0:
                    speed = file_size / elapsed
                    print(f"  ✓ Download complete! ({format_size(int(speed))}/s)")
                else:
                    print(f"  ✓ Download complete!")
            finally:
                stop_event.set()
        else:
            gfile.GetContentFile(output_path)
    else:
        gfile.GetContentFile(output_path)
    
    print(f"✓ Downloaded '{title}' to '{output_path}'")
    
    return output_path


def search_files(
    drive: GoogleDrive,
    query: Optional[str] = None,
    folder_id: Optional[str] = None,
    file_name: Optional[str] = None,
    max_results: int = 100,
    trashed: bool = False
) -> List[Dict[str, Any]]:
    """
    Search files in Google Drive.
    Tìm kiếm file trên Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        query: Custom search query (Google Drive query syntax)
        folder_id: Search within specific folder
        file_name: Search by file name (supports 'contains')
        max_results: Maximum number of results (default: 100)
        trashed: Include trashed files (default: False)
    
    Returns:
        List[Dict]: List of file metadata dictionaries
        
    Example:
        >>> # Search by name
        >>> files = search_files(drive, file_name="report")
        >>> 
        >>> # Search in folder
        >>> files = search_files(drive, folder_id="folder_id_here")
        >>> 
        >>> # Custom query
        >>> files = search_files(drive, query="title contains 'data' and mimeType = 'text/csv'")
    """
    # Build query
    query_parts = []
    
    if query:
        query_parts.append(query)
    
    if folder_id:
        query_parts.append(f"'{folder_id}' in parents")
    
    if file_name:
        query_parts.append(f"title contains '{file_name}'")
    
    if not trashed:
        query_parts.append("trashed = false")
    
    final_query = " and ".join(query_parts) if query_parts else None
    
    # Execute search
    params = {'maxResults': max_results}
    if final_query:
        params['q'] = final_query  # type: ignore
    
    file_list = drive.ListFile(params).GetList()
    
    # Format results
    results = []
    for gfile in file_list:
        results.append({
            'id': gfile['id'],
            'title': gfile['title'],
            'mimeType': gfile.get('mimeType', 'unknown'),
            'size': gfile.get('fileSize', 'N/A'),
            'createdDate': gfile.get('createdDate', 'N/A'),
            'modifiedDate': gfile.get('modifiedDate', 'N/A'),
            'downloadUrl': gfile.get('downloadUrl', None),
            'webViewLink': gfile.get('webViewLink', None),
        })
    
    print(f"✓ Found {len(results)} file(s)")
    
    return results


def delete_file(
    drive: GoogleDrive,
    file_id: Optional[str] = None,
    file_name: Optional[str] = None,
    confirm: bool = True
) -> bool:
    """
    Delete a file from Google Drive.
    Xóa file khỏi Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: ID of the file to delete
        file_name: Name of the file to search and delete
        confirm: Ask for confirmation before deleting (default: True)
    
    Returns:
        bool: True if deleted successfully
        
    Example:
        >>> delete_file(drive, file_id="abc123")
        >>> delete_file(drive, file_name="old_data.csv", confirm=False)
    """
    if file_id is None and file_name is None:
        raise ValueError("Either file_id or file_name must be provided")
    
    # Get file
    if file_id:
        gfile = drive.CreateFile({'id': file_id})
        gfile.FetchMetadata()
    else:
        # Search for file
        file_list = drive.ListFile({
            'q': f"title = '{file_name}' and trashed = false"
        }).GetList()
        
        if not file_list:
            raise FileNotFoundError(f"File not found: {file_name}")
        
        if len(file_list) > 1:
            print(f"⚠ Found {len(file_list)} files with name '{file_name}'")
            print("Deleting the first one. Use file_id for precise deletion.")
        
        gfile = file_list[0]
    
    title = gfile['title']
    fid = gfile['id']
    
    # Confirm deletion
    if confirm:
        response = input(f"Delete '{title}' (ID: {fid})? [y/N]: ")
        if response.lower() != 'y':
            print("Deletion cancelled")
            return False
    
    # Delete file
    gfile.Delete()
    
    print(f"✓ Deleted '{title}' (ID: {fid})")
    
    return True


def get_file_info(
    drive: GoogleDrive,
    file_id: str,
    show_path: bool = True
) -> Dict[str, Any]:
    """
    Get detailed information about a file.
    Lấy thông tin chi tiết về file.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: ID of the file
        show_path: Whether to print the full path (default: True)
    
    Returns:
        Dict: File metadata including path information
        
    Example:
        >>> info = get_file_info(drive, "abc123")
        >>> print(info['title'], info['fileSize'])
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    info = dict(gfile)
    
    if show_path:
        print(f"📄 File: {info['title']}")
        print(f"   ID: {file_id}")
        print(f"   View URL: https://drive.google.com/file/d/{file_id}/view")
        
        # Get and show path
        if 'parents' in info and len(info['parents']) > 0:
            parent_id = info['parents'][0]['id']
            path = get_file_path(drive, file_id)
            print(f"   Path: {path}")
            print(f"   Folder URL: https://drive.google.com/drive/folders/{parent_id}")
        else:
            print(f"   Path: My Drive/")
        
        if 'fileSize' in info:
            size_mb = int(info['fileSize']) / (1024 * 1024)
            print(f"   Size: {size_mb:.2f} MB")
    
    return info


def get_file_path(
    drive: GoogleDrive,
    file_id: str
) -> str:
    """
    Get the full path of a file in Google Drive.
    Lấy đường dẫn đầy đủ của file trên Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: ID of the file
    
    Returns:
        str: Full path from My Drive (e.g., "My Drive/Folder1/Folder2/file.txt")
        
    Example:
        >>> path = get_file_path(drive, "abc123")
        >>> print(f"File located at: {path}")
    """
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    # Build path from root to file
    path_parts = [gfile['title']]
    
    # Traverse parent folders
    current = gfile
    max_depth = 100  # Prevent infinite loop
    depth = 0
    
    while 'parents' in current and len(current['parents']) > 0 and depth < max_depth:
        parent_id = current['parents'][0]['id']
        
        # Stop at root
        if parent_id == 'root' or not parent_id:
            break
        
        # Get parent folder
        try:
            parent = drive.CreateFile({'id': parent_id})
            parent.FetchMetadata()
            path_parts.insert(0, parent['title'])
            current = parent
            depth += 1
        except:
            break
    
    # Build full path
    full_path = "My Drive/" + "/".join(path_parts)
    return full_path


def list_files_in_folder(
    drive: GoogleDrive,
    folder_id: Optional[str] = None,
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    List all files in a folder.
    Liệt kê tất cả file trong thư mục.
    
    Args:
        drive: Authenticated GoogleDrive instance
        folder_id: ID of the folder (None for root)
        max_results: Maximum number of results
    
    Returns:
        List[Dict]: List of files
        
    Example:
        >>> files = list_files_in_folder(drive, folder_id="xyz789")
    """
    return search_files(drive, folder_id=folder_id, max_results=max_results)
