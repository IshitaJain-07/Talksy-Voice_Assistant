#!/bin/bash

echo "Starting Talksy - Privacy-focused Voice Assistant"
echo "==============================================="

# Starting backend server
echo "Starting backend server..."
cd backend && python run.py &
BACKEND_PID=$!

# Wait for the backend to start up
echo "Waiting for backend to initialize (5 seconds)..."
sleep 5

# Starting frontend server
echo "Starting frontend server..."
cd ../frontend/talksy && npm run dev &
FRONTEND_PID=$!

echo ""
echo "Talksy is starting up:"
echo "- Backend: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo ""
echo "Open http://localhost:3000 in your browser to use Talksy."
echo ""
echo "Press Ctrl+C to stop all servers."

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 