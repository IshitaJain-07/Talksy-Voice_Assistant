@echo off
echo Starting Talksy - Privacy-focused Voice Assistant
echo ===============================================

REM Starting backend server
echo Starting backend server...
start cmd /k "cd backend && python run.py"

REM Wait for the backend to start up
echo Waiting for backend to initialize (5 seconds)...
timeout /t 5 /nobreak > nul

REM Starting frontend server
echo Starting frontend server...
start cmd /k "cd frontend/talksy && npm run dev"

echo.
echo Talksy is starting up:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo Open http://localhost:3000 in your browser to use Talksy.
echo.
echo Press any key to close this window. The servers will continue running.
pause > nul 