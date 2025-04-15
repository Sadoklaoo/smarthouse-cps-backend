// Switch to admin database and create root user
db = db.getSiblingDB('admin');
db.auth('admin', 'admin');

// Create application database
db = db.getSiblingDB('smart_house_db');

// Create collections
db.createCollection('users');
db.createCollection('devices');
db.createCollection('sensors');
db.createCollection('events');
db.createCollection('automations');
db.createCollection('actions');

// Create indexes
db.users.createIndex({ "email": 1 }, { unique: true });
db.devices.createIndex({ "device_id": 1 }, { unique: true });
db.sensors.createIndex({ "sensor_id": 1 }, { unique: true });
db.events.createIndex({ "timestamp": -1 });
db.automations.createIndex({ "name": 1 }, { unique: true });
db.actions.createIndex({ "automation_id": 1 }); 