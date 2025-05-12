# API Specification - Smart House Backend 🌐🚀

## Base URL

```
http://<host>:<port>
```

*No global prefix—each router is mounted at its own base path.*

---

## 1. User Management 👥

### 1.1 Register a New User

**POST** `/users/`
**Request** *(application/json)*:

```json
{
  "email": "user@example.com",
  "password": "strongPassword123",
  "full_name": "Alice Smith"
}
```

**Response** *(201 Created, UserRead)*:

```json
{
  "id": "6806a1e4d3f4b522c3a9f8d2",
  "email": "user@example.com",
  "full_name": "Alice Smith",
  "is_active": true,
  "created_at": "2025-05-12T14:23:45.678Z"
}
```

### 1.2 Get User by ID

**GET** `/users/{user_id}`
**Response** *(200 OK, UserRead)*:

```json
{
  "id": "6806a1e4d3f4b522c3a9f8d2",
  "email": "user@example.com",
  "full_name": "Alice Smith",
  "is_active": true,
  "created_at": "2025-05-12T14:23:45.678Z"
}
```

### 1.3 Update User

**PUT** `/users/{user_id}`
**Request** *(application/json, partial)*:

```json
{
  "full_name": "Alice Johnson",
  "password": "newSecurePassword"
}
```

**Response** *(200 OK, UserRead)*: same shape as Get User

### 1.4 Delete User

**DELETE** `/users/{user_id}`
**Response** *(204 No Content)*

---

## 2. Device Management 💡

### 2.1 Create Device

**POST** `/devices/`
**Request**:

```json
{
  "name": "Living Room Light",
  "type": "light",
  "location": "Living Room",
  "user_id": "6806a1e4d3f4b522c3a9f8d2",
  "is_active": true
}
```

**Response** *(201 Created, DeviceRead)*:

```json
{
  "id": "6806b2f7e5a4c633d4b0a9f3",
  "name": "Living Room Light",
  "type": "light",
  "location": "Living Room",
  "user_id": "6806a1e4d3f4b522c3a9f8d2",
  "is_active": true,
  "state": "off",
  "registered_at": "2025-05-12T14:30:22.123Z"
}
```

### 2.2 Get Device by ID

**GET** `/devices/{device_id}`
**Response** *(200 OK, DeviceRead)*: same shape as Create Device response

### 2.3 Get All Devices for a User

**GET** `/devices/user/{user_id}`
**Response** *(200 OK, List\[DeviceRead])*

### 2.4 Update Device

**PUT** `/devices/{device_id}`
**Request** *(partial)*:

```json
{
  "name": "Hallway Light",
  "state": "on"
}
```

**Response** *(200 OK, DeviceRead)*

### 2.5 Change Device State (Dedicated)

**POST** `/devices/{device_id}/state`
**Request**:

```json
{ "state": "off" }
```

**Response** *(200 OK, DeviceRead)*

### 2.6 Delete Device

**DELETE** `/devices/{device_id}`
**Response** *(204 No Content)*

---

## 3. Sensor Management 🌡️

### 3.1 Create Sensor

**POST** `/sensors/`
**Request**:

```json
{
  "name": "Temp Sensor",
  "type": "temperature",
  "device_id": "6806b2f7e5a4c633d4b0a9f3",
  "location": "Living Room",
  "unit": "°C"
}
```

**Response** *(201 Created, SensorRead)*

### 3.2 List All Sensors

**GET** `/sensors/`
**Response** *(200 OK, List\[SensorRead])*

### 3.3 List Sensors by Device

**GET** `/sensors/device/{device_id}`
**Response** *(200 OK, List\[SensorRead])*

### 3.4 Get Sensor by ID

**GET** `/sensors/{sensor_id}`
**Response** *(200 OK, SensorRead)*

### 3.5 Delete Sensor

**DELETE** `/sensors/{sensor_id}`
**Response** *(204 No Content)*

---

## 4. Rule Engine ⚙️

### 4.1 Create Rule

**POST** `/rules/`
**Request**:

```json
{
  "name": "Heat Alert",
  "trigger_type": "temperature_change",
  "condition": { "temperature": 28.0 },
  "operator": ">",
  "target_device_id": "6806b2f7e5a4c633d4b0a9f3",
  "action": "turn_on"
}
```

**Response** *(201 Created, RuleRead)*

### 4.2 List Rules

**GET** `/rules/`
**Response** *(200 OK, List\[RuleRead])*

### 4.3 Delete Rule

**DELETE** `/rules/{rule_id}`
**Response** *(204 No Content)*

---

## 5. Consequence Tracking 📋

### 5.1 List Consequences

**GET** `/consequences/`
**Response** *(200 OK, List\[ConsequenceRead])*

### 5.2 Get Consequence by ID

**GET** `/consequences/{consequence_id}`
**Response** *(200 OK, ConsequenceRead)*

### 5.3 Mark Consequence Executed

**PUT** `/consequences/{consequence_id}/execute`
**Response** *(200 OK, ConsequenceRead)*

---

## 6. Event Trigger 🔔

### Trigger an Event

**POST** `/monitor/trigger`
**Request**:

```json
{
  "type": "motion_detected",
  "sensor_id": "abc123",
  "timestamp": "2025-04-24T15:22:59.421322Z"
}
```

**Response** *(200 OK)*:

```json
{ "message": "Event queued successfully." }
```

---

## Error Responses ⚠️

All errors follow the shape:

```json
{
  "detail": "Error message here"
}
```

---

## Versioning & Documentation 📖

* **OpenAPI JSON** available at `/openapi.json`
* **Swagger UI** at `/docs`
* **ReDoc** at `/redoc`
