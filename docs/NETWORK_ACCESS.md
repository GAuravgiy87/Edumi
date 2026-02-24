# Network Access Guide

## Your Network Configuration

**Local IP Address:** `10.17.2.47`

## How to Access from Other Devices

### On This Computer
- Open browser and go to: `http://localhost:8000`
- Or: `http://10.17.2.47:8000`

### On Other Devices (Same WiFi)
1. Make sure the device is connected to the **same WiFi network**
2. Open a web browser on that device
3. Go to: `http://10.17.2.47:8000`
4. Login with your credentials

## Starting the Services

### Option 1: Use the Batch File
Double-click `start_network.bat` - it will start both services automatically

### Option 2: Manual Start
Open two command prompts and run:

**Terminal 1 (Camera Service):**
```bash
python camera_service/manage.py runserver 0.0.0.0:8001
```

**Terminal 2 (Main App):**
```bash
python manage.py runserver 0.0.0.0:8000
```

## Firewall Settings

If other devices can't connect, you may need to allow Python through Windows Firewall:

1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Find Python or add it manually
4. Allow both Private and Public networks
5. Click OK

## Troubleshooting

### Can't connect from other devices?
- Check if both devices are on the same WiFi
- Verify your IP hasn't changed: `ipconfig` in command prompt
- Check Windows Firewall settings
- Try disabling firewall temporarily to test

### IP Address Changed?
If your computer's IP changes, update these files:
1. `school_project/settings.py` - ALLOWED_HOSTS
2. `camera_service/camera_service/settings.py` - ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS
3. `start_network.bat` - Update the IP in the echo messages

## Security Note

⚠️ This configuration allows anyone on your WiFi to access the app. For production use:
- Use proper authentication
- Set up HTTPS
- Configure specific ALLOWED_HOSTS
- Use a proper web server (not Django development server)
