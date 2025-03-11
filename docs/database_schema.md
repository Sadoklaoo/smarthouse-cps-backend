# Database Schema - Smart House Backend

## Overview 🏠💾🔌
The Smart House backend requires a structured database to store information about users, devices, events, and automation rules. The database will be designed to handle real-time event processing while ensuring scalability and security.

## Database Choice 🛠️🔍💡
The database system has not been finalized yet, but it will likely be **PostgreSQL** (for structured relational data) or **MongoDB** (if we need flexible document storage). The schema below is designed to be adaptable to either option.

---

## Tables & Collections 📋🛠️🗂️

### **Users Table** 👤🔑📄
Stores registered users who interact with the system.

| Column       | Type           | Constraints |
|-------------|---------------|-------------|
| id          | UUID (Primary Key) | Unique, Auto-generated |
| username    | VARCHAR(255)   | Unique, Required |
| email       | VARCHAR(255)   | Unique, Required |
| password    | TEXT           | Required, Hashed |
| role        | ENUM('admin', 'resident', 'guest') | Default: 'resident' |
| created_at  | TIMESTAMP      | Default: CURRENT_TIMESTAMP |

---

### **Devices Table** 📱🔌🏠
Represents smart devices installed in the house.

| Column       | Type           | Constraints |
|-------------|---------------|-------------|
| id          | UUID (Primary Key) | Unique, Auto-generated |
| device_name | VARCHAR(255)   | Required |
| device_type | VARCHAR(100)   | Required (e.g., 'light', 'thermostat') |
| status      | ENUM('on', 'off') | Default: 'off' |
| user_id     | UUID (Foreign Key) | References users(id) |
| created_at  | TIMESTAMP      | Default: CURRENT_TIMESTAMP |

---

### **Events Table** 📡⚡🕒
Tracks events triggered by smart devices.

| Column       | Type           | Constraints |
|-------------|---------------|-------------|
| id          | UUID (Primary Key) | Unique, Auto-generated |
| device_id   | UUID (Foreign Key) | References devices(id) |
| event_type  | VARCHAR(255)   | Required (e.g., 'motion_detected') |
| timestamp   | TIMESTAMP      | Default: CURRENT_TIMESTAMP |

---

### **Automation Rules Table** 🤖🔄⚙️
Stores predefined automation rules that trigger actions based on conditions.

| Column       | Type           | Constraints |
|-------------|---------------|-------------|
| id          | UUID (Primary Key) | Unique, Auto-generated |
| condition   | VARCHAR(255)   | Required (e.g., 'motion_detected') |
| action      | VARCHAR(255)   | Required (e.g., 'turn_on_light') |
| device_id   | UUID (Foreign Key) | References devices(id) |
| created_at  | TIMESTAMP      | Default: CURRENT_TIMESTAMP |

---

## Future Considerations 🔮📈🔍
- Implement **WebSocket** integration for real-time event updates. 📡⚡
- Add **log history** to track user actions and device interactions. 📜🔎
- Introduce **AI-based automation rules** for predictive control. 🤖📊🔮

This schema provides a foundational structure for the backend. It can be expanded based on specific requirements. 🚀

