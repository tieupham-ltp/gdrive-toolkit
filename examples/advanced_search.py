"""
Advanced search examples for gdrive-toolkit.
Ví dụ tìm kiếm nâng cao.
"""

from gdrive_toolkit import quick_connect, search_files, print_file_list

def main():
    # Connect
    print("Connecting to Google Drive...")
    drive = quick_connect()
    
    # 1. Search by file name
    print("\n=== Search by File Name ===")
    files = search_files(drive, file_name="report")
    print_file_list(files)
    
    # 2. Search by custom query (CSV files)
    print("\n=== Search CSV Files ===")
    files = search_files(
        drive,
        query="mimeType = 'text/csv'",
        max_results=10
    )
    print_file_list(files)
    
    # 3. Search for folders
    print("\n=== Search Folders ===")
    files = search_files(
        drive,
        query="mimeType = 'application/vnd.google-apps.folder'",
        max_results=10
    )
    print_file_list(files)
    
    # 4. Search files modified in last 7 days
    print("\n=== Recently Modified Files ===")
    from datetime import datetime, timedelta
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    
    files = search_files(
        drive,
        query=f"modifiedDate >= '{week_ago}'",
        max_results=10
    )
    print_file_list(files, verbose=True)
    
    # 5. Search PDF files
    print("\n=== Search PDF Files ===")
    files = search_files(
        drive,
        query="mimeType = 'application/pdf'",
        max_results=10
    )
    print_file_list(files)
    
    # 6. Search by exact title
    print("\n=== Search by Exact Title ===")
    files = search_files(
        drive,
        query="title = 'important_document.pdf'",
    )
    print_file_list(files)
    
    print("\n✓ Search examples completed!")

if __name__ == "__main__":
    main()
