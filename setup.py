"""Setup script for gdrive-toolkit package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gdrive-toolkit",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight Google Drive toolkit for Kaggle, Colab, and local environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gdrive-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gdrive-toolkit=gdrive_toolkit.cli:main',
            'gdt=gdrive_toolkit.cli:main',  # Short alias
        ],
    },
    keywords="google-drive pydrive2 kaggle colab automation cli",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/gdrive-toolkit/issues",
        "Source": "https://github.com/yourusername/gdrive-toolkit",
    },
)
