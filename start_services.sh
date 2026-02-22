#!/bin/bash
# Start both services

echo "Starting Camera Service on port 8001..."
cd camera_service
python manage.py runserver 8001 &
CAMERA_PID=$!
cd ..

echo "Waiting for camera service to start..."
sleep 3

echo "Starting Main App on port 8000..."
python manage.py runserver 8000 &
MAIN_PID=$!

echo ""
echo "Services started:"
echo "  Main App: http://localhost:8000"
echo "  Camera Service: http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $CAMERA_PID $MAIN_PID; exit" INT
wait
