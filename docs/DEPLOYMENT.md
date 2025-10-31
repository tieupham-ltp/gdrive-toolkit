# Deployment Guide

Guide for deploying and publishing gdrive-toolkit.

## Pre-deployment Checklist

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] Version number updated in:
  - `setup.py`
  - `pyproject.toml`
  - `gdrive_toolkit/__init__.py`
  - `CHANGELOG.md`
- [ ] README examples work
- [ ] All examples tested

## Publishing to PyPI (Optional)

If you want to publish to PyPI:

### 1. Setup PyPI Account

1. Create account at https://pypi.org/
2. Create API token
3. Save token in `~/.pypirc`

### 2. Build Package

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*
```

### 3. Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ gdrive-toolkit
```

### 4. Upload to PyPI

```bash
twine upload dist/*
```

### 5. Test Installation

```bash
pip install gdrive-toolkit
```

## Publishing to GitHub

### 1. Create GitHub Repository

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Add remote
git remote add origin https://github.com/yourusername/gdrive-toolkit.git

# Push
git push -u origin main
```

### 2. Create Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v0.1.0`
4. Release title: `v0.1.0 - Initial Release`
5. Description: Copy from CHANGELOG.md
6. Publish release

### 3. Installation from GitHub

Users can now install with:
```bash
pip install git+https://github.com/yourusername/gdrive-toolkit.git
```

Or specific version:
```bash
pip install git+https://github.com/yourusername/gdrive-toolkit.git@v0.1.0
```

## Update Repository Settings

### Branch Protection

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews
   - Require status checks
   - Include administrators

### GitHub Actions (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, '3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest
    - name: Run tests
      run: python tests/test_install.py
```

## Documentation Hosting (Optional)

### GitHub Pages

1. Create `docs/` folder with documentation
2. Enable GitHub Pages in repository settings
3. Choose source: main branch, /docs folder

### Read the Docs

1. Import project to https://readthedocs.org/
2. Connect GitHub repository
3. Configure build settings

## Version Management

### Semantic Versioning

Follow semver: MAJOR.MINOR.PATCH

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Updating Version

1. Update version in all files
2. Update CHANGELOG.md
3. Commit changes
4. Tag release:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

## Maintenance

### Regular Updates

- Monitor issues and PRs
- Update dependencies
- Test on new Python versions
- Update documentation

### Security

- Monitor security advisories
- Update vulnerable dependencies
- Review access controls

## Community

### Create Templates

Add to `.github/`:
- ISSUE_TEMPLATE.md
- PULL_REQUEST_TEMPLATE.md
- CODE_OF_CONDUCT.md

### Add Badges

Update README.md with badges:
- PyPI version
- Python versions
- License
- Build status
- Downloads

Example:
```markdown
[![PyPI version](https://badge.fury.io/py/gdrive-toolkit.svg)](https://badge.fury.io/py/gdrive-toolkit)
[![Python](https://img.shields.io/pypi/pyversions/gdrive-toolkit.svg)](https://pypi.org/project/gdrive-toolkit/)
```

## Marketing (Optional)

- Share on Reddit (r/Python, r/datascience)
- Share on Twitter/X
- Share on LinkedIn
- Write blog post
- Create demo video

## Support

- Monitor GitHub issues
- Answer questions
- Fix bugs
- Accept contributions
