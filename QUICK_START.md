# Quick Start Guide

## 🚀 Start the Application

### Local Access Only
```bash
start_services.bat
```
Access at: `http://localhost:8000`

### Network Access (WiFi)
```bash
start_network.bat
```
Access from any device on WiFi: `http://10.17.2.47:8000`

## 📁 Project Organization

```
Root Directory (Clean!)
├── 📚 docs/          - All documentation
├── 🧪 tests/         - All test scripts
├── 🛠️ utils/         - Setup & utility scripts
├── 📱 accounts/      - User management
├── 📹 cameras/       - Camera features
├── 🎥 meetings/      - Video conferencing
└── 🎨 static/        - CSS, JS, images
```

## 🔧 Common Tasks

### Setup Admin User
```bash
python utils/setup_admin.py
```

### Test Camera Service
```bash
python tests/test_camera_service.py
```

### Check Network Access
```bash
python tests/test_network_access.py
```

### Fix Firewall (if needed)
```bash
allow_firewall.bat
```
(Run as Administrator)

## 📖 Full Documentation

- **README.md** - Complete project documentation
- **RUN.md** - Detailed running instructions
- **docs/NETWORK_ACCESS.md** - Network setup guide
- **docs/UPDATE.md** - Changelog

## 🆘 Need Help?

1. Check `docs/` folder for guides
2. Run test scripts in `tests/` folder
3. Use utility scripts in `utils/` folder

## 🌐 Default Credentials

After running `utils/setup_admin.py`:
- Username: `admin`
- Password: `admin123`

## 📞 Services

| Service | Port | URL |
|---------|------|-----|
| Main App | 8000 | http://localhost:8000 |
| Camera Service | 8001 | http://localhost:8001 |
