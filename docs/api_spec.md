# API Specification - Smart House Backend 🚀🏡🔌

## Overview ✨📡🏠
The Smart House backend API will manage smart devices, events, and user interactions in an automated home environment. This API will allow devices to communicate with each other, store event data, and trigger automated actions based on predefined conditions. 🔄⚙️💡

## Base URL 🌍🔗📡
```
/api/v1/
```

## Authentication 🔑🔒🛡️
- Authentication will use **JWT tokens** for secure access. 🏷️🔑📲
- Users must log in to obtain a token before making requests. 👤✅🔓
- Some endpoints will require admin privileges. 🏆🔐🖥️

## Endpoints 📌🛠️🔍

### 1. User Management 👥💼🔑
#### **Register a New User** ✍️📧🔐
**POST** `/users/register`
- Request Body:
```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "securepassword"
}
```
- Response:
```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com",
  "message": "User registered successfully."
}
```

#### **User Login** 🔓🔑📲
**POST** `/users/login`
- Request Body:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```
- Response:
```json
{
  "access_token": "jwt_token_here",
  "token_type": "Bearer"
}
```

### 2. Device Management 📱🏠🔌
#### **Add a New Device** ➕🖥️💡
**POST** `/devices/add`
- Request Body:
```json
{
  "device_name": "Living Room Light",
  "device_type": "light",
  "status": "off"
}
```
- Response:
```json
{
  "id": 1,
  "device_name": "Living Room Light",
  "status": "off",
  "message": "Device added successfully."
}
```

#### **Get All Devices** 🔍📋💾
**GET** `/devices`
- Response:
```json
[
  {
    "id": 1,
    "device_name": "Living Room Light",
    "status": "off"
  },
  {
    "id": 2,
    "device_name": "Thermostat",
    "status": "on"
  }
]
```

#### **Update Device Status** 🔄⚙️📶
**PUT** `/devices/{device_id}`
- Request Body:
```json
{
  "status": "on"
}
```
- Response:
```json
{
  "message": "Device status updated successfully."
}
```

### 3. Event Handling 🎯📡🔔
#### **Trigger an Event** ⚡🚀📲
**POST** `/events/trigger`
- Request Body:
```json
{
  "device_id": 1,
  "event_type": "motion_detected",
  "timestamp": "2025-03-10T12:00:00Z"
}
```
- Response:
```json
{
  "message": "Event triggered successfully."
}
```

#### **Get Event History** 🕒📊🔍
**GET** `/events`
- Response:
```json
[
  {
    "id": 1,
    "device_id": 1,
    "event_type": "motion_detected",
    "timestamp": "2025-03-10T12:00:00Z"
  }
]
```

### 4. Automation & Rules 🤖🔄⚙️
#### **Define an Automation Rule** 🎭⚙️🚦
**POST** `/rules/create`
- Request Body:
```json
{
  "condition": "motion_detected",
  "action": "turn_on_light",
  "device_id": 1
}
```
- Response:
```json
{
  "message": "Automation rule created successfully."
}
```

#### **Get All Automation Rules** 📜⚙️📌
**GET** `/rules`
- Response:
```json
[
  {
    "id": 1,
    "condition": "motion_detected",
    "action": "turn_on_light",
    "device_id": 1
  }
]
```

### Error Handling ⚠️🚨🛑
Errors will be returned in the following format:
```json
{
  "error": "Invalid credentials",
  "status": 401
}
```

## Future Considerations 🔮📈🧠
- WebSocket support for real-time event notifications. 📡📢💡
- Role-based access control (RBAC) for user permissions. 👤🔒⚙️
- Integration with cloud services for remote access. ☁️🔗📶

This API specification serves as a starting point. Additional refinements can be made as requirements evolve. 🚀📘🎯