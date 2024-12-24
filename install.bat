@echo off
echo Installing ReasonFlow...

:: Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install wheel if not present
pip install wheel

:: Install the package
pip install dist\*.whl

echo ReasonFlow installed successfully!
pause 