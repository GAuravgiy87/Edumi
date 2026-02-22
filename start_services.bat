@echo off
REM Start both services on Windows

echo Starting Camera Service on port 8001...
start "Camera Service" cmd /k "cd camera_service && python manage.py runserver 8001"

timeout /t 3 /nobreak > nul

echo Starting Main App on port 8000...
start "Main App" cmd /k "python manage.py runserver 8000"

echo.
echo Services started:
echo   Main App: http://localhost:8000
echo   Camera Service: http://localhost:8001
echo.
echo Close the command windows to stop services
