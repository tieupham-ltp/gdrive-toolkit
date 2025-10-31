"""
Authentication module for Google Drive.
Xác thực Google Drive cho nhiều môi trường (Colab, Kaggle, local).
"""

import os
import sys
from typing import Optional
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def detect_environment() -> str:
    """
    Detect the current environment.
    Phát hiện môi trường hiện tại.
    
    Returns:
        str: 'colab', 'kaggle', or 'local'
    """
    # Check for Kaggle FIRST (priority over Colab)
    # Kaggle có thể có google.colab installed nên phải check trước
    if os.path.exists('/kaggle/working'):
        return 'kaggle'
    
    # Check for Google Colab
    try:
        import google.colab  # type: ignore # noqa: F401
        return 'colab'
    except ImportError:
        pass
    
    # Default to local
    return 'local'


def authenticate_colab() -> GoogleDrive:
    """
    Authenticate Google Drive in Google Colab environment.
    Xác thực trong môi trường Google Colab.
    
    Returns:
        GoogleDrive: Authenticated Google Drive instance
    """
    try:
        from google.colab import auth  # type: ignore
        from oauth2client.client import GoogleCredentials  # type: ignore
    except ImportError:
        raise ImportError(
            "This function requires google.colab. "
            "Please run in Google Colab environment."
        )
    
    # Authenticate using Colab's built-in authentication
    auth.authenticate_user()
    
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    
    drive = GoogleDrive(gauth)
    print("✓ Successfully authenticated in Google Colab")
    return drive


def authenticate_kaggle() -> GoogleDrive:
    """
    Authenticate Google Drive in Kaggle environment.
    Xác thực trong môi trường Kaggle.
    
    Returns:
        GoogleDrive: Authenticated Google Drive instance
        
    Note:
        Requires Kaggle secrets: GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET, GDRIVE_REFRESH_TOKEN
    """
    try:
        from kaggle_secrets import UserSecretsClient  # type: ignore
    except ImportError:
        raise ImportError(
            "This function requires kaggle_secrets. "
            "Please run in Kaggle environment."
        )
    
    # Get secrets from Kaggle
    user_secrets = UserSecretsClient()
    
    try:
        client_id = user_secrets.get_secret("GDRIVE_CLIENT_ID")
        client_secret = user_secrets.get_secret("GDRIVE_CLIENT_SECRET")
        refresh_token = user_secrets.get_secret("GDRIVE_REFRESH_TOKEN")
    except Exception as e:
        raise ValueError(
            "Missing Kaggle secrets. Please add: "
            "GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET, GDRIVE_REFRESH_TOKEN. "
            f"Error: {e}"
        )
    
    # Create settings for PyDrive
    settings = {
        "client_config_backend": "settings",
        "client_config": {
            "client_id": client_id,
            "client_secret": client_secret
        },
        "save_credentials": False,
        "oauth_scope": ["https://www.googleapis.com/auth/drive"]
    }
    
    gauth = GoogleAuth(settings=settings)
    gauth.credentials = gauth.flow.step2_exchange(refresh_token)
    
    drive = GoogleDrive(gauth)
    print("✓ Successfully authenticated in Kaggle")
    return drive


def authenticate_local(
    credentials_file: str = "mycreds.txt",
    client_secrets_file: str = "client_secrets.json"
) -> GoogleDrive:
    """
    Authenticate Google Drive on local machine.
    Xác thực trên máy local.
    
    Args:
        credentials_file: Path to save/load credentials (default: 'mycreds.txt')
        client_secrets_file: Path to client secrets JSON file (default: 'client_secrets.json')
    
    Returns:
        GoogleDrive: Authenticated Google Drive instance
        
    Note:
        First-time use requires client_secrets.json from Google Cloud Console.
        Download from: https://console.cloud.google.com/
    """
    # Check if client_secrets.json exists
    if not os.path.exists(client_secrets_file):
        raise FileNotFoundError(
            f"'{client_secrets_file}' not found. "
            "Please download OAuth 2.0 credentials from Google Cloud Console:\n"
            "1. Go to https://console.cloud.google.com/\n"
            "2. Create/select a project\n"
            "3. Enable Google Drive API\n"
            "4. Create OAuth 2.0 credentials (Desktop app)\n"
            "5. Download and save as 'client_secrets.json'"
        )
    
    gauth = GoogleAuth()
    
    # Configure settings
    settings = {
        "client_config_backend": "file",
        "client_config_file": client_secrets_file,
        "save_credentials": True,
        "save_credentials_backend": "file",
        "save_credentials_file": credentials_file,
        "oauth_scope": ["https://www.googleapis.com/auth/drive"]
    }
    
    gauth.settings = settings
    
    # Try to load saved credentials
    gauth.LoadCredentialsFile(credentials_file)
    
    if gauth.credentials is None:
        # Authenticate if credentials don't exist
        print("First-time authentication required. Opening browser...")
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh credentials if expired
        print("Refreshing expired credentials...")
        gauth.Refresh()
    else:
        # Use existing valid credentials
        print("Using existing credentials...")
        gauth.Authorize()
    
    # Save credentials for next time
    gauth.SaveCredentialsFile(credentials_file)
    
    drive = GoogleDrive(gauth)
    print("✓ Successfully authenticated on local machine")
    return drive


def quick_connect(
    credentials_file: str = "mycreds.txt",
    client_secrets_file: str = "client_secrets.json",
    force_env: Optional[str] = None
) -> GoogleDrive:
    """
    Quick connect to Google Drive with auto-detection of environment.
    Kết nối nhanh với Google Drive, tự động nhận diện môi trường.
    
    This is the recommended method for authentication as it automatically
    detects whether you're running on Colab, Kaggle, or local machine.
    
    Args:
        credentials_file: Path to credentials (local only, default: 'mycreds.txt')
        client_secrets_file: Path to client secrets (local only, default: 'client_secrets.json')
        force_env: Force specific environment ('colab', 'kaggle', or 'local'). 
                   If None, auto-detects. Use this if auto-detection fails.
    
    Returns:
        GoogleDrive: Authenticated Google Drive instance
        
    Examples:
        >>> # Auto-detect environment
        >>> drive = quick_connect()
        
        >>> # Force Kaggle authentication (if auto-detect fails)
        >>> drive = quick_connect(force_env='kaggle')
        
        >>> # Force Colab authentication
        >>> drive = quick_connect(force_env='colab')
        
        >>> # Force local authentication
        >>> drive = quick_connect(force_env='local')
    """
    if force_env:
        env = force_env.lower()
        if env not in ['colab', 'kaggle', 'local']:
            raise ValueError(
                f"Invalid force_env: '{force_env}'. "
                "Must be 'colab', 'kaggle', or 'local'"
            )
        print(f"🎯 Forced environment: {env.upper()}")
    else:
        env = detect_environment()
        print(f"🔍 Detected environment: {env.upper()}")
    
    if env == 'colab':
        return authenticate_colab()
    elif env == 'kaggle':
        return authenticate_kaggle()
    else:  # local
        return authenticate_local(credentials_file, client_secrets_file)


# Backward compatibility aliases
def auth_colab() -> GoogleDrive:
    """Alias for authenticate_colab()."""
    return authenticate_colab()


def auth_kaggle() -> GoogleDrive:
    """Alias for authenticate_kaggle()."""
    return authenticate_kaggle()


def auth_local(
    credentials_file: str = "mycreds.txt",
    client_secrets_file: str = "client_secrets.json"
) -> GoogleDrive:
    """Alias for authenticate_local()."""
    return authenticate_local(credentials_file, client_secrets_file)
