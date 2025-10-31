# Examples

This folder contains example scripts demonstrating how to use gdrive-toolkit.

## Files

- **basic_usage.py** - Basic operations (connect, upload, download, search)
- **folder_operations.py** - Working with folders (create, share, list)
- **batch_operations.py** - Batch upload and download multiple files
- **advanced_search.py** - Advanced search queries and filters
- **colab_example.py** - Usage example for Google Colab
- **kaggle_example.py** - Usage example for Kaggle notebooks

## Running Examples

### Local Machine

1. Make sure you have `client_secrets.json` in your project root
2. Install gdrive-toolkit:
   ```bash
   pip install -e .
   ```
3. Run any example:
   ```bash
   python examples/basic_usage.py
   ```

### Google Colab

1. Install the package in a cell:
   ```python
   !pip install git+https://github.com/yourusername/gdrive-toolkit.git
   ```
2. Copy code from `colab_example.py` and run in a cell

### Kaggle

1. Set up secrets in Kaggle (see `kaggle_example.py` for details)
2. Install the package:
   ```python
   !pip install git+https://github.com/yourusername/gdrive-toolkit.git
   ```
3. Copy code from `kaggle_example.py` and run

## Tips

- Start with `basic_usage.py` to understand the fundamentals
- Use `folder_operations.py` to learn folder management
- Check `advanced_search.py` for powerful search queries
- `batch_operations.py` shows how to handle multiple files efficiently
