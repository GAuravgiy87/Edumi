<div align="center">

<img src="static/logo.svg" alt="EduMi Logo" width="400" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2800&pause=2000&color=6366F1&center=true&vCenter=true&width=940&lines=Real-Time+Video+Conferencing+Platform;Built+for+Schools+%26+Universities;WebRTC+%7C+Django+%7C+Channels" alt="Typing SVG" />

<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/WebRTC-333333?style=for-the-badge&logo=webrtc&logoColor=white" />
  <img src="https://img.shields.io/badge/Channels-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/yourusername/edumi?style=flat-square&color=6366f1" />
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" />
</p>

### ✨ *Where Learning Meets Innovation* ✨

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🎥 Real-Time Video Meetings
```
✓ HD video conferencing with WebRTC
✓ Full quality screen sharing (up to 4K @ 60fps)
✓ Dynamic layout (Google Meet style)
✓ Automatic quality adjustment
✓ Zero latency optimization
```

</td>
<td width="50%">

### 👥 User Management
```
✓ Role-based access (Teachers/Students)
✓ User profiles with avatars
✓ Admin dashboard
✓ Secure authentication
✓ Meeting permissions
```

</td>
</tr>
<tr>
<td width="50%">

### 📹 Camera Monitoring
```
✓ RTSP camera integration
✓ Live feed monitoring
✓ Multi-camera support
✓ Dedicated microservice
✓ Optimized streaming
```

</td>
<td width="50%">

### 💬 Real-Time Chat
```
✓ In-meeting chat
✓ Message history
✓ Unread notifications
✓ Emoji support
✓ WebSocket powered
```

</td>
</tr>
</table>

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="1000">
</div>

---

## 🚀 Quick Start

<details open>
<summary><b>📦 Installation</b></summary>

```bash
# Clone the repository
git clone <repository-url>
cd edumi

# Install dependencies
pip install -r requirements.txt
pip install -r camera_service/requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (optional)
python setup_admin.py
```

</details>

<details open>
<summary><b>▶️ Running the Application</b></summary>

### Windows
```bash
./start_services.bat
```

### Linux/Mac
```bash
chmod +x start_services.sh
./start_services.sh
```

<img src="https://user-images.githubusercontent.com/74038190/216122041-518ac897-8d92-4c6b-9b3f-ca01dcaf38ee.png" width="30" /> **Both services will start automatically!**

</details>

<details>
<summary><b>🌐 Access Points</b></summary>

| Service | URL | Description |
|---------|-----|-------------|
| 🏠 **Main App** | `http://localhost:8000` | Login, meetings, dashboards |
| 📹 **Camera Service** | `http://localhost:8001` | Camera streaming API |

</details>

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">
</div>

---

## 🏗️ Architecture

<div align="center">

```mermaid
graph TB
    A[� User Browser] -->|HTTP/WebSocket| B[🌐 Main App :8000]
    A -->|Camera Feeds| C[📹 Camera Service :8001]
    B -->|ASGI/Channels| D[🔌 WebSocket Server]
    B -->|Shared DB| E[(💾 SQLite)]
    C -->|Shared DB| E
    C -->|RTSP| F[📷 IP Cameras]
    D -->|WebRTC| G[🎥 Video Conferencing]
    
    style A fill:#6366f1,stroke:#4f46e5,color:#fff
    style B fill:#10b981,stroke:#059669,color:#fff
    style C fill:#f59e0b,stroke:#d97706,color:#fff
    style D fill:#8b5cf6,stroke:#7c3aed,color:#fff
    style E fill:#ec4899,stroke:#db2777,color:#fff
    style F fill:#06b6d4,stroke:#0891b2,color:#fff
    style G fill:#ef4444,stroke:#dc2626,color:#fff
```

</div>

### 🎯 Microservices Design

<table>
<tr>
<td width="50%">

#### 🌐 Main Application (Port 8000)
- Django with ASGI support
- Channels for WebSocket
- Daphne as ASGI server
- Authentication & Authorization
- Meeting Management
- User Dashboards

</td>
<td width="50%">

#### 📹 Camera Microservice (Port 8001)
- Lightweight Django service
- WSGI-based (no conflicts)
- RTSP streaming
- OpenCV video processing
- Dedicated camera handling
- Optimized performance

</td>
</tr>
</table>

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284136-03988914-d899-44b4-b1d9-4eeccf656e44.gif" width="1000">
</div>

---

## � Technology Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend** | ![Django](https://img.shields.io/badge/Django_4.2-092E20?style=flat-square&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python_3.8+-3776AB?style=flat-square&logo=python&logoColor=white) |
| **Real-Time** | ![Channels](https://img.shields.io/badge/Django_Channels-092E20?style=flat-square&logo=django&logoColor=white) ![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=flat-square&logo=socket.io&logoColor=white) |
| **Video** | ![WebRTC](https://img.shields.io/badge/WebRTC-333333?style=flat-square&logo=webrtc&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL_Ready-4169E1?style=flat-square&logo=postgresql&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |

</div>

---

## 📊 Performance Metrics

<div align="center">

| Metric | Camera | Screen Share |
|--------|--------|--------------|
| **Resolution** | 480x360 | Up to 4K (3840x2160) |
| **Frame Rate** | 15 fps | Up to 60 fps |
| **Bitrate** | 500 Kbps | 5 Mbps |
| **Latency** | ~100ms | ~50ms |
| **CPU Usage** | 11% | 15% |

<img src="https://github-readme-stats.vercel.app/api?username=yourusername&show_icons=true&theme=tokyonight&hide_border=true&bg_color=1a1b27&title_color=6366f1&icon_color=6366f1&text_color=c9d1d9" width="48%" />
<img src="https://github-readme-streak-stats.herokuapp.com/?user=yourusername&theme=tokyonight&hide_border=true&background=1a1b27&stroke=6366f1&ring=6366f1&fire=6366f1&currStreakLabel=6366f1" width="48%" />

</div>

---

## 🎯 Key Features Explained

<details>
<summary><b>🎥 Meeting Room (Google Meet Style)</b></summary>

- **Single Participant**: Full-screen video
- **Multiple Participants**: Dynamic grid layout (2-4 columns)
- **Screen Sharing**: Full quality up to 4K @ 60fps with blue highlight
- **Floating Controls**: Modern pill-shaped button group
- **Responsive Design**: Works on desktop, tablet, and mobile

</details>

<details>
<summary><b>� Security</b></summary>

- CSRF protection
- Secure WebSocket connections
- Role-based access control
- Meeting code authentication
- User session management

</details>

<details>
<summary><b>⚡ Performance Optimizations</b></summary>

- **Video**: Optimized resolution and frame rates
- **WebRTC**: Low-latency configuration
- **Camera Service**: Efficient RTSP streaming
- **UI**: Hardware-accelerated rendering
- **Network**: Adaptive bitrate control

</details>

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" width="100">
</div>

---

## 📁 Project Structure

```
edumi/
├── 📱 accounts/              # User authentication & profiles
├── 📹 cameras/               # Camera management UI
├── 🎥 camera_service/        # Dedicated streaming microservice
│   ├── camera_api/           # API endpoints
│   ├── camera_service/       # Service settings
│   └── requirements.txt      # Service dependencies
├── 🤝 meetings/              # Video conferencing logic
│   ├── consumers.py          # WebSocket consumers
│   ├── routing.py            # WebSocket routing
│   └── models.py             # Meeting models
├── 📄 pages/                 # Static pages
├── 🎨 static/                # CSS, JavaScript, assets
│   ├── css/
│   │   ├── meeting-room.css  # Google Meet-style UI
│   │   └── ...
│   └── js/
├── 📝 templates/             # HTML templates
│   ├── meetings/
│   │   └── meeting_room.html # Main meeting interface
│   └── ...
├── ⚙️ school_project/        # Main Django settings
├── 📚 docs/                  # Documentation
│   ├── NETWORK_ACCESS.md     # Network setup guide
│   ├── APP_STATUS_REPORT.md  # Status reports
│   └── UPDATE.md             # Complete changelog
├── 🧪 tests/                 # Test scripts
│   ├── test_*.py             # Various test files
│   └── check_*.py            # Status check scripts
├── 🛠️ utils/                 # Utility scripts
│   ├── setup_*.py            # Setup scripts
│   └── fix_*.py              # Fix scripts
├── 🚀 Startup Scripts/
│   ├── start_services.bat    # Windows startup
│   ├── start_services.sh     # Linux/Mac startup
│   ├── start_network.bat     # Network access startup
│   └── allow_firewall.bat    # Firewall configuration
├── .gitignore
├── requirements.txt
├── README.md                 # Main documentation
├── RUN.md                    # Running instructions
└── manage.py
```

---

## 🎓 Use Cases

<div align="center">

| Use Case | Description |
|----------|-------------|
| 🏫 **Virtual Classrooms** | Conduct live online classes with screen sharing |
| 👨‍🎓 **Student Meetings** | Group study sessions and collaboration |
| 👨‍🏫 **Teacher Collaboration** | Staff meetings and planning sessions |
| 🎥 **Campus Monitoring** | Security camera integration and monitoring |
| 🔄 **Hybrid Learning** | Combine in-person and remote students |

</div>

---

## 📖 Documentation

<div align="center">

| Document | Location | Description |
|----------|----------|-------------|
| 📘 **README.md** | Root | Main documentation (you are here) |
| 🚀 **RUN.md** | Root | Detailed running instructions |
| 🌐 **NETWORK_ACCESS.md** | docs/ | Network setup & WiFi access guide |
| 📊 **APP_STATUS_REPORT.md** | docs/ | Application status & features |
| 📝 **UPDATE.md** | docs/ | Complete changelog & fixes |

</div>

---

## 🛠️ Development

<details>
<summary><b>Running Tests</b></summary>

```bash
python manage.py test
```

</details>

<details>
<summary><b>Creating Migrations</b></summary>

```bash
python manage.py makemigrations
python manage.py migrate
```

</details>

<details>
<summary><b>Accessing Admin Panel</b></summary>

```bash
# Create superuser
python manage.py createsuperuser

# Access at http://localhost:8000/admin/
```

</details>

---

## 🤝 Contributing

<div align="center">

Contributions are welcome! Please feel free to submit a Pull Request.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="400">

</div>

---

## 📝 License

<div align="center">

This project is licensed under the MIT License.

</div>

---

## 🙏 Acknowledgments

<div align="center">

<table>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" /><br>
<b>Django Team</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/WebRTC-333333?style=for-the-badge&logo=webrtc&logoColor=white" /><br>
<b>WebRTC Community</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" /><br>
<b>OpenCV Contributors</b>
</td>
</tr>
</table>

</div>

---

<div align="center">

### 💡 Built with ❤️ for Education
### Gaurav Chauhan

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=3000&pause=1000&color=6366F1&center=true&vCenter=true&width=600&lines=EduMi+-+Empowering+Education;Through+Technology;Real-Time+Video+Conferencing;For+Schools+%26+Universities" alt="Typing SVG" />

<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">

**[⬆ Back to Top](#-edumi)**

<p>
<img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Powered%20by-Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/Real--Time-WebRTC-333333?style=for-the-badge&logo=webrtc&logoColor=white" />
</p>

<sub>⭐ Star this repo if you find it helpful!</sub>

</div>
