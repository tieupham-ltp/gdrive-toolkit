from pydrive2.auth import GoogleAuth

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
gauth.GetFlow()

print("=" * 70)
print("Redirect URI đang được sử dụng:")
print(gauth.flow.redirect_uri)
print("=" * 70)
print()
print("Bạn cần thêm redirect URI này vào Google Cloud Console:")
print("1. Vào: https://console.cloud.google.com/apis/credentials")
print("2. Click vào OAuth 2.0 Client ID của bạn")
print("3. Thêm redirect URI này vào 'Authorized redirect URIs'")
print("4. Save và chạy lại get_refresh_token.py")
