from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate
from typing import List, Optional

async def create_sensor(sensor_data: SensorCreate) -> Sensor:
    sensor = Sensor(**sensor_data.dict())
    await sensor.insert()
    return sensor

async def get_sensor_by_id(sensor_id: str) -> Optional[Sensor]:
    return await Sensor.find_one(Sensor.sensor_id == sensor_id)

async def get_sensors_by_device_id(device_id: str) -> List[Sensor]:
    return await Sensor.find(Sensor.device_id == device_id).to_list()

async def get_all_sensors() -> List[Sensor]:
    return await Sensor.find_all().to_list()

async def delete_sensor(sensor_id: str) -> bool:
    sensor = await get_sensor_by_id(sensor_id)
    if sensor:
        await sensor.delete()
        return True
    return False
