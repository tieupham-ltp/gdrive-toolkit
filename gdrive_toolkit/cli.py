"""
CLI interface for gdrive-toolkit.
Giao diện dòng lệnh cho gdrive-toolkit.
"""

import os
import sys
import click
from typing import Optional

# Import functions
from .auth import quick_connect
from .client import (
    upload_file,
    download_file,
    create_folder,
    list_folder,
    search_files,
    delete_file_or_folder,
    share_anyone_reader,
    zip_and_upload,
)
from .utils import format_size, print_progress_bar


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    gdrive-toolkit - Google Drive operations from command line.
    
    Examples:
        gdrive-toolkit upload myfile.txt
        gdrive-toolkit download abc123 --output ./downloads/
        gdrive-toolkit search "report"
    """
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--folder', '-f', help='Folder name or ID to upload to')
@click.option('--name', '-n', help='Custom name for uploaded file')
@click.option('--share', is_flag=True, help='Share file after upload')
@click.option('--no-progress', is_flag=True, help='Disable progress display')
def upload(file_path: str, folder: Optional[str], name: Optional[str], share: bool, no_progress: bool):
    """Upload a file to Google Drive."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    # Find or create folder
    folder_id = None
    if folder:
        click.echo(f"📁 Looking for folder: {folder}")
        results = search_files(drive, name_contains=folder, 
                             mime_type='application/vnd.google-apps.folder')
        
        if results:
            folder_id = results[0]['id']
            click.echo(f"✓ Found folder: {results[0]['title']}")
        else:
            click.echo(f"Creating new folder: {folder}")
            folder_id = create_folder(drive, folder)
    
    # Upload file
    click.echo(f"📤 Uploading: {file_path}")
    file_id = upload_file(drive, file_path, parent_id=folder_id, file_name=name, show_progress=not no_progress)
    
    # Share if requested
    if share:
        link = share_anyone_reader(drive, file_id)
        click.echo(f"🔗 Shareable link: {link}")
    
    click.echo(f"✅ Done! File ID: {file_id}")


@cli.command()
@click.argument('file_id')
@click.option('--output', '-o', default='.', help='Output path (default: current directory)')
@click.option('--no-progress', is_flag=True, help='Disable progress display')
def download(file_id: str, output: str, no_progress: bool):
    """Download a file from Google Drive."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    click.echo(f"📥 Downloading file ID: {file_id}")
    path = download_file(drive, file_id, output, show_progress=not no_progress)
    
    click.echo(f"✅ Downloaded to: {path}")


@cli.command()
@click.argument('query', required=False)
@click.option('--folder', '-f', help='Search in specific folder ID')
@click.option('--type', '-t', help='Filter by MIME type (e.g., text/csv)')
@click.option('--limit', '-l', default=20, help='Maximum results (default: 20)')
def search(query: Optional[str], folder: Optional[str], type: Optional[str], limit: int):
    """Search files in Google Drive."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    click.echo(f"🔍 Searching...")
    results = search_files(
        drive,
        name_contains=query,
        parent_id=folder,
        mime_type=type,
        max_results=limit
    )
    
    if not results:
        click.echo("No files found.")
        return
    
    click.echo(f"\n{'='*80}")
    click.echo(f"Found {len(results)} file(s)")
    click.echo(f"{'='*80}\n")
    
    for i, file in enumerate(results, 1):
        size = file.get('size', 'N/A')
        if size != 'N/A' and size.isdigit():
            size = format_size(int(size))
        
        click.echo(f"{i}. {file['title']}")
        click.echo(f"   ID: {file['id']}")
        click.echo(f"   Type: {file['mimeType']}")
        click.echo(f"   Size: {size}")
        click.echo()


@cli.command()
@click.argument('name')
@click.option('--parent', '-p', help='Parent folder ID (default: root)')
def mkdir(name: str, parent: Optional[str]):
    """Create a folder in Google Drive."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    click.echo(f"📁 Creating folder: {name}")
    folder_id = create_folder(drive, name, parent_id=parent or "root")
    
    click.echo(f"✅ Created! Folder ID: {folder_id}")


@cli.command()
@click.argument('folder_id', required=False)
@click.option('--limit', '-l', default=50, help='Maximum results (default: 50)')
def ls(folder_id: Optional[str], limit: int):
    """List files in a folder."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    parent = folder_id or "root"
    click.echo(f"📂 Listing folder: {parent}")
    
    files = list_folder(drive, parent_id=parent, max_results=limit)
    
    if not files:
        click.echo("Empty folder.")
        return
    
    click.echo(f"\n{'='*80}")
    click.echo(f"{len(files)} item(s)")
    click.echo(f"{'='*80}\n")
    
    for file in files:
        is_folder = file['mimeType'] == 'application/vnd.google-apps.folder'
        icon = "📁" if is_folder else "📄"
        
        size = file.get('size', 'N/A')
        if size != 'N/A' and size.isdigit():
            size = format_size(int(size))
        
        click.echo(f"{icon} {file['title']}")
        click.echo(f"   ID: {file['id']} | Size: {size}")


@cli.command()
@click.argument('file_id')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation')
def delete(file_id: str, yes: bool):
    """Delete a file or folder."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    click.echo(f"🗑️  Deleting: {file_id}")
    delete_file_or_folder(drive, file_id, confirm=not yes)
    
    click.echo("✅ Deleted!")


@cli.command()
@click.argument('file_id')
def share(file_id: str):
    """Get shareable link for a file."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    click.echo(f"🔗 Sharing: {file_id}")
    link = share_anyone_reader(drive, file_id)
    
    click.echo(f"\n✅ Shareable link:")
    click.echo(link)


@cli.command()
@click.argument('folder_path', type=click.Path(exists=True))
@click.option('--name', '-n', help='Custom zip name')
@click.option('--folder', '-f', help='Upload to specific folder ID')
def zip_upload(folder_path: str, name: Optional[str], folder: Optional[str]):
    """Zip a folder and upload to Google Drive."""
    click.echo("🔐 Authenticating...")
    drive = quick_connect()
    
    click.echo(f"📦 Zipping and uploading: {folder_path}")
    file_id = zip_and_upload(drive, folder_path, parent_id=folder, zip_name=name)
    
    click.echo(f"✅ Done! File ID: {file_id}")


@cli.command()
def info():
    """Show authentication and environment info."""
    from .utils import detect_environment
    
    env = detect_environment()
    
    click.echo(f"\n{'='*60}")
    click.echo("gdrive-toolkit - Information")
    click.echo(f"{'='*60}")
    click.echo(f"Version: 0.1.0")
    click.echo(f"Environment: {env.upper()}")
    click.echo(f"Python: {sys.version.split()[0]}")
    
    if env == 'local':
        creds_exist = os.path.exists('mycreds.txt')
        secrets_exist = os.path.exists('client_secrets.json')
        
        click.echo(f"Credentials file: {'✓' if creds_exist else '✗'} mycreds.txt")
        click.echo(f"Client secrets: {'✓' if secrets_exist else '✗'} client_secrets.json")
        
        if not secrets_exist:
            click.echo("\n⚠️  client_secrets.json not found!")
            click.echo("   See docs/CREDENTIALS_SETUP.md for setup instructions")
    
    click.echo(f"{'='*60}\n")


def main():
    """Main entry point for CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n\n👋 Interrupted by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
