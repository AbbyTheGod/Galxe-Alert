@echo off
echo 🤖 Galxe Quest Monitor Bot
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import telegram, requests, bs4, selenium, dotenv" >nul 2>&1
if errorlevel 1 (
    echo ❌ Dependencies not installed
    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo Creating from template...
    copy env_example.txt .env
    echo.
    echo Please edit .env file with your Telegram bot credentials
    echo Then run this script again
    pause
    exit /b 1
)

echo ✅ All checks passed
echo.
echo 🚀 Starting bot...
echo Press Ctrl+C to stop
echo.

REM Run the bot
python run_bot.py

pause 