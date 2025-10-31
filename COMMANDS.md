# Quick Command Reference

Các lệnh hữu ích khi làm việc với gdrive-toolkit.

## Installation & Setup

```bash
# Install in development mode
pip install -e .

# Install from GitHub
pip install git+https://github.com/yourusername/gdrive-toolkit.git

# Install specific version
pip install git+https://github.com/yourusername/gdrive-toolkit.git@v0.1.0

# Uninstall
pip uninstall gdrive-toolkit
```

## Testing

```bash
# Quick installation test
python tests\test_install.py

# Run with pytest (if installed)
pytest tests/

# Run specific test
python tests\test_install.py
```

## Examples

```bash
# Run all examples
python examples\basic_usage.py
python examples\folder_operations.py
python examples\batch_operations.py
python examples\advanced_search.py

# Colab/Kaggle examples - copy code to respective platforms
```

## Development

```bash
# Install dev dependencies
pip install pytest black flake8 mypy

# Format code
black gdrive_toolkit\

# Check code style
flake8 gdrive_toolkit\

# Type checking
mypy gdrive_toolkit\

# Clean build artifacts
rmdir /s /q build dist gdrive_toolkit.egg-info
```

## Credentials Setup

```bash
# Run interactive setup helper
python setup_credentials.py

# Manual setup - download client_secrets.json from:
# https://console.cloud.google.com/
```

## Git Commands

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit: gdrive-toolkit v0.1.0"

# Create GitHub repo first, then:
git remote add origin https://github.com/YOUR_USERNAME/gdrive-toolkit.git
git branch -M main
git push -u origin main

# Create tag for release
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Update after changes
git add .
git commit -m "Your commit message"
git push
```

## Build & Publish (Optional)

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check distribution
twine check dist\*

# Upload to TestPyPI (test first!)
twine upload --repository testpypi dist\*

# Upload to PyPI
twine upload dist\*

# Clean before rebuild
rmdir /s /q dist build
```

## Python Package Commands

```bash
# Create distribution
python setup.py sdist bdist_wheel

# Install from local build
pip install dist\gdrive_toolkit-0.1.0-py3-none-any.whl

# Show package info
pip show gdrive-toolkit

# List installed files
pip show -f gdrive-toolkit
```

## Documentation

```bash
# View documentation
start docs\QUICK_START.md
start docs\API_REFERENCE.md
start docs\CREDENTIALS_SETUP.md

# Or just open in VS Code
code docs\
```

## Useful Checks

```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Check if gdrive-toolkit is installed
pip show gdrive-toolkit

# Check package dependencies
pip show gdrive-toolkit | findstr Requires
```

## Environment Variables (Optional)

```bash
# Windows - Set environment variable
set GDRIVE_CLIENT_ID=your_client_id
set GDRIVE_CLIENT_SECRET=your_client_secret

# Or use .env file with python-dotenv
pip install python-dotenv
```

## Quick Python Tests

```python
# Test imports
python -c "import gdrive_toolkit; print(gdrive_toolkit.__version__)"

# Test environment detection
python -c "from gdrive_toolkit import detect_environment; print(detect_environment())"

# Test utilities
python -c "from gdrive_toolkit import format_size; print(format_size(1536000))"
```

## Jupyter Notebook (Optional)

```bash
# Install Jupyter
pip install jupyter

# Start Jupyter
jupyter notebook

# Create new notebook and test:
# from gdrive_toolkit import quick_connect
# drive = quick_connect()
```

## VS Code Commands

```json
// Add to .vscode/tasks.json for quick tasks
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Test Installation",
      "type": "shell",
      "command": "python tests/test_install.py"
    },
    {
      "label": "Run Basic Example",
      "type": "shell",
      "command": "python examples/basic_usage.py"
    },
    {
      "label": "Format Code",
      "type": "shell",
      "command": "black gdrive_toolkit/"
    }
  ]
}
```

## Troubleshooting Commands

```bash
# Reinstall package
pip uninstall gdrive-toolkit -y
pip install -e .

# Clear Python cache
rmdir /s /q __pycache__
del /s /q *.pyc

# Check for import errors
python -c "import gdrive_toolkit"

# Verbose installation
pip install -e . -v

# Show import path
python -c "import gdrive_toolkit; print(gdrive_toolkit.__file__)"
```

## Update Version

```bash
# 1. Update version in:
# - setup.py
# - pyproject.toml
# - gdrive_toolkit/__init__.py
# - CHANGELOG.md

# 2. Commit changes
git add .
git commit -m "Bump version to 0.2.0"

# 3. Create tag
git tag -a v0.2.0 -m "Release v0.2.0"

# 4. Push
git push
git push origin v0.2.0
```

## Common Issues

```bash
# Issue: Module not found
# Solution: Install package
pip install -e .

# Issue: Import error for pydrive2
# Solution: Install dependencies
pip install -r requirements.txt

# Issue: Permission denied
# Solution: Run as administrator or use virtual environment

# Issue: Git not recognized
# Solution: Install Git from https://git-scm.com/
```

---

**💡 Tip**: Add these commands to your favorite terminal or create shell scripts for frequent tasks!
