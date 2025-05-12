# Smart House Backend 🏠🔌💡

## Overview ✨📡🏠
The **Smart House Backend** is a high-performance RESTful API built with Python and FastAPI. It serves as the central nervous system for a smart home environment, enabling management of users, smart devices, sensors, and automation rules. The system processes real-time events via Redis, evaluates user-defined rules, logs consequences, and simulates device-state changes via MQTT. Its asynchronous design ensures scalability and responsiveness.

## Core Features 🚀🌟
-   **User Management**
    -   Register new users (`POST /users/`)
    -   Retrieve user details (`GET /users/{user_id}`)
    -   Update user profiles (`PUT /users/{user_id}`)
    -   Delete users (`DELETE /users/{user_id}`)

-   **Device Management**
    -   CRUD operations for smart devices (`/devices` endpoints)
    -   Each device has a live `state` ("on"/"off")
    -   Change state via generic update or `POST /devices/{id}/state`

-   **Sensor Management**
    -   CRUD operations for sensors (`/sensors` endpoints)
    -   Filter sensors by device (`GET /sensors/device/{device_id}`)

-   **Event Handling & Reactor**
    -   Submit events to Redis queue (`app/queues/event_producer.py`)
    -   Background reactor consumes events, matches rules, and logs consequences

-   **Rule Engine**
    -   Define automation rules (`POST /rules/`) with trigger type, condition, operator, target device, and action
    -   List rules (`GET /rules/`) and delete rules (`DELETE /rules/{rule_id}`)

-   **Consequence Tracking**
    -   Log each action as a `Consequence` in MongoDB
    -   Automatic status update to `executed` with timestamp
    -   List consequences (`GET /consequences/`) and execute pending (`PUT /consequences/{id}/execute`)

-   **Device State Simulation**
    -   Reactor triggers `turn_on`/`turn_off` actions via `set_device_state()` service

-   **MQTT Simulation**
    -   Simple Paho-MQTT scripts to publish control messages and log device responses

## Tech Stack 🛠️💻
-   Python 3.10+
-   FastAPI + Uvicorn
-   MongoDB (Beanie ODM + Motor)
-   Redis for event queuing
-   Paho-MQTT for device simulation
-   Docker & Docker Compose
-   Pytest + pytest-asyncio + httpx for testing

## Project Structure 📂
```
smarthouse-cps-backend/
├── app/
│   ├── api/routes/       # FastAPI routers (users, devices, sensors, rules, consequences)
│   ├── core/             # Configuration & Redis client
│   ├── devices/          # MQTT simulator scripts
│   ├── models/           # Beanie Document models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic & database operations
│   ├── queues/           # Event producer & reactor worker
│   └── main.py           # FastAPI application entrypoint
├── docker-compose.yml    # Service definitions (backend, mqtt, mongo)
├── Dockerfile            # Backend image build
├── requirements.txt      # Python dependencies
└── tests/                # Test suite
```

## API Endpoints 📡
-   **Users** (`/users`)
    -   `POST /users/`
    -   `GET /users/{user_id}`
    -   `PUT /users/{user_id}`
    -   `DELETE /users/{user_id}`

-   **Devices** (`/devices`)
    -   `POST /devices/`
    -   `GET /devices/` (by user)
    -   `GET /devices/{device_id}`
    -   `PUT /devices/{device_id}`
    -   `POST /devices/{device_id}/state` (on/off)
    -   `DELETE /devices/{device_id}`

-   **Sensors** (`/sensors`)
    -   `POST /sensors/`
    -   `GET /sensors/`
    -   `GET /sensors/device/{device_id}`
    -   `GET /sensors/{sensor_id}`
    -   `DELETE /sensors/{sensor_id}`

-   **Rules** (`/rules`)
    -   `POST /rules/`
    -   `GET /rules/`
    -   `DELETE /rules/{rule_id}`

-   **Consequences** (`/consequences`)
    -   `GET /consequences/`
    -   `GET /consequences/{id}`
    -   `PUT /consequences/{id}/execute`

-   **Event Trigger** (`/monitor/trigger`)
    -   `POST /monitor/trigger` to enqueue an event

## Environment & Deployment 🚀
-   Configure via `.env`
-   Launch with `docker-compose up --build`
-   Explore Swagger UI at `http://localhost:8000/docs`

## Testing 🧪
```bash
pytest
```

## Future Enhancements & Roadmap 🔮🗺️
-   WebSocket Integration for instant, real-time device and sensor updates.
-   Device & Sensor History endpoints for comprehensive audit trails and analytics.
-   Advanced Authentication & Authorization, including refresh tokens, OAuth2 support, and role-based access control enhancements.
-   Dashboards & Visualization to present smart home data, trends, and system health.
-   CI/CD Pipeline with automated testing, linting, and deployments.
-   Third-Party Integrations (e.g., voice assistants, IFTTT, Home Assistant).
-   Backup & Restore Mechanism for user data and configurations.

## Contributing 🤝📝
Contributions are welcome! Please fork the repo, create a feature branch, and submit a pull request with descriptive commits.

## License 📜
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
