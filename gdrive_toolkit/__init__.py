"""
gdrive-toolkit - A lightweight Google Drive toolkit
Thư viện gọn nhẹ để thao tác với Google Drive

Author: Your Name
License: MIT
"""

__version__ = "0.1.0"

# Import authentication functions
from .auth import (
    quick_connect,
    authenticate_colab,
    authenticate_kaggle,
    authenticate_local,
    detect_environment,
    # Backward compatibility aliases
    auth_colab,
    auth_kaggle,
    auth_local,
)

# Import file operations
from .operations import (
    upload_file,
    download_file,
    search_files,
    delete_file,
    get_file_info,
    get_file_path,
    list_files_in_folder,
)

# Import folder operations
from .folder import (
    create_folder,
    share_file,
    get_folder_id_by_name,
    create_folder_path,
    list_folders,
    delete_folder,
)

# Import client operations (advanced)
from .client import (
    upload_file as upload_file_client,
    download_file as download_file_client,
    create_folder as create_folder_client,
    list_folder,
    search_files as search_files_client,
    delete_file_or_folder,
    share_anyone_reader,
    get_shareable_link,
    zip_and_upload,
    upload_large_file,
    download_file_with_progress,
    copy_file,
    move_file,
    get_folder_size,
)

# Import utilities
from .utils import (
    format_size,
    print_file_list,
    validate_file_path,
    get_mime_type,
    guess_mime_type,
    detect_environment as detect_env,
    print_progress_bar,
    format_file_size,
    batch_upload,
    batch_download,
    create_readme_file,
)

# Define what gets imported with "from gdrive_toolkit import *"
__all__ = [
    # Version
    '__version__',
    
    # Authentication
    'quick_connect',
    'authenticate_colab',
    'authenticate_kaggle',
    'authenticate_local',
    'detect_environment',
    'auth_colab',
    'auth_kaggle',
    'auth_local',
    
    # File operations
    'upload_file',
    'download_file',
    'search_files',
    'delete_file',
    'get_file_info',
    'list_files_in_folder',
    
    # Folder operations
    'create_folder',
    'share_file',
    'get_folder_id_by_name',
    'create_folder_path',
    'list_folders',
    'delete_folder',
    
    # Client operations (advanced)
    'list_folder',
    'delete_file_or_folder',
    'share_anyone_reader',
    'get_shareable_link',
    'zip_and_upload',
    'upload_large_file',
    'download_file_with_progress',
    'copy_file',
    'move_file',
    'get_folder_size',
    
    # Utilities
    'format_size',
    'print_file_list',
    'validate_file_path',
    'get_mime_type',
    'guess_mime_type',
    'detect_env',
    'print_progress_bar',
    'format_file_size',
    'batch_upload',
    'batch_download',
    'create_readme_file',
]
