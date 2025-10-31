#!/usr/bin/env python
"""
Interactive setup script for gdrive-toolkit credentials.
Script tương tác để thiết lập credentials.
"""

import os
import sys
import json

def main():
    """Run interactive setup."""
    print("=" * 70)
    print("gdrive-toolkit - Credentials Setup Helper")
    print("=" * 70)
    print()
    
    # Check environment
    try:
        import google.colab  # type: ignore
        print("✓ Running in Google Colab - No setup needed!")
        print("  Just use: quick_connect()")
        return
    except ImportError:
        pass
    
    if os.path.exists('/kaggle/working'):
        print("✓ Running in Kaggle")
        print()
        print("Setup instructions:")
        print("1. Go to Kaggle Account → Add-ons → Secrets")
        print("2. Add these secrets:")
        print("   - GDRIVE_CLIENT_ID")
        print("   - GDRIVE_CLIENT_SECRET")
        print("   - GDRIVE_REFRESH_TOKEN")
        print()
        print("See docs/CREDENTIALS_SETUP.md for details")
        return
    
    # Local setup
    print("✓ Running on local machine")
    print()
    
    if os.path.exists('client_secrets.json'):
        print("✓ Found client_secrets.json")
        print()
        print("You're ready to go! Run:")
        print("  python examples/basic_usage.py")
        return
    
    print("✗ client_secrets.json not found")
    print()
    print("Setup steps:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project")
    print("3. Enable Google Drive API")
    print("4. Create OAuth 2.0 credentials (Desktop app)")
    print("5. Download JSON and save as 'client_secrets.json'")
    print()
    print("See docs/CREDENTIALS_SETUP.md for detailed instructions")
    print()
    
    response = input("Do you want to create a template client_secrets.json? [y/N]: ")
    
    if response.lower() == 'y':
        template = {
            "installed": {
                "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                "client_secret": "YOUR_CLIENT_SECRET",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["http://localhost:8080/"]
            }
        }
        
        with open('client_secrets.json', 'w') as f:
            json.dump(template, f, indent=2)
        
        print()
        print("✓ Created template client_secrets.json")
        print("  Please replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET")
        print("  with your actual credentials from Google Cloud Console")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
