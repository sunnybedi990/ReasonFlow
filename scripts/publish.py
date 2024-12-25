import os
import subprocess
from pathlib import Path

def clean_dist():
    """Clean distribution directories"""
    for dir_name in ['dist', 'build', '*.egg-info']:
        os.system(f'rm -rf {dir_name}')

def build_package():
    """Build the package"""
    subprocess.run(['python', '-m', 'build'], check=True)

def upload_to_test_pypi():
    """Upload to Test PyPI first"""
    subprocess.run(['python', '-m', 'twine', 'upload', '--repository-url', 'https://test.pypi.org/legacy/', 'dist/*'], check=True)

def upload_to_pypi():
    """Upload to PyPI"""
    subprocess.run(['python', '-m', 'twine', 'upload', 'dist/*'], check=True)

def main():
    # Clean previous builds
    clean_dist()
    
    # Build package
    build_package()
    
    # Ask for confirmation
    response = input("Do you want to upload to Test PyPI first? (y/n): ")
    if response.lower() == 'y':
        upload_to_test_pypi()
        
        # Test installation from Test PyPI
        print("\nTesting installation from Test PyPI...")
        subprocess.run(['pip', 'install', '--index-url', 'https://test.pypi.org/simple/', 'reasonflow'], check=True)
        
        response = input("\nDo you want to proceed with PyPI upload? (y/n): ")
        if response.lower() != 'y':
            print("Aborting PyPI upload")
            return
    
    # Upload to PyPI
    upload_to_pypi()
    print("\nPackage successfully uploaded to PyPI!")

if __name__ == "__main__":
    main() 