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

