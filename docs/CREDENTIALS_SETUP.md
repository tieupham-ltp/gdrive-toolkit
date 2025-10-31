# How to Get Google Drive Credentials

This guide shows you how to set up OAuth 2.0 credentials for gdrive-toolkit.

## For Local Machine

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" → "New Project"
3. Enter project name (e.g., "gdrive-toolkit")
4. Click "Create"

### Step 2: Enable Google Drive API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on it and press "Enable"

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: gdrive-toolkit
   - User support email: your email
   - Developer contact: your email
   - Save and continue through all screens
4. Back to "Create OAuth client ID":
   - Application type: Desktop app
   - Name: gdrive-toolkit-desktop
   - Click "Create"
5. Download the JSON file
6. Rename it to `client_secrets.json`
7. Place it in your project root directory

### Step 4: First-Time Authentication

Run your script:
```bash
python examples/basic_usage.py
```

A browser window will open:
1. Choose your Google account
2. Click "Advanced" → "Go to gdrive-toolkit (unsafe)"
3. Click "Allow"
4. The credentials will be saved to `mycreds.txt`

Future runs will use the saved credentials automatically!

## For Kaggle

### Step 1-3: Same as Local Machine

Follow steps 1-3 above to create OAuth credentials.

### Step 4: Get Refresh Token

Run this script locally once to get your refresh token:

```python
from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

print("Add these to Kaggle Secrets:")
print(f"GDRIVE_CLIENT_ID: {gauth.credentials.client_id}")
print(f"GDRIVE_CLIENT_SECRET: {gauth.credentials.client_secret}")
print(f"GDRIVE_REFRESH_TOKEN: {gauth.credentials.refresh_token}")
```

### Step 5: Add Secrets to Kaggle

1. Go to your Kaggle account settings
2. Navigate to "Add-ons" → "Secrets"
3. Add these three secrets:
   - `GDRIVE_CLIENT_ID`
   - `GDRIVE_CLIENT_SECRET`
   - `GDRIVE_REFRESH_TOKEN`

Now you can use `quick_connect()` in Kaggle notebooks!

## For Google Colab

No setup needed! Colab has built-in Google Drive authentication.

Just run:
```python
from gdrive_toolkit import quick_connect
drive = quick_connect()
```

Colab will prompt you to authenticate when you run the code.

## Troubleshooting

### "Access blocked: This app's request is invalid"

- Make sure you set up the OAuth consent screen
- Add your email as a test user in OAuth consent screen

### "File 'client_secrets.json' not found"

- Make sure the file is in your project root
- Check the filename is exactly `client_secrets.json`

### "The credentials are not valid"

- Delete `mycreds.txt` and authenticate again
- Check your credentials are not expired

### Kaggle: "Secret not found"

- Double-check secret names (case-sensitive)
- Make sure secrets are enabled in your notebook

## Security Notes

- **Never commit** `client_secrets.json` or `mycreds.txt` to Git
- Both files are in `.gitignore` by default
- For production, use service accounts instead of OAuth
- Kaggle secrets are encrypted and only accessible to your notebooks
