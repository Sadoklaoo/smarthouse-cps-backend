# Smart House Backend

## Overview 🏠🔌
The **Smart House Backend** is a RESTful API designed to manage smart home devices, automate actions, and track real-time events. The system enables users to control connected devices, trigger automation rules, and monitor events seamlessly.

## Features 🚀
- User authentication & role-based access control
- Device management (add, update, retrieve devices)
- Event handling system for tracking smart home interactions
- Automation rules to trigger actions based on conditions
- WebSocket support for real-time event notifications (future enhancement)

## Tech Stack 🛠️
- **Backend Framework**: FastAPI, Beanie, Redis, Celery, MQTT
- **Database**: MongoDB
- **Authentication**: JWT-based authentication
- **Containerization**: Docker (for easy deployment)
- **Testing**: Pytest (for unit and integration tests)

## Installation 🏗️
### **1. Clone the Repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/smart-house-backend.git
cd smart-house-backend
```

### **2. Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows (PowerShell)
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the Application**
```bash
uvicorn app.main:app --reload
```

## API Endpoints 📡
### **User Management**
- `POST /users/register` → Register a new user
- `POST /users/login` → Authenticate user & get JWT token

### **Device Management**
- `POST /devices/add` → Add a new smart device
- `GET /devices` → Retrieve all devices
- `PUT /devices/{device_id}` → Update device status

### **Event Handling**
- `POST /events/trigger` → Log an event from a smart device
- `GET /events` → Retrieve event history

### **Automation Rules**
- `POST /rules/create` → Define an automation rule
- `GET /rules` → List all automation rules

## Running Tests 🧪
```bash
pytest tests/
```

## Deployment 📦
To deploy using Docker:
```bash
docker build -t smart-house-backend .
docker run -p 8000:8000 smart-house-backend
```

## Contributing 🤝
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Commit changes: `git commit -m 'Add new feature'`.
4. Push the branch: `git push origin feature/new-feature`.
5. Open a Pull Request.

## Future Enhancements 🔮
- Implement WebSockets for real-time updates
- Role-based access control (RBAC) for enhanced security
- AI-based predictive automation rules

## License 📜
This project is licensed under the MIT License.

---

💡 *Let's make smart homes even smarter!* 🚀🏡
