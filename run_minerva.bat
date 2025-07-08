@echo off
TITLE Minerva AI Server

echo Activating virtual environment...

rem This command finds and activates the Python environment where all your packages are installed.
call "%~dp0venv\Scripts\activate"

echo.
echo Starting Flask server at http://127.0.0.1:5001
echo THIS WINDOW MUST REMAIN OPEN TO RUN THE APP.
echo.

rem This command executes your main Python script, starting the web server.
python "%~dp0app.py"

echo.
echo Server stopped.
pause