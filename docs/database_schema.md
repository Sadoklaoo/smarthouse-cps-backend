# Database Schema - Smart House Backend 🏠💾🔌

## Overview

This document describes the MongoDB collections and their schemas as implemented with Beanie ODM. The schema supports users, devices, sensors, automation rules, events, and consequence tracking in a fully asynchronous architecture.

---

## Collections 📂

### 1. `users`

Stores application users with secure credentials and profile data.

```json
// Example Document
{
  "_id": ObjectId("6806a1e4d3f4b522c3a9f8d2"),
  "email": "user@example.com",
  "hashed_password": "$2b$12$...",
  "full_name": "Alice Smith",
  "is_active": true,
  "created_at": ISODate("2025-05-12T14:23:45.678Z")
}
```

| Field             | Type              | Description                   |
| ----------------- | ----------------- | ----------------------------- |
| `_id`             | ObjectId          | Primary key                   |
| `email`           | String (EmailStr) | Unique, validated by Pydantic |
| `hashed_password` | String            | Bcrypt-hashed                 |
| `full_name`       | String (optional) | User's display name           |
| `is_active`       | Boolean           | Account active flag           |
| `created_at`      | datetime          | Timestamp at creation         |

---

### 2. `devices`

Represents user-owned smart devices with current state.

```json
// Example Document
{
  "_id": ObjectId("6806b2f7e5a4c633d4b0a9f3"),
  "name": "Living Room Light",
  "type": "light",
  "location": "Living Room",
  "user_id": ObjectId("6806a1e4d3f4b522c3a9f8d2"),
  "is_active": true,
  "state": "off",
  "registered_at": ISODate("2025-05-12T14:30:22.123Z")
}
```

| Field           | Type                | Description                               |
| --------------- | ------------------- | ----------------------------------------- |
| `_id`           | ObjectId            | Primary key                               |
| `name`          | String              | Device name                               |
| `type`          | String              | Device category (e.g., light, thermostat) |
| `location`      | String (optional)   | Physical location of the device           |
| `user_id`       | ObjectId            | Reference to `users._id`                  |
| `is_active`     | Boolean             | Device active flag                        |
| `state`         | String ("on"/"off") | Current power state                       |
| `registered_at` | datetime            | Timestamp when device was registered      |

Indexes:

* `user_id` for querying devices by user

---

### 3. `sensors`

Holds sensor configurations linked to devices.

```json
// Example Document
{
  "_id": ObjectId("6806c3a8f6b5d744e5c1b2d4"),
  "name": "Temperature Sensor",
  "type": "temperature",
  "device_id": ObjectId("6806b2f7e5a4c633d4b0a9f3"),
  "location": "Living Room",
  "unit": "°C",
  "is_active": true,
  "registered_at": ISODate("2025-05-12T14:35:10.456Z")
}
```

| Field           | Type              | Description                             |
| --------------- | ----------------- | --------------------------------------- |
| `_id`           | ObjectId          | Primary key                             |
| `name`          | String            | Sensor name                             |
| `type`          | String            | Sensor type (temperature, motion, etc.) |
| `device_id`     | ObjectId          | Reference to `devices._id`              |
| `location`      | String (optional) | Location or zone monitored              |
| `unit`          | String (optional) | Measurement unit (°C, %, etc.)          |
| `is_active`     | Boolean           | Sensor active flag                      |
| `registered_at` | datetime          | Timestamp when sensor was registered    |

Indexes:

* `device_id` for querying sensors by device

---

### 4. `rules`

Defines automation rules to trigger actions based on events.

```json
// Example Document
{
  "_id": ObjectId("6806d4b9a7c6e855f6d2c3e5"),
  "name": "Heat Alert",
  "trigger_type": "temperature_change",
  "condition": { "temperature": 28.0 },
  "operator": ">",
  "target_device_id": "6806b2f7e5a4c633d4b0a9f3",
  "action": "turn_on",
  "created_at": ISODate("2025-05-12T14:40:05.789Z")
}
```

| Field              | Type            | Description                                     |
| ------------------ | --------------- | ----------------------------------------------- |
| `_id`              | ObjectId        | Primary key                                     |
| `name`             | String          | Human-friendly rule name                        |
| `trigger_type`     | String          | Event type to match (e.g., temperature\_change) |
| `condition`        | Document        | Key-value map of threshold conditions           |
| `operator`         | String (> < ==) | Comparison operator                             |
| `target_device_id` | String          | Device ID string to perform action on           |
| `action`           | String          | Action command (e.g., turn\_on, turn\_off)      |
| `created_at`       | datetime        | Timestamp when rule was created                 |

---

### 5. `consequences`

Logs the outcome of rule evaluations and actions taken.

```json
// Example Document
{
  "_id": ObjectId("6806e5cab8d7f96607e3d4f6"),
  "event_id": "evt123",
  "rule_id": "6806d4b9a7c6e855f6d2c3e5",
  "action": "turn_on",
  "device_id": "6806b2f7e5a4c633d4b0a9f3",
  "status": "executed",
  "timestamp": ISODate("2025-05-12T14:45:30.012Z")
}
```

| Field       | Type     | Description                                 |
| ----------- | -------- | ------------------------------------------- |
| `_id`       | ObjectId | Primary key                                 |
| `event_id`  | String   | Unique identifier from event producer       |
| `rule_id`   | String   | ID of the rule that triggered the action    |
| `action`    | String   | Action performed                            |
| `device_id` | String   | Device on which the action was executed     |
| `status`    | String   | `pending` or `executed`                     |
| `timestamp` | datetime | When the consequence was logged or executed |

---

## Change Streams & Event Logs 🔄

* The application captures raw events in Redis and optionally logs them permanently if needed (e.g., an `event_logs` collection).
* Recommended: use MongoDB Change Streams on `consequences` or `devices` to push real-time updates to clients.

---

*This schema directly mirrors your Beanie models and ensures efficient queries via dedicated indexes.*
