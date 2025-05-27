@echo off
echo ========================================
echo Flask API Environment Setup
echo ========================================

REM Check if Python is installed
echo [1/6] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR]: Python is not installed or not in PATH
    pause
    exit /b 1
)

python --version
echo [OK] Python successfully detected

REM Create virtual environment
echo.
echo [2/6] Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists
) else (
    echo [PROCESSING] Creating environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR]: Unable to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment successfully created
)

REM Activate virtual environment
echo.
echo [3/6] Activating virtual environment...
echo [PROCESSING] Activation in progress...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR]: Unable to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Update pip
echo.
echo [4/6] Updating pip...
echo [PROCESSING] Downloading and installing the latest version of pip...
python -m pip install --upgrade pip
echo [OK] pip successfully updated

REM Install dependencies
echo.
echo [5/6] Installing Flask dependencies...
echo [PROCESSING] This step may take a few minutes (downloading packages)...
echo [PACKAGES] Installation in progress:
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR]: Unable to install dependencies
    pause
    exit /b 1
)
echo [OK] All dependencies successfully installed!

REM Show installed packages
echo.
echo [6/6] Verifying installation...
echo [PROCESSING] Generating list of installed packages...
echo.
echo ========================================
echo [PACKAGES] Installed packages:
echo ========================================
pip list

echo.
echo ========================================
echo [SUCCESS] Setup completed successfully!
echo ========================================
echo.
echo [OK] The virtual environment is now activated.
echo [START] You can now use Flask commands:
echo.
echo   flask --version
echo   python app.py
echo   flask run
echo.
echo [TIP] To deactivate the virtual environment later:
echo   deactivate
echo.
echo ========================================
echo [CONSOLE] Opening command prompt...
echo ========================================

REM Open a new command prompt with the environment activated
cmd /k