# Contributing to gdrive-toolkit

Thank you for considering contributing to gdrive-toolkit! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists
- Provide a clear use case
- Explain how it fits with the library's goals

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/gdrive-toolkit.git
   cd gdrive-toolkit
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guide
   - Add docstrings (English + short Vietnamese comments)
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Run examples to ensure they work
   python examples/basic_usage.py
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe your changes
   - Link related issues
   - Wait for review

## Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings in English
- Add short Vietnamese comments for clarity
- Keep functions simple and focused

### Example:

```python
def upload_file(
    drive: GoogleDrive,
    file_path: str,
    folder_id: Optional[str] = None
) -> str:
    """
    Upload a file to Google Drive.
    Upload file lên Google Drive.
    
    Args:
        drive: Authenticated GoogleDrive instance
        file_path: Path to the local file
        folder_id: Target folder ID (None for root)
    
    Returns:
        str: ID of uploaded file
    """
    # Implementation here
    pass
```

## Development Setup

1. Install in development mode:
   ```bash
   pip install -e .
   ```

2. Install development dependencies:
   ```bash
   pip install pytest black flake8
   ```

3. Run code formatting:
   ```bash
   black gdrive_toolkit/
   flake8 gdrive_toolkit/
   ```

## Documentation

- Update README.md if adding major features
- Add examples to `examples/` folder
- Update API_REFERENCE.md for new functions
- Keep docstrings up to date

## Questions?

Feel free to open an issue for any questions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
