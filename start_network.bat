@echo off
echo ========================================
echo Starting DigiRoom on Network
echo ========================================
echo.
echo Your local IP: 10.17.2.47
echo.
echo Starting Camera Service on port 8001...
start "Camera Service" cmd /k "python camera_service/manage.py runserver 0.0.0.0:8001"
timeout /t 3 /nobreak >nul

echo Starting Main App on port 8000...
start "Main App" cmd /k "python manage.py runserver 0.0.0.0:8000"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo Services Started!
echo ========================================
echo.
echo Access from this computer:
echo   http://localhost:8000
echo.
echo Access from other devices on WiFi:
echo   http://10.17.2.47:8000
echo.
echo Share this URL with others on your WiFi!
echo ========================================
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo Stopping services...
taskkill /F /FI "WINDOWTITLE eq Camera Service*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Main App*" >nul 2>&1
echo Services stopped.
