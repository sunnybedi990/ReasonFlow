import os
import shutil
import subprocess
from datetime import datetime

def clean_build_dirs():
    """Clean up build directories"""
    dirs_to_clean = ['build', 'dist', 'reasonflow.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")

def build_package():
    """Build the package"""
    try:
        # Clean previous builds
        clean_build_dirs()
        
        # Create build timestamp (PEP 440 compliant)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        version = f"0.1.0.dev0+{timestamp}"  # PEP 440 compliant version
        
        # Update version in setup.py with timestamp
        with open('setup.py', 'r', encoding='utf-8') as f:
            setup_content = f.read()
        
        # Add build timestamp to version
        setup_content = setup_content.replace(
            'version="0.1.0"',
            f'version="{version}"'
        )
        
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        # Build package
        print("\nBuilding package...")
        subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'], check=True)
        
        # Get the built wheel file
        wheel_file = None
        for file in os.listdir('dist'):
            if file.endswith('.whl'):
                wheel_file = os.path.join('dist', file)
                break
        
        if wheel_file:
            print(f"\nPackage built successfully!")
            print(f"Wheel file: {wheel_file}")
            print("\nTo install in another project:")
            print(f"pip install {wheel_file}")
        else:
            print("No wheel file found in dist directory")
            
    except Exception as e:
        print(f"Error building package: {str(e)}")
        raise
    finally:
        # Restore original setup.py
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write(setup_content.replace(
                f'version="{version}"',
                'version="0.1.0"'
            ))

def create_install_script():
    """Create an installation script"""
    script_content = """#!/bin/bash
# ReasonFlow Installation Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install wheel if not present
pip install wheel

# Install the package
pip install dist/*.whl

echo "ReasonFlow installed successfully!"
"""
    
    with open('install.sh', 'w') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod('install.sh', 0o755)
    print("Created install.sh script")

if __name__ == "__main__":
    print("Building ReasonFlow package...")
    build_package()
    create_install_script()
    print("\nBuild complete!") 