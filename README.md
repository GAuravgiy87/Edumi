<div align="center">

# 🎓 EduMi

### *Educational Meeting Platform - Where Learning Meets Innovation*

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/WebRTC-333333?style=for-the-badge&logo=webrtc&logoColor=white" />
<img src="https://img.shields.io/badge/Channels-092E20?style=for-the-badge&logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />

---

### ✨ *A modern, real-time video conferencing platform designed specifically for educational institutions*

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Updates](#-updates)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🎥 **Real-Time Video Meetings**
- HD video conferencing with WebRTC
- Screen sharing capabilities
- Dynamic layout (Google Meet style)
- Automatic video quality adjustment

</td>
<td width="50%">

### 👥 **User Management**
- Role-based access (Teachers/Students)
- User profiles with avatars
- Admin dashboard
- Secure authentication

</td>
</tr>
<tr>
<td width="50%">

### 📹 **Camera Monitoring**
- RTSP camera integration
- Live feed monitoring
- Multi-camera support
- Dedicated microservice architecture

</td>
<td width="50%">

### 💬 **Real-Time Chat**
- In-meeting chat
- Message history
- Unread notifications
- Emoji support

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
```

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd digiroom

# Install dependencies
pip install -r requirements.txt
pip install -r camera_service/requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (optional)
python setup_admin.py

# Create test users (optional)
python setup_test_users.py
```

### Running the Application

**Windows:**
```bash
./start_services.bat
```

**Linux/Mac:**
```bash
./start_services.sh
```

This will start:
- 🌐 **Main App** on `http://localhost:8000`
- 📹 **Camera Service** on `http://localhost:8001`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        EduMi Platform                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │   Main Application   │      │  Camera Microservice │    │
│  │    (Port 8000)       │◄────►│    (Port 8001)       │    │
│  │                      │      │                      │    │
│  │  • Authentication    │      │  • RTSP Streaming    │    │
│  │  • Meetings (ASGI)   │      │  • Live Feeds        │    │
│  │  • WebRTC/WebSocket  │      │  • Camera Management │    │
│  │  • User Management   │      │  • OpenCV Processing │    │
│  │  • Dashboards        │      │                      │    │
│  └──────────────────────┘      └──────────────────────┘    │
│           │                              │                   │
│           └──────────┬───────────────────┘                   │
│                      │                                       │
│              ┌───────▼────────┐                             │
│              │   SQLite DB    │                             │
│              │  (Shared)      │                             │
│              └────────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 4.2 |
| **Real-Time** | Django Channels, WebSockets |
| **Video** | WebRTC, OpenCV |
| **Database** | SQLite (Development) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Streaming** | RTSP, MJPEG |

---

## 📁 Project Structure

```
digiroom/
├── 📱 accounts/          # User authentication & profiles
├── 📹 cameras/           # Camera management UI
├── 🎥 camera_service/    # Dedicated streaming microservice
├── 🤝 meetings/          # Video conferencing logic
├── 📄 pages/             # Static pages
├── 🎨 static/            # CSS, JavaScript, assets
├── 📝 templates/         # HTML templates
├── ⚙️ school_project/    # Main Django settings
└── 📚 Documentation files
```

---

## 🎯 Key Features Explained

### 🎥 Meeting Room (Google Meet Style)

- **Single Participant**: Full-screen video
- **Multiple Participants**: Dynamic grid layout (2-4 columns)
- **Screen Sharing**: Main screen + participant sidebar
- **Fixed Controls**: Top bar and bottom controls stay in place
- **Responsive Design**: Works on desktop, tablet, and mobile

### 🔐 Security

- CSRF protection
- Secure WebSocket connections
- Role-based access control
- Meeting code authentication

### 🎨 User Interface

- Modern, clean design
- Smooth animations
- Intuitive controls
- Dark mode for meetings
- Accessibility compliant

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [RUN.md](RUN.md) | Detailed running instructions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture details |
| [README_MICROSERVICES.md](README_MICROSERVICES.md) | Microservices explanation |
| [UPDATE.md](UPDATE.md) | Complete changelog & fixes |
| [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) | Setup guide |
| [QUICK_START.md](QUICK_START.md) | Quick start guide |

---

## 🛠️ Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Admin Panel

```bash
# Create superuser
python manage.py createsuperuser

# Access at http://localhost:8000/admin/
```

---

## 🎓 Use Cases

- **Virtual Classrooms**: Conduct live online classes
- **Student Meetings**: Group study sessions
- **Teacher Collaboration**: Staff meetings and planning
- **Campus Monitoring**: Security camera integration
- **Hybrid Learning**: Combine in-person and remote students

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Django & Django Channels teams
- WebRTC community
- OpenCV contributors
- All open-source libraries used

---

<div align="center">

### 💡 Built with ❤️ for Education

**EduMi** - *Empowering Education Through Technology*

[⬆ Back to Top](#-edumi)

</div>
