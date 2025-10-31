"""
Folder operations module for Google Drive.
Các thao tác với thư mục trên Google Drive.
"""

from typing import Optional, List, Dict, Any
from pydrive2.drive import GoogleDrive


def create_folder(
    drive: GoogleDrive,
    folder_name: str,
    parent_id: Optional[str] = None
) -> str:
    """
    Create a new folder in Google Drive.
    Tạo thư mục mới trên Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        folder_name: Name of the folder to create
        parent_id: ID of parent folder (None for root)
    
    Returns:
        str: ID of the created folder
        
    Example:
        >>> folder_id = create_folder(drive, "My Data")
        >>> subfolder_id = create_folder(drive, "Subfolder", parent_id=folder_id)
    """
    metadata = {
        'title': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    if parent_id:
        metadata['parents'] = [{'id': parent_id}]  # type: ignore
    
    folder = drive.CreateFile(metadata)
    folder.Upload()
    
    folder_id = folder['id']
    print(f"✓ Created folder '{folder_name}' (ID: {folder_id})")
    
    return folder_id


def share_file(
    drive: GoogleDrive,
    file_id: str,
    permission: str = "reader",
    share_type: str = "anyone"
) -> str:
    """
    Share a file or folder and get its shareable link.
    Chia sẻ file/folder và lấy link.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_id: ID of file/folder to share
        permission: Permission level - "reader", "writer", "commenter" (default: "reader")
        share_type: Who can access - "anyone", "user", "group", "domain" (default: "anyone")
    
    Returns:
        str: Shareable link
        
    Example:
        >>> link = share_file(drive, file_id="abc123")
        >>> print(f"Share this link: {link}")
        >>> 
        >>> # Share with edit permission
        >>> link = share_file(drive, file_id="abc123", permission="writer")
    """
    # Valid permission types
    valid_permissions = ["reader", "writer", "commenter"]
    if permission not in valid_permissions:
        raise ValueError(
            f"Invalid permission: {permission}. "
            f"Must be one of: {', '.join(valid_permissions)}"
        )
    
    # Get file
    gfile = drive.CreateFile({'id': file_id})
    gfile.FetchMetadata()
    
    # Set permissions
    permission_data = {
        'type': share_type,
        'role': permission,
        'withLink': True
    }
    
    # Insert permission
    gfile.InsertPermission(permission_data)
    
    # Get shareable link
    link = gfile['alternateLink']
    
    title = gfile['title']
    print(f"✓ Shared '{title}' with {permission} access")
    print(f"  Link: {link}")
    
    return link


def get_folder_id_by_name(
    drive: GoogleDrive,
    folder_name: str,
    parent_id: Optional[str] = None
) -> Optional[str]:
    """
    Find folder ID by name.
    Tìm ID của folder theo tên.
    
    Args:
        drive: Authenticated GoogleDrive instance
        folder_name: Name of the folder to find
        parent_id: ID of parent folder to search in (None for root)
    
    Returns:
        Optional[str]: Folder ID if found, None otherwise
        
    Example:
        >>> folder_id = get_folder_id_by_name(drive, "My Folder")
    """
    query_parts = [
        f"title = '{folder_name}'",
        "mimeType = 'application/vnd.google-apps.folder'",
        "trashed = false"
    ]
    
    if parent_id:
        query_parts.append(f"'{parent_id}' in parents")
    
    query = " and ".join(query_parts)
    
    folder_list = drive.ListFile({'q': query}).GetList()
    
    if not folder_list:
        return None
    
    if len(folder_list) > 1:
        print(f"⚠ Found {len(folder_list)} folders named '{folder_name}', returning first")
    
    return folder_list[0]['id']


def create_folder_path(
    drive: GoogleDrive,
    path: str,
    parent_id: Optional[str] = None
) -> Optional[str]:
    """
    Create a folder path (like mkdir -p).
    Tạo đường dẫn thư mục (giống mkdir -p).
    
    Args:
        drive: Authenticated GoogleDrive instance
        path: Folder path to create (e.g., "Folder1/Folder2/Folder3")
        parent_id: ID of parent folder (None for root)
    
    Returns:
        str: ID of the final folder in the path
        
    Example:
        >>> folder_id = create_folder_path(drive, "Projects/2025/Data")
    """
    folder_names = path.split('/')
    current_parent_id = parent_id
    
    for folder_name in folder_names:
        folder_name = folder_name.strip()
        if not folder_name:
            continue
        
        # Check if folder already exists
        existing_id = get_folder_id_by_name(
            drive, folder_name, current_parent_id
        )
        
        if existing_id:
            print(f"  Folder '{folder_name}' already exists")
            current_parent_id = existing_id
        else:
            # Create new folder
            current_parent_id = create_folder(
                drive, folder_name, current_parent_id
            )
    
    return current_parent_id


def list_folders(
    drive: GoogleDrive,
    parent_id: Optional[str] = None,
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    List all folders in a location.
    Liệt kê tất cả thư mục.
    
    Args:
        drive: Authenticated GoogleDrive instance
        parent_id: ID of parent folder (None for root)
        max_results: Maximum number of results
    
    Returns:
        List[Dict]: List of folder metadata
        
    Example:
        >>> folders = list_folders(drive)
        >>> for folder in folders:
        ...     print(folder['title'], folder['id'])
    """
    query_parts = [
        "mimeType = 'application/vnd.google-apps.folder'",
        "trashed = false"
    ]
    
    if parent_id:
        query_parts.append(f"'{parent_id}' in parents")
    
    query = " and ".join(query_parts)
    
    folder_list = drive.ListFile({
        'q': query,
        'maxResults': max_results
    }).GetList()
    
    results = []
    for folder in folder_list:
        results.append({
            'id': folder['id'],
            'title': folder['title'],
            'createdDate': folder.get('createdDate', 'N/A'),
            'modifiedDate': folder.get('modifiedDate', 'N/A'),
            'webViewLink': folder.get('webViewLink', None),
        })
    
    print(f"✓ Found {len(results)} folder(s)")
    
    return results


def delete_folder(
    drive: GoogleDrive,
    folder_id: Optional[str] = None,
    folder_name: Optional[str] = None,
    confirm: bool = True
) -> bool:
    """
    Delete a folder from Google Drive.
    Xóa thư mục khỏi Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        folder_id: ID of the folder to delete
        folder_name: Name of the folder to delete
        confirm: Ask for confirmation (default: True)
    
    Returns:
        bool: True if deleted successfully
        
    Warning:
        This will delete the folder and all its contents!
        
    Example:
        >>> delete_folder(drive, folder_id="xyz789")
    """
    if folder_id is None and folder_name is None:
        raise ValueError("Either folder_id or folder_name must be provided")
    
    # Get folder
    if folder_id:
        folder = drive.CreateFile({'id': folder_id})
        folder.FetchMetadata()
    else:
        folder_id = get_folder_id_by_name(drive, folder_name)  # type: ignore
        if not folder_id:
            raise FileNotFoundError(f"Folder not found: {folder_name}")
        folder = drive.CreateFile({'id': folder_id})
        folder.FetchMetadata()
    
    title = folder['title']
    fid = folder['id']
    
    # Confirm deletion
    if confirm:
        response = input(
            f"⚠ Delete folder '{title}' and ALL its contents? [y/N]: "
        )
        if response.lower() != 'y':
            print("Deletion cancelled")
            return False
    
    # Delete folder
    folder.Delete()
    
    print(f"✓ Deleted folder '{title}' (ID: {fid})")
    
    return True
