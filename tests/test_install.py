"""
Quick test script to verify installation and basic functionality.
Script kiểm tra nhanh để xác nhận cài đặt.
"""

import sys

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    
    try:
        import gdrive_toolkit
        print(f"✓ gdrive_toolkit version {gdrive_toolkit.__version__}")
        
        from gdrive_toolkit import (
            quick_connect,
            upload_file,
            download_file,
            search_files,
            create_folder,
            share_file,
        )
        print("✓ All main functions imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_environment_detection():
    """Test environment detection."""
    print("\nTesting environment detection...")
    
    try:
        from gdrive_toolkit import detect_environment
        env = detect_environment()
        print(f"✓ Detected environment: {env}")
        return True
    except Exception as e:
        print(f"✗ Environment detection error: {e}")
        return False


def test_utilities():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    try:
        from gdrive_toolkit import format_size
        
        # Test format_size
        assert format_size(1024) == "1.00 KB"
        assert format_size(1536000) == "1.46 MB"
        print("✓ Utility functions work correctly")
        
        return True
    except Exception as e:
        print(f"✗ Utility test error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("gdrive-toolkit - Quick Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_environment_detection,
        test_utilities,
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("\nNext steps:")
        print("1. Set up credentials (see docs/CREDENTIALS_SETUP.md)")
        print("2. Run examples: python examples/basic_usage.py")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ Some tests failed!")
        print("Please check the errors above.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
