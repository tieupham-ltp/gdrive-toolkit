#!/usr/bin/env python
"""
Script to generate Google Drive Refresh Token.
Chạy script này để lấy refresh token cho Kaggle.

Usage:
    python get_refresh_token.py
    
Then copy the refresh_token to Kaggle Secrets as GDRIVE_REFRESH_TOKEN
"""

import json
import sys
from pydrive2.auth import GoogleAuth


def get_refresh_token():
    """Generate and display refresh token."""
    print("=" * 70)
    print("Google Drive Refresh Token Generator")
    print("=" * 70)
    print()
    
    # Check if client_secrets.json exists
    try:
        with open('client_secrets.json', 'r') as f:
            secrets = json.load(f)
            
            # Support both 'installed' (Desktop app) and 'web' (Web app)
            if 'installed' in secrets:
                client_id = secrets['installed']['client_id']
                client_secret = secrets['installed']['client_secret']
                app_type = 'Desktop app'
            elif 'web' in secrets:
                client_id = secrets['web']['client_id']
                client_secret = secrets['web']['client_secret']
                app_type = 'Web app'
            else:
                raise ValueError("Invalid client_secrets.json format")
            
            print("✓ Found client_secrets.json")
            print(f"  App type: {app_type}")
            print(f"  Client ID: {client_id[:20]}...")
    except FileNotFoundError:
        print("❌ Error: client_secrets.json not found!")
        print()
        print("Please download OAuth 2.0 credentials from Google Cloud Console:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Select your project")
        print("3. Go to 'APIs & Services' > 'Credentials'")
        print("4. Click 'Create Credentials' > 'OAuth client ID'")
        print("5. Choose 'Desktop app'")
        print("6. Download JSON and save as 'client_secrets.json' in this folder")
        return
    except Exception as e:
        print(f"❌ Error reading client_secrets.json: {e}")
        return
    
    print()
    print("Starting OAuth flow...")
    print()
    
    # Configure GoogleAuth with proper settings dict
    settings = {
        "client_config_backend": "file",
        "client_config_file": "client_secrets.json",
        "save_credentials": True,
        "save_credentials_backend": "file",
        "save_credentials_file": "credentials_temp.json",
        "get_refresh_token": True,
        "oauth_scope": ["https://www.googleapis.com/auth/drive"]
    }
    
    gauth = GoogleAuth(settings=settings)
    
    try:
        # Start local webserver authentication
        print("Opening browser for authentication...")
        print("Please login and authorize the app.")
        print()
        gauth.LocalWebserverAuth()
        
        if gauth.credentials is None:
            print("❌ Authentication failed!")
            return
        
        # Get refresh token
        refresh_token = gauth.credentials.refresh_token
        
        if not refresh_token:
            print("❌ No refresh token received!")
            print("This might happen if you've already authorized this app before.")
            print()
            print("Solutions:")
            print("1. Revoke access at: https://myaccount.google.com/permissions")
            print("2. Delete credentials_temp.json and try again")
            print("3. Or use a different Google account")
            return
        
        print()
        print("=" * 70)
        print("✓ SUCCESS! Authentication completed")
        print("=" * 70)
        print()
        print("Your credentials:")
        print()
        print(f"CLIENT_ID:     {client_id}")
        print(f"CLIENT_SECRET: {client_secret}")
        print(f"REFRESH_TOKEN: {refresh_token}")
        print()
        print("=" * 70)
        print("📋 Next Steps - Add to Kaggle Secrets:")
        print("=" * 70)
        print()
        print("1. Go to: https://www.kaggle.com/settings")
        print("2. Click on 'Secrets' (or 'Add-ons' > 'Secrets')")
        print("3. Add these 3 secrets:")
        print()
        print("   Name: GDRIVE_CLIENT_ID")
        print(f"   Value: {client_id}")
        print()
        print("   Name: GDRIVE_CLIENT_SECRET")
        print(f"   Value: {client_secret}")
        print()
        print("   Name: GDRIVE_REFRESH_TOKEN")
        print(f"   Value: {refresh_token}")
        print()
        print("4. Enable all 3 secrets in your Kaggle Notebook settings")
        print()
        print("=" * 70)
        print("✓ Done! You can now use gdrive-toolkit on Kaggle")
        print("=" * 70)
        
        # Save to file for convenience
        output = {
            "GDRIVE_CLIENT_ID": client_id,
            "GDRIVE_CLIENT_SECRET": client_secret,
            "GDRIVE_REFRESH_TOKEN": refresh_token
        }
        
        with open('kaggle_secrets.txt', 'w') as f:
            for key, value in output.items():
                f.write(f"{key}={value}\n")
        
        print()
        print("💾 Credentials also saved to: kaggle_secrets.txt")
        print("   (Keep this file secure and don't commit to Git!)")
        
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    get_refresh_token()
